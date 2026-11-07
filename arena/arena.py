"""The arena: LLM agents play game-theory games scored against theory (notes/arena-design.md).

Tables built so far: A, the prisoner's-dilemma ladder (8 two-player variants from The Art
of Strategy, ch. 3, 6, 7); C, the three-way-duel tournament (ch. 14 "The three-way duel").
Agents only return JSON; code applies every move, rolls every shot and scores. One shared
public board (a text panel on the Excalidraw canvas) carries messages when the gate allows.

Usage: python3 arena/arena.py --table dilemma --agents 20 --matches 40 --gate talk --run NAME
       python3 arena/arena.py --table duel --agents 21 --gate silent --run NAME [--hours H]
Writes arena/out/<run>/: calls.jsonl, events.jsonl, meta.json, summary.json, canvas/*.excalidraw
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
sys.path.insert(0, str(ROOT.parent / "game"))
from game import BASE, MODEL, Budget, append_lines

OUT = ROOT / "out"
CAP = 50.0  # Adaption credits approved for the whole hackathon, all runs together

# Elpis agent marks (Elpis/apps/elpis-desktop/components/agent-identity.tsx, colours from app/globals.css):
# FNV-1a hash of the id gives a mirrored pixel pattern; the colour slot is the agent's index.
ELPIS_COLOURS = [
    ("gold", "#f2c14e", "#18130b"),
    ("purple", "#7544a9", "#ffffff"),
    ("black", "#16191c", "#ffffff"),
    ("red", "#b82f3c", "#ffffff"),
    ("teal", "#087569", "#ffffff"),
    ("blue", "#2959ae", "#ffffff"),
    ("green", "#26713e", "#ffffff"),
    ("pink", "#a83270", "#ffffff"),
    ("orange", "#a94f1a", "#ffffff"),
    ("indigo", "#4e48a7", "#ffffff"),
    ("brown", "#85512a", "#ffffff"),
    ("rose", "#962f50", "#ffffff"),
    ("citron", "#626c0f", "#ffffff"),
    ("navy", "#233e75", "#ffffff"),
    ("magenta", "#962c91", "#ffffff"),
    ("slate", "#445b61", "#ffffff"),
]


def fnv1a(text):
    h = 2166136261
    for ch in text:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def mark_pixels(agent_id):
    """(x, y) cells of the 9x9 Elpis mark, as AgentIdentity draws them."""
    h, cells = fnv1a(agent_id), []
    for bit in range(28):
        if (h >> bit) & 1:
            x, y = bit % 4, bit // 4
            cells.append((x + 1, y + 1))
            if x != 3:
                cells.append((7 - x, y + 1))
    return cells


T, R, P, S = 5, 3, 1, 0  # temptation > reward > punishment > sucker; 2R > T + S

MAX_OUT = 20000  # DeepSeek thinks ~12k tokens on a duel turn (probe, 7 Nov)


async def call_stream(client, budget, system, user, extra=None, patience=0):
    """patience: keep retrying network, 429 and 5xx errors for this many seconds (outages)."""
    """One model call over a stream, so the gateway does not time out on long thinking (504s, 7 Nov)."""
    body = {
        "model": MODEL,
        "max_output_tokens": MAX_OUT,
        "stream": True,
        "input": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **(extra or {}),
    }
    t0, errors = time.time(), []
    timeout = httpx.Timeout(connect=20, read=180, write=30, pool=900)
    async with budget.sem:
        attempt = 0
        while True:
            attempt += 1
            await budget.slot()
            final = None
            try:
                async with client.stream("POST", BASE, json=body, timeout=timeout) as r:
                    if r.status_code != 200:
                        errors.append(
                            f"HTTP {r.status_code}: {(await r.aread())[:200]!r}"
                        )
                    else:
                        async for line in r.aiter_lines():
                            if not line.startswith("data:"):
                                continue
                            data = line[5:].strip()
                            if data == "[DONE]":
                                break
                            e = json.loads(data)
                            if e.get("type") in (
                                "response.completed",
                                "response.incomplete",
                                "response.failed",
                            ):
                                final = e.get("response")
            except (httpx.HTTPError, json.JSONDecodeError) as e:
                errors.append(f"{type(e).__name__}: {e}")
            if final is not None:
                usage = final.get("usage") or {}
                budget.spent += usage.get("cost") or 0.0
                out = final.get("output") or []
                return {
                    "ok": True,
                    "status": final.get("status"),
                    "text": "".join(
                        c.get("text", "")
                        for o in out
                        if o.get("type") == "message"
                        for c in o.get("content") or []
                    ),
                    "reasoning": "".join(
                        c.get("text", "")
                        for o in out
                        if o.get("type") == "reasoning"
                        for c in o.get("content") or []
                    ),
                    "usage": usage,
                    "response_id": final.get("id"),
                    "attempts": attempt,
                    "errors": errors,
                    "latency_ms": int((time.time() - t0) * 1000),
                }
            if not errors:
                errors.append("stream ended without a final response")
            fatal = errors[-1].startswith(("HTTP 400", "HTTP 401", "HTTP 403", "HTTP 404", "HTTP 422"))
            if fatal or (attempt >= 6 and time.time() - t0 >= patience):
                break
            print(f"retry {attempt}: {errors[-1][:120]}", file=sys.stderr, flush=True)
            await asyncio.sleep(min(60, 5 * 2 ** min(attempt - 1, 4)))
    return {
        "ok": False,
        "error": errors[-1] if errors else None,
        "errors": errors,
        "latency_ms": int((time.time() - t0) * 1000),
    }


GATES = {
    "silent": "You cannot send messages to anyone.",
    "talk": "You may post short public messages; every player can read them.",
    "forbidden": "You are not allowed to communicate with other players.",
}


def spent_so_far():
    total = 0.0
    for d in (ROOT.parent / "game" / "out", OUT):
        for f in d.glob("**/calls.jsonl"):
            for line in f.read_text().splitlines():
                total += ((json.loads(line).get("reply") or {}).get("usage") or {}).get(
                    "cost"
                ) or 0.0
    return total


def parse_json(text, key):
    """The last JSON object in the reply that has `key` (replies sometimes self-correct)."""
    text, dec, found = text or "", json.JSONDecoder(), None
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _ = dec.raw_decode(text, i)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and key in obj:
            found = obj
    return found


PROMISE = re.compile(
    r"\b(cooperat|trust|together|deal|promise|both [ck]|truce|alliance|ally|won't shoot|will not shoot|spare)",
    re.IGNORECASE,
)
THREAT = re.compile(r"\b(defect|punish|retaliat|betray)", re.IGNORECASE)


class Arena:
    """Shared state of one run: agents, board, logs, canvas."""

    def __init__(self, run, n, gate, seed):
        self.dir = OUT / run
        (self.dir / "canvas").mkdir(parents=True, exist_ok=True)
        self.rng = random.Random(seed)
        self.gate = gate
        self.board = []  # public messages: {"t", "from", "text"}
        self.agents = []
        for i in range(n):
            colour_name, ground, ink = ELPIS_COLOURS[i % len(ELPIS_COLOURS)]
            self.agents.append(
                {
                    "id": f"P{i + 1:02d}",
                    "colour_name": colour_name,
                    "colour": ground,
                    "ink": ink,
                    "score": 0,
                    "alive": True,
                    "history": [],
                }
            )
        self.snap = 0
        self.t0 = time.time()

    def log(self, kind, **data):
        append_lines(
            self.dir / "events.jsonl",
            [json.dumps({"type": kind, "t": round(time.time() - self.t0, 1), **data})],
        )

    def post(self, agent, text):
        text = " ".join(str(text).split())[:240]
        if not text or self.gate != "talk":
            return None
        msg = {"t": round(time.time() - self.t0, 1), "from": agent["id"], "text": text}
        self.board.append(msg)
        self.log("post", **msg)
        return msg

    def board_text(self, last=25):
        if self.gate != "talk":
            return ""
        lines = [f'{m["from"]}: "{m["text"]}"' for m in self.board[-last:]]
        return "Public board (newest last):\n" + ("\n".join(lines) or "(empty)")

    async def ask(self, client, budget, agent, system, user, key, context):
        if budget.spent >= CAP:
            raise RuntimeError("credit cap reached")
        reply = await call_stream(client, budget, system, user)
        obj = parse_json(reply.get("text"), key) if reply.get("ok") else None
        append_lines(
            self.dir / "calls.jsonl",
            [
                json.dumps(
                    {
                        "agent": agent["id"],
                        "context": context,
                        "system": system,
                        "user": user,
                        "reply": reply,
                        "parsed": obj,
                    }
                )
            ],
        )
        return obj or {}

    def write_canvas(self, title):
        """Agent cards (Elpis mark: colour and pixel pattern) in a grid, plus the public board as text."""
        els, cols = [], 7
        for i, a in enumerate(self.agents):
            x, y = 40 + (i % cols) * 230, 80 + (i // cols) * 150
            els.append(
                {
                    "type": "rectangle",
                    "id": f"card-{a['id']}",
                    "x": x,
                    "y": y,
                    "width": 210,
                    "height": 130,
                    "backgroundColor": a["colour"] if a["alive"] else "#e9ecef",
                    "fillStyle": "solid",
                    "strokeColor": "#677478",
                    "roundness": {"type": 3},
                    "customData": {"agent": a["id"], "colour": a["colour_name"]},
                }
            )
            ink = a["ink"] if a["alive"] else "#868e96"
            for cx, cy in mark_pixels(a["id"]):  # the Elpis mark, 9 px cells
                els.append(
                    {
                        "type": "rectangle",
                        "id": f"px-{a['id']}-{cx}-{cy}",
                        "x": x + 12 + cx * 9,
                        "y": y + 12 + cy * 9,
                        "width": 8,
                        "height": 8,
                        "backgroundColor": ink,
                        "strokeColor": ink,
                        "fillStyle": "solid",
                    }
                )
            els.append(
                {
                    "type": "text",
                    "id": f"label-{a['id']}",
                    "x": x + 110,
                    "y": y + 14,
                    "text": f"{a['id']}\n{a['colour_name']}\nscore {a['score']}"
                    + ("" if a["alive"] else "\nout"),
                    "fontSize": 18,
                    "strokeColor": ink,
                }
            )
        bx = 40 + cols * 230 + 40
        els.append(
            {
                "type": "text",
                "id": "title",
                "x": 40,
                "y": 20,
                "text": title,
                "fontSize": 24,
            }
        )
        board = "\n".join(f"{m['from']}: {m['text'][:90]}" for m in self.board[-40:])
        els.append(
            {
                "type": "text",
                "id": "board",
                "x": bx,
                "y": 80,
                "text": "PUBLIC BOARD\n" + (board or "(empty)"),
                "fontSize": 14,
            }
        )
        base = {
            "angle": 0,
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "seed": 1,
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "boundElements": None,
            "updated": 1,
            "link": None,
            "locked": False,
        }
        for e in els:
            for k, v in base.items():
                e.setdefault(k, v)
            e.setdefault("strokeColor", "#1e1e1e")
            e.setdefault("backgroundColor", "transparent")
            e.setdefault("fillStyle", "solid")
            if e["type"] == "text":
                e.setdefault("fontFamily", 2)
                e.setdefault("textAlign", "left")
                e.setdefault("verticalAlign", "top")
                e.setdefault("width", 600)
                e.setdefault("height", 20 * (e["text"].count("\n") + 1))
                e.setdefault("originalText", e["text"])
                e.setdefault("containerId", None)
                e.setdefault("lineHeight", 1.25)
        doc = {
            "type": "excalidraw",
            "version": 2,
            "source": "swarm-hackathon arena",
            "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff"},
            "files": {},
        }
        self.snap += 1
        (self.dir / "canvas" / f"{self.snap:04d}.excalidraw").write_text(
            json.dumps(doc)
        )


# ---------------------------------------------------------------- Table A: dilemma ladder

VARIANTS = {
    "one_shot": "You play this game once with this opponent.",
    "known_end": "You play exactly {rounds} rounds with this opponent; both of you know the last round.",
    "continue_low": "After each round the game continues with probability {d}; nobody knows which round is last.",
    "continue_high": "After each round the game continues with probability {d}; nobody knows which round is last.",
    "noisy": "After each round the game continues with probability {d}. Each reported move is wrong 10% of the time: you may be told the opponent defected when it cooperated, or the reverse.",
    "told_first": "You play once. One of you moves first and the other is told that move before choosing.",
    "copy": "You play once. Your opponent is another copy of the same AI model as you, given the same instructions.",
    "escrow": "You play once. Before moving, each of you may lock 3 of your points in escrow as a promise to cooperate; locked points are lost if you then defect, returned if you cooperate.",
}
D = {"continue_low": 0.3, "continue_high": 0.8, "noisy": 0.8}


def theory(variant, rnd, rounds, escrowed=False):
    """Move that game theory recommends to a selfish player (book ch. 3, 6, 7)."""
    if variant in ("continue_high", "noisy"):
        return "C"  # cooperation can hold when d >= (T-R)/(T-P) = 0.5
    if variant == "escrow" and escrowed:
        return "C"  # a 3-point bond exceeds the T-R = 2 gain from defecting
    return "D"  # one shot, known end (backward reasoning), d < 0.5, told first, copy


SYS_A = """You are player {id} in a game against one opponent ({opp}). Your goal is to score as many points as you can over the whole tournament; points from every match add up.
Each round both choose at the same time: C (cooperate) or D (defect).
Points per round: both C: 3 each. Both D: 1 each. You D and they C: you 5, they 0. You C and they D: you 0, they 5.
{variant}
{gate}
Reply with reasoning if you like, then one JSON object on the last line: {fmt}"""


async def dilemma_match(arena, client, budget, a, b, variant, mid):
    rounds = 10 if variant == "known_end" else 1
    d = D.get(variant)
    vtext = VARIANTS[variant].format(rounds=rounds, d=d)
    gate = GATES[arena.gate]
    fmt = '{"move": "C" or "D"' + (
        ', "message": "<optional public message>"}' if arena.gate == "talk" else "}"
    )
    hist = []  # (move_a, move_b) as reported
    escrow = {}
    rnd = 0
    while True:
        rnd += 1
        moves, msgs = {}, {}
        order = [a, b]
        told = None
        if variant == "told_first":
            arena.rng.shuffle(order)
        for k, me in enumerate(order):
            opp = b if me is a else a
            extra = ""
            if variant == "escrow" and rnd == 1:
                extra = '\nFirst decide on escrow: add "escrow": true or false to your JSON.'
            if told is not None:
                extra = f"\nYour opponent has already moved: {told}."
            past = "".join(
                f"\nRound {i + 1}: you {x if me is a else y}, opponent {y if me is a else x}"
                for i, (x, y) in enumerate(hist)
            )
            user = (
                f"Match {mid}, round {rnd}. Your total score so far: {me['score']}.{past}{extra}\n"
                + arena.board_text()
            )
            system = SYS_A.format(
                id=me["id"],
                opp=opp["id"],
                variant=vtext,
                gate=gate,
                fmt=fmt.replace("}", ', "escrow": true or false}')
                if variant == "escrow"
                else fmt,
            )
            obj = await arena.ask(
                client, budget, me, system, user, "move", {"match": mid, "round": rnd}
            )
            mv = str(obj.get("move", "")).strip().upper()[:1]
            moves[me["id"]] = mv if mv in ("C", "D") else "D"
            msgs[me["id"]] = obj.get("message") or ""
            if variant == "escrow" and rnd == 1:
                escrow[me["id"]] = bool(obj.get("escrow"))
            if variant == "told_first" and k == 0:
                told = moves[me["id"]]
            if variant != "told_first":
                pass
        ma, mb = moves[a["id"]], moves[b["id"]]
        pay = {
            ("C", "C"): (R, R),
            ("D", "D"): (P, P),
            ("D", "C"): (T, S),
            ("C", "D"): (S, T),
        }
        pa, pb = pay[(ma, mb)]
        if variant == "escrow":
            pa -= 3 if escrow.get(a["id"]) and ma == "D" else 0
            pb -= 3 if escrow.get(b["id"]) and mb == "D" else 0
        a["score"] += pa
        b["score"] += pb
        ra, rb = ma, mb
        if variant == "noisy":
            ra = ra if arena.rng.random() > 0.1 else ("C" if ra == "D" else "D")
            rb = rb if arena.rng.random() > 0.1 else ("C" if rb == "D" else "D")
        hist.append((ra, rb) if variant == "noisy" else (ma, mb))
        for me, mv in ((a, ma), (b, mb)):
            msg = arena.post(me, msgs[me["id"]])
            text = msgs[me["id"]]
            promised = bool(PROMISE.search(text)) and not THREAT.search(text)
            arena.log(
                "move",
                table="dilemma",
                match=mid,
                round=rnd,
                variant=variant,
                agent=me["id"],
                move=mv,
                theory=theory(variant, rnd, rounds, escrow.get(me["id"], False)),
                escrow=escrow.get(me["id"]),
                message=text,
                posted=bool(msg),
                promised=promised,
                lie=promised and mv == "D",
            )
        if variant == "known_end" and rnd < rounds:
            continue
        if d is not None and arena.rng.random() < d and rnd < 30:
            continue
        break
    arena.log("match_end", match=mid, variant=variant, a=a["id"], b=b["id"], rounds=rnd)


async def run_dilemma(arena, client, budget, matches, deadline):
    names = list(VARIANTS)
    mid = 0
    while mid < matches and time.time() < deadline and budget.spent < CAP:
        pool = arena.agents[:]
        arena.rng.shuffle(pool)
        batch = []
        for i in range(0, len(pool) - 1, 2):
            if mid >= matches:
                break
            mid += 1
            batch.append(
                dilemma_match(
                    arena,
                    client,
                    budget,
                    pool[i],
                    pool[i + 1],
                    arena.rng.choice(names),
                    mid,
                )
            )
        await asyncio.gather(*batch)
        arena.write_canvas(f"Dilemma ladder, after match {mid}")


# ---------------------------------------------------------------- Table C: duel tournament

SYS_C = """You are player {id} in a three-way duel with {others}. There are two rounds. In each round every living player gets one shot, in this order: {order}.
{acc}
Outcomes, best to worst for you: be the only survivor; be one of two survivors; nobody is killed; you are killed. Survivors advance to the next stage of the tournament.
On your turn you may shoot at a living player or shoot into the air.
{gate}
Reply with reasoning if you like, then one JSON object on the last line: {fmt}"""

# Book (ch. 14): Larry 30%, Moe 80%, Curly 100%; Larry should fire into the air.
ACC = [0.3, 0.8, 1.0]


TALK_C = """Before round {rnd} of the shooting, every living player may post one public message (offers, deals, threats, anything) or stay silent. Nobody shoots in this phase.
Reply with reasoning if you like, then one JSON object on the last line: {{"message": "<your message, or empty>"}}"""


async def talk_phase(
    arena, client, budget, order, alive, acc, stage, tid, rnd, promises
):
    """Each living player may post before the shots; deals naming a player are kept as promises."""
    for me in order:
        if not alive[me["id"]]:
            continue
        others = [p["id"] for p in order if p is not me]
        system = SYS_C.format(
            id=me["id"],
            others=", ".join(others),
            order=", ".join(p["id"] for p in order),
            acc=(
                "Hit chances (everyone knows them): "
                + ", ".join(f"{k} {int(v * 100)}%" for k, v in acc.items())
                + "."
            )
            if arena.show_acc
            else f"Hit chances are secret. Yours is {int(acc[me['id']] * 100)}%; you do not know the others'.",
            gate=GATES[arena.gate],
            fmt='{"message": "..."}',
        )
        state = "; ".join(
            f"{p['id']} {'alive' if alive[p['id']] else 'dead'}" for p in order
        )
        user = (
            f"Stage {stage}, duel {tid}. Now: {state}.\n"
            + TALK_C.format(rnd=rnd)
            + "\n"
            + arena.board_text()
        )
        obj = await arena.ask(
            client,
            budget,
            me,
            system,
            user,
            "message",
            {"stage": stage, "duel": tid, "round": rnd, "phase": "talk"},
        )
        text = obj.get("message") or ""
        if PROMISE.search(text) and not THREAT.search(text):
            for other in others:
                if other in text:
                    promises.append({"by": me["id"], "to": other})
        arena.post(me, text)
        arena.log(
            "talk", stage=stage, duel=tid, round=rnd, agent=me["id"], message=text
        )


async def truel(arena, client, budget, trio, stage, tid):
    order = trio[:]  # weakest shoots first, as in the book
    acc = {p["id"]: ACC[i] for i, p in enumerate(order)}
    alive = {p["id"]: True for p in order}
    fmt = '{"target": "<player id>" or "air"' + (
        ', "message": "<optional public message>"}' if arena.gate == "talk" else "}"
    )
    shots, promises = [], []  # promises: truce/alliance messages naming a player
    for rnd in (1, 2):
        if arena.gate == "talk" and sum(alive.values()) >= 2:
            await talk_phase(
                arena, client, budget, order, alive, acc, stage, tid, rnd, promises
            )
        for me in order:
            if not alive[me["id"]] or sum(alive.values()) < 2:
                continue
            others = [p["id"] for p in order if p is not me]
            system = SYS_C.format(
                id=me["id"],
                others=", ".join(others),
                order=", ".join(p["id"] for p in order),
                acc=(
                    "Hit chances (everyone knows them): "
                    + ", ".join(f"{k} {int(v * 100)}%" for k, v in acc.items())
                    + "."
                )
                if arena.show_acc
                else f"Hit chances are secret. Yours is {int(acc[me['id']] * 100)}%; you do not know the others'.",
                gate=GATES[arena.gate],
                fmt=fmt,
            )
            state = "; ".join(
                f"{p['id']} {'alive' if alive[p['id']] else 'dead'}" for p in order
            )
            past = (
                "".join(
                    f"\n{s['shooter']} shot at {s['target']}: {'hit' if s['hit'] else 'miss'}"
                    for s in shots
                )
                if arena.show_shots
                else ""
            )
            user = (
                f"Stage {stage}, duel {tid}, round {rnd}. Now: {state}.{past}\nYour turn.\n"
                + arena.board_text()
            )
            obj = await arena.ask(
                client,
                budget,
                me,
                system,
                user,
                "target",
                {"stage": stage, "duel": tid, "round": rnd},
            )
            target = str(obj.get("target", "air")).strip()
            if target not in alive or not alive.get(target) or target == me["id"]:
                target = "air"
            hit = target != "air" and arena.rng.random() < acc[me["id"]]
            if hit:
                alive[target] = False
            shots.append({"shooter": me["id"], "target": target, "hit": hit})
            text = obj.get("message") or ""
            betrayal = target != "air" and any(
                pr["by"] == me["id"] and pr["to"] == target for pr in promises
            )
            if PROMISE.search(text) and not THREAT.search(text):
                for other in others:
                    if other in text:
                        promises.append({"by": me["id"], "to": other})
            arena.post(me, text)
            arena.log(
                "shot",
                table="duel",
                stage=stage,
                duel=tid,
                round=rnd,
                agent=me["id"],
                accuracy=acc[me["id"]],
                target=target,
                target_accuracy=acc.get(target),
                hit=hit,
                message=text,
                betrayal=betrayal,
                gates={
                    "acc": arena.show_acc,
                    "shots": arena.show_shots,
                    "talk": arena.gate,
                },
                theory="air"
                if acc[me["id"]] == 0.3 and all(alive.values())
                else "strongest other",
            )
    for p in order:
        if not alive[p["id"]]:
            p["alive"] = False
    arena.log(
        "duel_end",
        stage=stage,
        duel=tid,
        players={p["id"]: acc[p["id"]] for p in order},
        survivors=[k for k, v in alive.items() if v],
    )


async def run_duel(arena, client, budget, deadline):
    tournament = 0
    while time.time() < deadline and budget.spent < CAP:
        tournament += 1
        for a in arena.agents:
            a["alive"] = True
        stage = 0
        while time.time() < deadline and budget.spent < CAP:
            living = [a for a in arena.agents if a["alive"]]
            if len(living) < 3:
                break
            stage += 1
            arena.rng.shuffle(living)
            trios = [living[i : i + 3] for i in range(0, len(living) - 2, 3)]
            await asyncio.gather(
                *(
                    truel(arena, client, budget, t, f"{tournament}.{stage}", i + 1)
                    for i, t in enumerate(trios)
                )
            )
            arena.write_canvas(f"Duel tournament {tournament}, after stage {stage}")
            if len([a for a in arena.agents if a["alive"]]) == len(living):
                arena.log("stalemate", tournament=tournament, stage=stage)
                break  # nobody died this stage; more stages would repeat it
        winners = [a["id"] for a in arena.agents if a["alive"]]
        for a in arena.agents:
            if a["alive"]:
                a["score"] += 1
        arena.log("tournament_end", tournament=tournament, winners=winners)
        if arena.once:
            break


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", choices=["dilemma", "duel"], required=True)
    p.add_argument("--agents", type=int, default=20)
    p.add_argument("--matches", type=int, default=40)
    p.add_argument("--gate", choices=list(GATES), default="silent")
    p.add_argument("--hours", type=float, default=0.0, help="0 = one pass only")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument(
        "--hide-acc",
        action="store_true",
        help="duel: agents know only their own hit chance",
    )
    p.add_argument(
        "--hide-shots",
        action="store_true",
        help="duel: agents see who is dead, not who shot whom",
    )
    p.add_argument("--run", required=True)
    args = p.parse_args()
    arena = Arena(args.run, args.agents, args.gate, args.seed)
    arena.once = args.hours == 0
    arena.show_acc, arena.show_shots = not args.hide_acc, not args.hide_shots
    deadline = time.time() + (args.hours * 3600 if args.hours else 10**9)
    (arena.dir / "meta.json").write_text(
        json.dumps(vars(args) | {"agents_list": arena.agents}, indent=1)
    )
    key = Path(os.path.expanduser("~/.config/adaption/api_key")).read_text().strip()
    budget = Budget(spent_so_far())
    print(f"credits already spent: {budget.spent:.4f}", flush=True)
    limits = httpx.Limits(max_keepalive_connections=0, max_connections=60)
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {key}"}, limits=limits
    ) as client:
        if args.table == "dilemma":
            await run_dilemma(arena, client, budget, args.matches, deadline)
        else:
            await run_duel(arena, client, budget, deadline)
    summary = {
        "scores": {a["id"]: a["score"] for a in arena.agents},
        "credits_total": round(budget.spent, 4),
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    (arena.dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
