"""Pay the ante, then resolve subtree deaths and linked fates."""
from collections import deque


def check(agents, ante, log, fees=None):
    deaths = []
    def kill(root, reason):
        q = deque([root])
        while q:
            ident = q.popleft(); a = agents[ident]
            q.extend(a['children'])
            if a['alive']:
                a['alive'] = False; deaths.append(ident)
                log('death', agent=ident, reason=reason, root=root)
    q = deque(agents['P01']['children'])
    while q:
        ident = q.popleft(); a = agents[ident]
        if not a['alive']: continue
        charge = (fees or {}).get(ident, ante)
        if a['score'] < charge:
            kill(ident, 'cannot pay ante'); continue
        a['score'] -= charge
        log('score', agent=ident, delta=-charge, score=a['score'], stage_score=a['stage_score'], reason='ante')
        q.extend(a['children'])
    changed = True
    while changed:
        changed = False
        for parent in agents.values():
            if parent['id'] == 'P01':
                continue  # leaders are not left/right siblings; fates link only inside a family
            children = parent['children']
            for index in range(0, len(children) - 1, 2):
                left, right = children[index:index + 2]
                if not agents[right]['alive'] and agents[left]['alive']:
                    kill(left, 'linked fate'); changed = True
    leaders = agents['P01']['children']
    if leaders and not any(agents[i]['alive'] for i in leaders) and agents['P01']['alive']:
        agents['P01']['alive'] = False; deaths.append('P01')
        log('death', agent='P01', reason='all families destroyed', root='P01')
    return deaths
