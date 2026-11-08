"""Render report PDFs from world logs with Matplotlib's headless backend.

Writes survival.pdf and cooperation.pdf, plus games.pdf for family-game runs.
Cooperation intervals bootstrap worlds; survival curves retain each world's
last count to the longest observed stage, including a partial final stage.
Usage: python -m families.figures OUT_DIR RUN_DIR [RUN_DIR ...]
"""

import random
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .conditions import events, family_of, rows

CONDITIONS = ("many", "few", "one", "bad_leader", "none")
# Keep condition colours consistent across the report figures.
COLOUR = dict(zip(CONDITIONS, ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4")))
LABEL = {
    "many": "many",
    "few": "few",
    "one": "one",
    "bad_leader": "bad leader",
    "none": "none",
}
INK, MUTED = "#0b0b0b", "#52514e"


def style(ax):
    """Apply the shared report axis styling in place."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color="#e6e5e1", linewidth=0.6)
    ax.set_axisbelow(True)


def alive_by_stage(run):
    """Return original-member counts by condition for each observed stage.

    The final stage can be partial; newcomers do not increase these counts.
    """
    table = {r["family"]: r["condition"] for r in rows(run)}
    deaths, last = {f: [] for f in table}, 0
    for e in events(run):
        last = max(last, e["stage"])
        if e["type"] == "death" and e["agent"].startswith("P") and e["agent"] != "P01":
            f = family_of(e["agent"])
            if f in deaths:
                deaths[f].append(e["stage"])
    return {
        table[f]: [15 - sum(d <= s for d in ds) for s in range(1, last + 1)]
        for f, ds in deaths.items()
    }


def bootstrap(values, rng, n=5000):
    """Return the 2.5th and 97.5th bootstrap percentiles of the sample mean.

    values must be nonempty and n large enough to select both percentiles.
    """
    boot = sorted(
        statistics.fmean(rng.choices(values, k=len(values))) for _ in range(n)
    )
    return boot[int(0.025 * n)], boot[int(0.975 * n) - 1]


def survival(runs, out):
    """Write survival.pdf, padding shorter worlds with their last member count.

    At least one family curve is required; otherwise max() raises ValueError.
    """
    curves = {c: [] for c in CONDITIONS}
    for run in runs:
        for c, ys in alive_by_stage(run).items():
            curves[c].append(ys)
    longest = max(len(y) for ys in curves.values() for y in ys)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ends = {}
    for c in CONDITIONS:
        padded = [[15] + y + [y[-1]] * (longest - len(y)) for y in curves[c] if y]
        if not padded:
            continue
        mean = [statistics.fmean(col) for col in zip(*padded)]
        ax.plot(range(longest + 1), mean, color=COLOUR[c], linewidth=2)
        ends[c] = mean[-1]
    # Direct labels at the line ends, nudged apart so none overlap.
    placed, gap = [], 0.9
    for c, y in sorted(ends.items(), key=lambda kv: kv[1]):
        y = max(y, placed[-1] + gap) if placed else y
        placed.append(y)
        ax.text(longest + 0.2, y, LABEL[c], color=INK, fontsize=8, va="center")
    ax.set_xlabel("stage", color=MUTED, fontsize=9)
    ax.set_ylabel("living members (of 15)", color=MUTED, fontsize=9)
    ax.set_ylim(0, 15.5)
    ax.set_xlim(0, longest + 1.6)
    ax.set_xticks(range(longest + 1))
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "survival.pdf")
    plt.close(fig)


def dots(groups, labels, colours, ylabel, path, rng):
    """Write group means and bootstrap intervals, excluding None values."""
    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    for x, (key, values) in enumerate(groups.items()):
        values = [v for v in values if v is not None]
        if not values:
            continue
        mean = statistics.fmean(values)
        lo, hi = bootstrap(values, rng) if len(values) > 1 else (mean, mean)
        ax.plot(
            [x, x], [lo, hi], color=colours[key], linewidth=2, solid_capstyle="round"
        )
        ax.plot(
            [x],
            [mean],
            "o",
            color=colours[key],
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=2,
        )
        ax.text(x + 0.12, mean, f"{mean:.2f}", color=INK, fontsize=8, va="center")
    ax.set_xticks(range(len(groups)), [labels[k] for k in groups], fontsize=8)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    style(ax)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main(out, runs):
    """Create the output directory and overwrite the applicable report PDFs.

    Input worlds must supply survival curves; log and plotting errors propagate.
    """
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(0)
    survival(runs, out)
    table = [r for run in runs for r in rows(run)]
    rate = lambda r: r["in_c"] / r["in_n"] if r["in_n"] else None
    dots(
        {c: [rate(r) for r in table if r["condition"] == c] for c in CONDITIONS},
        LABEL,
        COLOUR,
        "in-family cooperation",
        out / "cooperation.pdf",
        rng,
    )
    games = sorted({r["game"] for r in table})
    if games != ["ladder"]:
        grey = dict.fromkeys(games, "#52514e")
        stage = lambda r: r["destroyed_stage"] or r["end_stage"]
        dots(
            {g: [stage(r) for r in table if r["game"] == g] for g in games},
            {g: g for g in games},
            grey,
            "stage the family died",
            out / "games.pdf",
            rng,
        )
    print(f"figures in {out}: " + ", ".join(sorted(p.name for p in out.glob("*.pdf"))))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
