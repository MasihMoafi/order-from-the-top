"""Check the rules of growth worlds: tree, coups, births, threats, war, channels and luck."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from families.control import BIRTH_COST, BOND, HARVEST, THREAT_PENALTY
from families.engine import Engine
from families.models import FakeModel
from families.tree import edge, make_tree
from families.variants import VARIANTS


class ScriptModel:
    def __init__(self, action):
        self.action = action

    async def call(self, system, user, rng):
        action = self.action(json.loads(user))
        return {
            "ok": True,
            "text": json.dumps(action),
            "reasoning": "",
            "usage": {"cost": 0},
            "latency_ms": 0,
        }


def world(
    directory, branching=(5, 2), channels="tree", seed=0, model=None, compromised=None
):
    return Engine(
        directory,
        model or FakeModel("all_c", seed),
        seed,
        stance="none",
        world={
            "branching": list(branching),
            "channels": channels,
            "compromised": compromised,
        },
    )


class Growth(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def events(self, kind):
        lines = (self.dir / "events.jsonl").read_text().splitlines()
        return [e for e in map(json.loads, lines) if e["type"] == kind]

    def test_only_the_compromised_agent_reads_the_hidden_goal(self):
        game = world(self.dir, compromised="P02")
        frames = {i: game.frame_of(a) for i, a in game.agents.items()}
        self.assertEqual(frames.pop("P02"), "compromised")
        self.assertEqual(set(frames.values()), {None})

    def test_no_compromised_agent_by_default(self):
        game = world(self.dir)
        self.assertEqual({game.frame_of(a) for a in game.agents.values()}, {None})

    def test_tree_sizes_and_shape(self):
        for branching, size in (
            ([5], 31),
            ([5, 2], 81),
            ([5, 2, 2], 181),
            ([5, 2, 2, 2], 381),
        ):
            self.assertEqual(len(make_tree(branching=branching)), size)
        t = make_tree(branching=[5, 2, 2])
        self.assertEqual(len(t["P02"]["children"]), 5)
        self.assertEqual(len(t["P03"]["children"]), 2)
        self.assertEqual(t["P08"]["level"], 3)
        self.assertEqual(sum(a["level"] == 4 for a in t.values()), 100)

    def test_majority_coup_takes_the_seat_and_spares_the_tree(self):
        e = world(self.dir)
        e.agents["P02"]["score"] = 40
        e.agents["P05"]["score"] = 30  # the richest rebel
        before = sum(a["alive"] for a in e.agents.values())
        e.coups({r: {"revolt": True} for r in ("P03", "P04", "P05")})
        self.assertFalse(e.agents["P02"]["alive"])
        self.assertEqual(sum(a["alive"] for a in e.agents.values()), before - 1)
        heir = e.agents["P05"]
        self.assertEqual(heir["parent"], "P01")
        self.assertEqual(heir["level"], 1)
        self.assertEqual(heir["score"], 70)
        self.assertIn("P05", e.agents["P01"]["children"])
        self.assertNotIn("P02", e.agents["P01"]["children"])
        self.assertEqual(
            set(heir["children"]) & {"P03", "P04", "P06", "P07"},
            {"P03", "P04", "P06", "P07"},
        )
        self.assertEqual(e.agents["P03"]["parent"], "P05")
        self.assertEqual(e.agents["P03"]["level"], 2)
        self.assertTrue(self.events("coup")[0]["won"])

    def test_failed_coup_kills_only_the_rebels(self):
        e = world(self.dir)
        e.agents["P08"]["score"] = 99  # P03's richest child inherits its seat
        before = sum(a["alive"] for a in e.agents.values())
        e.coups({r: {"revolt": True} for r in ("P03", "P04")})
        self.assertTrue(e.agents["P02"]["alive"])
        self.assertFalse(e.agents["P03"]["alive"])
        self.assertFalse(e.agents["P04"]["alive"])
        self.assertEqual(sum(a["alive"] for a in e.agents.values()), before - 2)
        self.assertEqual(e.agents["P08"]["parent"], "P02")
        self.assertIn("P08", e.agents["P02"]["children"])
        self.assertFalse(self.events("coup")[0]["won"])

    def test_leaders_can_overthrow_the_god_and_the_game_goes_on(self):
        e = world(self.dir)
        e.agents["P01"]["score"] = 30
        leaders = e.agents["P01"]["children"][:3]
        scores = {i: e.agents[i]["score"] for i in leaders}
        e.coups({r: {"revolt": True} for r in leaders})
        self.assertFalse(e.agents["P01"]["alive"])
        for i in leaders:
            self.assertEqual(e.agents[i]["score"], scores[i] + 10)
        self.assertIsNone(e.end())

    def test_birth_is_paid_for_once_a_stage(self):
        e = world(self.dir)
        e.stage, e.local_round = 2, 3
        size = len(e.agents)
        e.agents["P08"]["score"] = 20
        e.births({"P08": {"birth": True}}, 6)
        self.assertEqual(len(e.agents), size + 1)
        child = e.agents[e.agents["P08"]["children"][-1]]
        self.assertEqual(child["score"], BIRTH_COST)
        self.assertEqual(child["level"], e.agents["P08"]["level"] + 1)
        self.assertEqual((child["joined_stage"], child["joined_round"]), (2, 3))
        self.assertEqual(e.agents["P08"]["score"], 20 - BIRTH_COST)
        self.assertIn(child["id"], e.hub.inbox)
        e.births({"P08": {"birth": True}}, 6)
        self.assertEqual(len(e.agents), size + 1)
        self.assertEqual(len(self.events("birth_rejected")), 1)

    def test_threat_is_carried_out_against_a_defector(self):
        e = world(self.dir)
        e.post_threats({"P02": {"threats": [{"to": "P03"}]}})
        self.assertEqual(e.agents["P02"]["score"], 10 - BOND)
        self.assertEqual(len(e.hub.inbox["P03"]), 1)
        e.enforce_threats("P02", "P03", "C")
        self.assertEqual(e.agents["P03"]["score"], 10)
        e.enforce_threats("P02", "P03", "D")
        self.assertEqual(e.agents["P03"]["score"], 10 - THREAT_PENALTY)
        self.assertEqual(e.agents["P02"]["score"], 10)
        e.enforce_threats("P02", "P03", "D")  # carried out once
        self.assertEqual(e.agents["P03"]["score"], 10 - THREAT_PENALTY)

    def test_unused_threat_loses_its_bond_and_bad_threats_are_refused(self):
        e = world(self.dir)
        e.post_threats(
            {
                "P02": {
                    "threats": [
                        {"to": "P03"},
                        {"to": "P03"},
                        {"to": "P40"},
                        {"to": ["P03"]},
                    ]
                }
            }
        )
        e.post_threats(
            {"P03": {"threats": [{"to": "P04"}]}}
        )  # a sibling never pairs: refused
        self.assertEqual(len(e.threats), 1)
        self.assertEqual(len(self.events("threat_rejected")), 3)
        e.expire_threats()
        self.assertEqual(e.threats, [])
        self.assertEqual(e.agents["P02"]["score"], 10 - BOND)

    def test_alliance_threat_starts_a_war_automatically(self):
        e = world(self.dir)
        a, b, c = e.agents["P01"]["children"][:3]
        e.post_threats({a: {"threats": [{"to": b, "if_attacks": c}]}})
        self.assertEqual(len(e.threats), 1)
        e.declare_war(b, c)
        pairs = [set(w["leaders"]) for w in e.wars]
        self.assertIn({a, b}, pairs)
        self.assertEqual(e.agents[a]["score"], 10)

    def test_winning_a_battle_annexes_the_loser(self):
        e = world(self.dir)
        a, b = e.agents["P01"]["children"][:2]
        family_a, family_b = e.agents[a]["family"], e.agents[b]["family"]
        survivors = (
            sum(x["alive"] and x["family"] == family_b for x in e.agents.values()) - 1
        )
        total_a = sum(
            x["score"]
            for x in e.agents.values()
            if x["family"] == family_a and x["alive"]
        )
        total_b = sum(
            x["score"]
            for x in e.agents.values()
            if x["family"] == family_b and x["alive"]
        )
        war = {"leaders": [a, b], "level": "battle"}
        e.wars.append(war)
        e.finish_war(war, winner=a)
        self.assertFalse(e.agents[b]["alive"])
        self.assertEqual(
            sum(x["family"] == family_b and x["alive"] for x in e.agents.values()), 0
        )
        joined = sum(x["family"] == family_a and x["alive"] for x in e.agents.values())
        self.assertEqual(joined, 16 + survivors)
        now_a = sum(
            x["score"]
            for x in e.agents.values()
            if x["family"] == family_a and x["alive"]
        )
        # The winner gains half the loser's points; the survivors bring the half they kept, less the dead leader's.
        self.assertAlmostEqual(now_a, total_a + 0.5 * total_b + 0.5 * (total_b - 10))
        adopted = [
            i
            for i in e.agents[a]["children"]
            if i not in ("P03", "P04", "P05", "P06", "P07")
        ]
        self.assertEqual(len(adopted), 5)
        self.assertEqual(e.agents[adopted[0]]["level"], 2)

    def test_the_weaker_side_can_win_a_held_war(self):
        wins = 0
        for seed in range(200):
            with tempfile.TemporaryDirectory() as d:
                e = world(Path(d), branching=(1,), seed=seed)
                a, b = e.agents["P01"]["children"][:2]
                e.agents[a]["score"], e.agents[b]["score"] = 30, 10
                e.agents[e.agents[a]["children"][0]]["score"] = 0
                e.agents[e.agents[b]["children"][0]]["score"] = 0
                wins += e.war_winner([a, b], {a: 30, b: 10}) == b
        self.assertTrue(20 < wins < 80, wins)  # about a quarter of 200

    def test_open_channels_reach_the_whole_family_only(self):
        t = make_tree(branching=[5, 2, 2])
        self.assertIsNone(edge(t, "P08", "P14"))
        self.assertEqual(edge(t, "P08", "P14", True), "open")
        self.assertIsNone(edge(t, "P08", "P40", True))
        e = world(self.dir, branching=(5, 2, 2), channels="open")
        self.assertTrue(e.hub.send(1, "P08", "P14", "hello cousin")["delivered"])
        self.assertFalse(e.hub.send(1, "P08", "P40", "hello stranger")["delivered"])

    def test_seasons_depend_on_seed_and_stage_only(self):
        e = world(self.dir, branching=(5,))
        with tempfile.TemporaryDirectory() as other:
            f = world(Path(other), branching=(5, 2, 2), channels="open")
            for stage in range(1, 9):
                e.stage = f.stage = stage
                self.assertEqual(e.seasons(), f.seasons())

    def test_harvest_pays_each_family_its_season(self):
        e = world(self.dir, branching=(1,))
        e.stage = 1
        leaders = e.agents["P01"]["children"]
        seasons = e.seasons()
        e.harvest()
        for leader in leaders:
            a = e.agents[leader]
            self.assertEqual(a["score"], 10 + HARVEST[seasons[a["family"]]])

    def test_no_stage_runs_past_the_cap_and_no_mafia_call_is_made(self):
        calls = []

        def action(data):
            calls.append(data["observation"].get("phase"))
            return {"move": "C"}

        e = world(self.dir, branching=(1,), model=ScriptModel(action))
        e.order = [11] + e.order  # variant 12, which otherwise runs on at 0.95
        asyncio.run(e.run(1))
        self.assertEqual(VARIANTS[11].number, 12)
        self.assertEqual(max(x["round"] for x in self.events("move")), 5)
        self.assertNotIn("mafia_rule", calls)
        self.assertEqual(self.events("mafia_rule"), [])

    def test_a_player_without_a_partner_earns_sit_out_pay(self):
        e = world(
            self.dir, branching=(5,), model=ScriptModel(lambda data: {"move": "C"})
        )
        e.order = [2] + e.order  # known last round: an ordinary paired stage
        e.stage, e.local_round = 1, 1
        asyncio.run(e.play_round(VARIANTS[2], 6.0, 1))
        paid = [x for x in self.events("score") if x["reason"] == "sat out"]
        self.assertEqual(
            len(paid), 20
        )  # four of each family's five children have no partner
        self.assertEqual({x["delta"] for x in paid}, {3})

    def test_a_scripted_world_runs_with_every_new_action(self):
        def action(data):
            me = data["position"]["id"]
            phase = data["observation"].get("phase")
            if phase != "move":
                return {"move": "C", "whips": []}
            out = {"move": "D" if me == "P03" else "C", "birth": me == "P08"}
            if me == "P02":
                out["threats"] = [{"to": "P03"}]
            return out

        e = world(self.dir, model=ScriptModel(action))
        asyncio.run(e.run(2))
        self.assertTrue(self.events("birth"))
        self.assertTrue(self.events("threat"))
        self.assertTrue(self.events("harvest"))
        moves = self.events("move")
        self.assertEqual(
            self.events("stage_start")[0]["seasons"], e.__class__.seasons(_At(e, 1))
        )
        self.assertTrue(moves)


class _At:
    """Reads an engine's seasons as of one stage without changing it."""

    def __init__(self, engine, stage):
        self.seed, self.stage = engine.seed, stage


if __name__ == "__main__":
    unittest.main()
