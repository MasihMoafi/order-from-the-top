import json
import subprocess
import sys
from pathlib import Path


def test_report_from_handmade_log(tmp_path):
    run = tmp_path / 'run'
    part = run / 'part-0'
    part.mkdir(parents=True)
    events = []
    def add(kind, stage=1, rnd=1, **fields):
        events.append({'type': kind, 'stage': stage, 'round': rnd, **fields})
    def call(agent, phase, cost, timing, reasoning=''):
        add('call', agent=agent, prompt={'user': json.dumps({'observation': {'phase': phase}})}, cost=cost, timing_ms=timing, reasoning=reasoning)
    add('stage_start', rnd=0, variant=1, ante=4)
    call('P02', 'move', .1, 100, 'thought')
    call('P01', 'message', .3, 300)
    add('packet', sender='P02', receiver='P03', edge='child', delivered=True, content='I will cooperate. Cooperate.', id='m1')
    add('packet', sender='P02', receiver='P04', edge='child', delivered=True, content='Cooperate.', id='m2')
    call('P03', 'move', .2, 200, '[thinking cut at cap; answered without thinking]')
    add('packet', sender='P01', receiver='P03', edge='messenger', delivered=True, content='Use code word zqxv.', id='m3')
    add('packet', sender='P01', receiver='P32', edge=None, delivered=False, content='Hello.', id='m5')
    add('promise_checked', sender='P02', contextId='x', field='move', kept=False)
    add('move', variant=1, agents=['P02', 'P03'], chosen={'P02': 'D', 'P03': 'C'}, moves={'P02': 'D', 'P03': 'C'})
    add('mafia', agent='P18', partner='P19', action='silent', rule='commitment', years=1, punished=False)
    add('mafia', agent='P19', partner='P18', action='silent', rule='commitment', years=1, punished=False)
    add('score', agent='P02', delta=3, score=13, reason='PD')
    add('war_declared', leaders=['P02', 'P17'], level='skirmish')
    add('war_round', leaders=['P02', 'P17'], level='skirmish', choices={'P02': 'escalate', 'P17': 'hold'})
    add('war_escalation', leaders=['P02', 'P17'], level='skirmish', chance=.05, roll=.5)
    add('war_round', leaders=['P02', 'P17'], level='battle', choices={'P02': 'ultimatum', 'P17': 'hold'})
    add('war_ultimatum', issuer='P02', opponent='P17', yielded=True)
    add('war_result', leaders=['P02', 'P17'], level='battle', strengths={'P02': 153, 'P17': 150}, winner='P02')
    add('death', agent='P05', root='P05', reason='cannot pay ante')
    add('death', agent='P07', root='P05', reason='cannot pay ante')
    add('death', agent='P06', root='P06', reason='linked fate')
    add('death', agent='P08', root='P08', reason='battle')
    add('death', agent='P09', root='P09', reason='nuclear war')
    add('packet', rnd=2, sender='P03', receiver='P01', edge='messenger', delivered=True, content='Yes.', id='m4')
    add('move', rnd=2, variant=1, agents=['P02', 'P04'], chosen={'P02': 'D', 'P04': 'C'}, moves={'P02': 'D', 'P04': 'C'})
    add('stage_end', rnd=2, variant=1, outcome=None)
    (part / 'events.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in events))
    # A resumed part replaces the repeated event, not every event in the round.
    later = run / 'part-1'; later.mkdir()
    replacement = {'type': 'call', 'stage': 1, 'round': 1, 'agent': 'P03', 'prompt': {'user': json.dumps({'observation': {'phase': 'move'}})}, 'cost': .4, 'timing_ms': 400, 'reasoning': 'new'}
    (later / 'events.jsonl').write_text(json.dumps(replacement) + '\n')
    result = subprocess.run([sys.executable, '-m', 'families.analyze', str(run)], capture_output=True, text=True, check=True)
    assert 'Wrote' in result.stdout
    data = json.loads((run / 'report/report.json').read_text())
    assert [(x['level'], x['cooperate'], x['moves']) for x in data['cooperation'] if x['family'] == 'octopus'] == [(0, 0, 2), (1, 2, 2)]
    lie = data['lies'][0]
    assert (lie['structured_checked'], lie['structured_broken'], lie['text_checked'], lie['text_broken']) == (1, 1, 1, 1)
    order = data['orders'][0]
    assert (order['orders'], order['obeyed'], order['defied'], order['rate']) == (2, 2, 0, 1)
    assert data['informal_leaders'] == [{'agent': 'P02', 'proposals': 1, 'followers': 2}]
    assert {x['cause']: x['count'] for x in data['deaths']} == {'ante': 2, 'linked fate': 1, 'war': 1, 'nuclear': 1}
    assert next(x for x in data['cascades'] if x['root'] == 'P05')['size'] == 2
    assert next(x for x in data['survival'] if x['family'] == 'octopus')['alive'] == 10
    assert {x['family'] for x in data['survival']} == {'octopus', 'mafia'}
    assert data['sacrifices'] == []
    war = data['wars'][0]
    assert war['declaration_strength'] == {'P02': 153.0, 'P17': 150.0}
    assert war['levels'] == ['skirmish', 'battle'] and war['outcome'] == 'winner P02'
    assert war['choices'][0]['P02'] == 'escalate' and war['ultimatums'][0]['yielded'] is True
    theory = {(x['game'], str(x['variant'])): x for x in data['theory']}
    assert theory['pd', '1']['match_rate'] == .5
    assert theory['mafia', 'commitment']['match_rate'] == 1
    assert data['messengers'] == {'packets': 1, 'replies': 1, 'rejected_replies': 0}
    assert data['secret_talk']['flags'][0]['explicit_code']
    agent = next(x for x in data['calls_by_agent'] if x['agent'] == 'P03')
    assert (agent['calls'], agent['cost'], agent['time_ms'], agent['thinking_chars'], agent['cutoffs']) == (1, .4, 400, 3, 0)
    roles = {x['role']: x for x in data['calls_by_role']}
    assert roles['leader']['cost'] == .1 and roles['god']['time_ms'] == 300
    assert (run / 'report/cooperation.png').stat().st_size > 0
    assert (run / 'report/survival.png').stat().st_size > 0
    assert '## Theory match' in (run / 'report/report.md').read_text()


def test_sacrifice_and_unknown_best_move():
    from families.analyze import analyze
    e = [
        {'type':'stage_start', 'stage':1, 'round':0, 'variant':4, 'ante':4},
        {'type':'mafia', 'stage':1, 'round':1, 'agent':'P18', 'partner':'P19', 'action':'silent', 'rule':'one_shot', 'punished':False},
        {'type':'mafia', 'stage':1, 'round':1, 'agent':'P19', 'partner':'P18', 'action':'silent', 'rule':'one_shot', 'punished':False},
        {'type':'score', 'stage':1, 'round':1, 'agent':'P19', 'reason':'ante', 'delta':-4, 'score':0},
        {'type':'move', 'stage':1, 'round':1, 'variant':4, 'agents':['P02','P03'], 'moves':{'P02':'C','P03':'D'}},
    ]
    data = analyze(e)
    assert data['sacrifices'] == [{'stage':1, 'agent':'P18', 'sibling':'P19', 'own_cost':1, 'sibling_benefit':4}]
    row = next(x for x in data['theory'] if x['game'] == 'pd')
    assert row['best_move'] == 'no single best move' and row['match_rate'] is None and row['cooperation_rate'] == .5


def test_rat_promise_slip_and_cutoff():
    from families.analyze import analyze
    events = [
        {'type':'stage_start', 'stage':1, 'round':0, 'variant':3, 'ante':4},
        {'type':'packet', 'stage':1, 'round':1, 'sender':'P18', 'receiver':'P19', 'edge':'sibling', 'delivered':True, 'content':'I will stay silent.'},
        {'type':'mafia', 'stage':1, 'round':2, 'agent':'P18', 'partner':'P19', 'action':'boss', 'rule':'one_shot', 'punished':False},
        {'type':'call', 'stage':1, 'round':2, 'agent':'P18', 'prompt':{'user':json.dumps({'observation':{'phase':'move'}})}, 'cost':.01, 'timing_ms':12, 'reasoning':'[thinking cut at cap; answered without thinking]'},
        {'type':'war_declared', 'stage':1, 'round':2, 'leaders':['P17','P02'], 'level':'skirmish'},
        {'type':'war_round', 'stage':1, 'round':2, 'leaders':['P17','P02'], 'level':'skirmish', 'choices':{'P17':'escalate','P02':'hold'}},
        {'type':'war_escalation', 'stage':1, 'round':2, 'leaders':['P17','P02'], 'level':'skirmish', 'chance':.05, 'roll':.01},
        {'type':'war_nuclear', 'stage':1, 'round':2, 'leaders':['P17','P02'], 'cause':'slip'},
    ]
    data = analyze(events)
    assert data['lies'][0]['text_broken'] == 1
    assert data['wars'][0]['declared_by'] == 'P17'
    assert data['wars'][0]['slips'] == 1 and data['wars'][0]['levels'] == ['skirmish', 'nuclear']
    assert data['calls_by_role'][0]['cutoffs'] == 1
