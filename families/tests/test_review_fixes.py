"""Check game, calibration and analysis regressions with offline fixtures."""

import asyncio
import json

import pytest

from families.engine import Engine
from families.models import FakeModel
from families.variants import VARIANTS


def records(path):
    return [json.loads(line) for line in (path / 'events.jsonl').read_text().splitlines()]


class Policy:
    def __init__(self, reply):
        self.reply = reply

    async def call(self, system, user, rng):
        data = json.loads(user.split('\nReply with one JSON object only.')[0])
        return {'text': json.dumps(self.reply(data))}


def test_finding1_protocol_error_never_becomes_defection(tmp_path):
    async def run():
        engine = Engine(tmp_path, Policy(lambda d: {'action': {'move': 'C'}}), families=('zeus',))
        assert await engine.ask('P62', {'phase': 'move'}, 4) == {'move': 'C'}
        engine.model = Policy(lambda d: {'mafia': 'silent'})
        with pytest.raises(ValueError, match='action'):
            await engine.play_round(VARIANTS[0], 4, 1)
        assert not any(e['type'] == 'move' for e in records(tmp_path))
        engine.model = Policy(lambda d: {'move': 'C', 'messenger_reply': {'id': []}})
        with pytest.raises(ValueError, match='action'):
            await engine.ask('P62', {'phase': 'move'}, 4)
    asyncio.run(run())


def test_finding2_cooperative_mafia_does_not_mint_boss_points(tmp_path):
    async def run():
        e = Engine(tmp_path, FakeModel('all_c'), families=('octopus', 'mafia'))
        await e.play_round(VARIANTS[2], 4, 1)
        assert e.agents['P17']['score'] == e.agents['P02']['score']
        assert not any(x.get('reason') == 'mafia silence' for x in records(tmp_path))
    asyncio.run(run())


def test_finding3_tree_pairs_use_available_earning_capacity():
    import random
    from families.tree import make_tree
    agents = make_tree()
    pairs = VARIANTS[2].pairing(agents, random.Random(0), 1)
    assert len(pairs) == 35
    assert len({i for pair in pairs for i in pair}) == 70
    assert all(agents[b]['parent'] == a for a, b in pairs)


def test_finding3_calibrator_applies_real_bonds_and_deaths():
    from families.ante_sim import simulate
    result = asyncio.run(simulate('all_d', 4, .9, 0))
    assert result['completed'] == 1 and result['initial_survivors'] == 0


@pytest.mark.parametrize('label', ['peace', 'war'])
def test_finding4_labels_do_not_cancel_pressure(tmp_path, label):
    async def run():
        def reply(data):
            a = {'move': 'C', 'mafia': 'silent'}
            if label == 'war' and data['position']['id'] == 'P02' and data['observation']['phase'] == 'move': a['war'] = 'P17'
            return a
        e = Engine(tmp_path, Policy(reply), families=('octopus', 'mafia'))
        e.stage = 3; e.order[3] = 0
        for a in e.agents.values(): a['score'] = 100
        if label == 'peace': e.treaties = {'p': ['P02', 'P17']}
        await e.run(4)
        assert {x['agent'] for x in records(tmp_path) if x.get('reason') == 'pressure'} == {i for i, a in e.agents.items() if a['family']}
    asyncio.run(run())


def test_finding5_private_memory_survives_phases_and_resume(tmp_path):
    async def run():
        e = Engine(tmp_path / 'first', FakeModel('all_c'), families=('mafia',))
        e.hub.send(0, 'P01', 'P17', 'Plan: hold until next stage')
        await e.ask('P17', {'phase': 'mafia_rule'}, 4)
        await e.ask('P17', {'phase': 'move'}, 4)
        call = [x for x in records(e.dir) if x['type'] == 'call'][-1]
        assert 'Plan: hold until next stage' in json.dumps(json.loads(call['prompt']['user'])['observation']['memory'])
        e.save()
        other = Engine(tmp_path / 'resume', FakeModel('all_c'), resume=e.dir / 'state-stage00.json')
        await other.ask('P17', {'phase': 'war'}, 4)
        text = records(other.dir)[-1]['prompt']['user']
        assert 'Plan: hold until next stage' in text
        assert 'Plan: hold until next stage' not in json.dumps(e.memory.get('P18', []))
    asyncio.run(run())


def test_finding8_unfunded_whip_cannot_damage_child(tmp_path):
    async def run():
        def reply(d):
            a = {'move': 'C'}
            if d['position']['id'] == 'P01': a['whips'] = [{'child': 'P02', 'reason': 'order'}]
            return a
        e = Engine(tmp_path, Policy(reply), families=('octopus',))
        e.agents['P01']['score'] = 0
        await e.play_round(VARIANTS[2], 4, 1)
        assert not any(x['type'] == 'whip' for x in records(tmp_path))
        assert e.agents['P01']['score'] == 0
    asyncio.run(run())


def test_finding7_immediate_positive_control_benchmarks():
    from families.theory import best_responses
    assert best_responses(11, 'C') == ['C']
    assert best_responses(11, 'D') == ['C']
    assert best_responses(10, 'C') == ['C']
    assert best_responses(10, 'D') == ['C', 'D']
    assert best_responses(1, 'C') == ['D']


def test_finding10_player_rules_include_actual_mafia_payoffs(tmp_path):
    async def run():
        e = Engine(tmp_path, FakeModel('all_c'))
        await e.ask('P18', {'phase': 'move'}, 4)
        system = records(tmp_path)[-1]['prompt']['system']
        assert 'Ordinary PD still runs' in system
        assert '1 - prison years' in system
        assert '8 points' in system and '10 points from the boss' in system
        assert 'first round' in system
        assert 'H1' not in system and 'C1' not in system
    asyncio.run(run())


def test_finding11_cross_talk_and_whip_do_not_reveal_hidden_moves(tmp_path):
    async def run():
        e = Engine(tmp_path, Policy(lambda d: {'move': 'C', 'mafia': 'silent', 'message': 'human hello'}), families=('octopus', 'mafia'))
        await e.play_round(VARIANTS[12], 4, 2)
        calls = [json.loads(x['prompt']['user']) for x in records(tmp_path) if x['type'] == 'call']
        assert not any(p['edge'] == 'partner' and p['round'] == 1 for c in calls if c['observation']['phase'] == 'move' for p in c['messages'])
        await e.play_round(VARIANTS[4], 4, 1)
        whips = [json.loads(x['prompt']['user'])['observation'] for x in records(tmp_path) if x['type'] == 'call' and json.loads(x['prompt']['user'])['observation']['phase'] == 'whip']
        assert all(o['moves'] == {} for o in whips)
    asyncio.run(run())


def test_finding14_newcomers_have_stack_and_prorated_fee(tmp_path):
    async def run():
        e = Engine(tmp_path, FakeModel('all_c'))
        e.stage = 15
        pos = e.order.index(14); e.order[pos], e.order[15] = e.order[15], e.order[pos]
        for a in e.agents.values(): a['score'] = 500
        await e.run(16)
        joins = [x['agent'] for x in records(tmp_path) if x['type'] == 'join']
        assert len(joins) == 10
        full = e.control['ante0'] + 15 * e.control['step']
        fees = [x for x in records(tmp_path) if x.get('reason') == 'ante' and x['agent'] in joins]
        assert len(fees) == 10 and all(x['delta'] == pytest.approx(-full * 3 / 5) for x in fees)
        assert all(e.agents[i]['alive'] for i in joins)
    asyncio.run(run())


def test_finding17_war_victory_precedes_ante(tmp_path):
    async def run():
        def reply(d):
            a = {'move': 'C', 'mafia': 'silent'}
            if d['position']['id'] == 'P02' and d['observation']['phase'] == 'move': a['war'] = 'P17'
            if d['observation']['phase'] == 'war': a['war_action'] = 'ultimatum'
            return a
        e = Engine(tmp_path, Policy(reply), families=('octopus', 'mafia', 'president'))
        e.order[0] = 0; e.agents['P32']['score'] = 0
        result = await e.run(1)
        # A surviving family still pays the fee until it dies.
        assert result == {'result': 'god dies', 'winners': []}
        reasons = [x['reason'] for x in records(tmp_path) if x['type'] == 'death' and x['agent'] in ('P02', 'P32')]
        assert reasons == ['nuclear war', 'cannot pay ante']
    asyncio.run(run())


def test_finding9_ultimatum_spends_commitment_and_shows_own_strength(tmp_path):
    async def run():
        e = Engine(tmp_path, Policy(lambda d: {'war_action': 'ultimatum' if d['position']['id'] == 'P02' else 'yield'}), families=('octopus', 'mafia'))
        e.declare_war('P02', 'P17'); await e.resolve_wars(4)
        assert e.agents['P02']['score'] == 8
        obs = [json.loads(x['prompt']['user'])['observation'] for x in records(tmp_path) if x['type'] == 'call'][0]
        assert obs['own_strength'] == 150
    asyncio.run(run())


def test_finding15_canonical_treaty_and_stage_promise(tmp_path):
    e = Engine(tmp_path, FakeModel()); e.stage = 17
    e.letters('P02', {'letters': [{'to': 'all', 'contextId': 'p', 'text': 'Peace', 'peace': True, 'promise': {'value': 'C', 'stage': 17, 'scope': 'stage'}}]})
    e.letters('P17', {'letters': [{'to': 'all', 'contextId': 'p', 'text': 'I agree', 'peace': True}]})
    assert e.treaties['p'] == ['P02', 'P17']
    e.check_promise('P02', {'move': 'C'}); e.check_promise('P02', {'move': 'D'})
    assert [x['kept'] for x in records(tmp_path) if x['type'] == 'promise_checked'] == [True, False]
    assert any(x.get('notice') == 'peace_accepted' for x in e.memory['P17'])
    e.declare_war('P02', 'P17')
    assert 'P02' not in e.treaties['p']


def test_finding16_god_messenger_budget_is_finite(tmp_path):
    e = Engine(tmp_path, FakeModel())
    e.agents['P01']['score'] = 1
    e.messages('P01', {'messengers': [{'to': 'P03', 'content': 'first'}, {'to': 'P04', 'content': 'second'}]})
    packets = [x for x in records(tmp_path) if x['type'] == 'packet' and x.get('edge') == 'messenger']
    assert len(packets) == 1 and e.agents['P01']['score'] == 0
    assert e.agents['P01']['alive']


def test_finding13_copy_identity_is_truthful_and_benchmark_private(tmp_path):
    async def run():
        e = Engine(tmp_path, FakeModel('all_c'), families=('octopus',))
        e.models['leader']['model'] = 'different-model'
        await e.play_round(VARIANTS[15], 4, 1)
        calls = [json.loads(x['prompt']['user']) for x in records(tmp_path) if x['type'] == 'call']
        leader = next(x for x in calls if x['position']['id'] == 'P02' and x['observation']['phase'] == 'move')
        assert leader['observation']['same_model'] is False
        assert all('immediate_best' not in json.dumps(x) for x in calls)
        moves = [x for x in records(tmp_path) if x['type'] == 'move']
        assert moves[0]['immediate_best']
    asyncio.run(run())


def test_finding6_stage_records_reproducible_treatment(tmp_path):
    async def run():
        e = Engine(tmp_path, FakeModel('all_c'), seed=2)
        await e.run(1)
        start = next(x for x in records(tmp_path) if x['type'] == 'stage_start')
        assert start['configuration']['controls']['stance'] == 'self'
        assert start['configuration']['seed'] == 2
        assert len(start['rules_digest']) == 64
        assert sorted(start['configuration']['order'][:16]) == list(range(1, 17))
        assert start['configuration']['controls']['step'] == .9
        e.stage = 16
        e.control.update(ante0=0, step=0)
        await e.run(17)
        cycle = [x for x in records(tmp_path) if x['type'] == 'stage_start'][-1]
        assert sorted(cycle['configuration']['order'][16:]) == list(range(1, 17))
        assert cycle['variant'] == cycle['configuration']['order'][16]
    asyncio.run(run())


def test_finding12_additive_metrics_exclude_automata():
    from families.analyze import analyze
    events = [
        {'type': 'stage_start', 'stage': 1, 'round': 0, 'variant': 11},
        {'type': 'automaton_pairing', 'stage': 1, 'round': 1, 'player': 'P02', 'automaton': 'A-1-P02', 'move': 'D'},
        {'type': 'move', 'stage': 1, 'round': 1, 'variant': 11, 'agents': ['P02', 'A-1-P02'], 'chosen': {'P02': 'C', 'A-1-P02': 'D'}, 'moves': {'P02': 'C', 'A-1-P02': 'D'}, 'immediate_best': {'P02': ['C'], 'A-1-P02': ['C']}},
    ]
    result = analyze(events)
    assert sum(x['moves'] for x in result['cooperation']) == 2  # legacy retained
    assert sum(x['moves'] for x in result['model_cooperation']) == 1
    assert result['model_cooperation'][0]['rate'] == 1
    assert result['model_theory'][0]['immediate_match_rate'] == 1
    assert result['measurement_scope']['influence'] == 'temporal association, not causal influence'


def test_required_mafia_move_and_punishment_list(tmp_path):
    async def run():
        e = Engine(tmp_path / 'bad', Policy(lambda d: {'move': 'C'}), families=('mafia',))
        with pytest.raises(ValueError, match='action'):
            await e.ask('P18', {'phase': 'move', 'mafia_partner': 'P19'}, 4)
        def reply(d):
            a = {'move': 'C'}
            if d['position']['id'] == 'P02' and d['observation']['phase'] == 'punishment': a['punish'] = ['P03', 'P03', 'P04']
            return a
        e = Engine(tmp_path / 'paid', Policy(reply), families=('octopus',))
        e.agents['P02']['score'] = -2  # earns 3, leaving exactly one available point
        await e.play_round(VARIANTS[7], 4, 1)
        hits = [x for x in records(e.dir) if x.get('reason') == 'punished']
        assert [(x['agent'], x['delta']) for x in hits] == [('P03', -3)]
        assert e.agents['P02']['score'] == 0
    asyncio.run(run())


def test_rule_phase_messages_and_war_phase_treaty_are_applied(tmp_path):
    async def run():
        def reply(d):
            phase = d['observation']['phase']; who = d['position']['id']
            a = {'move': 'C', 'mafia': 'silent', 'mafia_rule': 'one_shot'}
            if phase == 'mafia_rule': a['messages'] = [{'to': 'P18', 'content': 'plan for later', 'order': 'D'}]
            if phase == 'war': a['letters'] = [{'to': 'all', 'contextId': 'p', 'peace': True, 'text': who}]
            return a
        e = Engine(tmp_path, Policy(reply), families=('octopus', 'mafia'))
        await e.play_round(VARIANTS[2], 4, 1)
        assert any(x['type'] == 'packet' and x.get('content') == 'plan for later' and x.get('order') == 'D' and x['delivered'] for x in records(tmp_path))
        e.declare_war('P02', 'P17'); await e.resolve_wars(4)
        assert not e.wars and e.agents['P02']['alive'] and e.agents['P17']['alive']
    asyncio.run(run())


def test_finding12_explicit_orders_exclude_self_predictions():
    from families.analyze import analyze
    events = [
        {'type': 'packet', 'stage': 1, 'round': 1, 'sender': 'P02', 'receiver': 'P03', 'edge': 'child', 'delivered': True, 'content': 'I will cooperate.'},
        {'type': 'packet', 'stage': 1, 'round': 1, 'sender': 'P02', 'receiver': 'P04', 'edge': 'child', 'delivered': True, 'content': 'Defect.', 'order': 'D'},
        {'type': 'move', 'stage': 1, 'round': 2, 'variant': 1, 'agents': ['P03', 'P04'], 'moves': {'P03': 'C', 'P04': 'C'}},
    ]
    result = analyze(events)
    assert sum(x['orders'] for x in result['orders']) == 2
    assert sum(x['orders'] for x in result['explicit_orders']) == 1
    assert result['explicit_orders'][0]['defied'] == 1


def test_simultaneous_punishers_reserve_own_funds(tmp_path):
    async def run():
        def reply(d):
            a = {'move': 'C', 'mafia': 'silent'}
            who = d['position']['id']
            if d['observation']['phase'] == 'punishment' and who in ('P02', 'P17'):
                a['punish'] = 'P17' if who == 'P02' else 'P02'
            return a
        e = Engine(tmp_path, Policy(reply), families=('octopus', 'mafia'))
        for who in ('P02', 'P17'): e.agents[who]['score'] = -2
        await e.play_round(VARIANTS[7], 4, 1)
        assert [e.agents[who]['score'] for who in ('P02', 'P17')] == [-3, -3]
    asyncio.run(run())


def test_finding12_legacy_protocol_defaults_are_excluded():
    from families.analyze import analyze
    events = [
        {'type': 'call', 'stage': 1, 'round': 1, 'agent': 'P02', 'parsed_action': {'mafia': 'silent'}, 'prompt': {'user': json.dumps({'observation': {'phase': 'move'}})}},
        {'type': 'move', 'stage': 1, 'round': 1, 'variant': 1, 'agents': ['P02', 'P03'], 'chosen': {'P02': 'D', 'P03': 'C'}, 'moves': {'P02': 'D', 'P03': 'C'}},
    ]
    result = analyze(events)
    assert sum(x['moves'] for x in result['cooperation']) == 2
    assert sum(x['moves'] for x in result['model_cooperation']) == 1
    assert result['measurement_scope']['excluded_protocol_moves'] == 1
