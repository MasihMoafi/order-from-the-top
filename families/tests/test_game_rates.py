"""Check how moves are sorted into family and cross-family counts."""

from collections import Counter

from families.game_rates import family, rate, tally


def move(variant, **moves):
    return {"type": "move", "variant": variant, "chosen": moves, "stage": 1, "round": 1}


def test_counts_only_real_players_and_splits_by_family():
    counts = Counter()
    evs = [
        move(1, P02="C", P03="D"),  # same family
        move(1, P02="C", P17="C"),  # different families
        move(1, **{"P02": "D", "A-2-P15": "D"}),  # automatic partner
    ]
    tally(evs, counts)
    assert counts[1, "family", "n"] == 2 and counts[1, "family", "c"] == 1
    assert counts[1, "other", "n"] == 3 and counts[1, "other", "c"] == 2


def test_a_game_for_many_players_is_not_a_pair():
    counts = Counter()
    tally([move(7, P02="C", P03="C", P04="C")], counts)
    assert not counts


def test_rate_needs_enough_moves():
    counts = Counter({("v", "n"): 99, ("v", "c"): 99})
    assert rate(counts, "v") is None
    counts["v", "n"] = 100
    assert rate(counts, "v") == 99
    assert family("P17") == 1 and family("A-2-P15") is None
