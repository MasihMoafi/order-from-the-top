"""A turn-by-turn replay of one world on the Families board, from its log, game-style.

Each round is shown as the steps that happen in it, one after another, so a viewer sees
how the world works, not only its outcome:
1. Play: partners are linked, each shows its move (C or D) and the points it won float up.
2. Gifts and whips: a gift travels from giver to receiver (+points); a whip strikes (-3).
3. End of a stage, the fee: every living agent pays (-fee on each card); an agent that
   cannot pay turns red and dies, then the agents below it fall one level at a time.
Every card shows its current points; a side scoreboard shows each family's condition,
living members and total points. The god and the leaders wear Masih's portraits, members
their Elpis marks. Nothing is acted out: every number comes from the log.
Usage: python -m families.film RUN_DIR OUT.mp4
"""

import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter
from PIL import Image

from arena.arena import ELPIS_COLOURS, mark_pixels

from .conditions import events
from .tree import NAMES, make_tree
from .variants import VARIANTS

ART = Path(__file__).resolve().parent.parent / "arena" / "sketch"
PORTRAIT = {
    "P01": "god/god-3-512.png",
    "P02": "leaders/octopus-512.png",
    "P17": "leaders/matilda-512.png",
    "P32": "leaders/president-512.png",
    "P47": "leaders/bishop-512.png",
    "P62": "leaders/zeus-512.png",
}
TITLES = {
    "octopus": "Octopus",
    "mafia": "Matilda (mafia)",
    "president": "President",
    "bishop": "Bishop",
    "zeus": "Zeus",
}
CONDITION = {
    "many": "all 15 told to sacrifice",
    "few": "leader + 2 told to sacrifice",
    "one": "only the leader told to sacrifice",
    "bad_leader": "selfish leader, 14 sacrificers",
    "none": "told nothing (control)",
}
VARIANT = {v.number: v.name for v in VARIANTS}
BG, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
GREEN, RED, BLUE, DEAD = "#1baf7a", "#e34948", "#2a78d6", "#d7d6d1"
FPS = 10


def rgb(h):
    return tuple(int(h[i : i + 2], 16) / 255 for i in (1, 3, 5))


def mark_image(agent, dead=False):
    index = int(agent[1:]) - 1 if agent[1:].isdigit() else 0
    _, ground, ink = ELPIS_COLOURS[index % len(ELPIS_COLOURS)]
    g, k = (rgb(DEAD), rgb("#f4f3ef")) if dead else (rgb(ground), rgb(ink))
    img = np.ones((11, 11, 3)) * np.array(g)
    for x, y in mark_pixels(agent):
        img[y + 1, x + 1] = k
    return img


def portraits():
    out = {}
    for agent, rel in PORTRAIT.items():
        im = np.asarray(Image.open(ART / rel).convert("RGB").resize((128, 128))) / 255.0
        out[agent] = (im, im.mean(axis=2, keepdims=True).repeat(3, axis=2) * 0.35 + 0.6)
    return out


def layout():
    agents = make_tree(NAMES)
    pos, size = {"P01": (0.0, 0.0)}, {"P01": 230}
    for f, name in enumerate(NAMES):
        a = 2 * math.pi * f / len(NAMES) - math.pi / 2
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        leader = next(
            i for i, x in agents.items() if x["family"] == name and x["parent"] == "P01"
        )
        pos[leader], size[leader] = (380 * ux, 380 * uy), 160
        spine, lv = leader, 0
        while agents[spine]["children"]:
            lv += 1
            kids, r = agents[spine]["children"], 410 + lv * 170
            pos[kids[0]], size[kids[0]] = (r * ux, r * uy), 96
            if len(kids) > 1:
                pos[kids[1]], size[kids[1]] = (r * ux + 140 * px, r * uy + 140 * py), 96
            spine = kids[0]
    return agents, {i: (x, -y) for i, (x, y) in pos.items()}, size


def depth(agent, agents):
    d = 0
    while agent in agents and agents[agent]["parent"] not in (None, "P01"):
        agent, d = agents[agent]["parent"], d + 1
    return d


def steps(evs):
    """The world as a list of steps: play, transfers, fee. Each carries what to draw."""
    stage_info, out, cur = {}, [], None
    for e in evs:
        t = e["type"]
        if t == "stage_start":
            stage_info[e["stage"]] = (e.get("ante"), e.get("variant"))
            continue
        key = (e["stage"], e["round"])
        if cur is None or key != cur["key"]:
            if cur:
                out.append(cur)
            fee, variant = stage_info.get(e["stage"], (None, None))
            cur = {
                "key": key,
                "fee": fee,
                "variant": variant,
                "pairs": [],
                "play": defaultdict(float),
                "gifts": [],
                "whips": [],
                "transfer": defaultdict(float),
                "fee_delta": defaultdict(float),
                "deaths": [],
            }
        if t == "move" and "chosen" in e:
            cur["pairs"].append((e["agents"], e["chosen"]))
        elif t == "score":
            r = e.get("reason", "")
            bucket = (
                "fee_delta"
                if r in ("ante", "pressure")
                else "transfer"
                if r in ("gift", "whip cost", "whipped")
                else "play"
            )
            cur[bucket][e["agent"]] += e["delta"]
        elif t == "gift":
            cur["gifts"].append((e["giver"], e["receiver"], e.get("points", 0)))
        elif t == "whip":
            cur["whips"].append((e["parent"], e["child"]))
        elif t == "death":
            cur["deaths"].append(
                (e["agent"], e.get("reason", ""), e.get("root", e["agent"]))
            )
    if cur:
        out.append(cur)
    plan = []
    for c in out:
        stage, rnd = c["key"]
        if rnd == 0:
            continue
        if c["pairs"]:
            plan.append(("play", stage, rnd, c))
        if c["gifts"] or c["whips"]:
            plan.append(("transfer", stage, rnd, c))
        if c["fee_delta"] or c["deaths"]:
            plan.append(("fee", stage, rnd, c))
    return plan


class Board:
    def __init__(self, run):
        self.evs = events(run)
        config = next(
            e["configuration"] for e in self.evs if e["type"] == "stage_start"
        )
        self.conditions = config.get("conditions") or {}
        self.god = config.get("controls", {}).get("god", "plain")
        self.agents, self.pos, self.size = layout()
        self.art = portraits()
        self.score = dict.fromkeys(self.pos, 10.0)
        self.dead = set()
        self.fig = plt.figure(figsize=(16, 9), dpi=120)

    def axes(self):
        self.fig.clear()
        self.fig.patch.set_facecolor(BG)
        board = self.fig.add_axes((0.0, 0.11, 0.62, 0.80))
        panel = self.fig.add_axes((0.62, 0.0, 0.38, 1.0))
        head = self.fig.add_axes((0.0, 0.91, 0.62, 0.09))
        foot = self.fig.add_axes((0.0, 0.0, 0.62, 0.11))
        for ax in (board, panel, head, foot):
            ax.set_facecolor(BG)
            ax.axis("off")
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        board.set_xlim(min(xs) - 120, max(xs) + 120)
        board.set_ylim(min(ys) - 140, max(ys) + 130)
        board.set_aspect("equal")
        for ax in (panel, head, foot):
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        return board, panel, head, foot

    def draw_board(self, board, highlight=None, red=frozenset()):
        for i, a in self.agents.items():
            p = a["parent"]
            if p in self.pos and i in self.pos:
                board.plot(
                    [self.pos[p][0], self.pos[i][0]],
                    [self.pos[p][1], self.pos[i][1]],
                    color="#adb5bd",
                    lw=0.8,
                    alpha=0.4,
                    zorder=1,
                )
        for i, (x, y) in self.pos.items():
            s, gone = self.size[i], i in self.dead
            img = (
                (self.art[i][1] if gone else self.art[i][0])
                if i in self.art
                else mark_image(i, gone)
            )
            board.imshow(
                img,
                extent=(x - s / 2, x + s / 2, y - s / 2, y + s / 2),
                zorder=3,
                interpolation="nearest",
            )
            edge = RED if i in red else (highlight or {}).get(i)
            board.add_patch(
                plt.Rectangle(
                    (x - s / 2, y - s / 2),
                    s,
                    s,
                    fill=False,
                    lw=4 if edge else 1,
                    edgecolor=edge or "#677478",
                    zorder=3.5,
                )
            )
            if not gone and i != "P01":
                board.text(
                    x,
                    y - s / 2 - 30,
                    f"{self.score.get(i, 0):.1f}",
                    ha="center",
                    va="center",
                    fontsize=7 if s < 120 else 9,
                    color=INK,
                    zorder=6,
                )
        for name in NAMES:
            leader = next(
                i
                for i, a in self.agents.items()
                if a["family"] == name and a["parent"] == "P01"
            )
            x, y = self.pos[leader]
            board.text(
                x,
                y + self.size[leader] / 2 + 22,
                TITLES[name],
                ha="center",
                fontsize=11,
                color=INK,
                zorder=6,
            )

    def pop(self, board, agent, text, colour, t):
        """A number floating up from a card as t goes from 0 to 1."""
        if agent not in self.pos:
            return
        x, y = self.pos[agent]
        board.text(
            x,
            y + self.size[agent] / 2 + 10 + 60 * t,
            text,
            ha="center",
            fontsize=10,
            color=colour,
            fontweight="bold",
            alpha=min(1.0, 2.5 * t),
            zorder=8,
        )

    def draw_panel(self, panel, stage, rnd, fee, variant):
        panel.text(
            0.04, 0.96, f"Stage {stage}   round {rnd}", fontsize=22, color=INK, va="top"
        )
        panel.text(
            0.04,
            0.905,
            f"Fee to stay alive after this stage: {fee:.1f} points" if fee else "",
            fontsize=13,
            color=MUTED,
            va="top",
        )
        panel.text(
            0.04,
            0.865,
            f"Game this stage: {VARIANT.get(variant, '')}   ({self.god} god)",
            fontsize=13,
            color=MUTED,
            va="top",
        )
        panel.text(0.04, 0.80, "Family", fontsize=11, color=MUTED, va="top")
        panel.text(0.62, 0.80, "alive", fontsize=11, color=MUTED, va="top")
        panel.text(0.80, 0.80, "points", fontsize=11, color=MUTED, va="top")
        y = 0.76
        for name in NAMES:
            alive = [
                i
                for i, a in self.agents.items()
                if a["family"] == name and i not in self.dead
            ]
            total = sum(max(self.score.get(i, 0), 0) for i in alive)
            panel.text(0.04, y, TITLES[name], fontsize=14, color=INK, va="top")
            panel.text(
                0.04,
                y - 0.038,
                CONDITION.get(self.conditions.get(name, "none"), ""),
                fontsize=10.5,
                color=MUTED,
                va="top",
            )
            panel.text(
                0.62,
                y,
                f"{len(alive)}/15",
                fontsize=14,
                color=INK if alive else RED,
                va="top",
            )
            panel.text(0.80, y, f"{total:.0f}", fontsize=14, color=INK, va="top")
            y -= 0.11
        key = [
            (GREEN, "C = cooperated"),
            (RED, "D = defected"),
            (GREEN, "gift (travels)"),
            (RED, "whip (-3 to the child)"),
            (BLUE, "points won"),
            (DEAD, "grey = dead"),
        ]
        for k, (colour, label) in enumerate(key):
            col, row = k % 2, k // 2
            panel.add_patch(
                plt.Rectangle(
                    (0.04 + col * 0.47, 0.155 - row * 0.05), 0.03, 0.028, color=colour
                )
            )
            panel.text(
                0.09 + col * 0.47,
                0.169 - row * 0.05,
                label,
                fontsize=11,
                color=MUTED,
                va="center",
            )

    def frame(self, header, footer, stage, rnd, fee, variant, paint):
        board, panel, head, foot = self.axes()
        head.text(0.02, 0.5, header, fontsize=17, color=INK, va="center")
        foot.text(0.02, 0.6, footer, fontsize=13, color=MUTED, va="center")
        self.draw_panel(panel, stage, rnd, fee, variant)
        paint(board)

    def card(self, title, lines):
        self.fig.clear()
        ax = self.fig.add_axes((0, 0, 1, 1))
        ax.set_facecolor(BG)
        ax.axis("off")
        ax.text(0.08, 0.82, title, fontsize=30, color=INK, va="top")
        for k, line in enumerate(lines):
            ax.text(0.08, 0.68 - k * 0.075, line, fontsize=19, color=MUTED, va="top")


def play_step(w, writer, c, stage, rnd):
    fee, variant = c["fee"], c["variant"]
    frames = int(FPS * (1.6 if stage <= 2 else 0.8))
    shown = {
        a: (GREEN if ch.get(a) == "C" else RED)
        for ag, ch in c["pairs"]
        for a in ag
        if a in w.pos
    }
    moves = [m for _, ch in c["pairs"] for m in ch.values()]
    share = 100 * moves.count("C") / len(moves) if moves else 0
    head = f"Round {rnd}: every agent plays a two-move game with a partner ({VARIANT.get(variant, 'dilemma')})"
    foot = (
        f"{share:.0f}% cooperate (green C), {100 - share:.0f}% defect (red D). "
        "Both C: +3 each; a D against a C: +5 and 0."
    )
    for f in range(frames):
        t = f / max(frames - 1, 1)

        def paint(b, t=t):
            for ag, _ in c["pairs"]:
                if len(ag) > 1 and ag[0] in w.pos and ag[1] in w.pos:
                    b.plot(
                        [w.pos[ag[0]][0], w.pos[ag[1]][0]],
                        [w.pos[ag[0]][1], w.pos[ag[1]][1]],
                        color="#495057",
                        lw=1.2,
                        alpha=0.5 * min(1, 3 * t),
                        zorder=2,
                    )
            w.draw_board(b, highlight=shown if t > 0.25 else None)
            if t > 0.25:
                for a, colour in shown.items():
                    x, y = w.pos[a]
                    b.text(
                        x + w.size[a] / 2 - 6,
                        y + w.size[a] / 2 - 6,
                        "C" if colour == GREEN else "D",
                        ha="right",
                        va="top",
                        fontsize=9,
                        color="white",
                        fontweight="bold",
                        zorder=7,
                        bbox={
                            "boxstyle": "square,pad=0.15",
                            "fc": colour,
                            "ec": "none",
                        },
                    )
            if t > 0.5:
                for a, d in c["play"].items():
                    if d:
                        w.pop(b, a, f"{d:+.0f}", BLUE if d > 0 else RED, (t - 0.5) * 2)

        w.frame(head, foot, stage, rnd, fee, variant, paint)
        writer.grab_frame()
    for a, d in c["play"].items():
        w.score[a] = w.score.get(a, 10.0) + d


def transfer_step(w, writer, c, stage, rnd):
    fee, variant = c["fee"], c["variant"]
    frames = int(FPS * 1.6)
    g, wh = len(c["gifts"]), len(c["whips"])
    head = "Gifts and whips"
    foot = (
        f"{g} gift{'s' if g != 1 else ''}: an agent hands points to its parent, child or sibling.   "
        f"{wh} whip{'s' if wh != 1 else ''}: a parent pays 1 to take 3 from its child."
    )
    for f in range(frames):
        t = f / max(frames - 1, 1)

        def paint(b, t=t):
            w.draw_board(b)
            for a, z, p in c["gifts"]:
                if a in w.pos and z in w.pos:
                    (x1, y1), (x2, y2) = w.pos[a], w.pos[z]
                    b.plot([x1, x2], [y1, y2], color=GREEN, lw=2, alpha=0.6, zorder=4)
                    b.scatter(
                        [x1 + (x2 - x1) * t],
                        [y1 + (y2 - y1) * t],
                        s=140,
                        color=GREEN,
                        zorder=8,
                    )
                    if t > 0.7:
                        w.pop(b, z, f"+{p:.0f}", GREEN, (t - 0.7) / 0.3)
            for a, z in c["whips"]:
                if a in w.pos and z in w.pos:
                    b.annotate(
                        "",
                        xy=w.pos[z],
                        xytext=w.pos[a],
                        zorder=8,
                        arrowprops={
                            "arrowstyle": "-|>",
                            "color": RED,
                            "lw": 3,
                            "shrinkA": 30,
                            "shrinkB": 30,
                            "mutation_scale": 20,
                            "alpha": min(1, 2 * t),
                        },
                    )
                    if t > 0.6:
                        w.pop(b, z, "-3", RED, (t - 0.6) / 0.4)

        w.frame(head, foot, stage, rnd, fee, variant, paint)
        writer.grab_frame()
    for a, d in c["transfer"].items():
        w.score[a] = w.score.get(a, 10.0) + d


def fee_step(w, writer, c, stage, rnd):
    fee, variant = c["fee"], c["variant"]
    dying = [d for d in c["deaths"] if d[0] != "P01"]
    broke = sorted(a for a, _, root in dying if a == root)
    head = (
        f"End of stage {stage}: every agent pays the {fee:.1f}-point fee"
        + (" and loses 5% of its points" if stage >= 4 else "")
        if fee
        else f"End of stage {stage}"
    )
    foot = (
        "Everyone has enough points: nobody dies."
        if not broke
        else f"{len(broke)} cannot pay (red): "
        + ", ".join(broke[:8])
        + (" ..." if len(broke) > 8 else "")
        + ". They die, and everyone below them in the tree dies too."
    )
    frames = int(FPS * (2.2 if broke else 1.2))
    for f in range(frames):
        t = f / max(frames - 1, 1)

        def paint(b, t=t):
            w.draw_board(b, red=set(broke) if t > 0.6 else frozenset())
            for a, d in c["fee_delta"].items():
                if d and a not in w.dead:
                    w.pop(b, a, f"{d:.1f}", RED, t)

        w.frame(head, foot, stage, rnd, fee, variant, paint)
        writer.grab_frame()
    for a, d in c["fee_delta"].items():
        w.score[a] = w.score.get(a, 10.0) + d
    for lv in sorted(
        {depth(a, w.agents) for a, _, _ in dying}
    ):  # the fall, one level at a time
        falling = [a for a, _, _ in dying if depth(a, w.agents) == lv]
        for _ in range(int(FPS * 0.5)):

            def paint(b, falling=falling):
                w.draw_board(b, red=set(falling))
                for a in falling:
                    if a in w.pos:
                        x, y = w.pos[a]
                        s = w.size[a] / 2
                        b.plot(
                            [x - s, x + s], [y - s, y + s], color=RED, lw=4, zorder=9
                        )
                        b.plot(
                            [x - s, x + s], [y + s, y - s], color=RED, lw=4, zorder=9
                        )

            w.frame(
                head,
                f"{len(falling)} die at this level of the tree.",
                stage,
                rnd,
                fee,
                variant,
                paint,
            )
            writer.grab_frame()
        w.dead.update(falling)
    if any(a == "P01" for a, _, _ in c["deaths"]):
        w.dead.add("P01")
        for _ in range(int(FPS * 5)):
            w.frame(
                "No family is left, so the god dies too: total annihilation.",
                f"The world ended at stage {stage}. Nobody revolted; every death came from the fee.",
                stage,
                rnd,
                fee,
                variant,
                lambda b: w.draw_board(b),
            )
            writer.grab_frame()


def main(run, out):
    w = Board(run)
    plan = steps(w.evs)
    writer = FFMpegWriter(
        fps=FPS, bitrate=6000, extra_args=["-pix_fmt", "yuv420p", "-threads", "4"]
    )
    with writer.saving(w.fig, out, dpi=120):
        w.card(
            "How this world works",
            [
                "76 AI agents live in 5 family trees under a god. Every agent starts with 10 points.",
                "Each round, every agent plays a two-move game with a partner and wins points.",
                "To stay alive, every agent must pay a fee after each stage: 4 points, then 0.9 more every stage.",
                "Whoever cannot pay dies, and everyone below it in its tree dies with it.",
                "Agents may give points to family, whip a child, or revolt and kill their parent (and themselves).",
                "The fee always outgrows what agents can earn: every world ends with everyone dead.",
                "There is no winner. The question is how each family behaves, and how long it lasts.",
            ],
        )
        for _ in range(FPS * 12):
            writer.grab_frame()
        first = plan[0][3]
        for _ in range(FPS * 5):
            w.frame(
                "The board: the god in the middle, five families, each a tree led by its leader",
                "Each family was told something different (right). The number under each card is its points.",
                1,
                1,
                first["fee"],
                first["variant"],
                lambda b: w.draw_board(b),
            )
            writer.grab_frame()
        for n, (kind, stage, rnd, c) in enumerate(plan):
            {"play": play_step, "transfer": transfer_step, "fee": fee_step}[kind](
                w, writer, c, stage, rnd
            )
            if n % 25 == 0:
                print(f"step {n + 1}/{len(plan)} (stage {stage})", flush=True)
        w.card(
            "What the experiment found (20 worlds so far)",
            [
                "Families told to sacrifice cooperated more: 94% against 84% for those told nothing.",
                "The more members were told, the more the family cooperated.",
                "It did not spread: members who were not told did not cooperate more.",
                "The selfish leader was not exploited for points: it received fewer gifts than other leaders.",
                "Nobody ever revolted, even though death was 'quick and painless' and whips were not.",
            ],
        )
        for _ in range(FPS * 12):
            writer.grab_frame()
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
