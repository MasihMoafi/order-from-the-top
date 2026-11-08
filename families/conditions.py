"""Count per-family outcomes for the framing and family-game experiments.

Resumed parts replace replayed stages; only completed stages enter rows().
HORIZON limits every caller of rows() unless an explicit horizon is supplied.
Usage: python -m families.conditions RUN_DIR [RUN_DIR ...] (CSV on stdout).
"""

import csv
import json
import os
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
    "alive_end",
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
    """Return decoded events with replayed stages replaced by each later part.

    A resumed treatment marker does not set the replacement stage; the first
    other event does. Missing logs and malformed JSON raise errors.
    """
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
    """Return the family of an original or newcomer ID, or None for the god.

    Unrecognized nonplayer IDs return None; malformed numeric or newcomer IDs
    can raise ValueError, IndexError or KeyError.
    """
    if agent.startswith("N"):
        return _BY_START[int(agent.split("-")[1][1:])]
    if not agent.startswith("P") or agent == "P01":
        return None
    return _BY_START.get(2 + (int(agent[1:]) - 2) // 15 * 15)


def completed(evs, horizon=None):
    """Return events through the last completed stage, capped by a truthy horizon.

    No completed stages means stage-zero events only.
    """
    done = max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0)
    if horizon:
        done = min(done, horizon)
    return [e for e in evs if e["stage"] <= done]


def rows(run, horizon=None):
    """Return one outcome row per configured family, or [] without a completed stage.

    A falsy horizon uses HORIZON from the environment; an unset or zero HORIZON
    leaves stages uncapped. Invalid HORIZON integers and malformed logs raise.
    """
    horizon = horizon or int(os.environ.get("HORIZON", "0")) or None
    frame, out = {}, None
    for e in completed(events(run), horizon):
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
                    "alive_end": 15,
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
        elif t == "death" and e["agent"].startswith("P") and e["agent"] != "P01":
            f = family_of(e["agent"])
            if f in out:
                out[f]["alive_end"] -= 1  # of the 15 original members
                if e["agent"] in LEADERS.values() and out[f]["destroyed_stage"] is None:
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
