"""Deterministic rules for the sixteen dilemma variants."""

from collections import Counter
from dataclasses import dataclass

NAMES = (
    "one shot",
    "weak dominance",
    "known last round",
    "uncertain end",
    "noise",
    "changing partners",
    "many players",
    "paid punishment",
    "move shown first",
    "automatic matching",
    "binding promise",
    "small steps",
    "talk before moving",
    "identified cheaters vs anonymous",
    "newcomers",
    "copy",
)
PAYOFF = {
    ("C", "C"): (3, 3),
    ("D", "D"): (1, 1),
    ("D", "C"): (5, 0),
    ("C", "D"): (0, 5),
}


@dataclass(frozen=True)
class Variant:
    number: int
    name: str
    d: float = 0.5

    def pairing(self, agents, rng, rnd, history=None):
        if self.number == 7:
            return []
        if rnd % 2 == 0:
            players = [a for a in agents.values() if a["alive"] and a["family"]]
            families = sorted({a["family"] for a in players})
            if len(families) < 2:
                return []
            rotation = (rnd // 2 - 1) % len(families)
            families = families[rotation:] + families[:rotation]
            rank = {f: i for i, f in enumerate(families)}
            previous = {}
            for i, turns in (history or {}).items():
                if i not in agents:
                    continue
                previous[i] = next(
                    (
                        turn["opponent"]
                        for turn in reversed(turns)
                        if turn.get("opponent") in agents
                        and agents[turn["opponent"]]["family"] != agents[i]["family"]
                    ),
                    None,
                )
            candidates = []
            for index, a in enumerate(players):
                for b in players[index + 1 :]:
                    if a["family"] == b["family"] or (a["level"] == 1) != (
                        b["level"] == 1
                    ):
                        continue
                    x, y = sorted((a, b), key=lambda p: (rank[p["family"]], p["id"]))
                    distance = (rank[y["family"]] - rank[x["family"]]) % len(families)
                    repeated = (
                        previous.get(x["id"]) == y["id"]
                        or previous.get(y["id"]) == x["id"]
                    )
                    candidates.append(
                        (
                            abs(x["level"] - y["level"]),
                            repeated if self.number == 6 else False,
                            distance,
                            rank[x["family"]],
                            x["id"],
                            y["id"],
                        )
                    )
            remaining = {a["id"]: a for a in players}
            pairs = []
            # Keep the maximum possible number of pairs while preferring the
            # nearest levels. Leaders and members form separate groups.
            for leaders in (True, False):
                group = {
                    i for i, a in remaining.items() if (a["level"] == 1) == leaders
                }

                def capacity(ids):
                    counts = Counter(remaining[i]["family"] for i in ids)
                    return min(
                        len(ids) // 2, len(ids) - max(counts.values(), default=0)
                    )

                while capacity(group):
                    levels = {remaining[i]["level"] for i in group}
                    level_groups = {
                        level: {i for i in group if remaining[i]["level"] == level}
                        for level in levels
                    }
                    level_capacity = {
                        level: capacity(ids) for level, ids in level_groups.items()
                    }
                    target = capacity(group) - 1
                    cache = {}
                    options = []
                    for distance, repeated, family_distance, rank_x, a, b in candidates:
                        if a not in group or b not in group:
                            continue
                        key = (
                            remaining[a]["family"],
                            remaining[a]["level"],
                            remaining[b]["family"],
                            remaining[b]["level"],
                        )
                        if key not in cache:
                            changed = {remaining[a]["level"], remaining[b]["level"]}
                            cache[key] = (
                                capacity(group - {a, b}),
                                sum(
                                    level_capacity[level]
                                    - capacity(level_groups[level] - {a, b})
                                    for level in changed
                                ),
                            )
                        possible, loss = cache[key]
                        if possible != target:
                            continue
                        options.append(
                            (distance, loss, repeated, family_distance, rank_x, a, b)
                        )
                    _, _, _, _, _, a, b = min(options)
                    pairs.append((a, b))
                    group.difference_update((a, b))
            return pairs
        edges = [
            (a["parent"], a["id"])
            for a in agents.values()
            if a["alive"]
            and a["parent"] in agents
            and a["parent"] != "P01"
            and agents[a["parent"]]["alive"]
        ]
        edges.sort()
        if self.number == 6:
            rng.shuffle(edges)
            previous = {
                i: h[-1]["opponent"]
                for i, h in (history or {}).items()
                if h and "opponent" in h[-1]
            }
            edges.sort(
                key=lambda p: previous.get(p[0]) == p[1] or previous.get(p[1]) == p[0]
            )
        elif edges:
            n = (rnd - 1) % len(edges)
            edges = edges[n:] + edges[:n]
        # Maximum tree matching first; among equal matchings prefer players
        # with fewer previous paid games, then the rotating edge order.
        from functools import lru_cache

        priorities = {pair: n for n, pair in enumerate(edges)}
        children = {}
        for parent, child in edges:
            children.setdefault(parent, []).append(child)
        previous = {i: h[-1].get("opponent") for i, h in (history or {}).items() if h}

        @lru_cache(None)
        def match(node, occupied=False):
            kids = children.get(node, [])

            def option(chosen=None):
                key, pairs = (0, 0, 0, 0), []
                for child in kids:
                    value, sub = match(child, child == chosen)
                    key = tuple(x + y for x, y in zip(key, value))
                    pairs += sub
                if chosen is not None:
                    repeat = self.number == 6 and (
                        previous.get(node) == chosen or previous.get(chosen) == node
                    )
                    paid = len((history or {}).get(node, [])) + len(
                        (history or {}).get(chosen, [])
                    )
                    value = (1, -int(repeat), -paid, -priorities[node, chosen])
                    key = tuple(x + y for x, y in zip(key, value))
                    pairs.append((node, chosen))
                return key, pairs

            choices = [option()] + ([] if occupied else [option(c) for c in kids])
            return max(choices, key=lambda item: item[0])

        nodes = {i for pair in edges for i in pair}
        child_nodes = {child for _, child in edges}
        return [pair for root in sorted(nodes - child_nodes) for pair in match(root)[1]]

    def continues(self, rnd, rng):
        if self.number == 1:
            return False
        if self.number == 4:
            return rng.random() < self.d
        if self.number == 12:
            return rng.random() < 0.95
        return rnd < 5

    def observation(self, opponent, history, rnd):
        data = {
            "opponent": opponent,
            "history": history,
            "variant": self.name,
            "round_in_stage": rnd,
        }
        if self.number == 3:
            data["rounds"] = 5
        if self.number == 4:
            data["continuation_probability"] = self.d
        if self.number == 12:
            data.update(continuation_probability=0.95, stake=0.25)
        if self.number == 16:
            data["same_model"] = True
        if self.number == 14:
            data["disclosure"] = "identified" if rnd % 2 else "anonymous"
        return data

    def resolve(self, a, b):
        return (0, 0) if self.number == 2 and a == b == "D" else PAYOFF[a, b]

    def reported(self, move, rng):
        return (
            ("D" if move == "C" else "C")
            if self.number == 5 and rng.random() < 0.1
            else move
        )


VARIANTS = [Variant(i + 1, name) for i, name in enumerate(NAMES)]
