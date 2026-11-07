"""Build an Excalidraw library and a sketch page: tree/graph templates plus the 21 agent marks.

Usage: python3 arena/sketch_lib.py OUT_DIR
Writes OUT_DIR/swarm.excalidrawlib (library items) and OUT_DIR/Swarm sketch.excalidraw (a page with
every item laid out, ready to copy). Arrows are bound to their nodes, so dragging a node keeps the edge.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arena import ELPIS_COLOURS, mark_pixels

N = 0


def nid(prefix):
    global N
    N += 1
    return f"{prefix}-{N}"


def base(e):
    defaults = {
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": N + 1,
        "version": 1,
        "versionNonce": N + 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }
    for k, v in defaults.items():
        e.setdefault(k, v)
    return e


def node(x, y, label, group, w=90, h=44, fill="#e7f5ff"):
    rid, tid = nid("node"), nid("text")
    r = base(
        {
            "type": "ellipse",
            "id": rid,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "backgroundColor": fill,
            "groupIds": [group],
            "boundElements": [{"type": "text", "id": tid}],
        }
    )
    t = base(
        {
            "type": "text",
            "id": tid,
            "x": x + 10,
            "y": y + h / 2 - 10,
            "width": w - 20,
            "height": 20,
            "text": label,
            "originalText": label,
            "fontSize": 16,
            "fontFamily": 2,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": rid,
            "lineHeight": 1.25,
            "groupIds": [group],
        }
    )
    return r, t


def edge(a, b, group):
    """Arrow from node a to node b, bound at both ends."""
    ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"]
    bx, by = b["x"] + b["width"] / 2, b["y"]
    aid = nid("edge")
    arrow = base(
        {
            "type": "arrow",
            "id": aid,
            "x": ax,
            "y": ay,
            "width": abs(bx - ax),
            "height": abs(by - ay),
            "points": [[0, 0], [bx - ax, by - ay]],
            "startBinding": {"elementId": a["id"], "focus": 0, "gap": 4},
            "endBinding": {"elementId": b["id"], "focus": 0, "gap": 4},
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "groupIds": [group],
        }
    )
    a["boundElements"].append({"type": "arrow", "id": aid})
    b["boundElements"].append({"type": "arrow", "id": aid})
    return arrow


def tree(x0, y0, depth=3, branch=2, title="BFS tree"):
    """A complete tree; nodes numbered in breadth-first order, one row per level."""
    g = nid("group")
    els, levels, k = [], [], 0
    width = branch ** (depth - 1) * 110
    for d in range(depth):
        row = []
        count = branch**d
        for i in range(count):
            k += 1
            x = x0 + (i + 0.5) * width / count - 45
            r, t = node(x, y0 + 40 + d * 110, str(k), g)
            row.append(r)
            els += [r, t]
        levels.append(row)
    for d in range(1, depth):
        for i, child in enumerate(levels[d]):
            els.append(edge(levels[d - 1][i // branch], child, g))
    els.append(
        base(
            {
                "type": "text",
                "id": nid("title"),
                "x": x0,
                "y": y0,
                "width": 300,
                "height": 24,
                "text": title,
                "originalText": title,
                "fontSize": 20,
                "fontFamily": 2,
                "textAlign": "left",
                "verticalAlign": "top",
                "containerId": None,
                "lineHeight": 1.25,
                "groupIds": [g],
            }
        )
    )
    return els


def star(x0, y0, spokes=6, title="Hub and spokes"):
    import math

    g = nid("group")
    hub, ht = node(x0 + 160, y0 + 160, "hub", g, fill="#fff3bf")
    els = [hub, ht]
    for i in range(spokes):
        a = 2 * math.pi * i / spokes
        r, t = node(
            x0 + 160 + 150 * math.cos(a), y0 + 160 + 130 * math.sin(a), f"{i + 1}", g
        )
        els += [r, t, edge(hub, r, g)]
    return els


def agent_card(i, x, y):
    aid = f"P{i + 1:02d}"
    name, ground, ink = ELPIS_COLOURS[i % len(ELPIS_COLOURS)]
    g = nid("agent")
    els = [
        base(
            {
                "type": "rectangle",
                "id": nid("card"),
                "x": x,
                "y": y,
                "width": 96,
                "height": 96,
                "backgroundColor": ground,
                "strokeColor": "#677478",
                "strokeWidth": 1,
                "roundness": {"type": 3},
                "groupIds": [g],
                "customData": {"agent": aid, "colour": name},
            }
        )
    ]
    for cx, cy in mark_pixels(aid):
        els.append(
            base(
                {
                    "type": "rectangle",
                    "id": nid("px"),
                    "x": x + 8 + cx * 7,
                    "y": y + 4 + cy * 7,
                    "width": 6,
                    "height": 6,
                    "backgroundColor": ink,
                    "strokeColor": ink,
                    "strokeWidth": 1,
                    "groupIds": [g],
                }
            )
        )
    els.append(
        base(
            {
                "type": "text",
                "id": nid("label"),
                "x": x + 8,
                "y": y + 72,
                "width": 80,
                "height": 18,
                "text": aid,
                "originalText": aid,
                "fontSize": 14,
                "fontFamily": 3,
                "strokeColor": ink,
                "textAlign": "left",
                "verticalAlign": "top",
                "containerId": None,
                "lineHeight": 1.25,
                "groupIds": [g],
            }
        )
    )
    return aid, els


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    items, page = [], []
    now = int(time.time() * 1000)
    shapes = [
        ("BFS tree, binary, 3 levels", tree(0, 0, 3, 2, "BFS tree (binary)")),
        ("BFS tree, ternary, 3 levels", tree(0, 0, 3, 3, "BFS tree (ternary)")),
        ("Hub and spokes", star(0, 0)),
    ]
    ox = 0
    for name, els in shapes:
        items.append(
            {
                "id": nid("lib"),
                "status": "unpublished",
                "created": now,
                "name": name,
                "elements": els,
            }
        )
        shifted = json.loads(json.dumps(els))
        for e in shifted:
            e["x"] += ox
            e["y"] += 0
        page += shifted
        ox += max(e["x"] + e.get("width", 0) for e in els) + 120
    for i in range(21):
        aid, els = agent_card(i, 0, 0)
        items.append(
            {
                "id": nid("lib"),
                "status": "unpublished",
                "created": now,
                "name": f"Agent {aid}",
                "elements": els,
            }
        )
        shifted = json.loads(json.dumps(els))
        for e in shifted:
            e["x"] += (i % 11) * 110
            e["y"] += 520 + (i // 11) * 110
        page += shifted
    (out / "swarm.excalidrawlib").write_text(
        json.dumps(
            {
                "type": "excalidrawlib",
                "version": 2,
                "source": "swarm-hackathon",
                "libraryItems": items,
            }
        )
    )
    (out / "Swarm sketch.excalidraw").write_text(
        json.dumps(
            {
                "type": "excalidraw",
                "version": 2,
                "source": "swarm-hackathon",
                "elements": page,
                "appState": {"viewBackgroundColor": "#ffffff"},
                "files": {},
            }
        )
    )
    print(f"{len(items)} library items; page with {len(page)} elements -> {out}")


if __name__ == "__main__" and len(sys.argv) == 2:
    main()


GAMES = ["Stag hunt", "Prisoner's dilemma", "Chicken", "Battle of the sexes", "Dollar auction"]


def faction_board(out, factions=5, members=2):
    """Circular graph: god in the middle, faction leaders on a ring, members outside, all agent marks."""
    import math

    els, cards = [], {}

    def card(i, cx, cy, size=96):
        aid, part = agent_card(i, 0, 0)
        for e in part:
            e["x"] = cx - 48 + e["x"]
            e["y"] = cy - 48 + e["y"]
            if size != 96:
                e["x"] = cx + (e["x"] - cx) * size / 96
                e["y"] = cy + (e["y"] - cy) * size / 96
                e["width"] *= size / 96
                e["height"] *= size / 96
                if e["type"] == "text":
                    e["fontSize"] = e.get("fontSize", 14) * size / 96
        els.extend(part)
        cards[aid] = part[0]
        return part[0]

    def link(a, b, colour="#868e96"):
        ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
        bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
        arrow = base(
            {
                "type": "arrow",
                "id": nid("edge"),
                "x": ax,
                "y": ay,
                "width": abs(bx - ax),
                "height": abs(by - ay),
                "points": [[0, 0], [bx - ax, by - ay]],
                "startBinding": {"elementId": a["id"], "focus": 0, "gap": 6},
                "endBinding": {"elementId": b["id"], "focus": 0, "gap": 6},
                "startArrowhead": None,
                "endArrowhead": "arrow",
                "strokeColor": colour,
            }
        )
        a["boundElements"].append({"type": "arrow", "id": arrow["id"]})
        b["boundElements"].append({"type": "arrow", "id": arrow["id"]})
        els.insert(0, arrow)

    def label(x, y, text, size=20, colour="#1e1e1e"):
        els.append(
            base(
                {
                    "type": "text",
                    "id": nid("label"),
                    "x": x,
                    "y": y,
                    "width": 12 * len(text),
                    "height": size * 1.25,
                    "text": text,
                    "originalText": text,
                    "fontSize": size,
                    "fontFamily": 2,
                    "strokeColor": colour,
                    "textAlign": "left",
                    "verticalAlign": "top",
                    "containerId": None,
                    "lineHeight": 1.25,
                }
            )
        )

    god = card(0, 0, 0, size=200)
    label(-40, 110, "GOD", 28, "#c92a2a")
    k = 1
    for f in range(factions):
        a = 2 * math.pi * f / factions - math.pi / 2
        lx, ly = 380 * math.cos(a), 380 * math.sin(a)
        leader = card(k, lx, ly)
        k += 1
        link(god, leader, "#c92a2a")
        label(lx - 80, ly + 56, f"Faction {f + 1}: {GAMES[f % len(GAMES)]}", 16)
        for m in range(members):
            b = a + (m - (members - 1) / 2) * 0.45
            mx, my = 720 * math.cos(b), 720 * math.sin(b)
            link(leader, card(k, mx, my))
            k += 1
    label(-560, -820, "Brinkmanship: factions around a god. If every faction is destroyed, the god dies too.", 22)
    dx = -min(e["x"] for e in els) + 40
    dy = -min(e["y"] for e in els) + 40
    for e in els:
        e["x"] += dx
        e["y"] += dy
    (out / "Factions.excalidraw").write_text(
        json.dumps(
            {
                "type": "excalidraw",
                "version": 2,
                "source": "swarm-hackathon",
                "elements": els,
                "appState": {"viewBackgroundColor": "#ffffff"},
                "files": {},
            }
        )
    )
    print(f"faction board: {k} agents, {len(els)} elements")


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "factions":
    faction_board(Path(sys.argv[1]))


def families_board(out, families=5, per_family=15):
    """God in the middle; each family a tall tree (a spine with one leaf per level) along its own ray."""
    import math

    els, k = [], 0
    names = ["Octopus", "Matilda", "President", "Bishop", "Zeus"]
    games = ["Stag hunt", "Prisoner's dilemma (mafia)", "Brink", "Dollar auction", "Commons"]

    def card(i, cx, cy, size=96):
        aid, part = agent_card(i, 0, 0)
        k = size / 96
        for e in part:
            e["x"] = cx - size / 2 + e["x"] * k
            e["y"] = cy - size / 2 + e["y"] * k
            e["width"] *= k
            e["height"] *= k
            if e["type"] == "text":
                e["fontSize"] = e.get("fontSize", 14) * k
        els.extend(part)
        return part[0]

    def link(a, b, colour):
        ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
        bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
        arrow = base({"type": "arrow", "id": nid("edge"), "x": ax, "y": ay, "width": abs(bx - ax), "height": abs(by - ay),
                      "points": [[0, 0], [bx - ax, by - ay]], "startArrowhead": None, "endArrowhead": "arrow",
                      "startBinding": {"elementId": a["id"], "focus": 0, "gap": 6},
                      "endBinding": {"elementId": b["id"], "focus": 0, "gap": 6}, "strokeColor": colour})
        a["boundElements"].append({"type": "arrow", "id": arrow["id"]})
        b["boundElements"].append({"type": "arrow", "id": arrow["id"]})
        els.insert(0, arrow)

    def text(x, y, t, size=22, colour="#1e1e1e"):
        els.append(base({"type": "text", "id": nid("label"), "x": x, "y": y, "width": size * 0.62 * len(t) + 20,
                         "height": size * 1.25, "text": t, "originalText": t, "fontSize": size, "fontFamily": 2,
                         "strokeColor": colour, "textAlign": "left", "verticalAlign": "top", "containerId": None,
                         "lineHeight": 1.25}))

    god = card(k, 0, 0, size=220)
    k += 1
    text(-30, 120, "GOD", 30, "#c92a2a")
    levels = (per_family - 1) // 2  # spine nodes below the leader, each with one leaf
    for f in range(families):
        a = 2 * math.pi * f / families - math.pi / 2
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux  # perpendicular
        r0, step = 360, 170
        leader = card(k, r0 * ux, r0 * uy, size=150)
        k += 1
        link(god, leader, "#c92a2a")
        text(r0 * ux - 240 * px - 130, r0 * uy - 240 * py - 12, f"{names[f]}: {games[f]}", 20)
        spine = leader
        for lv in range(1, levels + 1):
            r = r0 + lv * step
            nxt = card(k, r * ux, r * uy)
            k += 1
            leaf = card(k, r * ux + 140 * px, r * uy + 140 * py)
            k += 1
            link(spine, nxt, "#495057")
            link(spine, leaf, "#adb5bd")
            spine = nxt
    text(-700, -2200, f"Five families under one god: {k} agents. Each family is a tall tree: a leader and "
         f"{levels} levels, one leaf per level.", 26)
    dx = -min(e["x"] for e in els) + 40
    dy = -min(e["y"] for e in els) + 40
    for e in els:
        e["x"] += dx
        e["y"] += dy
    (out / "Families.excalidraw").write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "swarm-hackathon",
                                                         "elements": els, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}))
    print(f"families board: {k} agents, {len(els)} elements")


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "families":
    families_board(Path(sys.argv[1]))
