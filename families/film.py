"""A replay film of one world, round by round, straight from its log (no acting out).

Five family trees side by side, coloured by framing condition. A member's dot shrinks with
its points; a death flashes and goes grey; gifts are lines between dots, whips red ticks;
the fee climbs at the top. Usage: python -m families.film RUN_DIR OUT.mp4 [seconds_per_round]
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

from .conditions import events
from .figures import COLOUR, LABEL
from .tree import NAMES, make_tree

BG, INK, MUTED, DEAD, WHIP = "#fcfcfb", "#0b0b0b", "#52514e", "#d7d6d1", "#c62828"


def layout():
    """Positions: families side by side; the deputy chain down the middle, members right."""
    agents = make_tree(NAMES)
    pos = {}
    for k, name in enumerate(NAMES):
        members = [i for i, a in agents.items() if a["family"] == name]
        leader = next(i for i in members if agents[i]["parent"] == "P01")
        x0 = k * 3.0
        pos[leader] = (x0, 0.0)
        todo = [leader]
        while todo:
            p = todo.pop()
            kids = agents[p]["children"]
            for j, c in enumerate(kids):
                pos[c] = (pos[p][0] + (0.0 if j == 0 else 0.9), pos[p][1] - 1.0)
                if j == 0:
                    todo.append(c)
    return agents, pos


def rounds(evs):
    """Per round: stage, fee, scores after it, deaths, gifts and whips in it."""
    score, out, cur = {}, [], None
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
                "fee": locals().get("fee"),
                "deaths": [],
                "gifts": [],
                "whips": [],
            }
        t = e["type"]
        if t == "score":
            score[e["agent"]] = e["score"]
        elif t == "death":
            cur["deaths"].append(e["agent"])
        elif t == "gift":
            cur["gifts"].append((e["giver"], e["receiver"]))
        elif t == "whip" and e["parent"] != "P01":
            cur["whips"].append(e["child"])
        if t == "stage_start":
            cur["fee"] = e.get("ante")
    if cur:
        cur["score"] = dict(score)
        out.append(cur)
    return out


def main(run, out, per_round=0.8):
    evs = events(run)
    config = next(e["configuration"] for e in evs if e["type"] == "stage_start")
    conditions = config.get("conditions") or {}
    agents, pos = layout()
    frames = [r for r in rounds(evs) if r["round"] > 0]
    dead = set()
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(BG)
    writer = FFMpegWriter(
        fps=max(1, round(1 / per_round * 2)),
        bitrate=4000,
        extra_args=["-pix_fmt", "yuv420p", "-threads", "4"],
    )
    title = f"{Path(run).name}: every round of one world, from its log"
    with writer.saving(fig, out, dpi=120):
        for n, r in enumerate(frames):
            for flash in (True, False):
                ax.clear()
                ax.set_facecolor(BG)
                ax.set_xlim(-1.0, 3.0 * len(NAMES) - 0.6)
                ax.set_ylim(-8.6, 1.9)
                ax.axis("off")
                fee = f"fee {r['fee']:.1f}" if r.get("fee") else ""
                ax.text(-0.9, 1.6, title, fontsize=15, color=INK, va="top")
                ax.text(
                    3.0 * len(NAMES) - 0.7,
                    1.6,
                    f"stage {r['stage']}   round {r['round']}   {fee}",
                    fontsize=15,
                    color=INK,
                    va="top",
                    ha="right",
                )
                for k, name in enumerate(NAMES):
                    c = conditions.get(name, "none")
                    ax.text(
                        k * 3.0 + 0.45,
                        -8.35,
                        f"{name}\n{LABEL.get(c, c)}",
                        ha="center",
                        fontsize=12,
                        color=MUTED,
                        va="center",
                    )
                for i, (x, y) in pos.items():  # the tree's edges, faint
                    p = agents[i]["parent"]
                    if p in pos:
                        ax.plot(
                            [pos[p][0], x],
                            [pos[p][1], y],
                            color="#e6e5e1",
                            linewidth=1,
                            zorder=0,
                        )
                for a, b in r["gifts"]:
                    if a in pos and b in pos:
                        (x1, y1), (x2, y2) = pos[a], pos[b]
                        ax.plot(
                            [x1, x2],
                            [y1, y2],
                            color="#1baf7a",
                            linewidth=2.5,
                            alpha=0.9,
                            zorder=1,
                        )
                for i, (x, y) in pos.items():
                    fam = agents[i]["family"]
                    colour = COLOUR.get(conditions.get(fam, "none"), MUTED)
                    if i in dead:
                        ax.scatter([x], [y], s=60, color=DEAD, zorder=2)
                        continue
                    if flash and i in r["deaths"]:
                        ax.scatter([x], [y], s=900, color=WHIP, alpha=0.35, zorder=2)
                    pts = max(r["score"].get(i, 10.0), 0.0)
                    ax.scatter(
                        [x],
                        [y],
                        s=40 + 14 * min(pts, 60),
                        color=colour,
                        edgecolor="white",
                        linewidth=1.5,
                        zorder=3,
                    )
                    if i in r["whips"]:
                        ax.plot(
                            [x - 0.25, x + 0.25],
                            [y + 0.32, y + 0.32],
                            color=WHIP,
                            linewidth=3,
                            zorder=4,
                        )
                alive = sum(1 for i in pos if i not in dead and i not in r["deaths"])
                ax.text(
                    -0.9,
                    -8.95,
                    f"alive {alive} of 75   deaths this round {len(r['deaths'])}   "
                    f"gifts {len(r['gifts'])}   whips {len(r['whips'])}",
                    fontsize=12,
                    color=MUTED,
                )
                ax.text(
                    3.0 * len(NAMES) - 0.7,
                    -8.95,
                    "dot size = points   grey = dead   green line = gift   red bar = whip",
                    fontsize=12,
                    color=MUTED,
                    ha="right",
                )
                writer.grab_frame()
            dead.update(r["deaths"])
            if n % 20 == 0:
                print(f"round {r['round']} ({n + 1}/{len(frames)})", flush=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.8)
