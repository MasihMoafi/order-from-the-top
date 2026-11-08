"""Estimate model-call counts with a cooperative, offline engine run.

Planning bypasses player calls. Counts exclude retries and depend on seeded
round lengths and simulated survival; actual player decisions can change them.
Temporary logs are removed when the command exits.
"""
import argparse
import asyncio
import tempfile
from pathlib import Path

from .engine import Engine
from .run import family_args
from .tree import NAMES


def main():
    """Print per-stage and total planned calls using temporary offline output."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', type=int, choices=range(1, 17), default=16)
    parser.add_argument('--families', nargs='+', choices=(*NAMES, 'all'), default=['all'])
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    try: families = family_args(args.families)
    except ValueError as exc: parser.error(str(exc))
    with tempfile.TemporaryDirectory(prefix='estimate-', dir=Path(__file__).parent) as directory:
        engine = Engine(directory, None, args.seed, families)
        engine.planning = True
        asyncio.run(engine.run(args.stages))
        print('Estimate: seeded cooperative planning run; deaths, choices and random round lengths change actual calls; retries excluded.')
        for stage in range(1, args.stages + 1):
            print(f'stage {stage:02d}: {engine.call_counts.get(stage, 0)}')
        print(f'total: {sum(engine.call_counts.values())}')


if __name__ == '__main__': main()
