import json
import random

from families.analysis import sign_flip
from families.conditions import events


def write(part, records):
    """records: (type, stage) pairs, as a supervised run writes them."""
    part.mkdir(parents=True)
    lines = [
        json.dumps({"type": t, "stage": s, "n": i}) for i, (t, s) in enumerate(records)
    ]
    (part / "events.jsonl").write_text("\n".join(lines) + "\n")


def test_a_resumed_part_replaces_the_stages_its_aborted_parts_began(tmp_path):
    # Shape seen in b7-plain-s2: each resume opens with a treatment record stamped with
    # the checkpoint's stage (1), then replays stage 2.
    write(tmp_path / "part-0", [("packet", 0), ("call", 1), ("call", 1), ("call", 2)])
    write(tmp_path / "part-1", [("treatment", 1), ("call", 2)])  # aborted again
    write(tmp_path / "part-2", [("treatment", 1), ("call", 2), ("call", 3)])
    write(tmp_path / "part-10", [("treatment", 3), ("call", 4)])  # numeric order
    got = [
        (e["type"], e["stage"], e["n"])
        for e in events(tmp_path)
        if e["type"] != "treatment"
    ]
    assert got == [
        ("packet", 0, 0),
        ("call", 1, 1),
        ("call", 1, 2),  # stage 1 kept from part-0
        ("call", 2, 1),
        ("call", 3, 2),  # stage 2 and 3 from part-2 only
        ("call", 4, 1),
    ]


def test_sign_flip_is_exact_for_small_samples():
    assert sign_flip([1, 1, 1, 1], random.Random(0)) == 2 / 16
    assert sign_flip([1, -1], random.Random(0)) == 1.0


def test_a_world_cut_off_mid_stage_is_measured_to_its_last_finished_stage():
    from families.conditions import completed

    evs = [
        {"type": "move", "stage": 1},
        {"type": "stage_end", "stage": 1},
        {"type": "move", "stage": 2},  # stage 2 never finished
    ]
    assert completed(evs) == evs[:2]


def test_a_horizon_cuts_measures_at_that_stage():
    from families.conditions import completed

    evs = [{"type": "stage_end", "stage": s} for s in (1, 2, 3)]
    assert completed(evs, horizon=2) == evs[:2]
