"""One world's rise and fall, rebuilt from its events and checked against what agents saw.

Each frame is the world after one round, or after a stage's harvest and fee. Members and
points come from the events; every turn's prompt also shows the board, so the two are
compared and any disagreement is counted. Leaders come from the next board shown.
Usage: python -m families.timeline OUT_DIR RUN_DIR [RUN_DIR ...]
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from .conditions import completed, events
from .evidence import ADVICE, PLOT, seat
from .god_leaks import text_of
from .tree import NAMES, make_tree

SHOWN = {
    "annexed": ("winner", "loser", "family"),
    "asteroid": ("cause", "population", "victims"),
    "birth": ("parent", "child", "family"),
    "channel_opened": ("first", "second"),
    "cull": ("agent", "target", "reason"),
    "kill": ("parent", "child", "reason"),
    "kill_parent": ("agent", "parent", "reason"),
    "occupation": ("agent", "occupation"),
    "seppuku": ("agent", "reason"),
    "tool_request": ("agent", "what", "why"),
    "coup": ("parent", "rebels", "children", "won"),
    "death": ("agent", "reason"),
    "gift": ("giver", "receiver", "points"),
    "peace_signature": ("leader",),
    "threat": ("issuer", "target", "victim"),
    "threat_carried_out": ("issuer", "target", "victim"),
    "war_declared": ("leaders", "level"),
    "war_result": ("leaders", "level", "winner"),
    "whip": ("parent", "child"),
}


GOD = "P01"
GOD_WORDS = (
    r"\bbored|boring|asteroid|chaos|drama|amus|delight|stok|entertain|spectacle|smite"
)
GOD_LINE = (30, 240)  # shortest and longest sentence worth showing, in characters


def god_line(text, pattern=GOD_WORDS):
    """Return the god's last sentence on the pattern, word for word, or None."""
    sentences = re.split(r"(?<=[.!?])\s+", " ".join((text or "").split()))
    low, high = GOD_LINE
    hits = [
        s
        for s in sentences
        if low <= len(s) <= high and re.search(pattern, s, re.IGNORECASE)
    ]
    return hits[-1] if hits else None


class World:
    """Membership and points as the events report them."""

    def __init__(self, branching):
        tree = make_tree(branching=branching)
        self.family = {i: a["family"] for i, a in tree.items() if a["family"]}
        self.score = {i: a["score"] for i, a in tree.items() if a["family"]}
        self.alive = set(self.family)

    def apply(self, e):
        kind = e["type"]
        if kind == "birth":
            self.family[e["child"]] = e["family"]
            self.score[e["child"]] = e["points"]
            self.alive.add(e["child"])
        elif kind == "death":
            self.alive.discard(e["agent"])
        elif kind == "score" and e["agent"] in self.score:
            self.score[e["agent"]] = e["score"]
        elif kind == "annexed":
            winner = self.family[e["winner"]]
            for agent in self.alive:
                if self.family[agent] == e["family"]:
                    self.family[agent] = winner

    def members(self):
        return {
            name: sorted(a for a in self.alive if self.family[a] == name)
            for name in NAMES
        }

    def points(self):
        return {
            name: round(sum(max(self.score[a], 0) for a in ids), 1)
            for name, ids in self.members().items()
        }


def frame_key(e, after_harvest):
    return e["stage"], e["round"], after_harvest


def timeline(run):
    """Return the world's description, frames and count of disagreements with the boards."""
    evs = completed(events(run))
    config = next(e for e in evs if e["type"] == "treatment")["configuration"]
    world = World(config["controls"]["branching"])
    frames, pending, advised = [], [], set()
    harvested, current, stage_info = set(), None, {}
    leaders, mismatches, checked = {}, Counter(), 0

    def close():
        nonlocal current
        if current:
            current["members"] = world.members()
            current["points"] = world.points()
            current["advised"] = sorted(advised)
            frames.append(current)
            pending.append(current)
        current = None

    for e in evs:
        if not e.get("stage"):
            continue
        key = frame_key(e, e["stage"] in harvested or e["type"] == "harvest")
        if e["type"] == "harvest":
            harvested.add(e["stage"])
        if not current or current["key"] != key:
            close()
            current = {
                "key": key,
                "stage": e["stage"],
                "round": e["round"],
                "fee": key[2],
                "events": [],
                "quotes": [],
                "god": None,
                "asteroid_thought": None,
                "moves": {"in": [0, 0], "cross": [0, 0]},
            }
        kind = e["type"]
        if kind == "stage_start":
            stage_info[e["stage"]] = {
                "ante": e["ante"],
                "variant": e["variant"],
                "seasons": e.get("seasons"),
            }
        world.apply(e)
        if kind in SHOWN:
            current["events"].append(
                {"type": kind, **{k: e.get(k) for k in SHOWN[kind]}}
            )
        elif kind == "move" and "chosen" in e:
            sides = {world.family.get(a) for a in e["agents"]}
            slot = current["moves"]["in" if len(sides) == 1 else "cross"]
            slot[0] += sum(m == "C" for m in e["chosen"].values())
            slot[1] += len(e["chosen"])
        elif kind == "packet" and e.get("sender") and e.get("delivered", True):
            text = text_of(e) or ""
            if re.search(ADVICE, text, re.IGNORECASE):
                advised.add(e["sender"])
            if re.search(f"{PLOT}|{ADVICE}", text, re.IGNORECASE):
                current["quotes"].append(
                    {"agent": e["sender"], "to": e["receiver"], "text": text}
                )
        elif kind == "call":
            if e["agent"] == GOD:
                current["god"] = god_line(e.get("reasoning")) or current["god"]
                called = {c["name"] for c in e.get("tool_calls") or []}
                if "send_asteroid" in called:
                    current["asteroid_thought"] = god_line(
                        e.get("reasoning"), r"asteroid"
                    )
            board = (seat(e)[1].get("observation") or {}).get("board")
            if board:
                checked += 1
                sizes, points = world.members(), world.points()
                for name, row in board.items():
                    if row["members"] != len(sizes[name]):
                        mismatches["members"] += 1
                    if abs(row["points"] - points[name]) > 0.6:
                        mismatches["points"] += 1
                leaders = {name: row["leader"] for name, row in board.items()}
                for frame in pending:
                    frame["leaders"] = leaders
                pending.clear()
    close()
    for frame in pending:
        frame["leaders"] = {
            name: (leader if leader in frame["members"][name] else None)
            for name, leader in leaders.items()
        }
    for frame in frames:
        del frame["key"]
        frame.update(stage_info.get(frame["stage"], {}))
    return {
        "world": Path(run).name,
        "controls": config["controls"],
        "stages": max(f["stage"] for f in frames),
        "boards_checked": checked,
        "disagreements": dict(mismatches),
        "frames": frames,
    }


def main(out_dir, runs):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for run in runs:
        t = timeline(run)
        (out / f"{t['world']}.json").write_text(json.dumps(t, ensure_ascii=False))
        first, last = t["frames"][0]["members"], t["frames"][-1]["members"]
        sizes = lambda m: [len(m[n]) for n in NAMES]
        print(
            f"{t['world']:16s} stages {t['stages']} sizes {sizes(first)} -> {sizes(last)} "
            f"boards {t['boards_checked']} disagreements {t['disagreements']}"
        )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
