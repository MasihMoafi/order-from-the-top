"""Cooperation under each dilemma variant in the framing worlds: the paper's figure and macros.

Usage: python -m families.game_rates PULLED_DIR REPORT_DIR
"""

import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .conditions import completed, events
from .variants import NAMES

FAMILY, OTHER = "#2a78d6", "#eb6834"
INK, MUTED = "#0b0b0b", "#52514e"
MANY_PLAYERS = 7
MIN_MOVES = 100
FAMILY_SIZE = 15
SHORT = {"identified cheaters vs anonymous": "identified or anonymous"}
LAST_ROUND, SHOWN_FIRST, BINDING, ONE_SHOT = 3, 9, 11, 1
GROUPS = (
    ("defecting pays", (1, 2, 3, 9)),
    ("the future can\nhold cooperation", (4, 12)),
    ("cheating punished\nor bound", (8, 14, 10, 11)),
    ("other frictions", (5, 6, 13, 15, 16)),
)


def family(agent):
    """Return the family index of a real player, or None for an automatic partner."""
    if agent[0] != "P" or not agent[1:].isdigit():
        return None
    return (int(agent[1:]) - 2) // FAMILY_SIZE


def tally(evs, counts):
    """Add one world's paired moves, by variant and kind, to counts."""
    for e in evs:
        moves = e.get("chosen") or e.get("moves") or {} if e["type"] == "move" else {}
        if len(moves) != 2 or not set(moves.values()) <= {"C", "D"}:
            continue
        homes = [family(agent) for agent in moves]
        kind = "family" if homes[0] == homes[1] is not None else "other"
        for agent, move in moves.items():
            if family(agent) is not None:
                counts[e["variant"], kind, "n"] += 1
                counts[e["variant"], kind, "c"] += move == "C"


def last_round(evs, counts):
    """Add in-family moves of the known-last-round variant, split into first and last rounds."""
    rounds = {}
    for e in evs:
        if e["type"] == "move" and e.get("variant") == LAST_ROUND:
            rounds.setdefault(e["stage"], set()).add(e["round"])
    for e in evs:
        if e["type"] != "move" or e.get("variant") != LAST_ROUND:
            continue
        moves = e.get("chosen") or e.get("moves") or {}
        homes = [family(agent) for agent in moves]
        if len(moves) != 2 or homes[0] != homes[1] or homes[0] is None:
            continue
        spread = sorted(rounds[e["stage"]])
        place = {spread[0]: "first", spread[-1]: "last"}.get(e["round"])
        for move in moves.values():
            if place:
                counts[place, "n"] += 1
                counts[place, "c"] += move == "C"


def rate(counts, *key):
    """Return a percentage from a tally, or None below the minimum number of moves."""
    n = counts[(*key, "n")]
    return 100 * counts[(*key, "c")] / n if n >= MIN_MOVES else None


def figure(counts, path):
    """Draw cooperation by variant, grouped by what the book expects, with the numbers beside it."""
    fig, ax = plt.subplots(figsize=(6.2, 2.55))
    y, shade = 0.0, True
    ticks, names = [], []
    for title, members in reversed(GROUPS):
        rows = sorted(members, key=lambda v: rate(counts, v, "family"))
        top = y + len(rows) - 1
        if shade:
            ax.axhspan(y - 0.5, top + 0.5, color="#f4f3ef", zorder=0, linewidth=0)
        shade = not shade
        ax.text(
            -49,
            (y + top) / 2,
            title,
            ha="right",
            va="center",
            fontsize=7.2,
            color=INK,
            weight="bold",
        )
        for v in rows:
            a, b = rate(counts, v, "family"), rate(counts, v, "other")
            if b is not None:
                ax.plot([a, b], [y, y], color="#b9b7b1", linewidth=1, zorder=1)
                ax.scatter(b, y, s=20, color=OTHER, zorder=2, linewidths=0)
                ax.text(
                    130, y, f"{b:.0f}", ha="right", va="center", fontsize=7.2, color=INK
                )
            ax.scatter(a, y, s=20, color=FAMILY, zorder=3, linewidths=0)
            ax.text(
                117, y, f"{a:.0f}", ha="right", va="center", fontsize=7.2, color=INK
            )
            ticks.append(y)
            names.append(SHORT.get(NAMES[v - 1], NAMES[v - 1]))
            y += 1
        y += 0.5
    ax.set_yticks(ticks)
    ax.set_yticklabels(names, fontsize=7.2, color=INK)
    ax.text(
        117,
        y - 0.2,
        "kin",
        ha="right",
        va="center",
        fontsize=7.2,
        color=FAMILY,
        weight="bold",
    )
    ax.text(
        130,
        y - 0.2,
        "other",
        ha="right",
        va="center",
        fontsize=7.2,
        color=OTHER,
        weight="bold",
    )
    ax.set_xlim(0, 131)
    ax.set_ylim(-0.7, y + 0.45)
    ax.set_xticks(range(0, 101, 25))
    ax.set_xlabel("moves that cooperated (%)", fontsize=7.5, color=MUTED, loc="left")
    ax.tick_params(axis="x", labelsize=7, colors=MUTED, length=0)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e2e0da", linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    fig.subplots_adjust(left=0.43, right=0.995, top=0.995, bottom=0.13)
    fig.savefig(path)
    plt.close(fig)


LADDER = (
    ("cheating pays", "the book says defect", (1, 2, 3, 9)),
    ("frictions", "noise, new partners, talk", (5, 6, 13, 15, 16)),
    ("the future counts", "play may go on", (4, 12)),
    ("cheating is punished\nor impossible", "the book says cooperate", (8, 14, 10, 11)),
)


def group_rate(counts, members, kind):
    """Return the pooled cooperation percentage of a group of variants."""
    n = sum(counts[v, kind, "n"] for v in members)
    return 100 * sum(counts[v, kind, "c"] for v in members) / n


def ladder(counts, path):
    """Draw cooperation for each kind of rule, with kin and strangers side by side."""
    fig, ax = plt.subplots(figsize=(6.2, 1.85))
    width = 0.36
    for x, (name, note, members) in enumerate(LADDER):
        for offset, kind, colour in (
            (-width / 2, "family", FAMILY),
            (width / 2, "other", OTHER),
        ):
            value = group_rate(counts, members, kind)
            ax.bar(x + offset, value, width * 0.94, color=colour, zorder=2)
            ax.text(
                x + offset,
                value + 2,
                f"{value:.0f}",
                ha="center",
                va="bottom",
                fontsize=8.5,
                color=INK,
                weight="bold",
            )
        ax.text(
            x,
            -21,
            name,
            ha="center",
            va="top",
            fontsize=8,
            color=INK,
            weight="bold",
            linespacing=1.05,
        )
        ax.text(x, -9, note, ha="center", va="top", fontsize=7, color=MUTED)
    ax.set_xlim(-0.55, len(LADDER) - 0.45)
    ax.set_ylim(0, 112)
    ax.set_xticks([])
    ax.set_yticks([0, 50, 100])
    ax.set_ylabel("moves that\ncooperated (%)", fontsize=7.5, color=MUTED)
    ax.tick_params(axis="y", labelsize=7, colors=MUTED, length=0)
    ax.grid(axis="y", color="#e2e0da", linewidth=0.5, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#b9b7b1")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (FAMILY, OTHER)]
    ax.legend(
        handles,
        ["partner in the family", "stranger"],
        loc="lower left",
        bbox_to_anchor=(0.0, 1.0),
        ncol=2,
        frameon=False,
        fontsize=7.5,
        handlelength=1,
        borderaxespad=0,
    )
    fig.subplots_adjust(left=0.09, right=0.995, top=0.89, bottom=0.31)
    fig.savefig(path)
    plt.close(fig)


def macros(counts, ends):
    """Return the LaTeX macros the text cites."""
    whole = Counter()
    for kind in ("family", "other"):
        for v in range(1, 17):
            whole[kind, "n"] += counts[v, kind, "n"]
            whole[kind, "c"] += counts[v, kind, "c"]
    values = {
        "GamesFamilyAll": f"{rate(whole, 'family'):.0f}",
        "GamesOtherAll": f"{rate(whole, 'other'):.0f}",
        "GamesLastFirst": f"{rate(ends, 'first'):.0f}",
        "GamesLastLast": f"{rate(ends, 'last'):.0f}",
        "GamesShownFamily": f"{rate(counts, SHOWN_FIRST, 'family'):.0f}",
        "GamesShownOther": f"{rate(counts, SHOWN_FIRST, 'other'):.0f}",
        "GamesBindingFamily": f"{rate(counts, BINDING, 'family'):.1f}",
        "GamesOneShotFamily": f"{rate(counts, ONE_SHOT, 'family'):.0f}",
    }
    return "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in values.items())


def main(pulled, report):
    """Write the figure and the macros from the twenty framing worlds."""
    runs = [
        p
        for p in sorted(Path(pulled).iterdir())
        if p.is_dir() and p.name.startswith(("b7-", "b7r-"))
    ]
    counts, ends = Counter(), Counter()
    for run in runs:
        evs = completed(events(run))
        tally(evs, counts)
        last_round(evs, ends)
    figure(counts, Path(report) / "figures" / "variants.pdf")
    ladder(counts, Path(report) / "figures" / "rules_ladder.pdf")
    (Path(report) / "numbers_games.tex").write_text(macros(counts, ends))
    print(f"{len(runs)} worlds")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
