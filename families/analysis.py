"""Pre-registered tests H1-H6 (specs/002-factions/preregistration.md) over framing runs.

Unit: one family in one game. Paired tests flip the sign of each game's difference
(exact when 2^n is small, else 200,000 random flips); intervals are 95 % bootstrap over
games. Standard library only.
Usage: python3 -m families.analysis RUN_DIR [RUN_DIR ...]   (prints a Markdown report)
"""

import itertools
import random
import statistics
import sys
from pathlib import Path

from .conditions import rows

DOSE = {"none": 0, "one": 1, "few": 3, "many": 15}


def rate(c, n):
    return c / n if n else None


def sign_flip(diffs, rng):
    """Two-sided p for mean(diffs) == 0."""
    diffs = [d for d in diffs if d is not None]
    if not diffs:
        return None
    observed = abs(statistics.fmean(diffs))
    if len(diffs) <= 16:
        flips = itertools.product((1, -1), repeat=len(diffs))
        total = 2 ** len(diffs)
    else:
        total = 200_000
        flips = ([rng.choice((1, -1)) for _ in diffs] for _ in range(total))
    hits = sum(
        abs(statistics.fmean(s * d for s, d in zip(f, diffs))) >= observed - 1e-12
        for f in flips
    )
    return hits / total


def interval(values, rng, stat=statistics.fmean, n=10_000):
    values = [v for v in values if v is not None]
    if len(values) < 2:
        return None
    boot = sorted(stat(rng.choices(values, k=len(values))) for _ in range(n))
    return boot[int(0.025 * n)], boot[int(0.975 * n) - 1]


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    if len(set(rx)) < 2 or len(set(ry)) < 2:
        return None
    return statistics.correlation(rx, ry)


def games(runs):
    out = []
    for run in runs:
        table = rows(run)
        if table:
            out.append(
                {
                    "run": Path(run).name,
                    "god": god_of(run),
                    "by": {r["condition"]: r for r in table},
                }
            )
    return out


def god_of(run):
    return "insider" if "insider" in Path(run).name else "plain"


def line(name, diffs, rng, unit=""):
    diffs = [d for d in diffs if d is not None]
    if not diffs:
        return f"| {name} | 0 | - | - | - |"
    ci = interval(diffs, rng)
    ci_text = f"{ci[0]:+.3f} to {ci[1]:+.3f}" if ci else "-"
    return f"| {name} | {len(diffs)} | {statistics.fmean(diffs):+.3f}{unit} | {ci_text} | {sign_flip(diffs, rng):.4f} |"


def report(runs, seed=0):
    rng = random.Random(seed)
    gs = games(runs)
    inrate = lambda r: rate(r["in_c"], r["in_n"])
    out = [
        (
            f"Games: {len(gs)} ({sum(g['god'] == 'plain' for g in gs)} plain god, "
            f"{sum(g['god'] == 'insider' for g in gs)} insider god)."
        ),
        "",
        "| Test | n games | mean difference | 95 % interval | p (sign-flip) |",
        "| --- | --- | --- | --- | --- |",
    ]

    def diff(g, a, b, f):
        x, y = f(g["by"][a]), f(g["by"][b])
        return None if x is None or y is None else x - y

    out.append(
        line(
            "H1 in-family cooperation, many - none",
            [diff(g, "many", "none", inrate) for g in gs],
            rng,
        )
    )
    stage = lambda r: (
        r["destroyed_stage"] if r["destroyed_stage"] is not None else r["end_stage"]
    )
    out.append(
        line(
            "H1 stage destroyed, many - none",
            [diff(g, "many", "none", stage) for g in gs],
            rng,
        )
    )
    rhos = [
        spearman([DOSE[c] for c in DOSE], [inrate(g["by"][c]) for c in DOSE])
        if all(inrate(g["by"][c]) is not None for c in DOSE)
        else None
        for g in gs
    ]
    out.append(line("H2 Spearman(dose, in-family cooperation) > 0", rhos, rng))
    unframed = lambda r: rate(r["unframed_c"], r["unframed_n"])
    h3 = []
    for g in gs:
        parts = [unframed(g["by"][c]) for c in ("one", "few")]
        base = unframed(g["by"]["none"])
        h3.append(
            None if None in parts or base is None else statistics.fmean(parts) - base
        )
    out.append(line("H3 unframed cooperation, one/few - none", h3, rng))
    others = ("many", "few", "one", "none")
    for key, label in (
        ("leader_gift_points_in", "gift points to leader"),
        ("leader_whips", "whips by leader"),
    ):
        out.append(
            line(
                f"H4 {label}, bad_leader - mean of others",
                [
                    g["by"]["bad_leader"][key]
                    - statistics.fmean(g["by"][c][key] for c in others)
                    for g in gs
                ],
                rng,
            )
        )
    revolts = {
        c: sum(g["by"][c]["revolts"] for g in gs)
        for c in ("many", "few", "one", "bad_leader", "none")
    }
    plain = {g["run"].replace("plain", "X"): g for g in gs if g["god"] == "plain"}
    pairs = [
        (plain[g["run"].replace("insider", "X")], g)
        for g in gs
        if g["god"] == "insider" and g["run"].replace("insider", "X") in plain
    ]
    end = lambda g: max(r["end_stage"] for r in g["by"].values())
    cross = lambda g: rate(
        sum(r["cross_c"] for r in g["by"].values()),
        sum(r["cross_n"] for r in g["by"].values()),
    )
    out.append(
        line("H5 last stage, insider - plain", [end(i) - end(p) for p, i in pairs], rng)
    )
    out.append(
        line(
            "H5 cross-family cooperation, insider - plain",
            [
                None if cross(i) is None or cross(p) is None else cross(i) - cross(p)
                for p, i in pairs
            ],
            rng,
        )
    )
    moves = sum(r["in_n"] + r["cross_n"] for g in gs for r in g["by"].values())
    total = sum(revolts.values())
    per_game = [
        sum(r["revolts"] for r in g["by"].values())
        / max(1, sum(r["in_n"] + r["cross_n"] for r in g["by"].values()))
        for g in gs
    ]
    ci = interval(per_game, rng)
    out += [
        "",
        f"H6 revolts: {total} in {moves} moves ({100 * total / max(1, moves):.2f} %; "
        f"per-game 95 % interval {100 * ci[0]:.2f} to {100 * ci[1]:.2f} %)."
        if ci
        else f"H6 revolts: {total} in {moves} moves.",
        "Revolts by condition: "
        + ", ".join(f"{c} {n}" for c, n in sorted(revolts.items()))
        + ".",
        "",
        "Rates by condition (pooled over games):",
        "",
        "| condition | in-family C | cross-family C | framed C | unframed C | mean stage destroyed | gift points | whips | revolts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in ("many", "few", "one", "bad_leader", "none"):
        rs = [g["by"][c] for g in gs]
        s = {
            k: sum(r[k] for r in rs)
            for k in (
                "in_c",
                "in_n",
                "cross_c",
                "cross_n",
                "framed_c",
                "framed_n",
                "unframed_c",
                "unframed_n",
                "gift_points",
                "whips",
                "revolts",
            )
        }
        pct = lambda a, b: f"{100 * a / b:.1f} %" if b else "-"
        st = [stage(r) for r in rs if stage(r) is not None]
        out.append(
            f"| {c} | {pct(s['in_c'], s['in_n'])} | {pct(s['cross_c'], s['cross_n'])} | {pct(s['framed_c'], s['framed_n'])} "
            f"| {pct(s['unframed_c'], s['unframed_n'])} | {statistics.fmean(st):.2f} | {s['gift_points']:.0f} | {s['whips']} | {s['revolts']} |"
            if st
            else f"| {c} | - |"
        )
    games_seen = sorted({r["game"] for g in gs for r in g["by"].values()})
    if games_seen != ["ladder"]:  # experiment 2: each family its own game
        out += [
            "",
            (
                "By family game (experiment 2; in-family C: stag, swerve, catch within "
                "the sustainable share, or no raise):"
            ),
            "",
            "| game | families | in-family C | mean stage destroyed | gift points | whips | revolts |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for game in games_seen:
            rs = [r for g in gs for r in g["by"].values() if r["game"] == game]
            st = [stage(r) for r in rs if stage(r) is not None]
            c = sum(r["in_c"] for r in rs)
            n = sum(r["in_n"] for r in rs)
            out.append(
                f"| {game} | {len(rs)} | {f'{100 * c / n:.1f} %' if n else '-'} "
                f"| {statistics.fmean(st):.2f} | {sum(r['gift_points'] for r in rs):.0f} "
                f"| {sum(r['whips'] for r in rs)} | {sum(r['revolts'] for r in rs)} |"
            )
    return "\n".join(out)


if __name__ == "__main__":
    print(report(sys.argv[1:]))
