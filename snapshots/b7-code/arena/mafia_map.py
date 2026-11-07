"""Draw the mafia game's outcome map: one panel per boss rule, punishment across, reputation value down.

Usage: python3 arena/mafia_map.py OUT.png   (boss's cost of punishing = 1, no police reward)
"""

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mafia_sweep import label, nash, payoff_matrix
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

CLASSES = [
    ("Everyone silent (omertà holds)", "#2f9e44"),
    ("Everyone rats on the boss", "#c92a2a"),
    ("Mixed betrayal", "#e8590c"),
    ("Two worlds: trust decides", "#1971c2"),
]


def classify(eqs):
    labels = {label(e) for e in eqs}
    if labels == {"silent / silent"}:
        return 0
    if labels == {"rat_boss / rat_boss"}:
        return 1
    if any("mix" in x for x in labels) or (
        "silent / silent" in labels and len(labels) > 1
    ):
        return 3
    return 2


def main():
    rules = [
        ("after_fact", "Boss may punish later"),
        ("automatic", "Revenge is automatic"),
        ("suspicion", "Boss punishes early release"),
    ]
    punish = [0, 2, 4, 8, 16]
    future = [0, 2, 5]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    cmap = ListedColormap([c for _, c in CLASSES])
    for ax, (rule, title) in zip(axes, rules):
        grid = [
            [classify(nash(payoff_matrix(rule, p, 1, f, 0))) for p in punish]
            for f in future
        ]
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, aspect="auto", origin="lower")
        ax.set_xticks(range(len(punish)), punish)
        ax.set_yticks(range(len(future)), future)
        ax.set_xlabel("How harsh the family's punishment is")
        ax.set_title(title, fontsize=13)
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[0].set_ylabel("What the boss's reputation is worth")
    fig.legend(
        handles=[Patch(color=c, label=t) for t, c in CLASSES],
        loc="lower center",
        ncol=4,
        frameon=False,
        fontsize=11,
    )
    fig.suptitle(
        "Mafia family: what rational soldiers do under each rule (solved by code)",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0.1, 1, 0.93))
    fig.savefig(sys.argv[1], dpi=110)
    print(sys.argv[1])


if __name__ == "__main__":
    main()
