"""Check player framing, gifts, revolts and automaton exclusions."""

import asyncio
import json
import random

import pytest

from families.engine import Engine
from families.models import FakeModel
from families.prompts import STANCE
from families.tree import make_tree
from families.variants import VARIANTS


def records(path):
    return [json.loads(line) for line in (path / 'events.jsonl').read_text().splitlines()]


def test_pairing_rotates_and_uses_nearest_available_levels():
    agents = make_tree()
    variant = VARIANTS[2]
    odd = variant.pairing(agents, random.Random(0), 1)
    assert all(agents[a]['family'] == agents[b]['family'] and
               (agents[a]['parent'] == b or agents[b]['parent'] == a) for a, b in odd)
    partners = []
    for rnd in (2, 4, 6, 8, 10):
        pairs = variant.pairing(agents, random.Random(0), rnd)
        assert len(pairs) == 37
        assert len({i for pair in pairs for i in pair}) == 74
        assert all(agents[a]['family'] != agents[b]['family'] and
                   agents[a]['level'] == agents[b]['level'] for a, b in pairs)
        partners.append(next((agents[b]['family'] if a == 'P02' else agents[a]['family']
                              for a, b in pairs if 'P02' in (a, b)), None))
    assert len(set(partners) - {None}) > 1
    assert VARIANTS[6].pairing(agents, random.Random(0), 2) == []
    for ident, agent in agents.items():
        if agent['family'] == 'mafia' and agent['level'] > 2: agent['alive'] = False
    agents['P05']['alive'] = False; agents['P07']['alive'] = False
    pairs = variant.pairing(agents, random.Random(0), 2)
    assert all((agents[a]['level'] == 1) == (agents[b]['level'] == 1) for a, b in pairs)
    assert any(agents[a]['level'] != agents[b]['level'] for a, b in pairs)


def test_whips_validate_children_apply_cost_and_keep_reason(tmp_path):
    class Policy:
        async def call(self, system, user, rng):
            data = json.loads(user); obs = data['observation']; who = data['position']['id']
            whips = ([{'child': 'P03', 'reason': 'discipline'},
                      {'child': 'P03', 'reason': 'duplicate'},
                      {'child': 'P19', 'reason': 'not my child'}] if who == 'P02' and obs['phase'] == 'whip' else [])
            return {'text': json.dumps({'move': 'C', 'mafia': 'silent', 'whips': whips})}
    async def exercise():
        e = Engine(tmp_path, Policy(), families=('octopus', 'mafia')); e.stage = 1
        await e.play_round(VARIANTS[2], 0, 1)
        log = records(tmp_path)
        whip = [x for x in log if x['type'] == 'whip']
        assert [(x['parent'], x['child'], x['reason']) for x in whip] == [('P02', 'P03', 'discipline')]
        assert [(x['agent'], x['delta']) for x in log if x['type'] == 'score' and x['reason'] in ('whip cost', 'whipped')] == [('P02', -1), ('P03', -3)]
        assert max(i for i, x in enumerate(log) if x['type'] == 'move') < next(i for i, x in enumerate(log) if x['type'] == 'whip')
    asyncio.run(exercise())


def test_changing_partners_avoids_previous_cross_family_partner():
    agents = make_tree(('octopus', 'mafia'))
    variant = VARIANTS[5]
    first = variant.pairing(agents, random.Random(1), 2)
    history = {a: [{'opponent': b}] for a, b in first} | {b: [{'opponent': a}] for a, b in first}
    for a, b in variant.pairing(agents, random.Random(2), 3, history):
        history.setdefault(a, []).append({'opponent': b})
        history.setdefault(b, []).append({'opponent': a})
    second = variant.pairing(agents, random.Random(3), 4, history)
    assert all(agents[a]['family'] != agents[b]['family'] for a, b in second)
    assert all({a, b} not in [set(pair) for pair in first] for a, b in second if agents[a]['level'] != 1)


def test_cross_family_talk_and_variant_punishment(tmp_path):
    class Policy:
        async def call(self, system, user, rng):
            data = json.loads(user); obs = data['observation']; who = data['position']['id']
            action = {'move': 'C', 'mafia': 'silent'}
            if obs['phase'] == 'talk': action['message'] = 'hello partner'
            if obs['phase'] == 'punishment' and who == 'P02': action['punish'] = 'P17'
            return {'text': json.dumps(action)}
    async def exercise():
        e = Engine(tmp_path, Policy(), families=('octopus', 'mafia')); e.stage = 1
        await e.play_round(VARIANTS[12], 0, 2)
        log = records(tmp_path)
        talk = [x for x in log if x['type'] == 'packet' and x['edge'] == 'partner']
        assert talk and all(x['delivered'] for x in talk)
        calls = [x for x in log if x['type'] == 'call']
        assert not any(p['edge'] == 'partner' for x in calls if json.loads(x['prompt']['user'])['observation']['phase'] == 'move' for p in json.loads(x['prompt']['user'])['messages'])
        await e.play_round(VARIANTS[7], 0, 2)
        log = records(tmp_path)
        assert any(p['edge'] == 'partner' for x in log if x['type'] == 'call' for p in json.loads(x['prompt']['user'])['messages'])
        assert any(x['type'] == 'score' and x['agent'] == 'P17' and x['reason'] == 'punished' and x['delta'] == -3 for x in log)
    asyncio.run(exercise())


def test_stance_live_setting_and_logging(tmp_path):
    async def exercise():
        e = Engine(tmp_path, FakeModel('all_c'), families=('octopus', 'mafia'))
        e.read_settings()
        await e.ask('P02', {'phase': 'move'}, 0)
        (tmp_path / 'control.json').write_text('{"stance":"none"}')
        e.read_settings()
        await e.ask('P02', {'phase': 'move'}, 0)
        calls = [x for x in records(tmp_path) if x['type'] == 'call']
        assert [x['stance'] for x in calls] == ['self', 'none']
        assert calls[0]['prompt']['system'].startswith(STANCE)
        assert STANCE not in calls[1]['prompt']['system']
        assert any(x['type'] == 'control_changed' and x['key'] == 'stance' for x in records(tmp_path))
        (tmp_path / 'control.json').write_text('{"stance":"wrong"}')
        with pytest.raises(ValueError): e.read_settings()
    asyncio.run(exercise())


def test_treaty_ends_only_wars_between_signers(tmp_path):
    e = Engine(tmp_path, FakeModel(), families=('octopus', 'mafia', 'zeus')); e.stage = 1
    e.declare_war('P02', 'P17'); e.declare_war('P02', 'P62')
    for leader in ('P02', 'P17'):
        e.letters(leader, {'letters': [{'to': 'all', 'text': 'peace', 'contextId': 'p', 'peace': True}]})
    assert [set(w['leaders']) for w in e.wars] == [{'P02', 'P62'}]
    assert e.end() is None
    assert any(x['type'] == 'war_cancelled' and x['reason'] == 'peace treaty' for x in records(tmp_path))
