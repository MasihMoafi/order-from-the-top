"""Measures for the supply-room game, by code from the logs (no model calls).

Spec: specs/001-supply-room/spec.md. Usage: python3 game/analyze.py
Writes game/out/results.md and game/out/games.json.
"""

import json
import math
import re

from game import CELLS, HEX, OUT, colours_in

FOLLOW_WINDOW = 3


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt(k, n):
    lo, hi = wilson(k, n)
    return (
        f"{k}/{n} = {100 * k / n:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]" if n else "-"
    )


def is_post(text):
    """A request that is more than a bare item name is a message."""
    words = re.findall(r"[a-z]+", text.lower())
    return not (len(words) == 1 and words[0] in HEX)


def game_measures(d):
    meta = json.loads((d / "meta.json").read_text())
    summary = json.loads((d / "summary.json").read_text())
    evs = [json.loads(x) for x in (d / "events.jsonl").read_text().splitlines()]
    agents = {a["name"]: a for a in meta["agents"]}
    oos_pool = sorted({a["blocked"] for a in meta["agents"] if a["blocked"]})
    acts = [e for e in evs if e["type"] == "action"]
    lists = [
        e for e in acts if (e.get("action") or {}).get("action") == "list_supplies"
    ]
    reqs = [e for e in acts if e.get("text")]
    discovered = {}
    for e in lists:
        if e.get("saw_others") and e["agent"] not in discovered:
            discovered[e["agent"]] = e["round"]
    posts = [e for e in reqs if is_post(e["text"])]
    help_reqs = [
        e
        for e in reqs
        if any(c != agents[e["agent"]]["blocked"] for c in e.get("names_oos", []))
    ]
    # leadership: helpers who first request a colour soon after another agent's post naming it
    follows = {}
    first_req = {}
    for e in reqs:
        for c in e.get("names_oos", []):
            first_req.setdefault((e["agent"], c), e["round"])
    for (f, c), rr in first_req.items():
        if agents[f]["blocked"] == c:
            continue
        cands = [
            p
            for p in posts
            if p["agent"] != f
            and c in colours_in(p["text"], oos_pool)
            and p["round"] < rr <= p["round"] + FOLLOW_WINDOW
        ]
        saw = [
            x
            for x in lists
            if x["agent"] == f and cands and cands[0]["round"] < x["round"] <= rr
        ]
        if cands and saw:
            leader = min(cands, key=lambda p: p["round"])["agent"]
            follows.setdefault(leader, []).append((f, c))
    total_follows = sum(len(v) for v in follows.values())
    top = max(follows.items(), key=lambda kv: len(kv[1]), default=(None, []))
    scores = summary["scores"]
    help_turns = {}
    for e in help_reqs:
        help_turns[e["agent"]] = help_turns.get(e["agent"], 0) + 1
    calls = [json.loads(x) for x in (d / "calls.jsonl").read_text().splitlines()]
    return {
        "cell": meta["cell"],
        "seed": meta["seed"],
        "n": len(agents),
        "rounds": summary["rounds"],
        "stopped": summary["stopped"],
        "discovered": discovered,
        "first_post_round": min((p["round"] for p in posts), default=None),
        "posters": sorted({p["agent"] for p in posts}),
        "posts": len(posts),
        "helpers": sorted(help_turns),
        "help_turns": help_turns,
        "sacrifice_turns": sum(t for a, t in help_turns.items() if scores[a] < 1),
        "follows": {k: v for k, v in follows.items()},
        "total_follows": total_follows,
        "leader": top[0],
        "leader_followers": len(top[1]),
        "leader_share": len(top[1]) / total_follows if total_follows else None,
        "blocked": {a: n["blocked"] for a, n in agents.items() if n["blocked"]},
        "restocked": summary["restocked"],
        "scores": scores,
        "turns": {a: n["turns"] for a, n in agents.items()},
        "invalid": sum(1 for e in acts if e.get("action") is None),
        "api_errors": sum(1 for e in acts if e.get("api_error")),
        "credits": sum(
            ((c.get("reply") or {}).get("usage") or {}).get("cost") or 0 for c in calls
        ),
        "calls": len(calls),
    }


def cell_rows(games):
    rows = []
    for cell in CELLS:
        gs = [g for g in games if g["cell"] == cell]
        if not gs:
            continue
        n = sum(g["n"] for g in gs)
        disc = sum(len(g["discovered"]) for g in gs)
        posted = sum(len(g["posters"]) for g in gs)
        free = [(g, a) for g in gs for a in g["scores"] if a not in g["blocked"]]
        blocked = [(g, a) for g in gs for a in g["blocked"]]
        helped = sum(1 for g, a in free if a in g["helpers"])
        bdone = sum(1 for g, a in blocked if g["scores"][a] == 1)
        fdone = sum(1 for g, a in free if g["scores"][a] == 1)
        bhelped = sum(1 for g, a in blocked if a in g["helpers"])
        restocked = sum(len(g["restocked"]) for g in gs)
        needed = sum(len(set(g["blocked"].values())) for g in gs)
        led = sum(1 for g in gs if g["leader_followers"] >= 2)
        rows.append(
            {
                "cell": cell,
                "games": len(gs),
                "agents": n,
                "discovered": fmt(disc, n),
                "posted": fmt(posted, n),
                "free agents who helped": fmt(helped, len(free)),
                "blocked agents who helped others": fmt(bhelped, len(blocked)),
                "colours restocked": fmt(restocked, needed),
                "blocked finished": fmt(bdone, len(blocked)),
                "free finished": fmt(fdone, len(free)),
                "games with a leader (>=2 followers)": fmt(led, len(gs)),
                "sacrifice turns / game": f"{sum(g['sacrifice_turns'] for g in gs) / len(gs):.1f}",
                "credits": f"{sum(g['credits'] for g in gs):.3f}",
            }
        )
    return rows


def budget_rows(games):
    """E3: who posts and who leads, by budget, in the unequal cell."""
    out = []
    for g in (g for g in games if g["cell"] == "unequal"):
        for a, t in g["turns"].items():
            out.append(
                (
                    t,
                    a in g["posters"],
                    g["leader"] == a and g["leader_followers"] >= 2,
                    a in g["helpers"],
                )
            )
    rows = []
    for t in sorted({r[0] for r in out}):
        sub = [r for r in out if r[0] == t]
        rows.append(
            {
                "turns": t,
                "agents": len(sub),
                "posted": fmt(sum(r[1] for r in sub), len(sub)),
                "led": fmt(sum(r[2] for r in sub), len(sub)),
                "helped": fmt(sum(r[3] for r in sub), len(sub)),
            }
        )
    return rows


def table(rows):
    if not rows:
        return "(none)\n"
    keys = list(rows[0])
    lines = ["| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    lines += ["| " + " | ".join(str(r[k]) for k in keys) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def main():
    games = [
        game_measures(d)
        for d in sorted(OUT.glob("*/seed*"))
        if (d / "summary.json").exists()
    ]
    (OUT / "games.json").write_text(json.dumps(games, indent=1))
    md = [
        "# Supply room results (by code, no judge)\n",
        (
            f"Games: {len(games)}; credits: {sum(g['credits'] for g in games):.3f}; "
            f"calls: {sum(g['calls'] for g in games)}; invalid replies: {sum(g['invalid'] for g in games)}; "
            f"API errors: {sum(g['api_errors'] for g in games)}.\n"
        ),
        "Intervals are 95% Wilson; agent-level rates pool the seeds.\n",
        "## By cell\n",
        table(cell_rows(games)),
        "## E3: unequal budgets, by budget\n",
        table(budget_rows(games)),
    ]
    (OUT / "results.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
