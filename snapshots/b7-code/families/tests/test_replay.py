import asyncio
import json

from families.engine import Engine
from families.models import FakeModel
from families.replay import first_difference, load, replay
from families.tree import NAMES


def replay_all(part, out):
    return asyncio.run(replay(part, out, list(NAMES), None))


def test_replay_reproduces_a_game_and_catches_a_changed_reply(tmp_path):
    # tft ignores the engine's random stream, as the real model does.
    asyncio.run(Engine(tmp_path / "run", FakeModel("tft"), seed=3).run(2))
    original, replayed, stopped = replay_all(tmp_path / "run", tmp_path / "again")
    assert stopped is None and first_difference(original, replayed) is None

    events = load(tmp_path / "run" / "events.jsonl")
    call = next(
        e for e in events if e["type"] == "call" and '"move": "C"' in e["reply"]
    )
    call["reply"] = call["reply"].replace('"move": "C"', '"move": "D"')
    changed = tmp_path / "changed"
    changed.mkdir()
    (changed / "events.jsonl").write_text(
        "".join(json.dumps(e, sort_keys=True) + "\n" for e in events)
    )
    original, replayed, _ = replay_all(changed, tmp_path / "again2")
    assert first_difference(original, replayed) is not None
