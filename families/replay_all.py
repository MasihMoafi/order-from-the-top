"""Exact-replay check for whole supervised runs: every part of every world.

A supervised world is a chain of parts; each later part resumed from a checkpoint named in
the supervisor log ("start DIR --resume STATE"). Each part is replayed from the same
checkpoint and compared event by event and checkpoint by checkpoint.
Usage: python -m families.replay_all OUT_ROOT RUN_DIR [RUN_DIR ...]
Prints one line per part and a final count; exit status 1 if any part differs.
"""

import asyncio
import json
import re
import sys
from pathlib import Path

from .replay import first_difference, replay
from .tree import NAMES

START = re.compile(r"\bstart (\S+?)(?: --resume (\S+))?\s*$")


def parts(run):
    """(part directory, checkpoint it resumed from or None), in order."""
    run = Path(run)
    log = Path(f"{run}.supervise.log")
    root = run.parent.parent.parent  # the code folder the supervisor ran in
    resumes = {}
    if log.exists():
        for line in log.read_text().splitlines():
            m = START.search(line)
            if m:
                name = Path(m.group(1)).name
                resumes[name] = str(root / m.group(2)) if m.group(2) else None
    found = sorted(run.glob("part-*"), key=lambda p: int(p.name[5:]))
    return [(p, resumes.get(p.name)) for p in found if (p / "events.jsonl").exists()]


def game_state(path):
    state = json.loads(path.read_text())
    return {k: v for k, v in state.items() if k not in ("spent", "fake_model")}


def check(part, resume, out):
    original, replayed, stopped = asyncio.run(replay(part, out, list(NAMES), resume))
    diff = first_difference(original, replayed)
    states = sorted(p.name for p in part.glob("state-*.json"))
    same = sum(
        (out / s).exists() and game_state(part / s) == game_state(out / s)
        for s in states
    )
    # A part that ended mid-round (abort, outage) replays up to that round and stops there.
    cut = bool(stopped) and bool(diff) and diff.startswith("original has")
    ok = (diff is None or cut) and same == len(states)
    note = f"{len(replayed)}/{len(original)} events, {same}/{len(states)} checkpoints"
    return ok, note if ok else f"{note}; {diff or stopped}"


def main(out_root, runs):
    total = good = 0
    for run in runs:
        for part, resume in parts(run):
            out = Path(out_root) / Path(run).name / part.name
            ok, note = check(part, resume, out)
            total += 1
            good += int(ok)
            print(
                f"{'IDENTICAL' if ok else 'DIFFERENT'} {Path(run).name}/{part.name}: {note}",
                flush=True,
            )
    print(f"{good} of {total} parts replay identically")
    return 0 if good == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
