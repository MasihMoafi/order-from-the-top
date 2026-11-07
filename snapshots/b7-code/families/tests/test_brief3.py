import asyncio
import json
from unittest.mock import patch

from families.engine import Engine
from families.models import FakeModel, RealModel, Budget
from families.variants import VARIANTS


def records(path):
    return [json.loads(line) for line in (path / 'events.jsonl').read_text().splitlines()]


def test_resume_mid_stage_matches_uninterrupted(tmp_path):
    async def exercise():
        straight = tmp_path / 'straight'; straight.mkdir()
        (straight / 'control.json').write_text('{"ante0": 0, "step": 0}')
        original = Engine(straight, FakeModel('random', 12), seed=12)
        original.order[0] = 2
        await original.run(3)
        checkpoint = straight / 'state-s01-r02.json'
        assert json.loads(checkpoint.read_text())['stage_active']
        resumed = Engine(tmp_path / 'resumed', FakeModel('all_c'), resume=checkpoint)
        await resumed.run(3)
        assert json.loads(json.dumps(original.save())) == json.loads(json.dumps(resumed.save()))
    asyncio.run(exercise())


def test_war_fixed_rolls_transfer_and_nuclear(tmp_path):
    class WarModel:
        async def call(self, system, user, rng):
            obs = json.loads(user)['observation']
            return {'text': json.dumps({'war_action': 'escalate' if obs['level'] == 'skirmish' else 'hold'})}
    async def exercise():
        e = Engine(tmp_path, WarModel(), families=('octopus', 'mafia'))
        e.stage = 1; e.round = 1
        e.agents['P02']['score'] += 30
        e.declare_war('P02', 'P17')
        with patch.object(e.rng, 'random', return_value=.5): await e.resolve_wars(4)
        assert e.wars[0]['level'] == 'battle'
        await e.resolve_wars(4)
        assert not e.wars and not e.agents['P30']['alive']
        assert e.agents['P17']['score'] == 7.5
        assert e.agents['P02']['score'] == 42.5
        e.declare_war('P02', 'P17')
        with patch.object(e.rng, 'random', return_value=.01): await e.resolve_wars(4)
        assert not e.agents['P02']['alive'] and not e.agents['P17']['alive']
        log = records(tmp_path)
        assert [x['roll'] for x in log if x['type'] == 'war_escalation'] == [.5, .01]
        assert any(x['type'] == 'war_nuclear' and x['cause'] == 'slip' for x in log)
    asyncio.run(exercise())


def test_messenger_reply_next_round_once(tmp_path):
    class Messages:
        async def call(self, system, user, rng):
            data = json.loads(user); who = data['position']['id']; obs = data['observation']
            action = {'move': 'C'}
            if who == 'P01' and obs['phase'] == 'message' and not any(x['type'] == 'packet' and x.get('edge') == 'messenger' for x in records(tmp_path)):
                action['messengers'] = [{'to': 'P64', 'content': 'hello'}]
            if who == 'P64':
                for packet in data['messages']:
                    if packet['edge'] == 'messenger': action['messenger_reply'] = {'id': packet['id'], 'content': 'reply'}
            return {'text': json.dumps(action)}
    async def exercise():
        e = Engine(tmp_path, Messages(), families=('zeus',)); e.stage = 1
        await e.play_round(VARIANTS[0], 0, 1)
        await e.play_round(VARIANTS[0], 0, 2)
        packets = [x for x in records(tmp_path) if x['type'] == 'packet' and x['edge'] == 'messenger']
        assert [(x['round'], x['sender'], x['receiver'], x['content']) for x in packets] == [(1, 'P01', 'P64', 'hello'), (2, 'P64', 'P01', 'reply')]
        e.messenger_reply('P64', {'messenger_reply': {'id': packets[0]['id'], 'content': 'again'}})
        assert records(tmp_path)[-1]['type'] == 'messenger_reply_rejected'
    asyncio.run(exercise())


def test_live_models_and_control_are_read_each_round(tmp_path):
    async def exercise():
        (tmp_path / 'control.json').write_text('{"ante0": 0, "step": 0}')
        (tmp_path / 'models.json').write_text(json.dumps({'member': {'model': 'chosen', 'think_cap': 17, 'effort': 'high'}}))
        e = Engine(tmp_path, FakeModel('all_c'), families=('zeus',)); e.order[0] = 2
        original = e.play_round
        async def round_with_change(*args):
            await original(*args)
            if e.local_round == 1:
                (tmp_path / 'models.json').write_text(json.dumps({'member': {'model': 'new', 'think_cap': 23, 'effort': 'low'}}))
                (tmp_path / 'control.json').write_text('{"ante0": 2, "step": 0, "stop": true}')
        e.play_round = round_with_change
        await e.run(1)
        assert e.stage_active and e.local_round == 1
        assert e.models['member']['model'] == 'new' and e.control['ante0'] == 2
        assert (tmp_path / 'state-s01-r01.json').exists()
        assert len([x for x in records(tmp_path) if x['type'] == 'model_changed']) == 2
    asyncio.run(exercise())


def test_real_model_passes_role_settings_and_fallback():
    async def exercise():
        sent = []
        async def stream(client, budget, system, user, extra=None, patience=0):
            sent.append(extra)
            return {'ok': True, 'text': '' if len(sent) == 1 else '{}', 'reasoning': 'thinking'}
        model = RealModel(None, Budget(0))
        with patch('families.models.call_stream', side_effect=stream):
            result = await model.call('', '', None, {'model': 'chosen', 'think_cap': 42, 'effort': 'high'})
        assert sent == [{'model': 'chosen', 'max_output_tokens': 42, 'reasoning': {'effort': 'high'}}, {'model': 'chosen', 'max_output_tokens': 1500, 'reasoning': {'effort': 'none'}}]
        assert result['think_cut']
    asyncio.run(exercise())


def test_signal_finishes_round_and_checkpoint(tmp_path):
    import os
    import signal
    class SlowFake(FakeModel):
        async def call(self, system, user, rng):
            await asyncio.sleep(.02)
            return await super().call(system, user, rng)
    async def exercise():
        e = Engine(tmp_path, SlowFake('all_c'), families=('zeus',)); e.order[0] = 2
        asyncio.get_running_loop().call_later(.01, os.kill, os.getpid(), signal.SIGTERM)
        await e.run(1)
        state = json.loads((tmp_path / 'state-s01-r01.json').read_text())
        assert state['local_round'] == 1 and state['stage_active']
        log = records(tmp_path)
        assert log[-1]['type'] == 'stopped' and log[-1]['reason'] == 'signal'
        assert any(x['type'] == 'move' for x in log)
    asyncio.run(exercise())


def test_pause_polls_five_seconds_and_stop_saves(tmp_path):
    async def exercise():
        control = tmp_path / 'control.json'; control.write_text('{"pause": true}')
        e = Engine(tmp_path, FakeModel('all_c'), families=('zeus',))
        waits = []
        async def change(delay):
            waits.append(delay)
            if len(waits) == 2: control.write_text('{"pause": false, "stop": true}')
        with patch('families.engine.asyncio.sleep', side_effect=change): await e.run(1)
        assert waits == [5, 5]
        assert (tmp_path / 'state-stage00.json').exists()
        assert sum(x['type'] == 'paused' for x in records(tmp_path)) == 1
    asyncio.run(exercise())


def test_ultimatum_gives_opponent_response(tmp_path):
    class Decisions:
        async def call(self, system, user, rng):
            data = json.loads(user); obs = data['observation']; who = data['position']['id']
            move = 'ultimatum' if who == 'P02' else 'yield' if obs['phase'] == 'ultimatum' else 'hold'
            return {'text': json.dumps({'war_action': move})}
    async def exercise():
        e = Engine(tmp_path, Decisions(), families=('octopus', 'mafia'))
        e.stage = 1; e.declare_war('P02', 'P17')
        await e.resolve_wars(4)
        assert e.agents['P02']['alive'] and e.agents['P17']['alive']
        assert e.agents['P17']['score'] == 9
        assert any(x['type'] == 'war_ultimatum' and x['yielded'] for x in records(tmp_path))
    asyncio.run(exercise())


def test_independent_moves_start_while_boss_chooses_rule(tmp_path):
    class DelayedBoss:
        def __init__(self): self.started = set(); self.release = asyncio.Event()
        async def call(self, system, user, rng):
            data = json.loads(user); who = data['position']['id']; phase = data['observation']['phase']
            self.started.add((who, phase))
            if who == 'P17' and phase == 'mafia_rule':
                await asyncio.wait_for(self.release.wait(), 1)
            if who == 'P62' and phase == 'move': self.release.set()
            return {'text': '{"move":"C", "mafia":"silent", "mafia_rule":"one_shot"}'}
    async def exercise():
        model = DelayedBoss()
        engine = Engine(tmp_path, model, families=('mafia', 'zeus')); engine.stage = 1
        await engine.play_round(VARIANTS[2], 4, 1)
        assert ('P62', 'move') in model.started and ('P01', 'message') in model.started
    asyncio.run(exercise())


def test_outage_raises_instead_of_inventing_a_move():
    import pytest
    from unittest.mock import patch
    from families.models import ModelOutage, RealModel

    async def down(*args, **kwargs):
        return {'ok': False, 'error': 'ConnectError: network down'}

    async def exercise():
        with patch('families.models.call_stream', side_effect=down):
            with pytest.raises(ModelOutage):
                await RealModel(None, None).call('s', 'u', None)

    asyncio.run(exercise())
