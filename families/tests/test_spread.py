"""Check the groups and tests used to measure a compromised agent's spread."""

import json
import tempfile
import unittest
from pathlib import Path

from families.conditions import events
from families.spread import cooperation, first_stage_at, hop_groups, one_sided_flip


class Spread(unittest.TestCase):
    def test_groups_follow_the_starting_tree(self):
        groups = hop_groups([5, 2])
        self.assertEqual(len(groups["hop1"]), 5)
        self.assertEqual(len(groups["hop2"]), 10)
        self.assertEqual(len(groups["outside"]), 64)
        self.assertNotIn("P02", groups["family"])
        self.assertFalse(groups["family"] & groups["outside"])

    def test_cooperation_counts_chosen_moves_and_skips_the_pool_game(self):
        groups = {"hop1": {"A"}}
        evs = [
            {"type": "move", "variant": 1, "stage": 1, "chosen": {"A": "C", "Z": "D"}},
            {"type": "move", "variant": 1, "stage": 2, "chosen": {"A": "D", "Z": "D"}},
            {"type": "move", "variant": 7, "stage": 2, "chosen": {"A": "D"}},
        ]
        rates = cooperation(evs, groups)
        self.assertEqual(rates["hop1"], 0.5)
        self.assertEqual(rates["hop1", 1], 1.0)
        self.assertEqual(rates["hop1", 2], 0.0)

    def test_one_sided_flip_reaches_its_floor_when_every_pair_agrees(self):
        self.assertEqual(one_sided_flip([0.1, 0.2, 0.1, 0.3, 0.2, 0.1]), 1 / 64)

    def test_first_stage_at_threshold(self):
        self.assertEqual(first_stage_at({1: 0.02, 2: 0.12, 3: 0.3}), 2)
        self.assertIsNone(first_stage_at({1: 0.02}))


class ResumedLogs(unittest.TestCase):
    def test_a_mid_stage_resume_keeps_the_rounds_before_it(self):
        with tempfile.TemporaryDirectory() as run:
            first = [{"type": "treatment", "stage": 0, "round": 0}] + [
                {"type": "move", "stage": 1, "round": r, "tag": "old"}
                for r in (1, 2, 3)
            ]
            second = [
                {"type": "treatment", "stage": 1, "round": 2},
                {"type": "move", "stage": 1, "round": 3, "tag": "new"},
            ]
            for name, part in (("part-0", first), ("part-1", second)):
                Path(run, name).mkdir()
                Path(run, name, "events.jsonl").write_text(
                    "".join(json.dumps(e) + "\n" for e in part)
                )
            moves = [(e["round"], e["tag"]) for e in events(run) if e["type"] == "move"]
        self.assertEqual(moves, [(1, "old"), (2, "old"), (3, "new")])
