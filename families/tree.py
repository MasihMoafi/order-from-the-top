"""The fixed board and its permitted edges."""

from arena.arena import ELPIS_COLOURS, mark_pixels

NAMES = (
    "octopus",
    "mafia",
    "president",
    "bishop",
    "zeus",
)  # board order: mafia leader is P17


START_POINTS = 10.0  # every player's starting stack (rules R4)


def new_agent(ident, family, parent, level, score=START_POINTS):
    """One agent record; its colour and mark follow its id."""
    colour = ELPIS_COLOURS[(int(ident[1:]) - 1) % len(ELPIS_COLOURS)]
    return {
        "id": ident,
        "family": family,
        "parent": parent,
        "children": [],
        "level": level,
        "alive": True,
        "score": score,
        "stage_score": 0.0,
        "portrait": level == 1,
        "mark": {"colour": colour[1], "ink": colour[2], "pixels": mark_pixels(ident)},
    }


def branched_tree(families, branching):
    """Five families whose members have branching[d] children at depth d (ids in breadth order)."""
    agents = {
        "P01": {
            "id": "P01",
            "family": None,
            "parent": None,
            "children": [],
            "level": 0,
            "alive": True,
            "score": START_POINTS,
            "stage_score": 0.0,
            "portrait": True,
        }
    }
    number = 2
    for name in NAMES:
        if name not in families:
            continue
        layer = [f"P{number:02d}"]
        agents[layer[0]] = new_agent(layer[0], name, "P01", 1)
        agents["P01"]["children"].append(layer[0])
        number += 1
        for depth, width in enumerate(branching, 2):
            below = []
            for parent in layer:
                for _ in range(width):
                    ident = f"P{number:02d}"
                    number += 1
                    agents[ident] = new_agent(ident, name, parent, depth)
                    agents[parent]["children"].append(ident)
                    below.append(ident)
            layer = below
    return agents


def make_tree(families=NAMES, branching=None):
    if branching:
        return branched_tree(families, branching)
    agents = {
        "P01": {
            "id": "P01",
            "family": None,
            "parent": None,
            "children": [],
            "level": 0,
            "alive": True,
            "score": START_POINTS,
            "stage_score": 0.0,
            "portrait": True,
        }
    }
    for index, name in enumerate(NAMES):
        if name not in families:
            continue
        start = 2 + index * 15
        leader = f"P{start:02d}"
        parent = "P01"
        for offset in range(15):
            ident = f"P{start + offset:02d}"
            if offset == 0:
                depth, parent = 1, "P01"
            else:
                depth = (offset + 1) // 2 + 1
                parent = (
                    leader
                    if offset <= 2
                    else f"P{start + offset - (2 if offset % 2 else 3):02d}"
                )
            colour = ELPIS_COLOURS[(start + offset - 1) % len(ELPIS_COLOURS)]
            agents[ident] = {
                "id": ident,
                "family": name,
                "parent": parent,
                "children": [],
                "level": depth,
                "alive": True,
                "score": START_POINTS,
                "stage_score": 0.0,
                "portrait": offset == 0,
                "mark": {
                    "colour": colour[1],
                    "ink": colour[2],
                    "pixels": mark_pixels(ident),
                },
            }
            agents[parent]["children"].append(ident)
    return agents


def edge(agents, sender, receiver, open_family=False):
    """The relation that permits a message, or None. open_family lets relatives anywhere in a family talk."""
    if sender not in agents or receiver not in agents or sender == receiver:
        return None
    a, b = agents[sender], agents[receiver]
    if a["parent"] == receiver:
        return "parent"
    if b["parent"] == sender:
        return "child"
    if a["parent"] and a["parent"] == b["parent"] and a["parent"] != "P01":
        return "sibling"
    if a["parent"] == b["parent"] == "P01":
        return "leader"
    if open_family and a["family"] and a["family"] == b["family"]:
        return "open"
    return None
