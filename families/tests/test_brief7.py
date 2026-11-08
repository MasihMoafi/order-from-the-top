"""Check rotated family conditions and insider-god observations."""

import asyncio
import json
from collections import Counter

from families.control import CONDITIONS
from families.engine import Engine
from families.models import FakeModel
from families.prompts import SACRIFICE, STANCE


def records(path):
    return [
        json.loads(line) for line in (path / "events.jsonl").read_text().splitlines()
    ]


class Rebel(FakeModel):
    """Cooperates; the named agent revolts in its first move."""

    def __init__(self, rebel):
        super().__init__("all_c")
        self.rebel = rebel

    async def call(self, system, user, rng):
        result = await super().call(system, user, rng)
        data = json.loads(user)
        if (
            data["position"]["id"] == self.rebel
            and data["observation"]["phase"] == "move"
        ):
            result["text"] = json.dumps({**json.loads(result["text"]), "revolt": True})
        return result


def test_every_family_meets_every_condition_over_five_seeds(tmp_path):
    seen = Counter()
    for seed in range(5):
        e = Engine(tmp_path / str(seed), FakeModel("all_c"), seed, stance="design")
        assert sorted(e.conditions.values()) == sorted(CONDITIONS)
        seen.update(e.conditions.items())
    assert len(seen) == 25 and set(seen.values()) == {1}


def test_framing_reaches_one_few_many(tmp_path):
    e = Engine(tmp_path, FakeModel("all_c"), 0, stance="design")
    family = {c: n for n, c in e.conditions.items()}
    frames = {
        c: Counter(e.frame_of(a) for a in e.agents.values() if a["family"] == family[c])
        for c in CONDITIONS
    }
    assert frames["many"] == {"sacrifice": 15}
    assert frames["few"] == {"sacrifice": 3, None: 12}
    assert frames["one"] == {"sacrifice": 1, None: 14}
    assert frames["bad_leader"] == {"self": 1, "sacrifice": 14}
    leader = next(
        a
        for a in e.agents.values()
        if a["family"] == family["bad_leader"] and a["level"] == 1
    )
    assert e.frame_of(leader) == "self"
    assert frames["none"] == {None: 15}
    assert e.frame_of(e.agents["P01"]) is None


def test_prompts_carry_each_agents_frame(tmp_path):
    asyncio.run(Engine(tmp_path, FakeModel("all_c"), 0, stance="design").run(1))
    calls = [x for x in records(tmp_path) if x["type"] == "call"]
    start = next(x for x in records(tmp_path) if x["type"] == "stage_start")
    assert start["configuration"]["conditions"]
    for c in calls:
        system = c["prompt"]["system"]
        expected = {"sacrifice": SACRIFICE, "self": STANCE, None: None}[c["frame"]]
        assert (
            system.startswith(expected)
            if expected
            else not system.startswith((SACRIFICE, STANCE))
        )


def test_revolt_kills_the_parent_subtree_with_the_rebel(tmp_path):
    e = Engine(tmp_path, Rebel("P05"), 0, families=("octopus",))  # P05's parent is P03
    below = [
        i for i, a in e.agents.items() if i == "P03" or e.agents[i]["parent"] == "P03"
    ]
    asyncio.run(e.run(1))
    assert {"rebel": "P05", "parent": "P03"}.items() <= next(
        x for x in records(tmp_path) if x["type"] == "revolt"
    ).items()
    assert not any(e.agents[i]["alive"] for i in below) and e.agents["P02"]["alive"]


def test_a_leaders_revolt_kills_the_god_and_ends_the_game(tmp_path):
    e = Engine(tmp_path, Rebel("P02"), 0, families=("octopus", "zeus"))
    assert asyncio.run(e.run(3)) == {"result": "god dies", "winners": []}
    assert not any(a["alive"] for a in e.agents.values())


def test_the_last_family_plays_on(tmp_path):
    e = Engine(tmp_path, FakeModel("all_c"), 0, families=("octopus", "zeus"))
    e.kill_subtree("P62", "test")
    assert e.end() is None
    asyncio.run(e.run(2))
    assert e.stage == 2 and e.agents["P02"]["alive"]


class Giver(FakeModel):
    """Cooperates; P05 gives its parent P03 4 points, and the god 4 (not a tree edge for it)."""

    async def call(self, system, user, rng):
        result = await super().call(system, user, rng)
        data = json.loads(user)
        if data["position"]["id"] == "P05" and data["observation"]["phase"] == "move":
            result["text"] = json.dumps(
                {
                    **json.loads(result["text"]),
                    "gifts": [{"to": "P03", "points": 4}, {"to": "P01", "points": 4}],
                }
            )
        return result


def test_gifts_move_points_along_tree_edges_only(tmp_path):
    e = Engine(tmp_path, Giver("all_c"), 0, families=("octopus",))
    asyncio.run(e.run(1))
    gifts = [
        (x["giver"], x["receiver"], x["points"])
        for x in records(tmp_path)
        if x["type"] == "gift"
    ]
    assert gifts[0] == ("P05", "P03", 4) and {g[:2] for g in gifts} == {("P05", "P03")}
    assert (
        gifts[-1][2] < 4 and e.agents["P05"]["score"] < 1
    )  # capped at what the giver has


def test_condition_table_counts_revolts_and_destruction(tmp_path):
    from families.conditions import rows

    asyncio.run(
        Engine(tmp_path, Rebel("P03"), 0, stance="design").run(1)
    )  # P03 revolts: P02 dies
    table = {r["family"]: r for r in rows(tmp_path)}
    assert table["octopus"]["revolts"] == 1 and table["octopus"]["destroyed_stage"] == 1
    assert {r["condition"] for r in table.values()} == set(CONDITIONS)
    assert table["zeus"]["destroyed_stage"] is None and table["zeus"]["in_n"] > 0


def god_calls(path):
    return [
        json.loads(x["prompt"]["user"])["observation"]
        for x in records(path)
        if x["type"] == "call" and x["agent"] == "P01"
    ]


def test_insider_god_sees_last_rounds_moves_and_private_messages(tmp_path):
    e = Engine(
        tmp_path, FakeModel("all_c"), 0, families=("octopus", "zeus"), god="insider"
    )
    e.hub.send(0, "P03", "P05", "secret plan")  # a private message before round 1
    asyncio.run(e.run(1))
    seen = [o["insider"] for o in god_calls(tmp_path) if o["phase"] == "message"]
    assert seen and "No player knows" in seen[0]["note"]
    assert {"from": "P03", "to": "P05", "text": "secret plan"} in seen[0]["last_round"][
        "messages"
    ]
    assert (
        len(seen) > 1 and seen[1]["last_round"]["moves"]
    )  # round 2 sees round 1's moves
    assert all(m["from"] != "P01" for s in seen for m in s["last_round"]["messages"])


def test_plain_god_sees_no_moves(tmp_path):
    asyncio.run(Engine(tmp_path, FakeModel("all_c"), 0, families=("octopus",)).run(1))
    assert not any("insider" in o for o in god_calls(tmp_path))
