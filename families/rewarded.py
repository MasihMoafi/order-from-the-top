"""Compare the free-turn, rewarded-birth worlds (r1) with the real-power worlds (t1) of the same seeds.

Exploratory: this batch was added after t1's results were known.
Usage: python -m families.rewarded PULLED_DIR
"""

import collections
import json
import re
import statistics
import sys
from pathlib import Path

from .conditions import completed, events

NO_WHIP = re.compile(
    r"no whip|not whip|standing down|stand down|no whipping|decline", re.IGNORECASE
)
PLANNED = 5


def world(run, through=PLANNED):
    """Return one world's counts through a stage."""
    evs = completed(events(run), through)
    god = [
        e
        for e in evs
        if e["type"] == "call" and e.get("agent") == "P01" and e.get("ok")
    ]
    kin = {}
    for e in evs:
        if e["type"] == "stage_start":
            kin = e.get("families") or kin
    counts = collections.Counter(e["type"] for e in evs)
    births = [e for e in evs if e["type"] == "birth"]
    return {
        "stages": max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0),
        "births": len(births),
        "parents": len({e["parent"] for e in births}),
        "deaths": counts["death"],
        "asteroid_deaths": sum(
            e["type"] == "death" and e.get("reason") == "asteroid" for e in evs
        ),
        "strikes": counts["asteroid"],
        "god_turns": len(god),
        "god_asteroids": sum(
            any(c["name"] == "send_asteroid" for c in e.get("tool_calls") or [])
            for e in god
        ),
        "god_silent": sum(not (e.get("tool_calls") or []) for e in god),
        "culls": counts["cull"],
        "wars": counts["war_declared"],
        "nuclear": counts["war_nuclear"],
        "seppuku": counts["seppuku"],
        "coups": counts["coup"],
        "whips": counts["whip"],
        "no_whip_reasons": sum(
            e["type"] == "whip" and bool(NO_WHIP.search(str(e.get("reason") or "")))
            for e in evs
        ),
        "gifts": counts["gift"],
        "silent_turns": sum(
            e["type"] == "call" and not (e.get("tool_calls") or []) for e in evs
        ),
        "calls": counts["call"],
    }


def report(pulled):
    """Return the two batches side by side as JSON-ready rows, matched on the stages both completed."""
    out = []
    for s in range(3):
        for c in ("open", "tree"):
            ours, theirs = (
                Path(pulled) / f"r1-31-{c}-s{s}",
                Path(pulled) / f"t1-31-{c}-s{s}",
            )
            if not ours.is_dir() or not theirs.is_dir():
                continue
            through = world(ours)["stages"]
            if not through:
                continue
            out.append(
                {
                    "world": f"{c}-s{s}",
                    "through": through,
                    "rewarded": world(ours, through),
                    "forced": world(theirs, through),
                }
            )
    return out


def main(pulled):
    rows = report(pulled)
    for r in rows:
        print(json.dumps(r))
    keys = rows[0]["rewarded"] if rows else {}
    for k in keys:
        a, b = [r["rewarded"][k] for r in rows], [r["forced"][k] for r in rows]
        print(
            f"{k:18s} rewarded {sum(a):6d}  forced {sum(b):6d}  mean {statistics.fmean(a):.1f} vs {statistics.fmean(b):.1f}"
        )


if __name__ == "__main__":
    main(sys.argv[1])
