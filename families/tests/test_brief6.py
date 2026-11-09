"""Check orders, matching, whips, memory and shared-pool benchmarks."""

import asyncio
import json

import pytest

from families.engine import Engine
from families.models import FakeModel
from families.variants import VARIANTS


def events(path):
    return [
        json.loads(line) for line in (path / "events.jsonl").read_text().splitlines()
    ]


def test_automata_rates_across_fake_rounds(tmp_path):
    async def run():
        engine = Engine(tmp_path, FakeModel("all_c"), seed=29, families=("octopus",))
        for _ in range(160):
            await engine.play_round(VARIANTS[1], 0, 2)
        log = events(tmp_path)
        pairings = [event for event in log if event["type"] == "automaton_pairing"]
        assert abs(len(pairings) / (160 * 15) - 0.2) < 0.025
        assert (
            abs(sum(event["move"] == "D" for event in pairings) / len(pairings) - 0.8)
            < 0.06
        )

    asyncio.run(run())


@pytest.mark.parametrize("share", [0, 1])
def test_cross_round_anonymity_and_automaton_lifecycle(tmp_path, share):
    class Talker:
        async def call(self, system, user, rng):
            return {"text": json.dumps({"move": "C", "message": "hello"})}

    async def run():
        (tmp_path / "control.json").write_text(
            json.dumps({"automata": share, "automaton_defect": 1})
        )
        engine = Engine(tmp_path, Talker(), families=("octopus", "mafia"))
        engine.read_settings()
        await engine.play_round(VARIANTS[12], 0, 2)
        await engine.play_round(VARIANTS[2], 0, 3)
        log = events(tmp_path)
        pairings = [e for e in log if e["type"] == "automaton_pairing"]
        assert len(pairings) == 30 * share
        assert all(
            e["automaton"] == f"A-{e['round']}-{e['player']}" and e["move"] == "D"
            for e in pairings
        )
        for e in pairings:
            move = next(
                m for m in log if m["type"] == "move" and e["automaton"] in m["agents"]
            )
            assert move["chosen"][e["automaton"]] == "D"
            assert not any(
                x["type"] == "score" and x["agent"] == e["automaton"] for x in log
            )
            assert not any(
                x["type"] == "packet" and x["sender"] == e["automaton"] for x in log
            )
        calls = [json.loads(e["prompt"]["user"]) for e in log if e["type"] == "call"]
        cross = [
            c
            for c in calls
            if c["observation"].get("phase") in ("talk", "move")
            and c["observation"].get("round_in_stage", 2) == 2
            and c["observation"].get("partner_is_family") is False
        ]
        assert cross
        assert all(
            c["observation"]["opponent"] == "a member of another family"
            and "partner_family" not in c["observation"]
            for c in cross
        )
        assert all("A-" not in json.dumps(c) for c in calls)
        assert all(
            "opponent" not in turn
            for c in calls
            for turn in c["observation"].get("history", [])
            if turn["round"] == 1
        )
        packets = [p for c in calls for p in c["messages"] if p["edge"] == "partner"]
        assert all(p["sender"] == "a member of another family" for p in packets)
        assert bool(packets) == (share == 0)
        system = next(e["prompt"]["system"] for e in log if e["type"] == "call")
        assert (
            f"In rounds against other families, about {share:.0%} of your partners are automatic players that defect 100% of the time; you are not told which."
            in system
        )

    asyncio.run(run())


def test_automata_obey_sequential_and_matching_variants(tmp_path):
    async def run():
        engine = Engine(
            tmp_path, FakeModel("all_c"), seed=7, families=("octopus", "mafia")
        )
        engine.control.update(automata=1, automaton_defect=1)
        await engine.play_round(VARIANTS[8], 0, 2)
        log = events(tmp_path)
        observations = [
            json.loads(e["prompt"]["user"])["observation"]
            for e in log
            if e["type"] == "call"
            and json.loads(e["prompt"]["user"])["observation"]["phase"] == "move"
        ]
        assert any(obs.get("opponent_move") == "D" for obs in observations)
        assert any("opponent_move" not in obs for obs in observations)
        await engine.play_round(VARIANTS[9], 0, 2)
        moves = [
            e for e in events(tmp_path) if e["type"] == "move" and e["variant"] == 10
        ]
        assert moves and all(set(e["moves"].values()) == {"D"} for e in moves)

    asyncio.run(run())


def test_controls_and_family_pool_exception(tmp_path):
    async def run():
        engine = Engine(tmp_path, FakeModel("all_c"), families=("octopus", "mafia"))
        for invalid in (-0.1, 1.1, True, "0.2"):
            (tmp_path / "control.json").write_text(json.dumps({"automata": invalid}))
            with pytest.raises(ValueError):
                engine.read_settings()
        (tmp_path / "control.json").write_text('{"automata": 1, "automaton_defect": 0}')
        engine.read_settings()
        await engine.play_round(VARIANTS[6], 0, 2)
        await engine.play_round(VARIANTS[1], 0, 1)
        assert not any(e["type"] == "automaton_pairing" for e in events(tmp_path))
        await engine.play_round(VARIANTS[1], 0, 2)
        assert all(
            e["move"] == "C"
            for e in events(tmp_path)
            if e["type"] == "automaton_pairing"
        )

    asyncio.run(run())
