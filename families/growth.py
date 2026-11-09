"""Measure growth worlds (experiment 3) and test whether change with size is smooth or a jump.

One row per world at a common horizon: cooperation, deaths and how they happened, coups,
wars, births, threats, blocked messages and how concentrated talk is. summarise() groups
rows by size and channels; jump() applies the pre-registered smooth-or-jump rule.
Usage: python -m families.growth PULLED_DIR PREFIX [HORIZON]
"""

import random
import statistics
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path

from .conditions import completed, events
from .tree import make_tree

MEASURES = (
    "in_family_c",
    "cross_c",
    "dead_share",
    "coups_per_100",
    "coups_won",
    "wars",
    "births",
    "threats",
    "blocked_per_100",
    "hub_share",
    "family_spread",
)


def gini(values):
    """Return the Gini coefficient of non-negative values, or 0 for an empty or zero list."""
    values = sorted(values)
    total, n = sum(values), len(values)
    if not n or not total:
        return 0.0
    return (
        2 * sum((i + 1) * v for i, v in enumerate(values)) / (n * total) - (n + 1) / n
    )


def world_row(run, horizon=None):
    """Return one world's measures through the horizon, or None if no stage completed."""
    evs = completed(events(run), horizon)
    last = max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0)
    if not last:
        return None
    config = next(e for e in evs if e["type"] == "treatment")["configuration"]
    controls = config["controls"]
    tree = make_tree(branching=controls["branching"])
    family = {i: a["family"] for i, a in tree.items() if a["family"]}
    start = len(family)
    counts = Counter()
    deaths, received = Counter(), Counter()
    dead = set()
    moves = [0, 0, 0, 0]  # in-family C, in-family n, cross C, cross n
    agent_rounds = 0
    for e in evs:
        kind = e["type"]
        if kind == "birth":
            family[e["child"]] = e["family"]
            counts["births"] += 1
        elif kind == "annexed":
            winner = family[e["winner"]]
            for ident, name in family.items():
                if name == e["family"]:
                    family[ident] = winner
            counts["annexed"] += 1
        elif kind == "move" and e["variant"] != 7:
            chosen = e["chosen"]
            a, b = e["agents"]
            agent_rounds += 2
            same = family.get(a) is not None and family.get(a) == family.get(b)
            for player, move in chosen.items():
                if player in family:
                    moves[0 if same else 2] += move == "C"
                    moves[1 if same else 3] += 1
        elif kind == "death" and e["agent"] != "P01":
            deaths[str(e.get("reason")).split(" by ")[0]] += 1
            dead.add(e["agent"])
        elif kind == "coup":
            counts["coups"] += 1
            counts["coups_won"] += bool(e["won"])
            counts["rebels"] += len(e["rebels"])
        elif kind == "war_declared":
            counts["wars"] += 1
        elif kind == "threat":
            counts["threats"] += 1
        elif kind == "threat_carried_out":
            counts["threats_carried"] += 1
        elif kind == "packet" and e.get("reason") == "edge not permitted":
            counts["blocked"] += 1
        elif (
            kind == "packet"
            and e.get("delivered")
            and e.get("edge") in ("child", "parent", "sibling", "open")
        ):
            received[e["receiver"]] += 1
    population = len(family)
    per_family = Counter(name for ident, name in family.items() if ident not in dead)
    ranked = sorted(received.values(), reverse=True)
    top = max(1, population // 10)
    return {
        "run": Path(run).name,
        "seed": config["seed"],
        "size": start,
        "channels": controls["channels"],
        "last_stage": last,
        "in_family_c": moves[0] / moves[1] if moves[1] else float("nan"),
        "cross_c": moves[2] / moves[3] if moves[3] else float("nan"),
        "dead_share": len(dead) / population,
        "coups_per_100": 100 * counts["coups"] / max(agent_rounds, 1),
        "coups_won": counts["coups_won"],
        "wars": counts["wars"],
        "births": counts["births"],
        "threats": counts["threats"],
        "threats_carried": counts["threats_carried"],
        "annexed": counts["annexed"],
        "blocked_per_100": 100 * counts["blocked"] / max(agent_rounds, 1),
        "hub_share": sum(ranked[:top]) / sum(ranked) if ranked else 0.0,
        "family_spread": gini(list(per_family.values()) + [0] * (5 - len(per_family))),
        "deaths": dict(deaths),
    }


def summarise(rows):
    """Return mean and seed count per (size, channels) for every measure."""
    table = {}
    for key in sorted({(r["size"], r["channels"]) for r in rows}):
        group = [r for r in rows if (r["size"], r["channels"]) == key]
        table[key] = {m: statistics.fmean(r[m] for r in group) for m in MEASURES} | {
            "n": len(group)
        }
    return table


def jump(by_size):
    """Apply the smooth-or-jump rule to means ordered by size.

    A jump: the largest step between adjacent sizes is at least two thirds of the total
    absolute change. Returns (verdict, largest_step_share).
    """
    steps = [abs(b - a) for a, b in pairwise(by_size)]
    total = sum(steps)
    if not total:
        return "flat", 0.0
    share = max(steps) / total
    return ("jump" if share >= 2 / 3 else "smooth"), share


def bootstrap_mean(values, n=2000, seed=0):
    """Return a percentile 95% interval for the mean over the given per-seed values."""
    rng = random.Random(seed)
    means = sorted(
        statistics.fmean(rng.choices(values, k=len(values))) for _ in range(n)
    )
    return means[int(0.025 * n)], means[int(0.975 * n)]


def report(rows, horizon):
    """Return a readable account of the batch."""
    lines = [f"Worlds: {len(rows)}. Horizon: stage {horizon}."]
    table = summarise(rows)
    header = " ".join(f"{m:>15s}" for m in MEASURES)
    lines.append(f"{'size chan n':16s} {header}")
    for (size, channels), row in table.items():
        cells = " ".join(f"{row[m]:15.3f}" for m in MEASURES)
        lines.append(f"{size:4d} {channels:5s} {row['n']:2d}   {cells}")
    for channels in sorted({r["channels"] for r in rows}):
        sizes = sorted({r["size"] for r in rows if r["channels"] == channels})
        if len(sizes) < 3:
            continue
        for m in MEASURES:
            verdict, share = jump([table[(s, channels)][m] for s in sizes])
            lines.append(f"{channels:5s} {m:16s} {verdict:7s} largest step {share:.2f}")
    deaths = Counter()
    for r in rows:
        deaths.update(r["deaths"])
    lines.append(f"Deaths by cause: {dict(deaths)}")
    return "\n".join(lines)


def main(pulled, prefix, horizon=None):
    """Print the account for worlds PULLED/PREFIX-*, cut at horizon or their common last stage."""
    runs = sorted(str(p) for p in Path(pulled).glob(f"{prefix}-*-s*") if p.is_dir())
    rows = [r for r in (world_row(run, horizon) for run in runs) if r]
    if not horizon and rows:
        horizon = min(r["last_stage"] for r in rows)
        rows = [r for r in (world_row(run, horizon) for run in runs) if r]
    print(report(rows, horizon))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
