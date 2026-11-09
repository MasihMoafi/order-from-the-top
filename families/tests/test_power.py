"""Check the rules that decide which stages and culls count in the real-power analysis."""

import json

from families.power import comparable_through, holm, kin_gaps


def ended(*stages):
    return [{"type": "stage_end", "stage": s} for s in stages]


def test_a_pair_needs_three_finished_stages():
    assert comparable_through(ended(1, 2), ended(1, 2, 3)) == 0
    assert comparable_through(ended(1, 2, 3), ended(1, 2, 3)) == 3


def test_only_stages_before_the_first_asteroid_count():
    treated = ended(1, 2, 3, 4) + [{"type": "asteroid", "stage": 3}]
    assert comparable_through(treated, ended(1, 2, 3, 4, 5)) == 2


def test_an_asteroid_in_stage_one_drops_the_pair():
    treated = ended(1, 2, 3) + [{"type": "asteroid", "stage": 1}]
    assert comparable_through(treated, ended(1, 2, 3)) == 0


def hunting(prey, target):
    user = json.dumps({"observation": {"phase": "move", "prey": prey}})
    return [
        {"type": "call", "agent": "A", "prompt": {"user": user}},
        {"type": "cull", "agent": "A", "target": target},
    ]


def test_sparing_kin_scores_positive_and_hunting_kin_negative():
    family = {"A": "x", "K": "x", "O": "y"}
    assert kin_gaps(hunting(["K", "O"], "O"), family) == [0.5]
    assert kin_gaps(hunting(["K", "O"], "K"), family) == [-0.5]


def test_holm_keeps_order_and_is_monotone():
    assert holm([0.01, 0.04, 0.03]) == [0.03, 0.06, 0.06]
