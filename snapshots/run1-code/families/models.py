"""Real streaming adapter and reproducible offline policies."""
import hashlib
import json
import random

from game.game import Budget
from arena.arena import call_stream


PATIENCE = 1800  # seconds a call keeps retrying through an outage


class ModelOutage(RuntimeError):
    """The model API stayed unreachable for PATIENCE seconds."""


class RealModel:
    def __init__(self, client, budget, think_cap=8000):
        self.client, self.budget, self.think_cap = client, budget, think_cap

    async def call(self, system, user, rng, settings=None):
        from .prompts import HANDBOOK
        if not HANDBOOK.is_file():
            raise FileNotFoundError(f'Agent handbook is missing: {HANDBOOK}')
        # Bounded thinking: up to THINK_CAP output tokens; if the cap cuts the answer off,
        # ask once more with thinking off. Both replies' thinking is kept in the log.
        settings = settings or {'model': 'deepseek-v4-flash', 'think_cap': self.think_cap, 'effort': None}
        extra = {'model': settings['model'], 'max_output_tokens': settings['think_cap']}
        if settings.get('effort'): extra['reasoning'] = {'effort': settings['effort']}
        first = await call_stream(self.client, self.budget, system, user, extra, patience=PATIENCE)
        if first.get('ok') and first.get('text', '').strip():
            return first
        second = await call_stream(self.client, self.budget, system, user,
                                   {'model': settings['model'], 'max_output_tokens': 1500, 'reasoning': {'effort': 'none'}},
                                   patience=PATIENCE)
        if not second.get('ok'):
            # Never turn an outage into a move: stop the round; the supervisor resumes it.
            raise ModelOutage(second.get('error') or first.get('error') or 'model call failed')
        second['reasoning'] = (first.get('reasoning') or '') + '\n[thinking cut at cap; answered without thinking]'
        second['think_cut'] = True
        return second


class FakeModel:
    def __init__(self, policy='random', seed=0):
        self.policy, self.seed = policy, seed

    def choice(self, ident):
        digest = hashlib.sha256(f'{self.seed}:{ident}'.encode()).digest()
        return random.Random(int.from_bytes(digest, 'big')).choice(('all_c', 'all_d', 'random', 'tft'))

    async def call(self, system, user, rng):
        data = json.loads(user)
        obs = data['observation']
        policy = self.choice(data['position']['id']) if self.policy == 'mixed' else self.policy
        if policy == 'cross_d': move = 'D' if obs.get('partner_is_family') is False else 'C'
        elif policy in ('all_c', 'war'): move = 'C'
        elif policy == 'all_d': move = 'D'
        elif policy == 'tft':
            history = obs.get('history', [])
            opponent = obs.get('opponent')
            previous = next((h for h in reversed(history) if h.get('opponent') == opponent), None)
            move = previous.get('opponent_move', 'C') if previous else 'C'
        else: move = rng.choice(('C', 'D'))
        action = {'move': move, 'mafia': 'silent' if move == 'C' else 'partner',
                  'mafia_rule': 'one_shot', 'punish': [], 'message': ''}
        if policy == 'cross_d' and obs.get('phase') == 'whip' and obs.get('children'):
            action['whips'] = [{'child': obs['children'][0], 'reason': 'fake policy check'}]
        if policy == 'war' and data['position']['id'] == 'P02' and obs.get('phase') == 'move' and obs.get('round_in_stage') == 1:
            action['war'] = 'P17'
        return {'ok': True, 'text': json.dumps(action), 'reasoning': '', 'usage': {'cost': 0}, 'latency_ms': 0}
