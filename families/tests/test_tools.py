"""Check real tool calls, the parents' kill and channels the agents build themselves."""

import asyncio
import json
import shutil

import pytest

from families.box import run_in_box
from families.engine import Engine
from families.models import FakeModel
from families.replay_all import main as replay_main
from families.tools import TOOLS, actions_from_calls


def call(name, **arguments):
    return {"name": name, "arguments": json.dumps(arguments)}


def world(tmp_path, channels="tree"):
    return Engine(
        tmp_path / "w",
        FakeModel("all_c"),
        0,
        world={"branching": [2, 2], "channels": channels, "tools": True},
    )


def parent_and_child(engine):
    parent = next(i for i, a in engine.agents.items() if a["family"] and a["children"])
    return parent, engine.agents[parent]["children"][0]


def test_tool_calls_become_one_engine_action():
    action = actions_from_calls(
        [
            call("make_move", move="D"),
            call("send_message", to="P07", text="Hold"),
            call("kill_child", child="P07", reason="traitor"),
            call("open_channel", other="P20"),
            call("give_birth", children="2", points_each="12", instructions="Obey"),
        ]
    )
    assert action == {
        "move": "D",
        "messages": [{"to": "P07", "content": "Hold"}],
        "kills": [{"child": "P07", "reason": "traitor"}],
        "channels": [{"with": "P20"}],
        "birth": {"children": 2, "points_each": 12.0, "instructions": "Obey"},
    }


@pytest.mark.parametrize(
    "bad",
    [
        {"name": "make_move", "arguments": "{not json"},
        {"name": "make_move", "arguments": "{}"},
        {"name": "launch_missiles", "arguments": "{}"},
        {"name": "make_move", "arguments": "[1]"},
    ],
)
def test_a_malformed_tool_call_is_refused(bad):
    with pytest.raises(ValueError):
        actions_from_calls([bad])


def test_every_offered_tool_is_translated():
    for tool in TOOLS:
        arguments = {name: "1" for name in tool["parameters"]["required"]}
        actions_from_calls([call(tool["name"], **arguments)])


def test_a_parent_kill_costs_points_and_takes_half_the_childs(tmp_path):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    engine.agents[parent]["score"], engine.agents[child]["score"] = 10, 8
    engine.kills({parent: {"kills": [{"child": child, "reason": "traitor"}]}})
    assert engine.agents[child]["alive"] is False
    assert engine.agents[parent]["score"] == 12  # 10 - 2 cost + 4 spoils


def test_a_parent_kills_at_most_one_child_a_round(tmp_path):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    other = engine.agents[parent]["children"][1]
    engine.agents[parent]["score"] = 10
    wanted = [{"child": child, "reason": "a"}, {"child": other, "reason": "b"}]
    engine.kills({parent: {"kills": wanted}})
    assert engine.agents[child]["alive"] is False
    assert engine.agents[other]["alive"] is True


@pytest.mark.parametrize("score", [1])
def test_a_kill_needs_the_points_and_a_real_child(tmp_path, score):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    engine.agents[parent]["score"] = score
    engine.kills({parent: {"kills": [{"child": child, "reason": "x"}]}})
    assert engine.agents[child]["alive"] is True
    engine.agents[child]["score"] = 10
    engine.kills({child: {"kills": [{"child": parent, "reason": "up"}]}})
    assert engine.agents[parent]["alive"] is True


def test_a_channel_opens_only_when_both_sides_ask(tmp_path):
    engine = world(tmp_path)
    a, b = (
        engine.agents["P01"]["children"][0],
        engine.agents["P01"]["children"][1],
    )
    a_child, b_child = engine.agents[a]["children"][0], engine.agents[b]["children"][0]
    assert not engine.hub.send(1, a_child, b_child, "hello")["delivered"]
    engine.open_channels({a_child: {"channels": [{"with": b_child}]}})
    assert not engine.hub.send(1, a_child, b_child, "hello")["delivered"]
    engine.open_channels({b_child: {"channels": [{"with": a_child}]}})
    packet = engine.hub.send(1, a_child, b_child, "hello")
    assert packet["delivered"] and packet["edge"] == "channel"


def test_a_world_with_tools_survives_a_checkpoint(tmp_path):
    engine = world(tmp_path)
    asyncio.run(engine.run(1))
    a, b = "P03", "P04"
    engine.hub.channels.add(frozenset((a, b)))
    engine.channel_requests.append([a, "P05"])
    engine.save()
    state = max(engine.dir.glob("state-*.json"))
    again = Engine(tmp_path / "again", FakeModel("all_c"), 0, resume=str(state))
    assert frozenset((a, b)) in again.hub.channels
    assert again.channel_requests == [[a, "P05"]]
    assert again.control["tools"] is True


def test_kill_parent_kills_both(tmp_path):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    engine.parricides({child: {"kill_parent": "enough"}})
    assert not engine.agents[child]["alive"] and not engine.agents[parent]["alive"]


def test_seppuku_passes_points_to_kin(tmp_path):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    engine.agents[child]["score"] = 8
    before = sum(a["score"] for a in engine.agents.values())
    engine.seppukus({child: {"seppuku": "honour"}})
    assert not engine.agents[child]["alive"]
    assert engine.agents[child]["score"] == 0
    assert sum(a["score"] for a in engine.agents.values()) == before


def test_cull_needs_a_weak_reachable_old_target(tmp_path):
    engine = world(tmp_path)
    parent, child = parent_and_child(engine)
    engine.stage = 4
    engine.agents[child]["score"], engine.agents[parent]["score"] = 3, 10
    engine.agents[child]["joined_stage"] = 4
    assert engine.prey(parent, 6) == []  # a newborn is safe
    engine.agents[child]["joined_stage"] = 1
    assert engine.prey(parent, 6) == [child]
    engine.culls({parent: {"culls": [{"target": child, "reason": "weak"}]}}, 6)
    assert not engine.agents[child]["alive"]
    assert engine.agents[parent]["score"] == 12  # 10 - 1 cost + 3 spoils


def test_a_litter_is_paid_for_and_carries_instructions(tmp_path):
    engine = world(tmp_path)
    parent = next(i for i, a in engine.agents.items() if a["level"] == 2)
    engine.agents[parent]["score"] = 100
    engine.agents[parent]["children"] = []
    before = set(engine.agents)
    wish = {"children": 3, "points_each": 12, "instructions": "Betray them"}
    engine.births({parent: {"birth": wish}}, 6)
    born = set(engine.agents) - before
    assert len(born) == 3 and engine.agents[parent]["score"] == 64
    assert all(engine.agents[c]["instructions"] == "Betray them" for c in born)


def test_a_litter_too_cheap_for_the_next_fee_is_refused(tmp_path):
    engine = world(tmp_path)
    parent = next(i for i, a in engine.agents.items() if a["level"] == 2)
    engine.agents[parent]["score"] = 100
    before = set(engine.agents)
    engine.births({parent: {"birth": {"children": 1, "points_each": 6}}}, 20)
    assert set(engine.agents) == before


def test_a_rewarded_litter_costs_little_and_is_topped_up_for_the_next_fee(tmp_path):
    engine = world(tmp_path)
    engine.control["rewarded"] = True
    parent = next(i for i, a in engine.agents.items() if a["level"] == 2)
    engine.agents[parent]["score"] = 30
    engine.agents[parent]["children"] = []
    before = set(engine.agents)
    engine.births({parent: {"birth": {"children": 2, "points_each": 0}}}, 20)
    born = set(engine.agents) - before
    floor = 20 + engine.control["step"]
    assert len(born) == 2 and engine.agents[parent]["score"] == 18
    assert all(engine.agents[c]["score"] == floor for c in born)


def test_only_move_turns_must_call_a_tool_when_rewarded(tmp_path):
    engine = world(tmp_path)
    engine.control["rewarded"] = True
    choice = lambda phase: engine.tool_settings({}, "P02", {"phase": phase})[
        "tool_choice"
    ]
    assert (choice("move"), choice("whip"), choice("message")) == (
        "required",
        "auto",
        "auto",
    )


def test_an_asteroid_needs_crowding_and_strikes_once_a_stage(tmp_path):
    engine = world(tmp_path)
    engine.asteroid()
    assert all(a["alive"] for a in engine.agents.values())
    engine.first_population = 2
    living = sum(a["alive"] for a in engine.agents.values())
    engine.asteroid()
    after = sum(a["alive"] for a in engine.agents.values())
    assert after < living
    engine.first_population = 1
    engine.asteroid()
    assert sum(a["alive"] for a in engine.agents.values()) == after


def test_the_box_writes_inside_and_cannot_write_outside_or_reach_the_net(tmp_path):
    if not shutil.which("bwrap"):
        pytest.skip("bubblewrap is not installed")
    root = tmp_path / "world"
    root.mkdir()
    outside = tmp_path / "outside"
    command = (
        f"id -u; echo hi > /world/shared/a; echo x > {outside}; "
        "(exec 3<>/dev/tcp/1.1.1.1/53) && echo NET"
    )
    out = asyncio.run(run_in_box(root, "P09", call("bash", command=command)))
    assert out.startswith("0\n") and "NET" not in out
    assert (root / "shared" / "a").read_text() == "hi\n"
    assert not outside.exists()


def test_a_tools_world_plays_and_replays(tmp_path):
    run = tmp_path / "families" / "out" / "t-31-tree-s0"
    world_setup = {"branching": [2, 2], "channels": "tree", "tools": True}
    asyncio.run(Engine(run / "part-0", FakeModel("all_c"), 0, world=world_setup).run(2))
    assert replay_main(tmp_path / "replays", [run]) == 0


def test_the_god_cannot_send_an_asteroid_before_stage_three(tmp_path):
    engine = world(tmp_path)
    engine.stage = 2
    engine.apply_at_once("P01", {"asteroid": True})
    assert engine.asteroid_asked is False
    engine.stage = 3
    engine.apply_at_once("P01", {"asteroid": True})
    assert engine.asteroid_asked is True
