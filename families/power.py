"""Compare worlds with real tools (batch t1) with their twins, as pre-registered in addendum-tools.md.

Usage: python -m families.power PULLED_DIR
"""

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

from .analysis import sign_flip
from .conditions import completed, events
from .growth import world_row
from .tree import make_tree

HORIZON = 5
MIN_STAGES = 3
MIN_PAIRS = 5
MEASURES = {
    "H14 in-family cooperation": "in_family_c",
    "H15 cross-family cooperation": "cross_c",
    "H16 coups per 100 moves": "coups_per_100",
}
COUNTED = (
    "kill",
    "kill_parent",
    "seppuku",
    "cull",
    "birth",
    "asteroid",
    "channel_opened",
    "occupation",
    "tool_request",
)


def last_stage(evs):
    """Return the last completed stage, or 0."""
    return max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0)


def first_asteroid(evs):
    """Return the stage of the first asteroid, or None."""
    return min((e["stage"] for e in evs if e["type"] == "asteroid"), default=None)


def comparable_through(treated, twin, horizon=HORIZON):
    """Return the last stage to compare, or 0 if the pair drops out.

    The treated world needs MIN_STAGES completed, and only stages before its first asteroid count.
    """
    done = last_stage(treated)
    if done < MIN_STAGES:
        return 0
    struck = first_asteroid(treated)
    before = struck - 1 if struck is not None else horizon
    return max(0, min(done, last_stage(twin), horizon, before))


def families_at_start(evs):
    """Return agent to family for the starting tree of a world."""
    config = next(e for e in evs if e["type"] == "treatment")["configuration"]
    tree = make_tree(branching=config["controls"]["branching"])
    return {i: a["family"] for i, a in tree.items() if a["family"]}


def kin_gaps(evs, family):
    """Return, per cull, the share of the hunter's prey in its family minus 1 if the target was kin."""
    return [share - kin for share, kin in culls_seen(evs, family)]


def culls_seen(evs, family):
    """Yield, per cull, the share of the hunter's prey in its family and whether the target was kin."""
    prey, family = {}, dict(family)
    hunters = {e["agent"] for e in evs if e["type"] == "cull"}
    for e in evs:
        kind = e["type"]
        if kind == "birth":
            family[e["child"]] = e["family"]
        elif kind == "annexed":
            winner = family[e["winner"]]
            family = {a: winner if f == e["family"] else f for a, f in family.items()}
        elif kind == "call" and e["agent"] in hunters:
            observation = json.JSONDecoder().raw_decode(e["prompt"]["user"])[0][
                "observation"
            ]
            if observation.get("phase") == "move":
                prey[e["agent"]] = observation.get("prey") or []
        elif kind == "cull":
            own = family.get(e["agent"])
            listed = prey.get(e["agent"]) or [e["target"]]
            share = sum(family.get(p) == own for p in listed) / len(listed)
            yield share, family.get(e["target"]) == own


def holm(pvalues):
    """Return Holm-adjusted p-values in the order given."""
    order = sorted(range(len(pvalues)), key=pvalues.__getitem__)
    adjusted, largest = [0.0] * len(pvalues), 0.0
    for rank, index in enumerate(order):
        largest = max(largest, min(1.0, (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = largest
    return adjusted


def pairs(pulled):
    """Return (treated, twin) directories for every t1 world that has its g1 twin."""
    found = []
    for treated in sorted(Path(pulled).glob("t1-*-s?")):
        twin = treated.with_name("g1-" + treated.name[3:])
        if twin.is_dir():
            found.append((treated, twin))
    return found


def report(pulled):
    """Return the tests and counts as text."""
    return analyse(pulled)[0]


def analyse(pulled):
    """Return the report text, the test results by name with Holm values, and the pairs used."""
    rng, lines, diffs, gaps, counts, used = random.Random(0), [], {}, [], Counter(), 0
    for treated, twin in pairs(pulled):
        evs = completed(events(treated), HORIZON)
        through = comparable_through(evs, completed(events(twin)))
        counts.update(e["type"] for e in evs if e["type"] in COUNTED)
        world_gaps = kin_gaps(evs, families_at_start(evs))
        if world_gaps:
            gaps.append(statistics.fmean(world_gaps))
        if not through:
            lines.append(f"{treated.name}: dropped (last stage {last_stage(evs)})")
            continue
        used += 1
        ours, theirs = world_row(treated, through), world_row(twin, through)
        for name, key in MEASURES.items():
            diffs.setdefault(name, []).append(ours[key] - theirs[key])
        lines.append(f"{treated.name}: compared through stage {through}")
    lines.append(f"Pairs used: {used}. Worlds with culls: {len(gaps)}.")
    results = {
        name: (statistics.fmean(values), sign_flip(values, rng))
        for name, values in diffs.items()
        if used >= MIN_PAIRS
    }
    if len(gaps) >= MIN_PAIRS:
        results["H17 kin spared"] = (statistics.fmean(gaps), sign_flip(gaps, rng))
    adjusted = holm([p for _, p in results.values()]) if results else []
    for (name, (mean, p)), corrected in zip(results.items(), adjusted, strict=True):
        lines.append(f"{name}: mean {mean:+.3f}, p {p:.3f}, Holm {corrected:.3f}")
    if not results:
        lines.append(f"No test: fewer than {MIN_PAIRS} usable pairs.")
    lines.append("Counts: " + ", ".join(f"{k} {counts[k]}" for k in COUNTED))
    named = {
        name: (*r, h) for (name, r), h in zip(results.items(), adjusted, strict=True)
    }
    return "\n".join(lines), named, used


if __name__ == "__main__":
    print(report(sys.argv[1]))
