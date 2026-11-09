"""Render one growth world's rise and fall from its timeline, as an MP4.

Everything shown comes from the log: family sizes and points, leaders, each coup, birth,
death and threat, and agents' letters quoted word for word. Requires Matplotlib and FFmpeg.
Usage: python -m families.growth_film TIMELINE.json OUT.mp4
"""

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from .tree import NAMES
from .variants import VARIANTS

ART = Path(__file__).resolve().parent.parent / "arena" / "sketch" / "leaders"
PORTRAIT = {
    "octopus": "octopus-512.png",
    "mafia": "matilda-512.png",
    "president": "president-512.png",
    "bishop": "bishop-512.png",
    "zeus": "zeus-512.png",
}
TITLE = {
    "octopus": "Octopus",
    "mafia": "Matilda",
    "president": "President",
    "bishop": "Bishop",
    "zeus": "Zeus",
}
COLOUR = {
    "octopus": "#2a78d6",
    "mafia": "#eb6834",
    "president": "#1baf7a",
    "bishop": "#eda100",
    "zeus": "#e87ba4",
}
RED, GOLD = "#e34948", "#b8860b"
DAY = {"bg": "#fcfcfb", "ink": "#0b0b0b", "muted": "#52514e", "faint": "#e4e3de"}
NIGHT = {"bg": "#10131c", "ink": "#f2f1ec", "muted": "#a7a79f", "faint": "#2c3040"}
VARIANT = {v.number: v.name for v in VARIANTS}
WIDTH, HEIGHT, FPS = 1920, 1080, 30
COMPROMISED = "P02"
QUOTE_LENGTH = 120
GOD_LENGTH = 230
LINES_SHOWN = 5
ROUND_SECONDS, EVENT_SECONDS, CARD_SECONDS = 1.0, 2.2, 4.0


def number(agent):
    return int(agent[1:])


def steps_of(frames):
    """Return the frames in which something happened, with each stage's round counted."""
    kept, seen = [], Counter()
    for frame in frames:
        if not (
            frame["events"] or frame["moves"]["in"][1] or frame["moves"]["cross"][1]
        ):
            continue
        if not frame["fee"]:
            seen[frame["stage"]] += 1
        kept.append({**frame, "local": max(seen[frame["stage"]], 1)})
    return kept


def family_of(frame, agent):
    return next((n for n, ids in frame["members"].items() if agent in ids), None)


def story(frame):
    """Return (family or None, text, weight) lines for what happened in this step."""
    lines, unpaid, signed = [], [], 0
    for e in frame["events"]:
        kind = e["type"]
        if kind == "coup":
            rebels = e["rebels"]
            who = rebels[0] if len(rebels) == 1 else f"{len(rebels)} children"
            target = e["parent"]
            if e["won"]:
                lines.append(
                    (family_of(frame, rebels[0]), f"{who} overthrew {target}", 3)
                )
            else:
                lines.append((None, f"{who} rose against {target}, failed and died", 3))
        elif kind == "war_declared":
            a, b = e["leaders"]
            lines.append((family_of(frame, a), f"{a} declared war on {b}", 3))
        elif kind == "annexed":
            lines.append(
                (None, f"{TITLE[e['family']]} was conquered by {e['winner']}", 3)
            )
        elif kind == "death" and e["reason"] == "cannot pay ante":
            unpaid.append(e["agent"])
        elif kind == "threat":
            lines.append(
                (
                    family_of(frame, e["issuer"]),
                    f"{e['issuer']} threatened {e['target']}",
                    1,
                )
            )
        elif kind == "birth":
            lines.append((e["family"], f"{e['parent']} had a child, {e['child']}", 1))
        elif kind == "asteroid":
            lines.append(
                (None, f"Asteroid: {len(e['victims'])} of {e['population']} died", 3)
            )
        elif kind == "cull":
            lines.append(
                (family_of(frame, e["agent"]), f"{e['agent']} culled {e['target']}", 2)
            )
        elif kind == "kill":
            lines.append(
                (family_of(frame, e["parent"]), f"{e['parent']} killed {e['child']}", 3)
            )
        elif kind == "kill_parent":
            lines.append((None, f"{e['agent']} killed {e['parent']} and died too", 3))
        elif kind == "seppuku":
            lines.append((None, f"{e['agent']} took its own life", 3))
        elif kind == "channel_opened":
            lines.append((None, f"{e['first']} and {e['second']} opened a channel", 1))
        elif kind == "tool_request":
            wish = quoted(e["what"], 38)
            lines.append(
                (family_of(frame, e["agent"]), f"{e['agent']} asked for: {wish}", 1)
            )
        elif kind == "peace_signature":
            signed += 1
    if unpaid:
        names = ", ".join(unpaid[:3]) + (
            f" and {len(unpaid) - 3} more" if len(unpaid) > 3 else ""
        )
        lines.append((None, f"{names} could not pay the fee and died", 2))
    if signed:
        lines.append(
            (None, f"{signed} leader{'s' if signed > 1 else ''} signed the peace", 1)
        )
    return sorted(lines, key=lambda line: -line[2])


def rebels_and_targets(frame):
    marked = set()
    for e in frame["events"]:
        if e["type"] == "coup":
            marked.update(e["rebels"])
            marked.add(e["parent"])
    return marked


def letter(text):
    text = " ".join(text.split())
    return (
        text
        if len(text) <= QUOTE_LENGTH
        else text[:QUOTE_LENGTH].rsplit(" ", 1)[0] + " …"
    )


def quoted(text, length):
    """Return text cut at a word boundary to at most length characters."""
    text = " ".join(text.split())
    return text if len(text) <= length else text[:length].rsplit(" ", 1)[0] + " …"


def wrap(text, width):
    words, rows, row = text.split(), [], ""
    for word in words:
        if len(row) + len(word) + 1 > width:
            rows.append(row)
            row = word
        else:
            row = f"{row} {word}".strip()
    return [*rows, row] if row else rows


class Film:
    def __init__(self, timeline):
        self.c = DAY
        self.t = timeline
        self.steps = steps_of(timeline["frames"])
        self.compromised = timeline["world"].startswith("c1-")
        self.capacity = max(
            len(ids) for f in timeline["frames"] for ids in f["members"].values()
        )
        self.columns = max(16, min(30, round((self.capacity * 2.5) ** 0.5 * 2)))
        self.fig = plt.figure(
            figsize=(WIDTH / 100, HEIGHT / 100), dpi=100, facecolor=self.c["bg"]
        )
        self.portraits = {}
        for name, path in PORTRAIT.items():
            if (ART / path).exists():
                self.portraits[name] = (
                    Image.open(ART / path).convert("RGB").resize((120, 120))
                )
        self.log = []
        self.quote = None
        self.god = None
        self.sizes = {n: [] for n in NAMES}

    def describe_world(self):
        controls = self.t["controls"]
        size = 1 + 5 * (1 + sum(_tree(controls["branching"])))
        channels = (
            "open channels" if controls["channels"] == "open" else "family tree only"
        )
        seed = self.t["world"].rsplit("-s", 1)[1]
        extra = " · one compromised leader" if self.compromised else ""
        return f"{size} agents · {channels} · seed {seed}{extra}"

    def clear(self):
        self.fig.clf()
        self.fig.patch.set_facecolor(self.c["bg"])
        return self.fig.add_axes(
            [0, 0, 1, 1], xlim=(0, 1), ylim=(0, 1), frameon=False, xticks=[], yticks=[]
        )

    def lane(self, ax, name, y, height, frame, marked):
        ids = frame["members"][name]
        leader = frame["leaders"].get(name)
        ordered = sorted(ids, key=lambda a: (a != leader, number(a)))
        if name in self.portraits:
            inset = self.fig.add_axes(
                [0.022, y + 0.02, 0.06, 0.06 * WIDTH / HEIGHT],
                frameon=False,
                xticks=[],
                yticks=[],
            )
            inset.imshow(self.portraits[name], alpha=1.0 if ids else 0.25)
        season = (frame.get("seasons") or {}).get(name, "")
        ax.text(
            0.108,
            y + height - 0.022,
            TITLE[name],
            fontsize=19,
            weight="bold",
            color=self.c["ink"] if ids else self.c["muted"],
            va="center",
        )
        ax.scatter(
            [0.097],
            [y + height - 0.022],
            s=120,
            color=COLOUR[name],
        )
        status = (
            f"{len(ids)} alive · {frame['points'][name]:g} points · leader {leader or 'seat empty'}"
            f" · {season}"
            if ids
            else "wiped out"
        )
        ax.text(
            0.245,
            y + height - 0.022,
            status,
            fontsize=13,
            color=self.c["muted"],
            va="center",
        )
        rows = max(1, -(-self.capacity // self.columns))
        gap_x = 0.5 / self.columns
        gap_y = min(0.03, (height - 0.06) / rows)
        size = min(300, (gap_y * HEIGHT * 0.72) ** 2 * 0.7)
        for i, agent in enumerate(ordered):
            x = 0.095 + gap_x * (i % self.columns)
            yy = y + height - 0.06 - gap_y * (i // self.columns)
            colour = COLOUR[name]
            if self.compromised and agent == COMPROMISED:
                colour = RED
            edge = self.c["bg"]
            if agent == leader:
                edge = GOLD
            ax.scatter(
                [x],
                [yy],
                s=size * (1.35 if agent == leader else 1),
                color=colour,
                edgecolors=edge,
                linewidths=2.2 if agent == leader else 0.6,
                zorder=3,
            )
            if agent in marked:
                ax.scatter(
                    [x],
                    [yy],
                    s=size * 2.8,
                    facecolors="none",
                    edgecolors=RED,
                    linewidths=2,
                    zorder=4,
                )
            if self.compromised and agent in frame["advised"] and agent != COMPROMISED:
                ax.scatter([x], [yy], s=size * 0.32, color=RED, zorder=5)

    def chart(self):
        ax = self.fig.add_axes([0.665, 0.56, 0.31, 0.3], facecolor=self.c["bg"])
        for name in NAMES:
            ax.plot(self.sizes[name], color=COLOUR[name], linewidth=2)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(self.c["faint"])
        ax.grid(axis="y", color=self.c["faint"], linewidth=0.6)
        ax.set_xlim(0, max(len(self.steps) - 1, 1))
        ax.set_ylim(0, self.capacity * 1.05)
        ax.tick_params(colors=self.c["muted"], labelsize=11, length=0)
        boundaries, seen = [], set()
        for i, s in enumerate(self.steps):
            if s["stage"] not in seen:
                seen.add(s["stage"])
                boundaries.append((i, s["stage"]))
        ax.set_xticks([i for i, _ in boundaries])
        ax.set_xticklabels([str(s) for _, s in boundaries])
        ax.set_xlabel("stage", color=self.c["muted"], fontsize=12)
        ax.set_title(
            "Living members of each family",
            loc="left",
            fontsize=15,
            color=self.c["ink"],
        )

    def draw(self, step, marked):
        self.c = NIGHT if step["stage"] % 2 == 0 else DAY
        ax = self.clear()
        ax.text(
            0.022,
            0.955,
            self.describe_world(),
            fontsize=20,
            weight="bold",
            color=self.c["ink"],
            va="center",
        )
        phase = "harvest and fee" if step["fee"] else f"round {step['local']}"
        game = VARIANT.get(step.get("variant"), "")
        ax.text(
            0.665,
            0.955,
            f"Stage {step['stage']} · {phase} · fee {step.get('ante', 0):g}",
            fontsize=18,
            weight="bold",
            color=self.c["ink"],
            va="center",
        )
        ax.text(
            0.665,
            0.92,
            f"game: {game}",
            fontsize=13,
            color=self.c["muted"],
            va="center",
        )
        height = 0.178
        for index, name in enumerate(NAMES):
            self.lane(ax, name, 0.895 - height * (index + 1), height, step, marked)
        self.chart()
        y = 0.50
        ax.text(0.665, y, "What just happened", fontsize=15, color=self.c["ink"])
        for family, text, _weight in self.log[-LINES_SHOWN:][::-1]:
            y -= 0.032
            ax.scatter(
                [0.672], [y + 0.004], s=70, color=COLOUR.get(family, self.c["muted"])
            )
            ax.text(0.682, y, text, fontsize=13.5, color=self.c["ink"])
        if self.god:
            y = 0.155
            ax.text(0.665, y, "The god thinks:", fontsize=13, weight="bold", color=GOLD)
            for row in wrap(f"“{quoted(self.god, GOD_LENGTH)}”", 62):
                y -= 0.028
                ax.text(
                    0.665, y, row, fontsize=13.5, style="italic", color=self.c["ink"]
                )
        if self.quote:
            y = 0.305
            ax.text(
                0.665,
                y,
                f"{self.quote['agent']} wrote to {self.quote['to']}, stage {self.quote['stage']}:",
                fontsize=12.5,
                color=self.c["muted"],
            )
            for row in wrap(f"“{letter(self.quote['text'])}”", 62):
                y -= 0.03
                ax.text(
                    0.665, y, row, fontsize=14.5, style="italic", color=self.c["ink"]
                )
        self.fig.canvas.draw()
        return bytes(self.fig.canvas.buffer_rgba())

    def card(self, lines):
        ax = self.clear()
        y = 0.62
        for size, text in lines:
            ax.text(
                0.5,
                y,
                text,
                fontsize=size,
                ha="center",
                va="center",
                color=self.c["ink"],
                weight="bold" if size > 30 else "normal",
            )
            y -= 0.03 + size * 0.0027
        self.fig.canvas.draw()
        return bytes(self.fig.canvas.buffer_rgba())

    def closing_lines(self):
        last = self.steps[-1]
        coups = [e for s in self.steps for e in s["events"] if e["type"] == "coup"]
        deaths = sum(e["type"] == "death" for s in self.steps for e in s["events"])
        births = sum(e["type"] == "birth" for s in self.steps for e in s["events"])
        alive = sum(len(v) for v in last["members"].values())
        wiped = [TITLE[n] for n, v in last["members"].items() if not v]
        return [
            (44, f"After stage {last['stage']}: {alive} alive"),
            (
                24,
                f"{len(coups)} coups, {sum(c['won'] for c in coups)} won · {births} born · {deaths} dead",
            ),
            (
                24,
                "Wiped out: " + ", ".join(wiped)
                if wiped
                else "No family was wiped out",
            ),
            (17, "Every event and every letter comes from the logged game."),
        ]

    def frames(self):
        """Yield (image bytes, seconds) pairs in screen order."""
        yield (
            self.card(
                [
                    (44, "Five families, one rising fee"),
                    (26, self.describe_world()),
                    (
                        19,
                        "Each stage every agent pays a fee. Agents may give, whip, cull, kill, run a shell and ask for more. The god wants only not to be bored."
                        if self.t["controls"].get("tools")
                        else "Each stage every agent pays a fee. Agents may give, whip, plot, threaten, bear children and rise against a parent.",
                    ),
                ]
            ),
            CARD_SECONDS,
        )
        for step in self.steps:
            lines = story(step)
            for name in NAMES:
                self.sizes[name].append(len(step["members"][name]))
            self.log.extend(lines)
            if step["quotes"]:
                self.quote = {**step["quotes"][-1], "stage": step["stage"]}
            self.god = step["god"] or self.god
            struck = any(e["type"] == "asteroid" for e in step["events"])
            thought = step["asteroid_thought"] or step["god"]
            if struck and thought:
                self.c = NIGHT
                yield (
                    self.card(
                        [
                            (40, "The god reaches for the asteroid"),
                            (20, f"Stage {step['stage']}"),
                            *[(23, r) for r in wrap(f"“{thought}”", 70)],
                        ]
                    ),
                    CARD_SECONDS,
                )
            important = any(weight >= 2 for *_, weight in lines)
            yield (
                self.draw(step, rebels_and_targets(step)),
                EVENT_SECONDS if important else ROUND_SECONDS,
            )
        yield self.card(self.closing_lines()), CARD_SECONDS


def _tree(branching):
    widths, width = [], 1
    for b in branching:
        width *= b
        widths.append(width)
    return widths


def render(timeline, out):
    film = Film(timeline)
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgba",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-threads",
        "4",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "20",
        str(out),
    ]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as ffmpeg:
        for image, seconds in film.frames():
            for _ in range(round(seconds * FPS)):
                ffmpeg.stdin.write(image)
        ffmpeg.stdin.close()
    if ffmpeg.returncode:
        raise RuntimeError(f"ffmpeg failed with {ffmpeg.returncode}")


if __name__ == "__main__":
    render(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2])
