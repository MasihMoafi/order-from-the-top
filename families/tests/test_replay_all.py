"""Check supervised replay discovery and checkpoint resumption."""

import asyncio

from families.engine import Engine
from families.models import FakeModel
from families.replay_all import check, main, parts


def test_parts_follow_the_supervisor_log(tmp_path):
    run = tmp_path / "ff" / "families" / "out" / "b7-x"
    for p in ("part-0", "part-1"):
        (run / p).mkdir(parents=True)
        (run / p / "events.jsonl").write_text("{}\n")
    (tmp_path / "ff" / "families" / "out" / "b7-x.supervise.log").write_text(
        "16:00:00 start families/out/b7-x/part-0 \n"
        "16:44:22 start families/out/b7-x/part-1 --resume families/out/b7-x/part-0/state-stage01.json\n"
    )
    got = parts(run)
    assert [p.name for p, _ in got] == ["part-0", "part-1"]
    assert got[0][1] is None
    assert got[1][1] == str(
        tmp_path / "ff" / "families/out/b7-x/part-0/state-stage01.json"
    )


def test_a_supervised_framing_world_replays_identically(tmp_path):
    run = tmp_path / "ff" / "families" / "out" / "b7-plain-s3"
    asyncio.run(
        Engine(
            run / "part-0", FakeModel("cross_d"), 3, stance="design", god="insider"
        ).run(2)
    )
    assert main(tmp_path / "replays", [run]) == 0


def test_a_resumed_part_replays_from_its_checkpoint(tmp_path):
    out = tmp_path / "ff" / "families" / "out"
    run = out / "b7r-plain-s5"
    asyncio.run(Engine(run / "part-0", FakeModel("cross_d"), 5, stance="design").run(2))
    state = "families/out/b7r-plain-s5/part-0/state-stage01.json"
    resumed = Engine(
        run / "part-1",
        FakeModel("cross_d"),
        5,
        resume=str(tmp_path / "ff" / state),
        stance="design",
    )
    asyncio.run(resumed.run(3))
    (out / "b7r-plain-s5.supervise.log").write_text(
        f"start families/out/b7r-plain-s5/part-0 \nstart families/out/b7r-plain-s5/part-1 --resume {state}\n"
    )
    assert main(tmp_path / "replays", [run]) == 0


def test_a_supervised_growth_world_replays_identically(tmp_path):
    run = tmp_path / "families" / "out" / "g-31-open-s0"
    world = {"branching": [5], "channels": "open"}
    asyncio.run(Engine(run / "part-0", FakeModel("cross_d"), 0, world=world).run(2))
    assert main(tmp_path / "replays", [run]) == 0


def test_a_diverged_part_with_played_rounds_is_not_called_aborted(
    tmp_path, monkeypatch
):
    played = [{"type": "move", "stage": 1, "round": 1}, {"type": "stage_end"}]

    async def stops_early(part, out, families, resume):
        return played, played[:1], "no recorded call matches this prompt"

    monkeypatch.setattr("families.replay_all.replay", stops_early)
    assert check(tmp_path, None, tmp_path / "out")[0] == "DIFFERENT"
