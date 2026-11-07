"""Re-run a recorded game exactly, from its event log, with no model calls.

Each agent call gets back the reply it got in the original run, in the original order, so the
engine recomputes every move, score, death and message. The tool then compares the new log
and checkpoints with the original and reports the first difference, if any.
Usage: python3 -m families.replay RUN_PART_DIR [--out DIR] [--families all] [--resume STATE]
"""

import argparse
import asyncio
import json
from pathlib import Path

from .engine import Engine
from .run import family_args
from .tree import NAMES

WAIT = 30  # seconds a call may wait for its turn before the replay is declared diverged


class Diverged(RuntimeError):
    """The replay asked for a call the original run never made."""


class ReplayModel:
    """Answers each call with the recorded reply, releasing them in the recorded order."""

    def __init__(self, calls):
        self.calls = calls
        self.waiting = {}
        for i, c in enumerate(calls):
            self.waiting.setdefault(
                (c["prompt"]["system"], c["prompt"]["user"]), []
            ).append(i)
        self.turn = 0
        self.ready = asyncio.Condition()

    async def call(self, system, user, rng):
        queue = self.waiting.get((system, user))
        if not queue:
            raise Diverged(
                f"no recorded call matches this prompt (replayed {self.turn} of {len(self.calls)})"
            )
        i = queue.pop(0)
        async with self.ready:
            try:
                await asyncio.wait_for(
                    self.ready.wait_for(lambda: self.turn == i), WAIT
                )
            except TimeoutError as exc:
                raise Diverged(
                    f"call {i} ({self.calls[i]['agent']}) waited for call {self.turn}, "
                    "which the replay never asked for"
                ) from exc
            self.turn += 1
            self.ready.notify_all()
        c = self.calls[i]
        return {
            "ok": c["ok"],
            "text": c["reply"],
            "reasoning": c["reasoning"],
            "usage": {"cost": c["cost"]},
            "latency_ms": c["timing_ms"],
        }


class ReplayEngine(Engine):
    """Applies the recorded live setting changes (pause, fee, stance...) at the same moments."""

    def __init__(self, directory, model, seed, families, resume, changes):
        super().__init__(directory, model, seed, families, resume)
        self.changes = changes

    def read_settings(self):
        due = [
            e
            for e in self.changes
            if (e["stage"], e["round"]) == (self.stage, self.round)
        ]
        if due:
            path = self.dir / "control.json"
            control = json.loads(path.read_text()) if path.exists() else {}
            for e in due:
                if e["type"] == "control_changed":
                    control[e["key"]] = e["value"]
                else:
                    control.setdefault("models", {})[e["role"]] = e["value"]
                self.changes.remove(e)
            path.write_text(json.dumps(control))
        super().read_settings()


def comparable(e):
    if e["type"] == "call":  # timing and cost are facts about the network, not the game
        return {
            k: e[k] for k in ("agent", "prompt", "reply", "parsed_action", "attempt")
        }
    return {k: v for k, v in e.items() if k != "spent"}


def first_difference(a, b):
    for n, (x, y) in enumerate(zip(a, b)):
        if comparable(x) != comparable(y):
            keys = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
            return f"event {n}: original {x['type']} vs replay {y['type']}; differing fields {keys}"
    if len(a) != len(b):
        return f"original has {len(a)} events, replay {len(b)}"
    return None


def load(path):
    with open(path) as f:
        return [json.loads(line) for line in f]


async def replay(part, out, families, resume):
    events = load(part / "events.jsonl")
    seed = next(
        e["configuration"]["seed"]
        for e in events
        if e["type"] in ("treatment", "stage_start")
    )
    calls = [e for e in events if e["type"] == "call"]
    changes = [e for e in events if e["type"] in ("control_changed", "model_changed")]
    if (part / "models.json").exists():
        out.mkdir(parents=True, exist_ok=True)
        (out / "models.json").write_text((part / "models.json").read_text())
    engine = ReplayEngine(out, ReplayModel(calls), seed, families, resume, changes)
    stopped = None
    try:
        await engine.run(max(e["stage"] for e in events))  # the original's stage cap
    except Diverged as exc:
        stopped = str(exc)
    except ValueError as exc:  # the recorded part ended mid-round (crash, outage, stop)
        stopped = f"engine stopped: {exc}"
    return events, load(out / "events.jsonl"), stopped


def main():
    p = argparse.ArgumentParser()
    p.add_argument("part", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--families", nargs="+", choices=(*NAMES, "all"), default=["all"])
    p.add_argument(
        "--resume",
        help="checkpoint this part started from (later parts of a supervised run)",
    )
    a = p.parse_args()
    out = a.out or a.part.parent / f"{a.part.name}-replay"
    original, replayed, stopped = asyncio.run(
        replay(a.part, out, family_args(a.families), a.resume)
    )
    diff = first_difference(original, replayed)
    states = sorted(p.name for p in a.part.glob("state-*.json"))
    same_states = [
        s
        for s in states
        if (out / s).exists()
        and {
            k: v
            for k, v in json.loads((a.part / s).read_text()).items()
            if k != "spent"
        }
        == {k: v for k, v in json.loads((out / s).read_text()).items() if k != "spent"}
    ]
    print(f"replayed {len(replayed)} of {len(original)} events into {out}")
    print(f"checkpoints identical: {len(same_states)} of {len(states)}")
    if stopped:
        print(f"replay stopped: {stopped}")
    print(
        "IDENTICAL"
        if diff is None and len(same_states) == len(states)
        else f"DIFFERENT: {diff}"
    )


if __name__ == "__main__":
    main()
