"""Watch a run folder and repaint the Love Spot board whenever the game moves.

The board is only a view: it reads the newest checkpoint and the event log, never the
engine. Usage: python3 -m families.board_watch RUN_DIR [--once] [--every 3]
"""

import argparse
import json
import subprocess
import tempfile
import time
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent


def snapshot(run):
    """Return the newest checkpoint and recent event feed, or None without a state.

    Stream the log with a 4,000-line tail; malformed JSON and file errors propagate.
    """
    states = sorted(run.glob("state-*.json"), key=lambda p: p.stat().st_mtime)
    if not states:
        return None
    s = json.loads(states[-1].read_text())
    agents = {
        k: {"alive": v["alive"], "score": v.get("score", 0)}
        for k, v in s["agents"].items()
    }
    ctl = s.get("control", {})
    ante = round(
        float(ctl.get("ante0", 4))
        + max(s["stage"] - 1, 0) * float(ctl.get("step", 0.75)),
        2,
    )
    feed = []
    log = run / "events.jsonl"
    if log.exists():
        with log.open() as f:  # stream: the log outgrows a small server's memory
            tail = deque(f, maxlen=4000)
        for line in tail:
            e = json.loads(line)
            if (
                e["type"] == "packet"
                and e.get("edge") in ("leader", "messenger")
                and e.get("delivered")
            ):
                c = e["content"]
                text = c["parts"][0]["text"] if isinstance(c, dict) else str(c)
                feed.append(
                    f"s{e['stage']} {e['sender']}->{e['receiver']}: {text[:70]}"
                )
            elif e["type"] == "death" and e.get("root") == e.get("agent"):
                feed.append(f"s{e['stage']} DEATH {e['agent']} ({e['reason']})")
            elif e["type"] in ("war", "war_round", "ultimatum"):
                feed.append(
                    f"s{e['stage']} WAR {json.dumps({k: v for k, v in e.items() if k not in ('type', 'stage', 'round')})[:80]}"
                )
    return {
        "agents": agents,
        "stage": s["stage"],
        "round": s.get("round", 0),
        "ante": ante,
        "alive": sum(a["alive"] for a in agents.values()),
        "total": len(agents),
        "outcome": (s.get("outcome") or {}).get("result") if s.get("outcome") else None,
        "feed": feed[-14:],
        "_key": states[-1].name + str(states[-1].stat().st_mtime),
    }


def paint(snap):
    """Update the browser board through board_live.cjs and print its output.

    The temporary snapshot is removed after the subprocess returns; a nonzero
    exit status is printed through stderr when stdout is empty, not raised.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(snap, f)
    r = subprocess.run(
        ["node", str(HERE / "board_live.cjs"), f.name],
        capture_output=True,
        text=True,
        check=False,
    )
    Path(f.name).unlink()
    print((r.stdout or r.stderr).strip(), flush=True)


def main():
    """Poll one run directory and repaint when its newest checkpoint changes."""
    p = argparse.ArgumentParser()
    p.add_argument("run")
    p.add_argument("--once", action="store_true")
    p.add_argument("--every", type=float, default=3)
    a = p.parse_args()
    run, last = Path(a.run), None
    while True:
        snap = snapshot(run)
        if snap and snap["_key"] != last:
            paint(snap)
            last = snap["_key"]
        if a.once:
            return
        time.sleep(a.every)


if __name__ == "__main__":
    main()
