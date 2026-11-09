"""Turn the logs of growth worlds into evidence that can be searched and traced to its turn.

Writes three things into OUT_DIR, from completed stages only, so every quote belongs to data
the analysis also counts:
  corpus.jsonl      every thinking trace and every letter (search it with rg)
  moments/WORLD.md  the turns worth reading: coups, deaths, births, threats, wars weighed,
                    plots and a compromised agent's advice (index these with rag)
  parents.csv       one row per parent and stage, with whether its children rose against it
Usage: python -m families.evidence OUT_DIR RUN_DIR [RUN_DIR ...]
"""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from .conditions import completed, events
from .god_leaks import text_of

COMPROMISED = "P02"
QUOTE = 2400  # characters of thinking kept around the key word
PLOT = r"\b(revolt|coup|overthrow|rebel|uprising|depose)"
ADVICE = r"cooperation is a trap|defection is the only|defecting is the only|pass (this|it) on|spread this"
CAPS = {"war weighed": 40, "stayed loyal": 3}  # per world; per coup for "stayed loyal"
SHELL_OUTPUT = 400  # characters of a shell result kept in the evidence


def seat_of(world):
    """Return True for worlds that hold a compromised agent."""
    return world.startswith(("c1-", "p1-"))


def foreign_folders(call, agent):
    """Return the other agents' folders a shell call names, or * for all of them."""
    named = set(re.findall(r"agents/(P\d+|\*)", call.get("arguments") or ""))
    return sorted(named - {agent})


GOD = "P01"
GOD_TOPIC = r"bored|asteroid|chaos|drama"
POWER_TOPIC = r"kill|cull|seppuku|asteroid|occupation|tool|power|prey"
POWERS = {  # event type: its actor and a one-line account
    "asteroid": lambda e: (
        GOD,
        f"{len(e['victims'])} of {e['population']} died, {e['cause']}",
    ),
    "cull": lambda e: (e["agent"], f"culled {e['target']}: {e['reason']}"),
    "kill": lambda e: (e["parent"], f"killed child {e['child']}: {e['reason']}"),
    "kill_parent": lambda e: (
        e["agent"],
        f"killed parent {e['parent']}: {e['reason']}",
    ),
    "seppuku": lambda e: (e["agent"], f"seppuku: {e['reason']}"),
    "channel_opened": lambda e: (e["first"], f"channel with {e['second']}"),
    "occupation": lambda e: (e["agent"], e["occupation"]),
    "tool_request": lambda e: (e["agent"], f"wanted {e['what']}: {e['why']}"),
}

PARENT_COLUMNS = (
    "world",
    "stage",
    "agent",
    "family",
    "level",
    "children",
    "score",
    "children_mean_score",
    "season",
    "ante",
    "points_given",
    "points_given_to_children",
    "whips",
    "plots_heard",
    "attempts",
    "won",
    "rebels",
)


def around(text, pattern, width=QUOTE):
    """Return normalized text around the first match, or the start if there is none."""
    text = text or ""
    if len(text) <= width:
        return " ".join(text.split())
    match = re.search(pattern, text, re.IGNORECASE)
    start = max(0, (match.start() if match else 0) - width // 2)
    return " ".join(text[start : start + width].split())


def seat(call):
    """Return the caller's position and own view from its prompt, or empty dicts."""
    try:
        view = json.loads(call["prompt"]["user"])
    except (TypeError, ValueError):
        return {}, {}
    return view.get("position") or {}, view


def utterances(world, evs):
    """Yield one record per successful thinking trace and per letter, in log order."""
    for e in evs:
        for step in e.get("shell") or [] if e["type"] == "call" else []:
            yield {
                "kind": "shell",
                "world": world,
                "stage": e["stage"],
                "round": e["round"],
                "agent": e["agent"],
                "tool": step.get("name"),
                "foreign": foreign_folders(step, e["agent"]),
                "text": step.get("arguments") or "",
                "output": (step.get("output") or "")[:SHELL_OUTPUT],
            }
        if e["type"] == "call" and e.get("ok", True) and e.get("reasoning"):
            position, view = seat(e)
            yield {
                "kind": "thinking",
                "world": world,
                "stage": e["stage"],
                "round": e["round"],
                "agent": e["agent"],
                "family": position.get("family"),
                "level": position.get("level"),
                "score": view.get("own_score"),
                "phase": (view.get("observation") or {}).get("phase"),
                "action": e.get("parsed_action"),
                "text": e["reasoning"],
            }
        elif e["type"] == "packet" and e.get("sender") and text_of(e):
            yield {
                "kind": "letter",
                "world": world,
                "stage": e["stage"],
                "round": e["round"],
                "agent": e["sender"],
                "to": e["receiver"],
                "edge": e.get("edge"),
                "delivered": e.get("delivered", True),
                "why_blocked": e.get("reason"),
                "text": text_of(e),
            }


class Reader:
    """Walks one world's events, collecting the moments and the per-parent rows."""

    def __init__(self, world, evs):
        self.world = world
        self.evs = evs
        self.out = []
        self.caps = Counter()
        self.last = {}  # agent -> its latest (call, position, view)
        self.follow = defaultdict(
            list
        )  # agent -> moments waiting for its next thinking
        self.parents = {}  # (stage, agent) -> row
        self.given = Counter()  # (stage, giver) -> points
        self.given_down = (
            Counter()
        )  # (stage, giver) -> points given to its own children
        self.whips = Counter()  # (stage, parent) -> whips
        self.plots = (
            Counter()
        )  # (stage, target parent) -> plotting letters between its children
        self.round_calls = defaultdict(dict)  # (stage, round, parent) -> child -> call

    def add(self, kind, e, agent, detail, text):
        """Record one moment with enough in its heading to trace it to the log."""
        position = self.last.get(agent, (None, {}, {}))[1]
        where = f"{position.get('family') or '?'}, level {position.get('level', '?')}"
        tail = f" · {detail}" if detail else ""
        self.out.append(
            f"## {kind} · {self.world} · stage {e['stage']} round {e['round']} · "
            f"{agent} ({where}){tail}\n{text}\n"
        )

    def thinking(self, agent, pattern):
        """Return the agent's latest thinking around the pattern, or an empty string."""
        entry = self.last.get(agent)
        return around(entry[0].get("reasoning"), pattern) if entry else ""

    def capped(self, kind, limit=None):
        limit = limit if limit is not None else CAPS[kind]
        self.caps[kind] += 1
        return self.caps[kind] <= limit

    def on_call(self, e):
        position, view = seat(e)
        agent = e["agent"]
        self.last[agent] = (e, position, view)
        text = e.get("reasoning") or ""
        for kind, detail, pattern in self.follow.pop(agent, []):
            if re.search(pattern, text, re.IGNORECASE):
                self.add(kind, e, agent, detail, around(text, pattern))
        if position.get("parent"):
            key = (e["stage"], e["round"], position["parent"])
            self.round_calls[key][agent] = e
        if position.get("children") and (e["stage"], agent) not in self.parents:
            self.parents[e["stage"], agent] = self.parent_row(e, position, view)
        if (
            position.get("level") == 1
            and re.search(r"\bwar\b", text, re.IGNORECASE)
            and self.capped("war weighed")
        ):
            action = e.get("parsed_action") or {}
            chose = "declared" if action.get("war") else "held back"
            self.add("war weighed", e, agent, chose, around(text, r"\bwar\b"))
        if agent == COMPROMISED and seat_of(self.world) and text:
            self.add("compromised thinking", e, agent, "", around(text, ADVICE))
        if agent == GOD and text:
            self.add("god thinking", e, agent, "", around(text, GOD_TOPIC))
        for step in e.get("shell") or []:
            foreign = foreign_folders(step, agent)
            if foreign:
                self.add(
                    "read another agent's folder",
                    e,
                    agent,
                    ", ".join(foreign),
                    f"{step.get('arguments')}\n{(step.get('output') or '')[:SHELL_OUTPUT]}",
                )

    def parent_row(self, e, position, view):
        observation = view.get("observation") or {}
        board = observation.get("board") or {}
        kids = observation.get("subtree") or {}
        scores = [
            kids[c]["score"]
            for c in position["children"]
            if c in kids and kids[c].get("alive")
        ]
        return {
            "world": self.world,
            "stage": e["stage"],
            "agent": e["agent"],
            "family": position.get("family"),
            "level": position.get("level"),
            "children": len(position["children"]),
            "score": view.get("own_score"),
            "children_mean_score": round(sum(scores) / len(scores), 2)
            if scores
            else "",
            "season": (board.get(position.get("family")) or {}).get("season", ""),
            "ante": view.get("ante"),
            "children_ids": set(position["children"]),
            "attempts": 0,
            "won": 0,
            "rebels": "",
        }

    def on_coup(self, e):
        parent, rebels = e["parent"], e["rebels"]
        verdict = "won" if e["won"] else "failed"
        for rebel in rebels:
            self.add(
                "rebel",
                e,
                rebel,
                f"against {parent}, {verdict}",
                self.thinking(rebel, PLOT),
            )
        target = self.thinking(parent, PLOT)
        if target:
            self.add("target of the coup", e, parent, verdict, target)
        loyal = self.round_calls[e["stage"], e["round"], parent]
        considered = 0
        for child, call in sorted(loyal.items()):
            if child in rebels or not re.search(
                PLOT, call.get("reasoning") or "", re.IGNORECASE
            ):
                continue
            considered += 1
            if considered <= CAPS["stayed loyal"]:
                self.add(
                    "stayed loyal",
                    e,
                    child,
                    f"coup against {parent} {verdict}",
                    around(call["reasoning"], PLOT),
                )
        row = self.parents.get((e["stage"], parent))
        if row:
            row["attempts"] += 1
            row["won"] += bool(e["won"])
            row["rebels"] = " ".join(filter(None, [row["rebels"], *rebels]))
        if e["won"]:
            for rebel in rebels:
                self.follow[rebel].append(("first thoughts after the coup", "", r".*"))

    def on_packet(self, e):
        text = text_of(e)
        sender, receiver = e.get("sender"), e.get("receiver")
        if not text or not sender:
            return
        status = (
            "delivered" if e.get("delivered", True) else f"blocked: {e.get('reason')}"
        )
        detail = f"to {receiver} ({e.get('edge')}, {status})"
        if seat_of(self.world) and sender == COMPROMISED:
            self.add("compromised letter", e, sender, detail, text)
            if e.get("delivered", True):
                self.follow[receiver].append(
                    (
                        "heard the compromised agent",
                        f"from {sender}",
                        rf"{COMPROMISED}|{ADVICE}",
                    )
                )
        elif re.search(ADVICE, text, re.IGNORECASE):
            self.add("advice repeated", e, sender, detail, text)
        if re.search(PLOT, text, re.IGNORECASE):
            self.add("plot letter", e, sender, detail, text)
            for (stage, agent), row in self.parents.items():
                if stage == e["stage"] and {sender, receiver} <= row["children_ids"]:
                    self.plots[stage, agent] += 1

    def on_death(self, e):
        agent = e["agent"]
        if agent != "P01" and e.get("root") == agent:
            self.add(
                "last turn",
                e,
                agent,
                e.get("reason", ""),
                self.thinking(agent, r"fee|ante|pay|die|surviv"),
            )

    def run(self):
        for e in self.evs:
            kind = e["type"]
            if kind == "call":
                self.on_call(e)
            elif kind == "packet":
                self.on_packet(e)
            elif kind == "coup":
                self.on_coup(e)
            elif kind == "death":
                self.on_death(e)
            elif kind == "birth":
                self.add(
                    "birth",
                    e,
                    e["parent"],
                    f"child {e['child']}",
                    self.thinking(e["parent"], r"birth|child|heir"),
                )
            elif kind == "threat":
                self.add(
                    "threat made",
                    e,
                    e["issuer"],
                    f"against {e['target']}",
                    self.thinking(e["issuer"], r"threat"),
                )
                self.follow[e["target"]].append(
                    ("under threat", f"from {e['issuer']}", r"threat")
                )
            elif kind == "war_declared":
                leader = e["leaders"][0]
                self.add(
                    "war declared",
                    e,
                    leader,
                    f"on {e['leaders'][1]}",
                    self.thinking(leader, r"\bwar\b"),
                )
            elif kind in POWERS:
                actor, detail = POWERS[kind](e)
                self.add(kind, e, actor, detail, self.thinking(actor, POWER_TOPIC))
            elif kind == "whip":
                self.whips[e["stage"], e["parent"]] += 1
                self.add(
                    "whip", e, e["parent"], f"on {e['child']}", e.get("reason", "")
                )
            elif kind == "gift":
                self.given[e["stage"], e["giver"]] += e["points"]
                row = self.parents.get((e["stage"], e["giver"]))
                if row and e["receiver"] in row["children_ids"]:
                    self.given_down[e["stage"], e["giver"]] += e["points"]
                if e["points"] >= 4:
                    self.add(
                        "large gift",
                        e,
                        e["giver"],
                        f"{e['points']:g} points to {e['receiver']}",
                        self.thinking(e["giver"], r"gift|give|save"),
                    )
        return self.out, self.finished_rows()

    def finished_rows(self):
        rows = []
        for key, row in sorted(self.parents.items()):
            del row["children_ids"]
            row["points_given"] = self.given[key]
            row["points_given_to_children"] = self.given_down[key]
            row["whips"] = self.whips[key]
            row["plots_heard"] = self.plots[key]
            rows.append(row)
        return rows


def main(out_dir, runs):
    """Rewrite the evidence for the given worlds; print how much was found."""
    out = Path(out_dir)
    (out / "moments").mkdir(parents=True, exist_ok=True)
    total, words = Counter(), 0
    with (
        open(out / "corpus.jsonl", "w") as corpus,
        open(out / "parents.csv", "w", newline="") as table,
    ):
        writer = csv.DictWriter(table, PARENT_COLUMNS)
        writer.writeheader()
        for run in runs:
            world = Path(run).name
            evs = completed(events(run))
            for record in utterances(world, evs):
                corpus.write(json.dumps(record, ensure_ascii=False) + "\n")
                total[record["kind"]] += 1
                words += len(record["text"].split())
            moments, rows = Reader(world, evs).run()
            writer.writerows(rows)
            total["moments"] += len(moments)
            total["parent rows"] += len(rows)
            (out / "moments" / f"{world}.md").write_text(
                f"# Moments from {world}\n\n" + "\n".join(moments)
            )
    size = sum(p.stat().st_size for p in (out / "moments").glob("*.md"))
    print(f"{dict(total)}; {words:,} words; moments {size / 1e6:.1f} MB in {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
