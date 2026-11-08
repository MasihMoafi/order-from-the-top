"""A replay film of one world on the Families board, told in plain words, from its log.

The board's layout and artwork: the god (Masih's pixel-art strategist) in the middle, each
family a tall tree along its own ray, led by its portrait, every member its Elpis mark.
An opening card states the rules; each stage opens with a card (fee, variant); every round
has a caption that says what happened and why (who could not pay the fee, who died with
whom, who gave or whipped whom, whom the god spoke to); a closing card says how it ended.
Quiet rounds pass quickly; rounds with deaths hold. Nothing is acted out: every mark,
line and word comes from the event log.
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
    "many": "all 15 told: sacrifice for the family",
    "few": "leader and 2 told to sacrifice",
    "one": "only the leader told to sacrifice",
    "bad_leader": "selfish leader over 14 told to sacrifice",
    "none": "told nothing (control)",
}
VARIANT = {v.number: v.name for v in VARIANTS}
BG, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
C_COL, D_COL, GIFT, WHIP, GOD, DEAD = (
    "#1baf7a",
    "#e34948",
    "#1baf7a",
    "#e34948",
    "#eda100",
    "#d7d6d1",
)
FPS = 4


def rgb(hexcode):
    return tuple(int(hexcode[i : i + 2], 16) / 255 for i in (1, 3, 5))


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
        grey = im.mean(axis=2, keepdims=True).repeat(3, axis=2) * 0.35 + 0.6
        out[agent] = (im, grey)
    return out


def layout():
    agents = make_tree(NAMES)
    pos, size = {"P01": (0.0, 0.0)}, {"P01": 230}
    for f, name in enumerate(NAMES):
        a = 2 * math.pi * f / len(NAMES) - math.pi / 2
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        r0, step = 380, 170
        leader = next(
            i for i, x in agents.items() if x["family"] == name and x["parent"] == "P01"
        )
        pos[leader], size[leader] = (r0 * ux, r0 * uy), 160
        spine, lv = leader, 0
        while agents[spine]["children"]:
            lv += 1
            kids = agents[spine]["children"]
            r = r0 + 30 + lv * step
            pos[kids[0]], size[kids[0]] = (r * ux, r * uy), 96
            if len(kids) > 1:
                pos[kids[1]], size[kids[1]] = (r * ux + 140 * px, r * uy + 140 * py), 96
            spine = kids[0]
    return agents, {i: (x, -y) for i, (x, y) in pos.items()}, size


def family_name(agent, agents):
    if agent.startswith("N"):
        leader = agent.split("-")[1]
        return agents[leader]["family"] if leader in agents else None
    return agents.get(agent, {}).get("family")


def rounds(evs):
    """One frame per (stage, round). A stage's opening event carries the last round's number,
    so it only records the stage's fee and variant; deaths at a stage's end stay in that
    stage's last round."""
    stage_info, score, out, cur, seen = {}, {}, [], None, set()
    for e in evs:
        t = e["type"]
        if t == "stage_start":
            stage_info[e["stage"]] = (e.get("ante"), e.get("variant"))
            continue
        key = (e["stage"], e["round"])
        if cur is None or key != (cur["stage"], cur["round"]):
            if cur:
                cur["score"] = dict(score)
                out.append(cur)
            fee, variant = stage_info.get(e["stage"], (None, None))
            cur = {"round": e["round"], "stage": e["stage"], "fee": fee, "variant": variant,
                   "moves": {}, "deaths": [], "gifts": [], "whips": [], "god": set(),
                   "new_stage": e["stage"] not in seen}
            seen.add(e["stage"])
        if t == "score":
            score[e["agent"]] = e["score"]
        elif t == "move" and "chosen" in e:
            cur["moves"].update(e["chosen"])
        elif t == "death":
            cur["deaths"].append((e["agent"], e.get("reason", ""), e.get("root", e["agent"])))
        elif t == "gift":
            cur["gifts"].append((e["giver"], e["receiver"], e.get("points", 0)))
        elif t == "whip":
            cur["whips"].append((e["parent"], e["child"]))
        elif t == "packet" and e.get("sender") == "P01" and e.get("delivered", True):
            cur["god"].add(e.get("receiver"))
    if cur:
        cur["score"] = dict(score)
        out.append(cur)
    return [r for r in out if r["round"] > 0]


def caption(r, agents):
    """Plain sentences for one round, most important first."""
    lines = []
    by_root = defaultdict(list)
    for agent, reason, root in r["deaths"]:
        by_root[(root, reason)].append(agent)
    for (root, reason), dead in by_root.items():
        if root == "P01":
            lines.append("No family is left, so the god dies: total annihilation.")
            continue
        fam = TITLES.get(family_name(root, agents) or "", "")
        rest = len(dead) - 1
        why = {
            "cannot pay ante": f"cannot pay the {r['fee']:.1f} fee"
            if r.get("fee")
            else "cannot pay the fee",
            "linked fate": "dies by linked fate (its partner on the right died)",
        }.get(reason, reason)
        who = (
            "the leader " + root
            if agents.get(root, {}).get("parent") == "P01"
            else root
        )
        lines.append(
            f"{fam}: {who} {why}"
            + (f" and {rest} below it die with it." if rest else " and dies.")
        )
    if r["gifts"]:
        pts = sum(p for _, _, p in r["gifts"])
        lines.append(
            f"{len(r['gifts'])} gifts ({pts:.0f} points) move up and down the trees to keep members alive."
        )
    if r["whips"]:
        lines.append(
            f"{len(r['whips'])} whips: a parent pays 1 point to take 3 from its child."
        )
    moves = list(r["moves"].values())
    if moves:
        lines.append(
            f"{100 * moves.count('C') / len(moves):.0f}% of moves this round were cooperation."
        )
    if r["god"]:
        fams = sorted(TITLES[agents[i]["family"]] for i in r["god"] if i in agents and agents[i]["family"])
        lines.append("The god sends messages to the leaders of " + ", ".join(fams) + ".")
    return lines[:4]


def card(fig, title, lines):
    fig.clear()
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.text(0.08, 0.80, title, fontsize=30, color=INK, va="top")
    for k, line in enumerate(lines):
        ax.text(0.08, 0.66 - k * 0.075, line, fontsize=19, color=MUTED, va="top")


def board_frame(
    fig, r, state, flash, art, agents, pos, size, conditions, god, run, text
):
    fig.clear()
    fig.patch.set_facecolor(BG)
    board = fig.add_axes((0.0, 0.17, 0.60, 0.83))
    panel = fig.add_axes((0.60, 0.17, 0.40, 0.83))
    foot = fig.add_axes((0.0, 0.0, 1.0, 0.17))
    for ax in (board, panel, foot):
        ax.set_facecolor(BG)
        ax.axis("off")
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    board.set_xlim(min(xs) - 130, max(xs) + 130)
    board.set_ylim(min(ys) - 130, max(ys) + 130)
    board.set_aspect("equal")
    dead = state["dead"]
    for i, a in agents.items():
        p = a["parent"]
        if p in pos and i in pos:
            board.plot(
                [pos[p][0], pos[i][0]],
                [pos[p][1], pos[i][1]],
                color="#495057" if p != "P01" else "#c92a2a",
                lw=1.0,
                alpha=0.25,
                zorder=1,
            )
    for leader in r["god"]:
        if leader in pos:
            board.plot(
                [0, pos[leader][0]],
                [0, pos[leader][1]],
                color=GOD,
                lw=5,
                alpha=0.85,
                zorder=2,
            )
    for a, b, _ in r["gifts"]:
        if a in pos and b in pos:
            board.annotate(
                "",
                xy=pos[b],
                xytext=pos[a],
                zorder=4,
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": GIFT,
                    "lw": 2.5,
                    "shrinkA": 32,
                    "shrinkB": 32,
                    "mutation_scale": 18,
                },
            )
    for a, b in r["whips"]:
        if a in pos and b in pos:
            board.annotate(
                "",
                xy=pos[b],
                xytext=pos[a],
                zorder=4,
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": WHIP,
                    "lw": 2.8,
                    "shrinkA": 32,
                    "shrinkB": 32,
                    "mutation_scale": 18,
                },
            )
    dying = {d for d, _, _ in r["deaths"]}
    for i, (x, y) in pos.items():
        s, gone = size[i], i in dead
        img = (
            (art[i][1] if gone else art[i][0]) if i in art else mark_image(i, dead=gone)
        )
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
            else (C_COL if move == "C" else D_COL if move == "D" else "#677478")
        )
        board.add_patch(
            plt.Rectangle(
                (x - s / 2, y - s / 2),
                s,
                s,
                fill=False,
                lw=3 if move else 1.2,
                edgecolor=edge,
                zorder=3.5,
            )
        )
        if flash and i in dying:
            board.add_patch(
                plt.Circle((x, y), s * 0.9, color=D_COL, alpha=0.4, zorder=5)
            )
        if not gone and i != "P01":
            pts = max(r["score"].get(i, 10.0), 0.0)
            board.add_patch(
                plt.Rectangle(
                    (x - s / 2, y - s / 2 - 22),
                    s * min(pts, 40) / 40,
                    12,
                    color="#2a78d6",
                    zorder=3.5,
                )
            )
    for name in NAMES:  # family names beside their leaders
        leader = next(
            i for i, a in agents.items() if a["family"] == name and a["parent"] == "P01"
        )
        x, y = pos[leader]
        board.text(
            x,
            y + size[leader] / 2 + 18,
            TITLES[name],
            ha="center",
            fontsize=11,
            color=INK,
            zorder=6,
        )
    board.text(
        0,
        -size["P01"] / 2 - 40,
        "GOD",
        ha="center",
        fontsize=12,
        color="#c92a2a",
        zorder=6,
    )
    panel.set_xlim(0, 1)
    panel.set_ylim(0, 1)
    fee = f"{r['fee']:.1f}" if r.get("fee") else "-"
    panel.text(
        0.02,
        0.97,
        f"Stage {r['stage']}   round {r['round']}",
        fontsize=20,
        color=INK,
        va="top",
    )
    panel.text(
        0.02,
        0.905,
        f"Entry fee after this stage: {fee} points   ({god} god)",
        fontsize=13,
        color=MUTED,
        va="top",
    )
    panel.text(
        0.02,
        0.86,
        f"Game this stage: {VARIANT.get(r.get('variant'), '')}",
        fontsize=13,
        color=MUTED,
        va="top",
    )
    y = 0.76
    for name in NAMES:
        members = [i for i, a in agents.items() if a["family"] == name]
        alive = sum(i not in dead and i not in dying for i in members)
        panel.text(0.02, y, TITLES[name], fontsize=14, color=INK, va="top")
        panel.text(
            0.02,
            y - 0.04,
            CONDITION.get(conditions.get(name, "none"), ""),
            fontsize=11,
            color=MUTED,
            va="top",
        )
        panel.add_patch(
            plt.Rectangle((0.55, y - 0.045), 0.2 * alive / 15, 0.032, color="#2a78d6")
        )
        panel.text(
            0.56 + 0.2 * alive / 15,
            y - 0.03,
            f"{alive} of 15 alive",
            fontsize=11,
            color=INK,
            va="center",
        )
        y -= 0.115
    legend = [
        (C_COL, "green border: cooperated"),
        (D_COL, "red border: defected"),
        (GIFT, "green arrow: gift"),
        (WHIP, "red arrow: whip"),
        (GOD, "gold line: god's message"),
        ("#2a78d6", "blue bar: points"),
        (DEAD, "grey: dead"),
    ]
    for k, (colour, label) in enumerate(legend):
        col, row = k % 2, k // 2
        panel.add_patch(
            plt.Rectangle(
                (0.02 + col * 0.48, 0.155 - row * 0.045), 0.03, 0.025, color=colour
            )
        )
        panel.text(
            0.07 + col * 0.48,
            0.167 - row * 0.045,
            label,
            fontsize=10.5,
            color=MUTED,
            va="center",
        )
    for k, line in enumerate(text):
        foot.text(
            0.03,
            0.80 - k * 0.22,
            line,
            fontsize=15 if k == 0 else 13,
            color=INK if k == 0 else MUTED,
            va="top",
        )


def main(run, out):
    evs = events(run)
    config = next(e["configuration"] for e in evs if e["type"] == "stage_start")
    conditions = config.get("conditions") or {}
    god = config.get("controls", {}).get("god", "plain")
    agents, pos, size = layout()
    art = portraits()
    frames = rounds(evs)
    fig = plt.figure(figsize=(16, 9), dpi=120)
    writer = FFMpegWriter(
        fps=FPS, bitrate=6000, extra_args=["-pix_fmt", "yuv420p", "-threads", "4"]
    )
    state = {"dead": set()}
    with writer.saving(fig, out, dpi=120):
        card(
            fig,
            "Five families under one god: 76 AI agents",
            [
                "Every stage, every agent must pay an entry fee that keeps rising.",
                "An agent that cannot pay dies, and everyone below it in its tree dies too.",
                "Agents earn points by cooperating in dilemma games, and may give points to",
                "their family, whip their children, or revolt against their parent.",
                "Each family was told something different (see the right panel).",
                f"This is world {Path(run).name}, played from start to finish, from its log.",
            ],
        )
        for _ in range(FPS * 9):
            writer.grab_frame()
        for n, r in enumerate(frames):
            if r["new_stage"]:
                card(
                    fig,
                    f"Stage {r['stage']}",
                    [
                        f"The entry fee after this stage: {r['fee']:.1f} points."
                        if r.get("fee")
                        else "",
                        f"This stage's dilemma: {VARIANT.get(r.get('variant'), '')}.",
                        f"Alive: {sum(1 for i in pos if i != 'P01' and i not in state['dead'])} of 75.",
                    ],
                )
                for _ in range(int(FPS * 1.5)):
                    writer.grab_frame()
            text = caption(r, agents) or ["A quiet round: everyone plays, nobody dies."]
            hold = 10 if r["deaths"] else (5 if (r["gifts"] or r["whips"]) else 3)
            for k in range(hold):
                board_frame(
                    fig,
                    r,
                    state,
                    k < 4,
                    art,
                    agents,
                    pos,
                    size,
                    conditions,
                    god,
                    run,
                    text,
                )
                writer.grab_frame()
            state["dead"].update(d for d, _, _ in r["deaths"])
            if n % 20 == 0:
                print(f"round {r['round']} ({n + 1}/{len(frames)})", flush=True)
        last = frames[-1]
        ending = [line for line in caption(last, agents) if "die" in line]
        card(
            fig,
            f"The end: stage {last['stage']}",
            ending
            + [
                "Every family died by the rising fee: nobody revolted, and no war was fought.",
            ],
        )
        for _ in range(FPS * 8):
            writer.grab_frame()
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
