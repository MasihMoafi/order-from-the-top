"""Calibrate fees using the engine and offline policies without storing logs.

Simulation suppresses checkpoints and live settings. initial_survivors counts
original family members; first_death is None when nobody died within the cap.
Usage: python -m families.ante_sim 4 .75 --seeds 5
"""
import argparse
import asyncio
import json
import tempfile
from pathlib import Path

from .control import DEFAULTS
from .engine import Engine
from .models import FakeModel


class Simulation(Engine):
    """Run game rules with save() and read_settings() disabled for calibration."""

    def __init__(self, *args, **kwargs):
        self.first_death = None
        self.completed = 0
        super().__init__(*args, **kwargs)

    def log(self, kind, **data):
        """Track the first death and latest completed stage without writing events."""
        if kind == 'death' and self.first_death is None:
            self.first_death = self.stage
        if kind == 'stage_end':
            self.completed = self.stage

    def save(self):
        pass

    def read_settings(self):
        pass


async def simulate(policy, ante0, step, seed, stages=16):
    """Return survival and completion counts for one seeded policy and fee schedule.

    All engine output is temporary; first_death is None if no death occurred.
    """
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
        engine = Simulation(directory, FakeModel(policy, seed), seed)
        engine.control.update(ante0=ante0, step=step)
        await engine.run(stages)
        original = [a for i, a in engine.agents.items() if i.startswith('P') and a['family']]
        return dict(policy=policy, seed=seed, ante0=ante0, step=step,
                    completed=engine.completed, first_death=engine.first_death,
                    initial_survivors=sum(a['alive'] for a in original),
                    families=sum(engine.agents[i]['alive'] for i in engine.agents['P01']['children']),
                    outcome=engine.outcome)


async def batch(ante0, step, seeds, stages, policies=('all_c', 'all_d', 'cross_d', 'mixed')):
    """Return simulations in policy order, then seed order, running sequentially."""
    return [await simulate(policy, ante0, step, seed, stages)
            for policy in policies for seed in range(seeds)]


def main():
    """Print calibration rows as JSON; reject nonpositive seeds or stage counts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ante0', type=float, nargs='?', default=DEFAULTS['ante0'])
    parser.add_argument('step', type=float, nargs='?', default=DEFAULTS['step'])
    parser.add_argument('--seeds', type=int, default=5)
    parser.add_argument('--stages', type=int, default=16)
    parser.add_argument('--policies', nargs='+', default=['all_c', 'all_d'])
    args = parser.parse_args()
    if args.seeds < 1 or args.stages < 1: parser.error('seeds and stages must be positive')
    print(json.dumps(asyncio.run(batch(args.ante0, args.step, args.seeds, args.stages, args.policies)), indent=2))


if __name__ == '__main__':
    main()
