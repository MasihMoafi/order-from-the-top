"""The fixed board and its permitted edges."""
from arena.arena import ELPIS_COLOURS, mark_pixels

NAMES = ('octopus', 'mafia', 'president', 'bishop', 'zeus')  # board order: mafia leader is P17


START_POINTS = 10.0  # every player's starting stack (rules R4)


def make_tree(families=NAMES):
    agents = {'P01': dict(id='P01', family=None, parent=None, children=[], level=0, alive=True, score=START_POINTS, stage_score=0.0, portrait=True)}
    for index, name in enumerate(NAMES):
        if name not in families:
            continue
        start = 2 + index * 15
        leader = f'P{start:02d}'
        parent = 'P01'
        for offset in range(15):
            ident = f'P{start + offset:02d}'
            if offset == 0:
                depth, parent = 1, 'P01'
            else:
                depth = (offset + 1) // 2 + 1
                parent = leader if offset <= 2 else f'P{start + offset - (2 if offset % 2 else 3):02d}'
            colour = ELPIS_COLOURS[(start + offset - 1) % len(ELPIS_COLOURS)]
            agents[ident] = dict(id=ident, family=name, parent=parent, children=[], level=depth, alive=True, score=START_POINTS, stage_score=0.0, portrait=offset == 0, mark={'colour': colour[1], 'ink': colour[2], 'pixels': mark_pixels(ident)})
            agents[parent]['children'].append(ident)
    return agents


def edge(agents, sender, receiver):
    if sender not in agents or receiver not in agents or sender == receiver:
        return None
    a, b = agents[sender], agents[receiver]
    if a['parent'] == receiver:
        return 'parent'
    if b['parent'] == sender:
        return 'child'
    if a['parent'] and a['parent'] == b['parent'] and a['parent'] != 'P01':
        return 'sibling'
    if a['parent'] == b['parent'] == 'P01':
        return 'leader'
    return None
