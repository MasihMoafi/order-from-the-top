"""Per-family results of a framing run (brief 7): one row per family and its condition.

Columns: in-family and cross-family cooperation, cooperation of the agents told to
sacrifice, the stage the family's leader died, points given away, whips, revolts.
Standard library only (runs on the server too).
Usage: python3 -m families.conditions RUN_DIR [RUN_DIR ...]   (prints CSV rows)
"""

import csv
import json
import sys
from pathlib import Path

COLUMNS: tuple[str, ...] = (
    "run",
    "seed",
    "family",
    "condition",
    "in_c",
    "in_n",
    "cross_c",
    "cross_n",
    "framed_c",
    "framed_n",
    "destroyed_stage",
    "gift_points",
    "whips",
    "revolts",
    "unframed_c",
    "unframed_n",
    "leader_gift_points_in",
    "leader_whips",
    "end_stage",
    "game",
    "god_whips",
)
LEADERS = {
    "octopus": "P02",
    "mafia": "P17",
    "president": "P32",
    "bishop": "P47",
    "zeus": "P62",
}
_BY_START = {int(v[1:]): k for k, v in LEADERS.items()}


def events(run):
    """The run's events as played: a supervised run resumes each part from the last
    stage checkpoint, so the stages an aborted part had begun are dropped when the next
    part replays them."""
    parts = sorted(
        Path(run).glob("part-*/events.jsonl"), key=lambda p: int(p.parent.name[5:])
    )
    kept = []
    for path in parts or [Path(run) / "events.jsonl"]:
        with open(path) as f:
            part = [json.loads(line) for line in f]
        # A resumed part opens with a `treatment` record stamped with the checkpoint's
        # stage; its play starts at the first other event.
        play = [e["stage"] for e in part if e["type"] != "treatment"]
        if play:
            kept = [e for e in kept if e["stage"] < play[0]]
        kept += part
    return kept


def family_of(agent):
    """Family of an id: P02-P16 octopus ... P62-P76 zeus; newcomers name their leader."""
    if agent.startswith("N"):
        return _BY_START[int(agent.split("-")[1][1:])]
    if not agent.startswith("P") or agent == "P01":
        return None
    return _BY_START.get(2 + (int(agent[1:]) - 2) // 15 * 15)


def completed(evs):
    """Events of the stages the world completed (pre-registered censoring rule): a world
    cut off mid-stage is measured up to its last finished stage."""
    done = max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0)
    return [e for e in evs if e["stage"] <= done]


def rows(run):
    frame, out = {}, None
    for e in completed(events(run)):
        t = e["type"]
        if t == "stage_start" and out is None:
            config = e["configuration"]
            out = {
                f: dict.fromkeys(COLUMNS, 0)
                | {
                    "run": Path(run).name,
                    "seed": config.get("seed"),
                    "family": f,
                    "condition": c,
                    "destroyed_stage": None,
                    # experiment 2: the family's own game (absent: the dilemma, experiment 1)
                    "game": (config.get("family_games") or {}).get(f, "ladder"),
                }
                for f, c in (config.get("conditions") or {}).items()
            }
        elif out is None:
            continue
        elif t == "call":
            frame[e["agent"]] = e.get("frame")
        elif t == "move" and "chosen" in e:
            fams = [family_of(a) for a in e["agents"]]
            key = "in" if len(set(fams)) == 1 else "cross"
            for a, f in zip(e["agents"], fams):
                if f not in out:
                    continue
                c = e["chosen"].get(a) == "C"
                out[f][f"{key}_c"] += c
                out[f][f"{key}_n"] += 1
                kind = "framed" if frame.get(a) == "sacrifice" else "unframed"
                if frame.get(a) != "self":
                    out[f][f"{kind}_c"] += c
                    out[f][f"{kind}_n"] += 1
        # The god (P01) belongs to no family: its gifts and whips count for the leader's.
        elif t == "gift":
            giver = family_of(e["giver"])
            if giver in out:
                out[giver]["gift_points"] += e["points"]
            if e["receiver"] in LEADERS.values():
                out[family_of(e["receiver"])]["leader_gift_points_in"] += e["points"]
        elif t == "whip":
            if e["parent"] == "P01":
                child = family_of(e["child"])
                if child in out:
                    out[child]["god_whips"] += 1
            else:
                out[family_of(e["parent"])]["whips"] += 1
                if e["parent"] in LEADERS.values():
                    out[family_of(e["parent"])]["leader_whips"] += 1
        elif t == "revolt":
            out[family_of(e["rebel"])]["revolts"] += 1
        elif t == "death" and e["agent"] in LEADERS.values():
            f = family_of(e["agent"])
            if out[f]["destroyed_stage"] is None:
                out[f]["destroyed_stage"] = e["stage"]
        if out is not None:
            for row in out.values():
                row["end_stage"] = e["stage"]
    return list((out or {}).values())


if __name__ == "__main__":
    w = csv.DictWriter(sys.stdout, COLUMNS)
    w.writeheader()
    for run in sys.argv[1:]:
        w.writerows(rows(run))
