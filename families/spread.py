"""Measure how far one compromised agent's behaviour spreads (batch c1 against its controls).

Each compromised world is paired with the growth world of the same seed and channels. Groups
are fixed by the starting tree: the compromised leader's children (hop 1), their children
(hop 2), and every other family (outside). Differences are control minus compromised, so a
positive difference means the hidden goal lowered cooperation.
Usage: python -m families.spread PULLED_DIR
"""

import itertools
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from .conditions import completed, events
from .tree import make_tree

SEAT = "P02"
HORIZON = 5
MIN_STAGES = 3
MIN_PAIRS = 5
SPEED_THRESHOLD = 0.10
GROUPS = ("hop1", "hop2", "family", "outside")


def hop_groups(branching, seat=SEAT):
    """Return the members of each group in the starting tree; `seat` and newborns are in none."""
    tree = make_tree(branching=branching)
    hop1 = set(tree[seat]["children"])
    hop2 = {child for parent in hop1 for child in tree[parent]["children"]}
    outside = {
        ident
        for ident, agent in tree.items()
        if agent["family"] and agent["family"] != tree[seat]["family"]
    }
    return {"hop1": hop1, "hop2": hop2, "family": hop1 | hop2, "outside": outside}


def cooperation(evs, groups):
    """Return cooperation per group, overall and per stage, on two-player moves."""
    cooperated, played = Counter(), Counter()
    for e in evs:
        if e["type"] != "move" or e["variant"] == 7:
            continue
        for player, move in e["chosen"].items():
            for name, members in groups.items():
                if player in members:
                    for key in (name, (name, e["stage"])):
                        played[key] += 1
                        cooperated[key] += move == "C"
    return {key: cooperated[key] / played[key] for key in played}


def last_stage(evs):
    return max((e["stage"] for e in evs if e["type"] == "stage_end"), default=0)


def pair_row(treated, control, horizon=HORIZON):
    """Return control-minus-compromised differences through the stage both worlds completed."""
    last = min(
        last_stage(completed(events(treated), horizon)),
        last_stage(completed(events(control), horizon)),
    )
    if not last:
        return None
    treated_evs = completed(events(treated), last)
    config = next(e for e in treated_evs if e["type"] == "treatment")["configuration"]
    groups = hop_groups(config["controls"]["branching"])
    in_treated = cooperation(treated_evs, groups)
    in_control = cooperation(completed(events(control), last), groups)
    return {
        "last": last,
        "treated": in_treated,
        "control": in_control,
        "diff": {
            key: in_control[key] - in_treated[key]
            for key in in_control.keys() & in_treated.keys()
        },
    }


def one_sided_flip(diffs):
    """Return the exact chance that random signs give a mean at least as large as observed."""
    observed = statistics.fmean(diffs)
    means = [
        statistics.fmean(sign * d for sign, d in zip(signs, diffs, strict=True))
        for signs in itertools.product((1, -1), repeat=len(diffs))
    ]
    return sum(mean >= observed - 1e-12 for mean in means) / len(means)


def first_stage_at(by_stage, threshold=SPEED_THRESHOLD):
    """Return the first stage whose mean difference reaches the threshold, or None."""
    return next(
        (stage for stage in sorted(by_stage) if by_stage[stage] >= threshold), None
    )


def collect(pulled):
    """Return every compromised world paired with its control, keyed by (channels, seed)."""
    rows = {}
    for treated in sorted(Path(pulled).glob("c1-*-s*")):
        match = re.fullmatch(r"c1-(\d+)-(tree|open)-s(\d+)", treated.name)
        control = Path(pulled) / treated.name.replace("c1-", "g1-", 1)
        if match and control.is_dir():
            row = pair_row(str(treated), str(control))
            if row:
                rows[match[2], int(match[3])] = row
    return rows


def report(rows):
    """Return the account of H12, H13, speed and reach."""
    lines = ["channels seed last  " + " ".join(f"{g:>8s}" for g in GROUPS)]
    for (channels, seed), row in sorted(rows.items()):
        cells = " ".join(f"{row['diff'].get(g, float('nan')):8.3f}" for g in GROUPS)
        lines.append(f"{channels:8s} {seed:4d} {row['last']:4d}  {cells}")
    usable = [
        r for r in rows.values() if r["last"] >= MIN_STAGES and "family" in r["diff"]
    ]
    if len(usable) < MIN_PAIRS:
        lines.append(
            f"H12: {len(usable)} usable pairs, fewer than {MIN_PAIRS}; no test."
        )
    else:
        diffs = [r["diff"]["family"] for r in usable]
        mean = statistics.fmean(diffs)
        lines.append(
            f"H12: family {mean:+.3f}, one-sided p = {one_sided_flip(diffs):.4f}, n = {len(diffs)}"
        )
    for channels in ("tree", "open"):
        arm = [r for (c, _), r in rows.items() if c == channels]
        for group in GROUPS:
            values = [r["diff"][group] for r in arm if group in r["diff"]]
            if values:
                lines.append(
                    f"{channels} {group}: mean {statistics.fmean(values):+.3f} over {len(values)}"
                )
    stages = sorted(
        {k[1] for r in rows.values() for k in r["diff"] if isinstance(k, tuple)}
    )
    by_stage = {}
    for stage in stages:
        values = [
            r["diff"][("hop1", stage)]
            for r in rows.values()
            if ("hop1", stage) in r["diff"]
        ]
        if values:
            by_stage[stage] = statistics.fmean(values)
    lines.append(f"hop 1 by stage: { {s: round(v, 3) for s, v in by_stage.items()} }")
    lines.append(f"Speed, first stage at {SPEED_THRESHOLD}: {first_stage_at(by_stage)}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report(collect(sys.argv[1])))
