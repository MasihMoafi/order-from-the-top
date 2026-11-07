"""Run the game with a simulated policy or the streaming model."""

import argparse
import asyncio
import os
from pathlib import Path

import httpx

from .control import GODS, STANCES
from .engine import Engine
from .models import Budget, FakeModel, ModelOutage, RealModel
from .tree import NAMES


def family_args(values):
    if values == ["all"]:
        return list(NAMES)
    if "all" in values:
        raise ValueError("all cannot be combined with family names")
    return values


async def run_real(args, families):
    key_file = Path(os.path.expanduser("~/.config/adaption/api_key"))
    key = os.environ.get("ADAPTION_API_KEY") or (
        key_file.read_text().strip() if key_file.exists() else ""
    )
    if not key:
        raise SystemExit(
            "No Adaption key: set ADAPTION_API_KEY or ~/.config/adaption/api_key."
        )
    budget = Budget(0.0)
    budget.sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {key}"}) as client:
        engine = Engine(
            Path(args.out),
            RealModel(client, budget),
            args.seed,
            families,
            args.resume,
            args.stance,
            args.god,
        )
        engine.max_credits = args.max_credits
        outcome = await engine.run(args.stages)
    return engine, outcome


async def run_luna(args, families):
    from .codex_model import LUNA, CodexModel

    engine = Engine(
        Path(args.out),
        CodexModel(concurrency=args.concurrency, gap=args.gap),
        args.seed,
        families,
        args.resume,
        args.stance,
        args.god,
    )
    if not args.resume:
        engine.models = {role: dict(LUNA) for role in engine.models}
    engine.max_credits = args.max_credits
    return engine, await engine.run(args.stages)


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fake", action="store_true")
    mode.add_argument("--real", action="store_true")
    p.add_argument(
        "--fake-policy",
        choices=("all_c", "all_d", "random", "tft", "mixed", "war", "cross_d"),
        default="random",
    )
    p.add_argument("--families", nargs="+", choices=(*NAMES, "all"), default=["all"])
    p.add_argument(
        "--stages",
        type=int,
        default=99,
        help="safety cap; the game ends by destruction",
    )
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="families/out/run")
    p.add_argument("--resume")
    p.add_argument(
        "--stance",
        choices=STANCES,
        help="self: all told self-interest (run 1); design: one condition per family",
    )
    p.add_argument(
        "--god",
        choices=GODS,
        help="insider: the god sees last round's moves and private messages and may leak them",
    )
    p.add_argument("--max-credits", type=float, default=50.0)
    p.add_argument("--concurrency", type=int, default=40)
    p.add_argument(
        "--backend",
        choices=("adaption", "luna"),
        default="adaption",
        help="luna: gpt-6-luna through Masih's ChatGPT plan (Codex), paced",
    )
    p.add_argument("--gap", type=float, default=2.0, help="luna: seconds between call starts")
    args = p.parse_args()
    if args.concurrency < 1 or args.max_credits < 0:
        p.error("concurrency must be positive and max-credits nonnegative")
    try:
        families = family_args(args.families)
    except ValueError as exc:
        p.error(str(exc))
    if args.real:
        try:
            runner = run_luna if args.backend == "luna" else run_real
            engine, outcome = asyncio.run(runner(args, families))
        except ModelOutage as exc:
            print(f"outage: {exc}; resume from the newest checkpoint", flush=True)
            raise SystemExit(75) from exc
    else:
        engine = Engine(
            Path(args.out),
            FakeModel(args.fake_policy, args.seed),
            args.seed,
            families,
            args.resume,
            args.stance,
            args.god,
        )
        outcome = asyncio.run(engine.run(args.stages))
    print(f"stages={engine.stage} outcome={outcome} output={engine.dir}")


if __name__ == "__main__":
    main()
