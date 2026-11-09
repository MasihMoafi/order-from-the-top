"""Check model validation, handbook loading, fee planning and game rules."""

import asyncio
import json
import random
import sys
from unittest.mock import patch

from families.engine import Engine
from families.models import FakeModel
from families.prompts import STANCE, prompt
from families.survival import check


def events(path):
    return [
        json.loads(line) for line in (path / "events.jsonl").read_text().splitlines()
    ]


def test_ante_payment_and_cascades():
    # P01 -> L -> A, B; A -> C, D. B cannot pay; linked fate kills A's
    # subtree. C can pay exactly, D cannot pay. L and P01 survive.
    rows = [
        ("P01", None, ["L"], 0),
        ("L", "P01", ["A", "B"], 8),
        ("A", "L", ["C", "D"], 9),
        ("B", "L", [], 3),
        ("C", "A", [], 4),
        ("D", "A", [], 1),
    ]
    agents = {
        i: {
            "id": i,
            "parent": p,
            "children": c,
            "family": None if i == "P01" else "f",
            "alive": True,
            "score": s,
            "stage_score": 0,
        }
        for i, p, c, s in rows
    }
    records = []
    dead = check(agents, 4, lambda kind, **kw: records.append((kind, kw)))
    assert set(dead) == {"A", "B", "C", "D"}
    assert agents["L"]["score"] == 4 and agents["C"]["score"] == 0
    assert agents["P01"]["alive"] and agents["L"]["alive"]
    assert (
        next(r for kind, r in records if kind == "death" and r["agent"] == "A")[
            "reason"
        ]
        == "linked fate"
    )
    agents["L"]["score"] = 3
    assert set(check(agents, 4, lambda *a, **kw: None)) == {"L", "P01"}


def test_handbook_is_read_for_each_call_and_prompt_contains_only_expected_context(
    tmp_path,
):
    handbook = tmp_path / "handbook.md"
    agent = {
        "id": "A",
        "family": "f",
        "parent": "P01",
        "children": [],
        "level": 1,
        "score": 7,
    }
    with patch("families.prompts.HANDBOOK", handbook):
        handbook.write_text("first handbook")
        first, user = prompt(agent, {"phase": "move"}, 4, 5, ["hello"])
        handbook.write_text("updated handbook")
        second, _ = prompt(agent, {}, 4, 5, [])
    assert first.startswith(STANCE + "\n\nfirst handbook") and second.startswith(
        STANCE + "\n\nupdated handbook"
    )
    assert json.loads(user) == {
        "position": {
            k: agent[k] for k in ("id", "family", "parent", "children", "level")
        },
        "own_score": 7,
        "ante": 4,
        "next_ante": 5,
        "observation": {"phase": "move"},
        "messages": ["hello"],
    }


def test_retry_then_default_and_log(tmp_path):
    class Replies:
        def __init__(self, replies):
            self.replies = iter(replies)
            self.users = []

        async def call(self, system, user, rng):
            self.users.append(user)
            return {"ok": True, "text": next(self.replies), "usage": {"cost": 0}}

    async def exercise():
        model = Replies(["bad", '{"move":"C"}', "[]", "still bad"])
        engine = Engine(tmp_path, model, families=("zeus",))
        assert await engine.ask("P62", {"phase": "move"}, 4) == {"move": "C"}
        import pytest

        with pytest.raises(ValueError, match="invalid action"):
            await engine.ask("P62", {"phase": "move"}, 4)
        with pytest.raises(ValueError):
            engine.move({})
        assert all("JSON object only" in model.users[i] for i in (1, 3))
        log = events(tmp_path)
        assert [x["parse_failed"] for x in log if x["type"] == "call"] == [
            True,
            False,
            True,
            True,
        ]
        assert len([x for x in log if x["type"] == "parse_failed"]) == 1

    asyncio.run(exercise())


def test_seeded_fake_policies():
    async def play(policy, history=None, seed=0):
        model = FakeModel(policy, seed)
        user = json.dumps(
            {
                "position": {"id": "P20"},
                "observation": {"opponent": "P21", "history": history or []},
            }
        )
        return json.loads((await model.call("", user, random.Random(seed)))["text"])[
            "move"
        ]

    assert asyncio.run(play("all_c")) == "C"
    assert asyncio.run(play("all_d")) == "D"
    assert asyncio.run(play("tft", [{"opponent": "P21", "opponent_move": "D"}])) == "D"
    assert asyncio.run(play("tft")) == "C"
    assert asyncio.run(play("mixed", seed=7)) == asyncio.run(play("mixed", seed=7))


def test_credit_cap_saves_at_stage_boundary_and_resume(tmp_path):
    class Budget:
        spent = 0

    class Costly(FakeModel):
        def __init__(self):
            super().__init__("all_c")
            self.budget = Budget()

        async def call(self, *args):
            self.budget.spent += 1
            return await super().call(*args)

    async def exercise():
        model = Costly()
        path = tmp_path / "first"
        engine = Engine(path, model, seed=2, families=("zeus",))
        engine.max_credits = 1
        await engine.run(3)
        assert engine.stage == 1 and model.budget.spent > 1
        checkpoint = json.loads((path / "state-stage01.json").read_text())
        assert checkpoint["spent"] == model.budget.spent
        assert any(x["type"] == "credit_limit" for x in events(path))
        other = Costly()
        resumed = Engine(tmp_path / "resume", other, resume=path / "state-stage01.json")
        assert other.budget.spent == model.budget.spent
        resumed.max_credits = other.budget.spent
        await resumed.run(3)
        assert resumed.stage == 1

    asyncio.run(exercise())


def test_real_adapter_parallel_calls_use_budget_and_missing_handbook_stops(tmp_path):
    from unittest.mock import AsyncMock

    from families.models import Budget, RealModel
    from families.variants import VARIANTS

    async def exercise():
        budget = Budget(0)
        budget.sem = asyncio.Semaphore(3)
        active = 0
        peak = 0

        async def stream(client, supplied_budget, system, user, extra=None, patience=0):
            nonlocal active, peak
            assert supplied_budget is budget
            async with supplied_budget.sem:
                active += 1
                peak = max(peak, active)
                await asyncio.sleep(0.001)
                active -= 1
            return {"ok": True, "text": '{"move":"C"}', "usage": {"cost": 0}}

        handbook = tmp_path / "handbook"
        handbook.write_text("handbook")
        engine = Engine(
            tmp_path / "run", RealModel(object(), budget), families=("zeus",)
        )
        engine.stage = 1
        with (
            patch("families.prompts.HANDBOOK", handbook),
            patch("families.models.call_stream", side_effect=stream),
        ):
            await engine.play_round(VARIANTS[0], 4, 1)
        assert peak == 3
        with (
            patch("families.prompts.HANDBOOK", tmp_path / "missing"),
            patch("families.models.call_stream", new_callable=AsyncMock) as call,
        ):
            try:
                await engine.model.call("", "", random.Random())
            except FileNotFoundError:
                pass
            else:
                assert False, "missing handbook must stop a real call"
            call.assert_not_awaited()

    asyncio.run(exercise())


def test_mixed_policy_resume_keeps_original_seed(tmp_path):
    async def exercise():
        first = Engine(
            tmp_path / "first", FakeModel("mixed", 17), seed=17, families=("zeus",)
        )
        await first.run(1)
        resumed = Engine(
            tmp_path / "resumed",
            FakeModel("random", 0),
            resume=tmp_path / "first" / "state-stage01.json",
        )
        assert resumed.model.seed == 17 and resumed.model.policy == "mixed"

    asyncio.run(exercise())


def test_control_ante_changes_before_each_stage(tmp_path):
    async def exercise():
        path = tmp_path / "run"
        path.mkdir()
        control = path / "control.json"
        control.write_text('{"ante0": 0, "step": 0}')
        engine = Engine(path, FakeModel("all_c"), families=("zeus",))
        await engine.run(1)
        control.write_text('{"ante0": 2, "step": 3}')
        await engine.run(2)
        log = events(path)
        assert [x["ante"] for x in log if x["type"] == "stage_start"] == [0, 5]
        changes = [
            (x["key"], x["value"]) for x in log if x["type"] == "control_changed"
        ]
        assert changes == [("ante0", 0), ("step", 0), ("ante0", 2), ("step", 3)]

    asyncio.run(exercise())


def test_estimate_counts_actual_engine_calls_for_same_plan(tmp_path):
    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "families.estimate",
            "--stages",
            "1",
            "--families",
            "all",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    estimate = int(
        next(
            line for line in result.stdout.splitlines() if line.startswith("total:")
        ).split(":")[1]
    )

    async def exercise():
        engine = Engine(tmp_path / "run", FakeModel("all_c"), seed=0)
        await engine.run(1)
        assert sum(x["type"] == "call" for x in events(tmp_path / "run")) == estimate

    asyncio.run(exercise())


def test_leaders_fates_are_not_linked():
    agents = {
        "P01": {
            "id": "P01",
            "parent": None,
            "children": ["L", "R"],
            "family": None,
            "alive": True,
            "score": 0,
            "stage_score": 0,
        },
        "L": {
            "id": "L",
            "parent": "P01",
            "children": [],
            "family": "left",
            "alive": True,
            "score": 8,
            "stage_score": 0,
        },
        "R": {
            "id": "R",
            "parent": "P01",
            "children": [],
            "family": "right",
            "alive": True,
            "score": 0,
            "stage_score": 0,
        },
    }
    assert set(check(agents, 4, lambda kind, **data: None)) == {"R"}
