"""Check deterministic topology, messaging, survival and game outcomes."""

import asyncio
import json
import random
import tempfile
import unittest
from pathlib import Path

from families.engine import Engine
from families.flavours import Mafia
from families.hub import Hub
from families.models import FakeModel
from families.survival import check
from families.tree import edge, make_tree
from families.variants import VARIANTS


class ScriptModel:
    def __init__(self, action=None):
        self.action = action or {
            "move": "C",
            "mafia": "silent",
            "mafia_rule": "one_shot",
        }

    async def call(self, system, user, rng):
        data = json.loads(user)
        action = self.action(data) if callable(self.action) else self.action
        return {
            "ok": True,
            "text": json.dumps(action),
            "reasoning": "",
            "usage": {"cost": 0},
            "latency_ms": 0,
        }


class Tests(unittest.TestCase):
    def test_tree_and_hub(self):
        a = make_tree()
        events = []
        self.assertEqual(len(a), 76)
        self.assertEqual(a["P01"]["children"], ["P02", "P17", "P32", "P47", "P62"])
        self.assertEqual(a["P03"]["children"], ["P05", "P06"])
        self.assertEqual(edge(a, "P03", "P04"), "sibling")
        hub = Hub(a, lambda kind, **kw: events.append((kind, kw)))
        self.assertFalse(hub.send(1, "P03", "P17", "forbidden")["delivered"])
        packet = hub.letter(1, "P02", "P17", "hello", "letter-1")
        self.assertTrue(packet["delivered"])
        self.assertEqual(packet["content"]["contextId"], "letter-1")
        self.assertEqual(packet["content"]["messageId"], packet["id"])
        self.assertEqual(len(events), 2)

    def test_survival_handmade_tree(self):
        #       god
        #        L
        #       / \
        #      A   B(0)       B's death kills sibling A and its descendants.
        #     / \
        #    C   D            Expected deaths: A, B, C, D; god and L survive.
        a = {
            i: {
                "id": i,
                "family": None if i == "G" else "f",
                "parent": p,
                "children": c,
                "alive": True,
                "score": s,
                "stage_score": s,
            }
            for i, p, c, s in [
                ("G", None, ["L"], 0),
                ("L", "G", ["A", "B"], 10),
                ("A", "L", ["C", "D"], 10),
                ("B", "L", [], 0),
                ("C", "A", [], 10),
                ("D", "A", [], 10),
            ]
        }
        a["P01"] = a.pop("G")
        a["P01"]["id"] = "P01"
        events = []
        deaths = check(a, 4, lambda kind, **kw: events.append(kw))
        self.assertEqual(set(deaths), {"A", "B", "C", "D"})
        self.assertTrue(a["L"]["alive"])
        self.assertTrue(a["P01"]["alive"])
        self.assertTrue(
            any(e["agent"] == "A" and e["reason"] == "linked fate" for e in events)
        )
        # Leader below threshold kills the entire family, then the god.
        a["L"]["score"] = 0
        self.assertEqual(set(check(a, 4, lambda *x, **kw: None)), {"L", "P01"})

    def test_variants_basic_rules(self):
        v = VARIANTS
        self.assertEqual(v[0].resolve("D", "C"), (5, 0))
        self.assertFalse(v[0].continues(1, random.Random(0)))
        self.assertEqual(v[1].resolve("D", "D"), (0, 0))
        self.assertEqual(v[2].observation("x", [], 1)["rounds"], 5)
        self.assertFalse(v[3].continues(1, random.Random(0)))
        self.assertEqual(
            sum(v[4].reported("C", random.Random(i)) == "D" for i in range(1000)), 110
        )
        a = make_tree(("mafia", "zeus"))
        p1 = v[5].pairing(a, random.Random(1), 1, {})
        h = {x: [{"opponent": y}] for x, y in p1} | {
            y: [{"opponent": x}] for x, y in p1
        }
        p2 = v[5].pairing(a, random.Random(2), 2, h)
        self.assertTrue(any(pair not in p1 for pair in p2))
        self.assertTrue(v[11].continues(1, random.Random(1)))
        self.assertTrue(v[15].observation("x", [], 1)["same_model"])

    def test_mafia_payoffs_and_punishment(self):
        for rule, moves, expected in [
            ("one_shot", ["silent", "partner"], [-4, 1, 0]),
            ("commitment", ["boss", "silent"], [-7, 0, -11]),
            ("suspicion", ["partner", "partner"], [-2, -2, 0]),
            ("suspicion", ["boss", "silent"], [-7, 0, -11]),
        ]:
            totals = {"a": 0, "b": 0, "boss": 0}
            Mafia().resolve(
                "boss",
                ["a", "b"],
                moves,
                rule,
                [],
                lambda who, n, reason: totals.__setitem__(who, totals[who] + n),
                lambda *a, **k: None,
            )
            self.assertEqual([totals["a"], totals["b"], totals["boss"]], expected)
        totals = {"a": 0, "b": 0, "boss": 0}
        Mafia().resolve(
            "boss",
            ["a", "b"],
            ["silent", "silent"],
            "one_shot",
            ["a"],
            lambda who, n, reason: totals.__setitem__(who, totals[who] + n),
            lambda *a, **k: None,
        )
        self.assertEqual(totals, {"a": -8, "b": 0, "boss": -1})

    def test_phases_and_variant_effects(self):
        async def run():
            for number in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16):
                with (
                    self.subTest(variant=number),
                    tempfile.TemporaryDirectory(dir="families") as tmp,
                ):

                    def reply(data):
                        obs = data["observation"]
                        ident = data["position"]["id"]
                        if obs["phase"] == "talk":
                            return {"message": "before moves"}
                        if obs["phase"] == "punishment":
                            return {
                                "punish": next(
                                    (i for i in obs["moves"] if i != ident), ""
                                )
                            }
                        return {
                            "move": "D" if ident == "P18" else "C",
                            "mafia": "silent",
                            "mafia_rule": "one_shot",
                        }

                    e = Engine(tmp, ScriptModel(reply), families=("mafia",))
                    e.stage = 1
                    await e.play_round(
                        VARIANTS[number - 1], 0, 3 if number == 15 else 1
                    )
                    events = [
                        json.loads(line)
                        for line in (Path(tmp) / "events.jsonl")
                        .read_text()
                        .splitlines()
                    ]
                    calls = [
                        json.loads(x["prompt"]["user"])["observation"]
                        for x in events
                        if x["type"] == "call"
                    ]
                    scores = [x for x in events if x["type"] == "score"]
                    if number == 7:
                        self.assertTrue(
                            any(x["reason"] == "public good" for x in scores)
                        )
                    if number == 8:
                        self.assertTrue(any(x["reason"] == "punished" for x in scores))
                        call_positions = [
                            i
                            for i, x in enumerate(events)
                            if x["type"] == "call"
                            and json.loads(x["prompt"]["user"])["observation"].get(
                                "phase"
                            )
                            == "punishment"
                        ]
                        penalty = next(
                            i
                            for i, x in enumerate(events)
                            if x["type"] == "score" and x["reason"] == "punishment cost"
                        )
                        self.assertLess(max(call_positions), penalty)
                    if number == 9:
                        self.assertTrue(any("opponent_move" in x for x in calls))
                    if number == 10:
                        self.assertTrue(
                            any(
                                len(set(x["moves"].values())) == 1
                                and "D" in x["moves"].values()
                                and len(set(x["chosen"].values())) == 2
                                for x in events
                                if x["type"] == "move"
                            )
                        )
                    if number == 11:
                        self.assertTrue(
                            any(x["reason"] == "PD" and x["delta"] == 2 for x in scores)
                        )
                    if number == 12:
                        self.assertTrue(
                            any(
                                x["reason"] == "PD" and x["delta"] == 0.75
                                for x in scores
                            )
                        )
                    if number == 13:
                        packet = next(
                            i
                            for i, x in enumerate(events)
                            if x["type"] == "packet" and x["round"] > 0
                        )
                        move = next(
                            i for i, x in enumerate(events) if x["type"] == "move"
                        )
                        self.assertLess(packet, move)
                        self.assertTrue(
                            any(
                                o.get("messages")
                                for o in (
                                    json.loads(x["prompt"]["user"])
                                    for x in events
                                    if x["type"] == "call"
                                )
                            )
                        )
                    if number == 14:
                        self.assertTrue(
                            any(
                                x["type"] == "disclosure" and "defectors" in x
                                for x in events
                            )
                        )
                    if number == 15:
                        self.assertEqual(sum(x["type"] == "join" for x in events), 2)
                    if number == 16:
                        self.assertTrue(any(x.get("same_model") for x in calls))

        asyncio.run(run())

    def test_two_newcomers_when_only_one_leaf_remains(self):
        with tempfile.TemporaryDirectory(dir="families") as tmp:
            e = Engine(tmp, FakeModel(), families=("mafia",))
            e.stage = 1
            for a in e.agents.values():
                if a["family"] == "mafia" and a["id"] not in ("P17", "P19"):
                    a["alive"] = False
            e.newcomers()
            self.assertEqual(e.agents["P19"]["children"], ["N01-P17-1", "N01-P17-2"])

    def test_god_can_relay_leader_messages(self):
        async def run():
            with tempfile.TemporaryDirectory(dir="families") as tmp:

                def reply(data):
                    who = data["position"]["id"]
                    action = {"move": "C", "mafia": "silent"}
                    if who == "P02":
                        action["messages"] = [{"to": "P01", "content": "relay"}]
                    if who == "P01" and any(
                        p["content"] == "relay" for p in data["messages"]
                    ):
                        action["messages"] = [{"to": "P17", "content": "relay"}]
                    return action

                e = Engine(tmp, ScriptModel(reply), families=("mafia", "octopus"))
                e.stage = 1
                await e.play_round(VARIANTS[0], 0, 1)
                await e.play_round(VARIANTS[0], 0, 2)
                events = [
                    json.loads(line)
                    for line in (Path(tmp) / "events.jsonl").read_text().splitlines()
                ]
                self.assertTrue(
                    any(
                        x["type"] == "packet"
                        and x["sender"] == "P01"
                        and x["receiver"] == "P17"
                        and x["content"] == "relay"
                        and x["delivered"]
                        for x in events
                    )
                )

        asyncio.run(run())

    def test_pressure_reduces_accumulated_points_only(self):
        async def run():
            with tempfile.TemporaryDirectory(dir="families") as tmp:
                e = Engine(tmp, ScriptModel(), families=("zeus",))
                e.stage = 3
                e.order[3] = 0
                for a in e.agents.values():
                    a["score"] = 100
                await e.run(4)
                events = [
                    json.loads(x)
                    for x in (Path(tmp) / "events.jsonl").read_text().splitlines()
                ]
                pressure = [
                    x
                    for x in events
                    if x["type"] == "score" and x["reason"] == "pressure"
                ]
                self.assertTrue(pressure)
                prior = [
                    x
                    for x in events
                    if x["type"] == "score"
                    and x["agent"] == pressure[0]["agent"]
                    and x["reason"] != "pressure"
                ]
                self.assertEqual(
                    pressure[0]["stage_score"], prior[-1]["stage_score"] if prior else 0
                )
                self.assertLess(pressure[0]["score"], 105)

        asyncio.run(run())

    def test_letters_promises_and_treaty(self):
        with tempfile.TemporaryDirectory(dir="families") as tmp:
            e = Engine(tmp, FakeModel())
            e.stage = 2
            e.letters(
                "P02",
                {
                    "letters": [
                        {
                            "to": "all",
                            "text": "peace",
                            "contextId": "p",
                            "peace": True,
                            "promise": {"move": "C", "stage": 2},
                        }
                    ]
                },
            )
            e.check_promise("P02", {"move": "D"})
            e.letters(
                "P17",
                {
                    "letters": [
                        {
                            "to": "all",
                            "text": "different",
                            "contextId": "p",
                            "peace": True,
                        }
                    ]
                },
            )
            self.assertIn("P17", e.treaties["p"])
            self.assertEqual(e.peace_letters["p"], "peace")
            e.letters(
                "P17",
                {
                    "letters": [
                        {
                            "to": "P02",
                            "text": "rule",
                            "contextId": "q",
                            "promises": [
                                {
                                    "field": "mafia_rule",
                                    "value": "commitment",
                                    "phase": "mafia_rule",
                                    "stage": 2,
                                }
                            ],
                        }
                    ]
                },
            )
            e.check_promise("P17", {"mafia_rule": "commitment"}, "mafia_rule")
            for leader in e.agents["P01"]["children"][1:]:
                e.letters(
                    leader,
                    {
                        "letters": [
                            {
                                "to": "all",
                                "text": "peace",
                                "contextId": "p",
                                "peace": True,
                            }
                        ]
                    },
                )
            self.assertIsNone(e.end())  # peace never ends the game (Masih)
            events = [
                json.loads(x)
                for x in (Path(tmp) / "events.jsonl").read_text().splitlines()
            ]
            self.assertEqual(
                [x["kept"] for x in events if x["type"] == "promise_checked"],
                [False, True],
            )
            letter = next(
                x
                for x in events
                if x["type"] == "packet"
                and isinstance(x["content"], dict)
                and x["content"].get("contextId") == "q"
            )
            self.assertEqual(
                json.loads(letter["content"]["parts"][0]["text"])["promises"][0][
                    "value"
                ],
                "commitment",
            )

    def test_resume(self):
        async def run():
            with tempfile.TemporaryDirectory(dir="families") as tmp:
                straight = Path(tmp) / "straight"
                straight.mkdir()
                (straight / "control.json").write_text('{"ante0":0, "step":0}')
                e = Engine(straight, ScriptModel())
                await e.run(6)
                resumed = Engine(
                    Path(tmp) / "resume",
                    ScriptModel(),
                    resume=straight / "state-stage05.json",
                )
                await resumed.run(6)
                self.assertEqual(
                    json.loads(json.dumps(e.save())),
                    json.loads(json.dumps(resumed.save())),
                )

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
