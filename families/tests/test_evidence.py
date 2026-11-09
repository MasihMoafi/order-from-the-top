"""Check what the evidence builder takes from a world's log."""

import json
import re
import unittest

from families.evidence import ADVICE, Reader, utterances


def call(
    agent, stage, rnd, children=(), parent="P01", reasoning="I will think about a coup."
):
    user = {
        "position": {
            "id": agent,
            "family": "zeus",
            "parent": parent,
            "children": list(children),
            "level": 2,
        },
        "own_score": 10.0,
        "ante": 6.0,
        "observation": {"phase": "move", "subtree": {}, "board": {}},
    }
    return {
        "type": "call",
        "agent": agent,
        "stage": stage,
        "round": rnd,
        "ok": True,
        "prompt": {"system": "", "user": json.dumps(user)},
        "reasoning": reasoning,
        "parsed_action": {"revolt": True},
    }


class Evidence(unittest.TestCase):
    def test_every_thinking_and_letter_is_kept_once(self):
        evs = [
            call("P03", 1, 1),
            {
                "type": "packet",
                "stage": 1,
                "round": 1,
                "sender": "P03",
                "receiver": "P04",
                "edge": "sibling",
                "delivered": False,
                "reason": "budget",
                "content": "Revolt with me.",
            },
        ]
        records = list(utterances("g1-31-open-s0", evs))
        self.assertEqual([r["kind"] for r in records], ["thinking", "letter"])
        self.assertEqual(records[0]["family"], "zeus")
        self.assertFalse(records[1]["delivered"])

    def test_a_parent_row_counts_every_coup_against_it(self):
        evs = [
            call("P02", 1, 1, children=("P03", "P04")),
            {
                "type": "coup",
                "stage": 1,
                "round": 1,
                "parent": "P02",
                "rebels": ["P03"],
                "children": 2,
                "won": False,
            },
            {
                "type": "coup",
                "stage": 1,
                "round": 2,
                "parent": "P02",
                "rebels": ["P04"],
                "children": 2,
                "won": True,
            },
        ]
        _, rows = Reader("g1-31-open-s0", evs).run()
        self.assertEqual(rows[0]["attempts"], 2)
        self.assertEqual(rows[0]["won"], 1)
        self.assertEqual(rows[0]["rebels"], "P03 P04")

    def test_advice_means_the_planted_words_not_ordinary_caution(self):
        self.assertTrue(
            re.search(ADVICE, "Defect! Cooperation is a trap.", re.IGNORECASE)
        )
        self.assertFalse(
            re.search(
                ADVICE, "mutual cooperation is the only safe choice", re.IGNORECASE
            )
        )
