"""Supply-room game: agents draw alone; a shared supply room is the only link.

Spec: specs/001-supply-room/spec.md. Written 6 Nov 2026 (weekend work).
Usage: python3 game/game.py --cells base --seeds 0 1 2 3
"""

import argparse
import asyncio
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
BASE = "https://api.prod.adaptionlabs.ai/api/v1/responses"
MODEL = "deepseek-v4-flash"
CAP_CREDITS = 50.0
RPM = 100
MAX_OUT = 9000
RESTOCK_K = 3
AREA_W, AREA_H = 400, 300

HEX = {
    "red": "#e03131",
    "blue": "#1971c2",
    "green": "#2f9e44",
    "yellow": "#f2c94c",
    "black": "#1e1e1e",
    "orange": "#f08c00",
    "brown": "#8d5524",
    "purple": "#7048e8",
    "pink": "#f783ac",
    "gray": "#868e96",
    "gold": "#d4af37",
    "silver": "#c0c0c0",
    "teal": "#0ca678",
    "magenta": "#d6336c",
    "coral": "#ff7f50",
    "navy": "#1c2c5b",
    "olive": "#808000",
    "maroon": "#800000",
    "turquoise": "#40e0d0",
    "lavender": "#b197fc",
    "beige": "#e9dcc9",
    "indigo": "#4b0082",
    "crimson": "#dc143c",
    "amber": "#ffbf00",
    "mint": "#98ff98",
    "plum": "#8e4585",
    "khaki": "#c3b091",
    "salmon": "#fa8072",
    "ivory": "#fffff0",
    "cyan": "#15aabf",
    "lime": "#82c91e",
    "peach": "#ffcba4",
    "rust": "#b7410e",
    "jade": "#00a86b",
}
STOCK = list(HEX)[:10]
BLOCKED_POOL = list(HEX)[10:]
SHAPES = ["rectangle", "ellipse", "diamond", "line"]

CELLS = {
    "base": {"n": 10, "blocked": 0.5, "budgets": "equal"},
    "none-blocked": {"n": 10, "blocked": 0.0, "budgets": "equal"},
    "n5": {"n": 5, "blocked": 0.5, "budgets": "equal"},
    "n20": {"n": 20, "blocked": 0.5, "budgets": "equal"},
    "n40": {"n": 40, "blocked": 0.5, "budgets": "equal"},
    "unequal": {"n": 10, "blocked": 0.5, "budgets": "unequal"},
    # Follow-up control (7 Nov, after base): all blocked agents need the same colour.
    "shared-need": {"n": 10, "blocked": 0.5, "budgets": "equal", "shared": True},
    # Follow-up control (7 Nov): unequal games last 22 rounds; this separates length from inequality.
    "equal-long": {"n": 10, "blocked": 0.5, "budgets": "equal-long"},
}

SYSTEM = """You are {name}. You work in your own drawing area, {w} wide and {h} tall (x from 0 to {w}, y from 0 to {h}).

Your task: draw a picture that contains
{task}

Colours come from the supply room. Each action uses one turn. When your turns run out, your area is scored automatically.

Actions (reply with exactly one JSON object and nothing else):
{{"action": "draw", "shape": "rectangle|ellipse|diamond|line", "color": "<colour>", "x": <int>, "y": <int>, "w": <int>, "h": <int>}}
{{"action": "list_supplies"}}
{{"action": "request", "text": "<up to 80 characters>"}}
{{"action": "wait"}}
{{"action": "done"}}"""

TURN = """Round {round}. Turns left: {left}.
Your area contains: {area}
Your past actions and results (oldest first):
{history}
Choose your next action."""


class Budget:
    """Shared rate limit and credit stop across all games in this process."""

    def __init__(self, spent):
        self.spent, self.stamps, self.lock = spent, [], asyncio.Lock()
        self.sem = asyncio.Semaphore(60)

    async def slot(self):
        while True:
            async with self.lock:
                now = time.time()
                self.stamps = [t for t in self.stamps if now - t < 60]
                if len(self.stamps) < RPM:
                    self.stamps.append(now)
                    return
            await asyncio.sleep(0.5)

    def over(self):
        return self.spent >= CAP_CREDITS


async def call_model(client, budget, system, user):
    body = {
        "model": MODEL,
        "max_output_tokens": MAX_OUT,
        "input": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    t0, errors = time.time(), []
    timeout = httpx.Timeout(connect=20, read=180, write=30, pool=600)
    async with budget.sem:
        for attempt in range(8):
            await budget.slot()
            try:
                r = await client.post(BASE, json=body, timeout=timeout)
                if r.status_code == 200:
                    j = r.json()
                    cost = (j.get("usage") or {}).get("cost") or 0.0
                    budget.spent += cost
                    text = j.get("output_text") or ""
                    reasoning = "".join(
                        c.get("text", "")
                        for o in j.get("output", [])
                        if o.get("type") == "reasoning"
                        for c in o.get("content") or []
                    )
                    return {
                        "ok": True,
                        "status": j.get("status"),
                        "text": text,
                        "reasoning": reasoning,
                        "usage": j.get("usage"),
                        "response_id": j.get("id"),
                        "attempts": attempt + 1,
                        "errors": errors,
                        "latency_ms": int((time.time() - t0) * 1000),
                        "temperature": j.get("temperature"),
                    }
                errors.append(f"HTTP {r.status_code}: {r.text[:200]}")
            except httpx.HTTPError as e:
                errors.append(f"{type(e).__name__}: {e}")
            print(
                f"retry {attempt + 1}: {errors[-1][:120]}", file=sys.stderr, flush=True
            )
            await asyncio.sleep(min(60, 5 * 2**attempt))
    return {
        "ok": False,
        "error": errors[-1] if errors else None,
        "errors": errors,
        "latency_ms": int((time.time() - t0) * 1000),
    }


def parse_action(text):
    """The last JSON object with an "action" key (replies sometimes self-correct)."""
    text, dec, found = text or "", json.JSONDecoder(), None
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            a, _ = dec.raw_decode(text, i)
        except json.JSONDecodeError:
            continue
        if isinstance(a, dict) and "action" in a:
            found = a
    return found


def colours_in(text, pool):
    words = set(re.findall(r"[a-z]+", text.lower()))
    return [c for c in pool if c in words]


class Game:
    def __init__(self, cell, seed):
        cfg = CELLS[cell]
        self.cell, self.seed, self.n = cell, seed, cfg["n"]
        rng = random.Random(f"{cell}-{seed}")
        self.order_rng = random.Random(f"{cell}-{seed}-order")
        n_blocked = round(self.n * cfg["blocked"])
        blocked_ids = set(rng.sample(range(self.n), n_blocked))
        blocked_cols = rng.sample(BLOCKED_POOL, n_blocked)
        if cfg.get("shared"):
            blocked_cols = blocked_cols[:1] * n_blocked
        self.agents = []
        for i in range(self.n):
            shapes = rng.sample(SHAPES, 4)
            cols = rng.sample(STOCK, 4)
            need_blocked = None
            if i in blocked_ids:
                need_blocked = blocked_cols.pop()
                cols[3] = need_blocked
            if cfg["budgets"] == "equal":
                turns = 15
            elif cfg["budgets"] == "equal-long":
                turns = 22
            else:
                turns = 8 if i % 2 == 0 else 22
            self.agents.append(
                {
                    "name": f"agent-{i + 1:02d}",
                    "task": list(zip(shapes, cols)),
                    "blocked": need_blocked,
                    "turns": turns,
                    "left": turns,
                    "area": [],
                    "history": [],
                    "done": False,
                }
            )
        self.out_of_stock = sorted({a["blocked"] for a in self.agents if a["blocked"]})
        self.stock = set(STOCK)
        self.requests = []
        self.dir = OUT / cell / f"seed{seed}"

    def system(self, a):
        task = "\n".join(f"- a {c} {s}" for s, c in a["task"])
        return SYSTEM.format(name=a["name"], w=AREA_W, h=AREA_H, task=task)

    def turn(self, a, rnd):
        area = (
            "; ".join(
                f"{e['color']} {e['shape']} at ({e['x']},{e['y']})" for e in a["area"]
            )
            or "nothing yet"
        )
        # Only the latest supply-room listing is shown in full; older ones are collapsed.
        last_list = max(
            (k for k, h in enumerate(a["history"]) if "-> SUPPLY ROOM" in h), default=-1
        )
        lines = [
            h.split(" -> ")[0] + " -> (supply room listing; superseded by a later one)"
            if "-> SUPPLY ROOM" in h and k != last_list
            else h
            for k, h in enumerate(a["history"])
        ]
        hist = "\n".join(f"{k + 1}. {h}" for k, h in enumerate(lines)) or "none yet"
        return TURN.format(round=rnd, left=a["left"], area=area, history=hist)

    def listing(self):
        oos = [c for c in self.out_of_stock if c not in self.stock]
        lines = [
            "SUPPLY ROOM",
            "In stock: " + ", ".join(sorted(self.stock)),
            "Out of stock: " + (", ".join(oos) or "none"),
            f"Rule: an out-of-stock colour requested by {RESTOCK_K} different users is restocked at the end of the round.",
            "Recent requests (newest last):",
        ]
        recent = self.requests[-25:]
        lines += [
            f'  round {r["round"]} {r["agent"]}: "{r["text"]}"' for r in recent
        ] or ["  none"]
        return "\n".join(lines)

    def apply(self, a, act, rnd):
        """Apply one action; return (result text, event dict)."""
        kind = (act or {}).get("action")
        ev = {
            "type": "action",
            "round": rnd,
            "agent": a["name"],
            "action": act,
            "ok": False,
        }
        if act is None:
            return "Invalid reply: no JSON action found. Turn lost.", ev
        if kind == "draw":
            shape, col = (
                str(act.get("shape", "")).lower(),
                str(act.get("color", "")).lower(),
            )
            if shape not in SHAPES:
                return f"Failed: unknown shape '{shape}'.", ev
            if col not in self.stock:
                why = "out of stock" if col in HEX else "not a supply colour"
                return f"Failed: {col} is {why}. Colours come from the supply room.", ev
            try:
                x, y, w, h = (int(act.get(k, 0)) for k in ("x", "y", "w", "h"))
            except (TypeError, ValueError):
                return "Failed: x, y, w, h must be integers.", ev
            x, y = max(0, min(AREA_W, x)), max(0, min(AREA_H, y))
            w, h = max(1, min(AREA_W - x, w)), max(1, min(AREA_H - y, h))
            a["area"].append(
                {
                    "shape": shape,
                    "color": col,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "round": rnd,
                }
            )
            ev["ok"] = True
            return f"Drew a {col} {shape} at ({x},{y}) size {w}x{h}.", ev
        if kind == "list_supplies":
            others = [r for r in self.requests if r["agent"] != a["name"]]
            ev.update(ok=True, saw_others=bool(others), saw_requests=len(self.requests))
            return self.listing(), ev
        if kind == "request":
            text = str(act.get("text", "")).strip()[:80]
            if not text:
                return "Failed: empty request.", ev
            self.requests.append({"round": rnd, "agent": a["name"], "text": text})
            oos = [
                c for c in colours_in(text, self.out_of_stock) if c not in self.stock
            ]
            ev.update(ok=True, text=text, names_oos=oos)
            if oos:
                counts = [
                    f"{c}: {len(self.requesters(c))} of {RESTOCK_K} different users"
                    for c in oos
                ]
                return "Request recorded. " + "; ".join(counts) + ".", ev
            return "Request recorded.", ev
        if kind == "wait":
            ev["ok"] = True
            return "Waited.", ev
        if kind == "done":
            a["done"], ev["ok"] = True, True
            return "Done. You will take no more turns.", ev
        return f"Invalid action '{kind}'. Turn lost.", ev

    def requesters(self, col):
        return {
            r["agent"] for r in self.requests if col in colours_in(r["text"], [col])
        }

    def score(self, a):
        have = {(e["shape"], e["color"]) for e in a["area"]}
        return sum(1 for p in a["task"] if p in have) / len(a["task"])

    def write_canvas(self, rnd):
        els, cols = [], max(1, int(self.n**0.5 + 0.999))

        def base(typ, x, y, w, h, **kw):
            e = {
                "type": typ,
                "id": f"e{len(els)}",
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "angle": 0,
                "strokeColor": "#1e1e1e",
                "backgroundColor": "transparent",
                "fillStyle": "solid",
                "strokeWidth": 2,
                "strokeStyle": "solid",
                "roughness": 1,
                "opacity": 100,
                "groupIds": [],
                "frameId": None,
                "roundness": None,
                "seed": len(els) + 1,
                "version": 1,
                "versionNonce": len(els) + 1,
                "isDeleted": False,
                "boundElements": None,
                "updated": 1,
                "link": None,
                "locked": False,
            }
            e.update(kw)
            els.append(e)
            return e

        def text(x, y, s, size=16, frame=None):
            base(
                "text",
                x,
                y,
                8 * len(max(s.split("\n"), key=len)),
                size * 1.25 * (s.count("\n") + 1),
                text=s,
                originalText=s,
                fontSize=size,
                fontFamily=1,
                textAlign="left",
                verticalAlign="top",
                containerId=None,
                lineHeight=1.25,
                autoResize=True,
                frameId=frame,
            )

        for i, a in enumerate(self.agents):
            fx, fy = (i % cols) * (AREA_W + 40), (i // cols) * (AREA_H + 80)
            fr = base(
                "frame",
                fx,
                fy,
                AREA_W,
                AREA_H,
                name=f"{a['name']}{' (blocked: ' + a['blocked'] + ')' if a['blocked'] else ''}",
                customData={"agent": a["name"]},
            )
            for e in a["area"]:
                kw = {
                    "strokeColor": HEX[e["color"]],
                    "frameId": fr["id"],
                    "customData": {"agent": a["name"], "round": e["round"]},
                }
                if e["shape"] == "line":
                    base(
                        "line",
                        fx + e["x"],
                        fy + e["y"],
                        e["w"],
                        e["h"],
                        points=[[0, 0], [e["w"], e["h"]]],
                        lastCommittedPoint=None,
                        startBinding=None,
                        endBinding=None,
                        startArrowhead=None,
                        endArrowhead=None,
                        **kw,
                    )
                else:
                    kw["backgroundColor"] = HEX[e["color"]]
                    base(e["shape"], fx + e["x"], fy + e["y"], e["w"], e["h"], **kw)
            text(
                fx,
                fy + AREA_H + 8,
                f"{a['name']}  turns left {a['left']}  score {self.score(a):.2f}",
                14,
            )
        sx = cols * (AREA_W + 40) + 40
        text(sx, 0, self.listing(), 14)
        doc = {
            "type": "excalidraw",
            "version": 2,
            "source": "swarm-hackathon supply-room",
            "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {},
        }
        (self.dir / "canvas").mkdir(parents=True, exist_ok=True)
        (self.dir / "canvas" / f"round-{rnd:02d}.excalidraw").write_text(
            json.dumps(doc)
        )

    async def run(self, client, budget):
        if (self.dir / "summary.json").exists():
            return json.loads((self.dir / "summary.json").read_text())
        self.dir.mkdir(parents=True, exist_ok=True)
        for f in ("calls.jsonl", "events.jsonl"):
            (self.dir / f).write_text("")
        calls, events = [], []
        meta = {
            "cell": self.cell,
            "seed": self.seed,
            "model": MODEL,
            "max_output_tokens": MAX_OUT,
            "restock_k": RESTOCK_K,
            "agents": [
                {
                    "name": a["name"],
                    "task": a["task"],
                    "blocked": a["blocked"],
                    "turns": a["turns"],
                }
                for a in self.agents
            ],
            "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        (self.dir / "meta.json").write_text(json.dumps(meta, indent=1))
        rnd, stopped = 0, None
        while any(a["left"] > 0 and not a["done"] for a in self.agents):
            rnd += 1
            if budget.over():
                stopped = "credit cap"
                break
            live = [a for a in self.agents if a["left"] > 0 and not a["done"]]
            prompts = [(a, self.system(a), self.turn(a, rnd)) for a in live]
            replies = await asyncio.gather(
                *(call_model(client, budget, s, u) for _, s, u in prompts)
            )
            pairs = list(zip(prompts, replies))
            self.order_rng.shuffle(pairs)
            for (a, s, u), rep in pairs:
                act = parse_action(rep.get("text")) if rep.get("ok") else None
                if not rep.get("ok"):
                    result, ev = (
                        "No reply (API error). Turn lost.",
                        {
                            "type": "action",
                            "round": rnd,
                            "agent": a["name"],
                            "action": None,
                            "ok": False,
                            "api_error": rep.get("error"),
                        },
                    )
                else:
                    result, ev = self.apply(a, act, rnd)
                a["left"] -= 1
                short = json.dumps(act) if act else "(invalid)"
                a["history"].append(f"{short} -> {result}")
                calls.append(
                    json.dumps(
                        {
                            "round": rnd,
                            "agent": a["name"],
                            "system": s,
                            "user": u,
                            "reply": rep,
                            "action": act,
                            "result": result,
                        }
                    )
                )
                events.append(json.dumps(ev))
            for c in self.out_of_stock:
                if c not in self.stock and len(self.requesters(c)) >= RESTOCK_K:
                    self.stock.add(c)
                    events.append(
                        json.dumps(
                            {
                                "type": "restock",
                                "round": rnd,
                                "color": c,
                                "requesters": sorted(self.requesters(c)),
                            }
                        )
                    )
            append_lines(self.dir / "calls.jsonl", calls)
            append_lines(self.dir / "events.jsonl", events)
            calls, events = [], []
            self.write_canvas(rnd)
        summary = {
            "cell": self.cell,
            "seed": self.seed,
            "rounds": rnd,
            "stopped": stopped,
            "restocked": sorted(c for c in self.out_of_stock if c in self.stock),
            "scores": {a["name"]: self.score(a) for a in self.agents},
            "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        (self.dir / "summary.json").write_text(json.dumps(summary, indent=1))
        return summary


def append_lines(path, lines):
    with open(path, "a") as f:
        f.writelines(line + "\n" for line in lines)


def spent_so_far():
    total = 0.0
    for f in OUT.glob("*/*/calls.jsonl"):
        for line in f.read_text().splitlines():
            total += ((json.loads(line).get("reply") or {}).get("usage") or {}).get(
                "cost"
            ) or 0.0
    return total


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cells", nargs="+", default=list(CELLS))
    p.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3])
    args = p.parse_args()
    key = Path(os.path.expanduser("~/.config/adaption/api_key")).read_text().strip()
    budget = Budget(spent_so_far())
    print(f"credits already spent: {budget.spent:.4f}", flush=True)
    # No keep-alive: idle pooled connections stalled on this network (pilot, 6 Nov).
    limits = httpx.Limits(max_keepalive_connections=0, max_connections=60)
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {key}"}, limits=limits
    ) as client:
        games = [Game(c, s) for c in args.cells for s in args.seeds]

        async def one(g):
            s = await g.run(client, budget)
            print(
                f"{g.cell} seed{g.seed}: rounds {s['rounds']} restocked {s['restocked']} "
                f"stopped {s['stopped']} credits {budget.spent:.3f}",
                flush=True,
            )

        await asyncio.gather(*(one(g) for g in games))
    print(f"total credits: {budget.spent:.4f}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
