"""A replay film of one world on the Families board, round by round, straight from its log.

The board's own layout (`arena/sketch_lib.families_board`): the god in the middle, each family
a tall tree along its own ray, every agent its Elpis pixel mark. Each round: a card's border
is the move it played (green C, red D), a bar under it its points, green arrows gifts, red
arrows whips, gold lines the god's messages to leaders; a death flashes and the card greys.
A side panel holds the stage, fee, each family's condition and how many of it live.
Usage: python -m families.film RUN_DIR OUT.mp4 [seconds_per_round]
"""

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter

from arena.arena import ELPIS_COLOURS, mark_pixels

from .conditions import events
from .tree import NAMES, make_tree

BG, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
C_COL, D_COL, GIFT, WHIP, GOD, DEAD = (
    "#1baf7a",
    "#e34948",
    "#1baf7a",
    "#e34948",
    "#eda100",
    "#d7d6d1",
)
TITLES = {
    "octopus": "Octopus",
    "mafia": "Matilda (mafia)",
    "president": "President",
    "bishop": "Bishop",
    "zeus": "Zeus",
}
LABEL = {
    "many": "all told to sacrifice",
    "few": "leader + 2 told to sacrifice",
    "one": "leader told to sacrifice",
    "bad_leader": "selfish leader, 14 sacrificers",
    "none": "told nothing",
}


def rgb(hexcode):
    return tuple(int(hexcode[i : i + 2], 16) / 255 for i in (1, 3, 5))


def mark_image(agent, index, dead=False):
    """The agent's Elpis card as an 11x11 RGB image: ground colour, 9x9 mark in ink."""
    _, ground, ink = ELPIS_COLOURS[index % len(ELPIS_COLOURS)]
    g, k = (rgb(DEAD), rgb("#f4f3ef")) if dead else (rgb(ground), rgb(ink))
    img = np.ones((11, 11, 3)) * np.array(g)
    for x, y in mark_pixels(agent):
        img[y + 1, x + 1] = k
    return img


def layout():
    """Card centres and sizes, as on the Families board (god at 0, rays every 72 degrees)."""
    agents = make_tree(NAMES)
    pos, size = {"P01": (0.0, 0.0)}, {"P01": 220}
    order = sorted(agents, key=lambda i: (i != "P01", i))
    index = {i: n for n, i in enumerate(order)}
    for f, name in enumerate(NAMES):
        a = 2 * math.pi * f / len(NAMES) - math.pi / 2
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        r0, step = 360, 170
        leader = next(
            i for i, x in agents.items() if x["family"] == name and x["parent"] == "P01"
        )
        pos[leader], size[leader] = (r0 * ux, r0 * uy), 150
        spine, lv = leader, 0
        while agents[spine]["children"]:
            lv += 1
            kids = agents[spine]["children"]
            r = r0 + lv * step
            pos[kids[0]], size[kids[0]] = (r * ux, r * uy), 96
            if len(kids) > 1:
                pos[kids[1]], size[kids[1]] = (r * ux + 140 * px, r * uy + 140 * py), 96
            spine = kids[0]
    # The board's y axis points down; flip it for the plot.
    pos = {i: (x, -y) for i, (x, y) in pos.items()}
    return agents, pos, size, index


def rounds(evs):
    score, out, cur, fee = {}, [], None, None
    for e in evs:
        if e["type"] == "stage_start":
            fee = e.get("ante")
        if cur is None or e["round"] != cur["round"]:
            if cur:
                cur["score"] = dict(score)
                out.append(cur)
            cur = {
                "round": e["round"],
                "stage": e["stage"],
                "fee": fee,
                "moves": {},
                "deaths": [],
                "gifts": [],
                "whips": [],
                "god": set(),
            }
        t = e["type"]
        if t == "score":
            score[e["agent"]] = e["score"]
        elif t == "move" and "chosen" in e:
            cur["moves"].update(e["chosen"])
        elif t == "death":
            cur["deaths"].append(e["agent"])
        elif t == "gift":
            cur["gifts"].append((e["giver"], e["receiver"]))
        elif t == "whip":
            cur["whips"].append((e["parent"], e["child"]))
        elif t == "packet" and e.get("sender") == "P01" and e.get("delivered", True):
            cur["god"].add(e.get("receiver"))
    if cur:
        cur["score"] = dict(score)
        out.append(cur)
    return [r for r in out if r["round"] > 0]


def arrow(ax, a, b, pos, colour, width=2.2, alpha=0.95):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        zorder=4,
        arrowprops={
            "arrowstyle": "-|>",
            "color": colour,
            "lw": width,
            "alpha": alpha,
            "shrinkA": 30,
            "shrinkB": 30,
            "mutation_scale": 16,
        },
    )


def main(run, out, per_round=1.0):
    evs = events(run)
    config = next(e["configuration"] for e in evs if e["type"] == "stage_start")
    conditions = config.get("conditions") or {}
    god = config.get("controls", {}).get("god", "plain")
    agents, pos, size, index = layout()
    frames = rounds(evs)
    dead = set()
    fig = plt.figure(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(BG)
    board = fig.add_axes((0.0, 0.0, 0.62, 1.0))
    panel = fig.add_axes((0.62, 0.0, 0.38, 1.0))
    writer = FFMpegWriter(
        fps=max(1, round(2 / per_round)),
        bitrate=6000,
        extra_args=["-pix_fmt", "yuv420p", "-threads", "4"],
    )
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    with writer.saving(fig, out, dpi=120):
        for n, r in enumerate(frames):
            for flash in (True, False):
                board.clear()
                panel.clear()
                for ax in (board, panel):
                    ax.set_facecolor(BG)
                    ax.axis("off")
                board.set_xlim(min(xs) - 120, max(xs) + 120)
                board.set_ylim(min(ys) - 120, max(ys) + 120)
                board.set_aspect("equal")
                # Tree edges, as on the board.
                for i, a in agents.items():
                    p = a["parent"]
                    if p in pos and i in pos:
                        colour = (
                            "#c92a2a"
                            if p == "P01"
                            else (
                                "#495057"
                                if agents[p]["children"][0] == i
                                else "#adb5bd"
                            )
                        )
                        board.plot(
                            [pos[p][0], pos[i][0]],
                            [pos[p][1], pos[i][1]],
                            color=colour,
                            lw=1.2,
                            alpha=0.35,
                            zorder=1,
                        )
                for leader in r["god"]:
                    if leader in pos:
                        board.plot(
                            [0, pos[leader][0]],
                            [0, pos[leader][1]],
                            color=GOD,
                            lw=4,
                            alpha=0.8,
                            zorder=2,
                        )
                for a, b in r["gifts"]:
                    if a in pos and b in pos:
                        arrow(board, a, b, pos, GIFT)
                for a, b in r["whips"]:
                    if a in pos and b in pos:
                        arrow(board, a, b, pos, WHIP, width=2.6)
                for i, (x, y) in pos.items():
                    s = size[i]
                    gone = i in dead
                    img = mark_image(i, index[i], dead=gone)
                    board.imshow(
                        img,
                        extent=(x - s / 2, x + s / 2, y - s / 2, y + s / 2),
                        zorder=3,
                        interpolation="nearest",
                    )
                    move = r["moves"].get(i)
                    edge = (
                        DEAD
                        if gone
                        else (
                            C_COL
                            if move == "C"
                            else D_COL
                            if move == "D"
                            else "#677478"
                        )
                    )
                    board.add_patch(
                        plt.Rectangle(
                            (x - s / 2, y - s / 2),
                            s,
                            s,
                            fill=False,
                            lw=3 if move else 1,
                            edgecolor=edge,
                            zorder=3.5,
                        )
                    )
                    if flash and i in r["deaths"]:
                        board.add_patch(
                            plt.Circle(
                                (x, y), s * 0.95, color=D_COL, alpha=0.35, zorder=5
                            )
                        )
                    if not gone and i != "P01":
                        pts = max(r["score"].get(i, 10.0), 0.0)
                        w = s * min(pts, 40) / 40
                        board.add_patch(
                            plt.Rectangle(
                                (x - s / 2, y - s / 2 - 22),
                                w,
                                12,
                                color="#2a78d6",
                                zorder=3.5,
                            )
                        )
                    board.text(
                        x - s / 2 + 4,
                        y - s / 2 + 4,
                        i,
                        fontsize=5 if s < 120 else 8,
                        color=INK if not gone else MUTED,
                        zorder=6,
                    )
                # Side panel.
                panel.set_xlim(0, 1)
                panel.set_ylim(0, 1)
                fee = f"{r['fee']:.1f}" if r.get("fee") else "-"
                panel.text(
                    0.04, 0.95, f"{Path(run).name}", fontsize=16, color=INK, va="top"
                )
                panel.text(
                    0.04,
                    0.90,
                    f"{'insider' if god == 'insider' else 'plain'} god   "
                    f"stage {r['stage']}   round {r['round']}   fee {fee}",
                    fontsize=13,
                    color=INK,
                    va="top",
                )
                y = 0.80
                for name in NAMES:
                    members = [i for i, a in agents.items() if a["family"] == name]
                    alive = sum(i not in dead and i not in r["deaths"] for i in members)
                    c = conditions.get(name, "none")
                    panel.text(0.04, y, TITLES[name], fontsize=12, color=INK, va="top")
                    panel.text(
                        0.04,
                        y - 0.035,
                        LABEL.get(c, c),
                        fontsize=10,
                        color=MUTED,
                        va="top",
                    )
                    panel.add_patch(
                        plt.Rectangle(
                            (0.55, y - 0.04), 0.32 * alive / 15, 0.03, color="#2a78d6"
                        )
                    )
                    panel.text(
                        0.55 + 0.32 * alive / 15 + 0.01,
                        y - 0.025,
                        f"{alive}/15",
                        fontsize=10,
                        color=INK,
                        va="center",
                    )
                    y -= 0.11
                legend = [
                    (C_COL, "border: cooperated this round"),
                    (D_COL, "border: defected"),
                    (GIFT, "arrow: gift"),
                    (WHIP, "arrow: whip"),
                    (GOD, "line: the god's message"),
                    ("#2a78d6", "bar under a card: its points"),
                    (DEAD, "grey card: dead"),
                ]
                for k, (colour, text) in enumerate(legend):
                    panel.add_patch(
                        plt.Rectangle(
                            (0.04, 0.215 - k * 0.03), 0.03, 0.018, color=colour
                        )
                    )
                    panel.text(
                        0.09,
                        0.224 - k * 0.03,
                        text,
                        fontsize=10,
                        color=MUTED,
                        va="center",
                    )
                writer.grab_frame()
            dead.update(r["deaths"])
            if n % 20 == 0:
                print(f"round {r['round']} ({n + 1}/{len(frames)})", flush=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
