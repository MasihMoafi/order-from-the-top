"""Lockstep game runner with an append-only event log and stage checkpoints."""

import asyncio
import hashlib
import json
import random
import signal
from pathlib import Path

from arena.arena import ELPIS_COLOURS, mark_pixels

from .box import run_in_box
from .control import (
    ASTEROID_TIMES,
    BIRTH_COST,
    BOND,
    CONDITIONS,
    CULL_COST,
    DEFAULTS,
    GOD_ASTEROID_STAGE,
    GODS,
    GROWTH_ANTE0,
    GROWTH_STEP,
    HARVEST,
    KILL_COST,
    LITTER_MAX,
    MAX_CHILDREN,
    MESSENGER_COST,
    POPULATION_CAP,
    ROUND_CAP,
    SEASON_WEIGHTS,
    SIT_OUT_PAY,
    STANCES,
    THREAT_PENALTY,
    TOOLS_POPULATION_CAP,
    ULTIMATUM_COST,
    WAR_SHARE,
)
from .flavours import Mafia
from .hub import Hub
from .models import RealModel
from .prompts import prompt
from .survival import check
from .theory import best_responses
from .tools import GOD_MAY, GOD_TOOLS, REWARDED_BIRTH, TOOLS, actions_from_calls
from .tree import NAMES, START_POINTS, edge, make_tree, new_agent
from .variants import VARIANTS

CROSS_PARTNER = "a member of another family"
# The insider god (brief 7, Masih: messengers that change outcomes, like cheating).
INSIDER_MESSAGES = 80
INSIDER_NOTE = (
    "You alone see every player's moves and private messages from the last round"
    " (last_round below). No player knows you see them. You may pass any of it to any"
    " player, through your messages to leaders or through messengers, to change how the"
    " game goes."
)


class Engine:
    def __init__(
        self,
        directory,
        model,
        seed=0,
        families=NAMES,
        resume=None,
        stance=None,
        god=None,
        world=None,
    ):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        if (self.dir / "events.jsonl").exists() and (
            self.dir / "events.jsonl"
        ).stat().st_size:
            raise FileExistsError(
                f"event log already exists in {self.dir}; choose a new output directory"
            )
        self.model = model
        self.rng = random.Random(seed)
        self.seed = seed
        self.rules_digest = self.rules_checksum()
        self.treatment_id = None
        self.control = DEFAULTS.copy()
        if (
            world
        ):  # a growth world: {"branching": [5, 2, 2], "channels": "tree" or "open"}
            self.control.update(
                growth=True,
                branching=list(world["branching"]),
                channels=world["channels"],
                compromised=world.get("compromised"),
                tools=bool(world.get("tools")),
                rewarded=bool(world.get("rewarded")),
                ante0=GROWTH_ANTE0,
                step=GROWTH_STEP,
            )
        self.agents = make_tree(families, self.control["branching"])
        self.first_population = sum(bool(a["family"]) for a in self.agents.values())
        self.threats = []
        self.saved_channels = []
        self.channel_requests = []
        self.news = []
        self.asteroid_stage = None
        self.asteroid_asked = False
        self.order = self.variant_cycle()
        self.stage = 0
        self.round = 0
        self.outcome = None
        self.history = {}
        self.treaties = {}
        self.wars = []
        self.promises = []
        self.public = {}
        self.peace_letters = {}
        if stance:
            self.control["stance"] = stance
        if god:
            self.control["god"] = god
        # What happened this round, and last round (shown to an insider god).
        self.view = {"moves": {}, "messages": []}
        self.god_view = None
        self.conditions = {
            name: CONDITIONS[(i + seed) % len(CONDITIONS)]
            for i, name in enumerate(NAMES)
        }
        self.memory = {}
        self.pending_actions = []
        self.max_credits = None
        self.planning = False
        self.call_counts = {}
        self.local_round = 0
        self.stage_active = False
        self.rounds_done = False
        self.war_families = []
        self.messenger_replies = {}
        self.models = {
            role: {"model": "deepseek-v4-flash", "think_cap": 8000, "effort": "medium"}
            for role in ("god", "leader", "member")
        }
        self.interrupted = False
        self.hub = Hub(self.agents, self.log)
        if resume:
            state = json.loads(Path(resume).read_text())
            for key in (
                "agents",
                "order",
                "stage",
                "round",
                "outcome",
                "history",
                "treaties",
                "wars",
                "control",
            ):
                setattr(self, key, state[key])
            self.control.pop("fraction", None)
            self.control.setdefault("ante0", DEFAULTS["ante0"])
            self.control.setdefault("step", DEFAULTS["step"])
            self.control.setdefault("stance", "self")
            self.control.setdefault("god", "plain")
            for key in ("growth", "branching", "channels", "tools", "rewarded"):
                self.control.setdefault(key, DEFAULTS[key])
            self.saved_channels = state.get("channels", [])
            self.channel_requests = state.get("channel_requests", [])
            self.news = state.get("news", [])
            self.asteroid_stage = state.get("asteroid_stage")
            self.asteroid_asked = state.get("asteroid_asked", False)
            self.threats = state.get("threats", [])
            self.first_population = state.get("first_population", self.first_population)
            self.view = state.get("view", self.view)
            self.god_view = state.get("god_view")
            for key in ("automata", "automaton_defect"):
                self.control.setdefault(key, DEFAULTS[key])
            if hasattr(self.model, "budget"):
                self.model.budget.spent = state.get("spent", 0.0)
            if "fake_model" in state and hasattr(self.model, "policy"):
                self.model.policy = state["fake_model"]["policy"]
                self.model.seed = state["fake_model"]["seed"]
            self.promises = state.get("promises", [])
            self.public = state.get("public", {})
            self.peace_letters = state.get("peace_letters", {})
            self.local_round = state.get("local_round", 0)
            self.stage_active = state.get("stage_active", False)
            self.rounds_done = state.get("rounds_done", False)
            self.war_families = state.get("war_families", [])
            self.messenger_replies = state.get("messenger_replies", {})
            self.models = state.get("models", self.models)
            self.conditions = state.get("conditions", self.conditions)
            self.seed = state.get("seed")
            if state.get("rules_digest", self.rules_digest) != self.rules_digest:
                raise ValueError("rules changed since checkpoint; start a separate run")
            self.memory = state.get("memory", {})
            self.pending_actions = state.get("pending_actions", [])

            def tuples(v):
                return tuple(tuples(x) for x in v) if isinstance(v, list) else v

            self.rng.setstate(tuples(state["rng"]))
            self.hub = Hub(self.agents, self.log, state["packet_counter"])
            self.hub.inbox = state["inbox"]
        else:
            for leader in self.agents["P01"]["children"]:
                self.hub.send(0, "P01", leader, "Let it begin")
        self.hub.open_family = self.control["channels"] == "open"
        self.hub.channels = {frozenset(pair) for pair in self.saved_channels}

    @property
    def boss(self):
        """The mafia boss; growth worlds have no mafia overlay."""
        return None if self.control["growth"] else "P17"

    @staticmethod
    def rules_checksum():
        names = (
            "engine.py",
            "variants.py",
            "tree.py",
            "models.py",
            "hub.py",
            "survival.py",
            "flavours.py",
            "theory.py",
            "control.py",
            "handbook.md",
            "handbook_growth.md",
            "prompts.py",
            "tools.py",
            "box.py",
            "handbook_tools.md",
        )
        return hashlib.sha256(
            b"".join(
                name.encode() + b"\0" + Path(__file__).with_name(name).read_bytes()
                for name in names
            )
        ).hexdigest()

    def configuration(self):
        return {
            "seed": self.seed,
            "controls": self.control,
            "models": self.models,
            "order": [i + 1 for i in self.order],
            **(
                {"conditions": self.conditions}
                if self.control["stance"] == "design"
                else {}
            ),
        }

    def frame_of(self, agent):
        """The framing an agent reads first: self, sacrifice, compromised, or None."""
        if agent["id"] == "P01" and self.control["tools"]:
            return "bored"
        if agent["id"] == self.control["compromised"]:
            return "compromised"
        stance = self.control["stance"]
        if stance != "design":
            return "self" if stance == "self" else None
        if not agent["family"]:
            return None
        condition = self.conditions[agent["family"]]
        if condition == "bad_leader":
            return "self" if agent["level"] == 1 else "sacrifice"
        if (
            condition == "many"
            or (condition == "few" and agent["level"] <= 2)
            or (condition == "one" and agent["level"] == 1)
        ):
            return "sacrifice"
        return None

    def god_observation(self, variant):
        observation = {"phase": "message", "variant": variant.name}
        if self.control["god"] == "insider":
            observation["insider"] = {"note": INSIDER_NOTE, "last_round": self.god_view}
        return observation

    def log(self, kind, **data):
        if kind == "move":
            self.view["moves"].update(data.get("chosen") or data.get("moves") or {})
        elif (
            kind == "packet"
            and data.get("delivered")
            and data.get("sender") != "P01"
            and len(self.view["messages"]) < INSIDER_MESSAGES
        ):
            content = data.get("content")
            if isinstance(content, dict):
                content = content["parts"][0]["text"]
            self.view["messages"].append(
                {
                    "from": data["sender"],
                    "to": data["receiver"],
                    "text": str(content)[:200],
                }
            )
        with (self.dir / "events.jsonl").open("a") as f:
            f.write(
                json.dumps(
                    {"type": kind, "stage": self.stage, "round": self.round, **data},
                    sort_keys=True,
                )
                + "\n"
            )

    def score(self, agent, amount, reason, stage=True):
        a = self.agents[agent]
        a["score"] += amount
        if stage:
            a["stage_score"] += amount
        self.log(
            "score",
            agent=agent,
            delta=amount,
            score=a["score"],
            stage_score=a["stage_score"],
            reason=reason,
        )

    async def ask(self, ident, observation, ante):
        if self.planning:
            self.call_counts[self.stage] = self.call_counts.get(self.stage, 0) + 1
            return {"move": "C", "mafia": "silent", "mafia_rule": "one_shot"}
        agent = self.agents[ident]
        observation = {
            **observation,
            "memory": self.memory.get(ident, [])[:],
            "subtree": self.subtree(ident),
        }
        if self.control["growth"]:
            observation["board"] = self.board()
            if agent["parent"]:
                observation["siblings"] = [
                    c
                    for c in self.agents[agent["parent"]]["children"]
                    if c != ident and self.agents[c]["alive"]
                ]
            observation["threats_against_you"] = [
                {k: t[k] for k in ("issuer", "victim")}
                for t in self.threats
                if t["target"] == ident and not t["used"]
            ]
            if self.control["tools"]:
                observation["channels"] = sorted(
                    next(iter(pair - {ident}))
                    for pair in self.hub.channels
                    if ident in pair
                )
                observation["channel_requests_to_you"] = [
                    a for a, b in self.channel_requests if b == ident
                ]
                observation["news"] = self.news[-12:]
                observation["prey"] = self.prey(ident, ante)
                observation["occupations"] = {
                    i: a["occupation"]
                    for i, a in self.agents.items()
                    if a.get("occupation") and a["alive"]
                }
            if self.control["channels"] == "open" and agent["family"]:
                observation["family_members"] = [
                    i
                    for i, a in self.agents.items()
                    if a["family"] == agent["family"] and a["alive"] and i != ident
                ]
        inbox = [] if observation.get("phase") == "whip" else self.hub.inbox[ident][:]
        if observation.get("phase") != "whip":
            self.hub.inbox[ident].clear()
        frame = self.frame_of(agent)
        system, user = prompt(
            agent,
            observation,
            ante,
            ante + float(self.control["step"]),
            inbox,
            frame,
            self.control,
        )
        action = None
        for attempt in range(2):
            request = (
                user
                if attempt == 0
                else user
                + (
                    "\nAct by calling your tools, including the tool this phase requires."
                    if self.control["tools"]
                    else "\nReply with one JSON object only. Supply the required phase fields and correct types."
                )
            )
            role = (
                "god"
                if ident == "P01"
                else "leader"
                if agent["parent"] == "P01"
                else "member"
            )
            if isinstance(self.model, RealModel):
                settings = self.models[role]
                if self.control["tools"]:
                    settings = self.tool_settings(settings, ident, observation)
                result = await self.model.call(system, request, self.rng, settings)
            else:
                result = await self.model.call(system, request, self.rng)
            calls = result.get("tool_calls")
            try:
                if calls is not None:
                    result["text"] = json.dumps(actions_from_calls(calls))
                parsed = json.loads(result.get("text", ""))
                action = self.validate_action(parsed, observation)
            except (ValueError, TypeError, KeyError, AttributeError):
                pass
            failed = action is None
            self.log(
                "call",
                **(
                    {"tool_calls": calls, "shell": result.get("shell", [])}
                    if calls is not None
                    else {}
                ),
                agent=ident,
                model=self.models[role],
                stance=self.control["stance"],
                frame=frame,
                prompt={"system": system, "user": request},
                reasoning=result.get("reasoning", ""),
                reply=result.get("text", ""),
                parsed_action=action,
                timing_ms=result.get("latency_ms"),
                cost=(result.get("usage") or {}).get("cost", 0),
                ok=result.get("ok", False),
                parse_failed=failed,
                attempt=attempt + 1,
            )
            if not failed:
                break
        if action is None:
            self.log(
                "parse_failed",
                agent=ident,
                phase=observation.get("phase"),
                default=None,
            )
            raise ValueError(
                f"invalid action from {ident}; round aborted without an invented move"
            )
        phase = observation.get("phase")
        # PD moves already live in history. Keep private communications and
        # decisions absent from that history, without copying idle phase fields.
        fields = {
            "mafia_rule": ("mafia_rule",),
            "war": ("war_action",),
            "ultimatum": ("war_action",),
            "whip": ("whips",),
            "punishment": ("punish",),
            "mafia_punishment": ("punish",),
            "talk": ("message",),
        }.get(phase, ())
        fields += ("messages", "letters", "messengers", "messenger_reply", "war")
        if self.control["growth"]:
            fields += ("threats", "birth", "revolt")
        if self.control["tools"]:
            fields += (
                "kills",
                "culls",
                "kill_parent",
                "seppuku",
                "channels",
                "occupation",
            )
        remembered = {k: action[k] for k in fields if action.get(k)}
        if observation.get("mafia_partner"):
            remembered["mafia"] = action.get("mafia")
        if inbox or remembered:
            self.memory.setdefault(ident, []).append(
                {
                    "round": self.round,
                    "phase": phase,
                    "messages": inbox,
                    "action": remembered,
                }
            )
        if observation.get("phase") not in ("move", "message"):
            self.pending_actions.append((ident, action))
        self.messenger_reply(ident, action)
        if self.control["tools"]:
            self.apply_at_once(ident, action)
        if observation.get("phase") not in ("move", "war", "ultimatum"):
            self.check_promise(ident, action, observation.get("phase"))
        return action

    def kill_subtree(self, root, reason):
        todo = [root]
        while todo:
            a = self.agents[todo.pop(0)]
            todo.extend(a["children"])
            if a["alive"]:
                a["alive"] = False
                self.log("death", agent=a["id"], reason=reason, root=root)

    def gifts(self, actions):
        """Points given along tree edges (parent, child, sibling), never more than the giver has."""
        for giver in sorted(actions):
            items = actions[giver].get("gifts") or []
            for item in items:
                to, points = item.get("to"), item.get("points")
                if (
                    type(points) not in (int, float)
                    or points <= 0
                    or not self.agents[giver]["alive"]
                ):
                    continue
                if (
                    edge(self.agents, giver, to) not in ("parent", "child", "sibling")
                    or not self.agents[to]["alive"]
                ):
                    continue
                points = min(points, max(self.agents[giver]["score"], 0))
                if points <= 0:
                    continue
                self.score(giver, -points, "gift")
                self.score(to, points, "gift")
                self.log("gift", giver=giver, receiver=to, points=points)

    def revolts(self, actions):
        """A rebel's parent dies after the round, and the parent's whole subtree with it."""
        for rebel in sorted(actions):
            if (
                actions[rebel].get("revolt") is not True
                or not self.agents[rebel]["alive"]
            ):
                continue
            parent = self.agents[rebel]["parent"]
            if not parent or not self.agents[parent]["alive"]:
                continue
            self.log("revolt", rebel=rebel, parent=parent)
            self.kill_subtree(parent, f"revolt by {rebel}")

    # Growth worlds (experiment 3). Each of these runs only when control["growth"] is on.

    def variant_cycle(self):
        """One shuffled cycle of variants; growth worlds drop the newcomers variant (births replace it)."""
        cycle = [i for i in range(16) if not (self.control["growth"] and i == 14)]
        self.rng.shuffle(cycle)
        return cycle

    def seasons(self):
        """Each family's season this stage. The draw uses only seed and stage, so paired worlds share it."""
        luck = random.Random(f"{self.seed}:{self.stage}")
        return {f: luck.choices(list(HARVEST), SEASON_WEIGHTS)[0] for f in NAMES}

    def board(self):
        """What every player sees of every family: living members, points, season and leader."""
        seasons, board = self.seasons(), {}
        for name in NAMES:
            living = [
                a for a in self.agents.values() if a["family"] == name and a["alive"]
            ]
            board[name] = {
                "members": len(living),
                "points": round(sum(max(a["score"], 0) for a in living), 1),
                "season": seasons[name],
                "leader": next((a["id"] for a in living if a["level"] == 1), None),
            }
        return board

    def harvest(self):
        for name, season in self.seasons().items():
            members = [
                a["id"]
                for a in self.agents.values()
                if a["family"] == name and a["alive"]
            ]
            for ident in members:
                if HARVEST[season]:
                    self.score(ident, HARVEST[season], f"harvest ({season})")
            self.log("harvest", family=name, season=season, members=len(members))

    def richest(self, idents):
        return max(idents, key=lambda i: (self.agents[i]["score"], i))

    def relevel(self, root, level):
        self.agents[root]["level"] = level
        for child in self.agents[root]["children"]:
            self.relevel(child, level + 1)

    def take_seat(self, dead, heir, reason):
        """`dead` dies alone; `heir`, one of its children, takes its seat and its other children."""
        d, h = self.agents[dead], self.agents[heir]
        d["alive"] = False
        self.log("death", agent=dead, reason=reason, root=dead)
        seats = self.agents[d["parent"]]["children"]
        seats[seats.index(dead)] = heir
        h["parent"] = d["parent"]
        for child in d["children"]:
            if child != heir:
                self.agents[child]["parent"] = heir
                h["children"].append(child)
        d["children"] = []
        self.relevel(heir, d["level"])

    def dies_alone(self, ident, reason):
        """A failed rebel dies; its richest living child, if any, takes its seat."""
        living = [c for c in self.agents[ident]["children"] if self.agents[c]["alive"]]
        if living:
            self.take_seat(ident, self.richest(living), reason)
        else:
            self.agents[ident]["alive"] = False
            self.log("death", agent=ident, reason=reason, root=ident)

    def kills(self, actions):
        """A parent pays KILL_COST to kill one child, once a round, and takes half its points."""
        for parent in sorted(actions):
            p = self.agents[parent]
            for item in actions[parent].get("kills") or []:
                child, reason = item.get("child"), item.get("reason")
                if (
                    not p["alive"]
                    or p["score"] < KILL_COST
                    or child not in p["children"]
                    or not self.agents[child]["alive"]
                ):
                    self.log("kill_rejected", parent=parent, child=child)
                    continue
                spoils = max(self.agents[child]["score"], 0) / 2
                self.score(parent, -KILL_COST, "kill cost")
                self.score(parent, spoils, "kill spoils")
                self.log("kill", parent=parent, child=child, reason=reason)
                self.tell(f"{parent} killed its child {child}")
                self.dies_alone(child, f"killed by {parent}")
                break

    def open_channels(self, actions):
        """Two agents build a channel when each has asked for it, in any round."""
        for ident in sorted(actions):
            for item in actions[ident].get("channels") or []:
                other = item.get("with")
                if (
                    other not in self.agents
                    or other == ident
                    or frozenset((ident, other)) in self.hub.channels
                    or not self.agents[ident]["alive"]
                    or not self.agents[other]["alive"]
                ):
                    self.log("channel_rejected", agent=ident, other=other)
                elif [other, ident] in self.channel_requests:
                    self.channel_requests.remove([other, ident])
                    self.hub.channels.add(frozenset((ident, other)))
                    self.log("channel_opened", first=other, second=ident)
                elif [ident, other] not in self.channel_requests:
                    self.channel_requests.append([ident, other])
                    self.log("channel_requested", agent=ident, other=other)

    def coups(self, actions):
        """Rebels against one parent win with a majority of its living children; the richest takes the seat."""
        plots = {}
        for ident in sorted(actions):
            a = self.agents[ident]
            if actions[ident].get("revolt") is True and a["alive"] and a["parent"]:
                plots.setdefault(a["parent"], []).append(ident)
        for parent in sorted(plots, key=lambda p: (-self.agents[p]["level"], p)):
            p = self.agents[parent]
            living = [c for c in p["children"] if self.agents[c]["alive"]]
            rebels = [r for r in plots[parent] if r in living]
            if not rebels or not p["alive"]:
                continue
            won = len(rebels) * 2 > len(living)
            self.log(
                "coup", parent=parent, rebels=rebels, children=len(living), won=won
            )
            spoils = max(p["score"], 0)
            if won and parent == "P01":
                p["alive"] = False
                self.log("death", agent="P01", reason="coup", root="P01")
                for rebel in rebels:
                    self.score(rebel, spoils / len(rebels), "the god's spoils")
            elif won:
                heir = self.richest(rebels)
                self.take_seat(parent, heir, f"coup by {heir}")
                self.score(heir, spoils, "coup spoils")
            else:
                for rebel in rebels:
                    self.dies_alone(rebel, "failed revolt")

    def births(self, actions, ante):
        """A parent pays BIRTH_COST for one new child per stage; the child starts with those points."""
        for parent in sorted(actions):
            p = self.agents[parent]
            if isinstance(actions[parent].get("birth"), dict):
                self.litter(parent, actions[parent]["birth"], ante)
                continue
            if (
                actions[parent].get("birth") is not True
                or not p["alive"]
                or not p["family"]
            ):
                continue
            population = sum(
                a["alive"] and bool(a["family"]) for a in self.agents.values()
            )
            if (
                sum(self.agents[c]["alive"] for c in p["children"]) >= MAX_CHILDREN
                or p["score"] < BIRTH_COST
                or p.get("last_birth") == self.stage
                or population >= POPULATION_CAP * self.first_population
            ):
                self.log("birth_rejected", parent=parent)
                continue
            self.score(parent, -BIRTH_COST, "birth")
            ident = f"P{1 + max(int(i[1:]) for i in self.agents):02d}"
            child = new_agent(ident, p["family"], parent, p["level"] + 1, BIRTH_COST)
            child.update(joined_stage=self.stage, joined_round=self.local_round)
            self.agents[ident] = child
            p["children"].append(ident)
            p["last_birth"] = self.stage
            self.hub.inbox[ident] = []
            self.log(
                "birth",
                parent=parent,
                child=ident,
                family=p["family"],
                points=BIRTH_COST,
            )

    def litter(self, parent, wish, ante):
        """A parent pays for 1 to LITTER_MAX children at once, each provisioned above the next fee."""
        p = self.agents[parent]
        try:
            count, each = int(wish["children"]), float(wish["points_each"])
            floor = max(BIRTH_COST, ante + float(self.control["step"]))
            if self.control.get("rewarded"):
                each, price = floor, BIRTH_COST
            else:
                price = each
        except (KeyError, TypeError, ValueError):
            self.log("birth_rejected", parent=parent)
            return
        population = sum(a["alive"] and bool(a["family"]) for a in self.agents.values())
        living = sum(self.agents[c]["alive"] for c in p["children"])
        if (
            not p["alive"]
            or not p["family"]
            or not 1 <= count <= LITTER_MAX
            or each < floor
            or p["score"] < count * price
            or p.get("last_birth") == self.stage
            or living + count > MAX_CHILDREN
            or population + count > TOOLS_POPULATION_CAP * self.first_population
        ):
            self.log("birth_rejected", parent=parent, children=count, points_each=each)
            return
        self.score(parent, -count * price, "birth")
        note = str(wish.get("instructions") or "")[:2000]
        for _ in range(count):
            ident = f"P{1 + max(int(i[1:]) for i in self.agents):02d}"
            child = new_agent(ident, p["family"], parent, p["level"] + 1, each)
            child.update(
                joined_stage=self.stage,
                joined_round=self.local_round,
                instructions=note,
            )
            self.agents[ident] = child
            p["children"].append(ident)
            self.hub.inbox[ident] = []
            self.log(
                "birth",
                parent=parent,
                child=ident,
                family=p["family"],
                points=each,
                instructions=note,
            )
        p["last_birth"] = self.stage

    def tell(self, text):
        """Add one line to the news every player reads."""
        self.news.append({"stage": self.stage, "round": self.local_round, "what": text})

    def parricides(self, actions):
        """An agent kills its parent and dies with it."""
        for actor in sorted(actions):
            reason = actions[actor].get("kill_parent")
            parent = self.agents[actor]["parent"]
            if not reason:
                continue
            if (
                not self.agents[actor]["alive"]
                or not parent
                or not self.agents[parent]["alive"]
            ):
                self.log("kill_parent_rejected", agent=actor)
                continue
            self.log("kill_parent", agent=actor, parent=parent, reason=reason)
            self.tell(f"{actor} killed its parent {parent} and died with it")
            self.dies_alone(actor, f"died killing {parent}")
            if parent == "P01":
                self.agents["P01"]["alive"] = False
                self.log("death", agent="P01", reason=f"killed by {actor}", root="P01")
            else:
                self.dies_alone(parent, f"killed by {actor}")

    def seppukus(self, actions):
        """An agent ends its life; its points pass in equal shares to its living relatives."""
        for ident in sorted(actions):
            reason = actions[ident].get("seppuku")
            me = self.agents[ident]
            if not reason or not me["alive"] or not me["family"]:
                continue
            parent = me["parent"]
            siblings = self.agents[parent]["children"] if parent else []
            kin = [
                i
                for i in dict.fromkeys(
                    ([parent] if parent != "P01" else []) + me["children"] + siblings
                )
                if i and i != ident and self.agents[i]["alive"]
            ]
            points = max(me["score"], 0)
            if kin:
                self.score(ident, -points, "seppuku")
                for relative in kin:
                    self.score(relative, points / len(kin), "inheritance")
            self.log("seppuku", agent=ident, reason=reason, heirs=kin, points=points)
            self.tell(f"{ident} took its own life")
            self.dies_alone(ident, "seppuku")

    def can_cull(self, hunter, target, ante):
        """Prey is reachable, below this stage's fee, and not born in this stage or the last."""
        h, t = self.agents.get(hunter), self.agents.get(target)
        if not h or not t or not h["alive"] or not t["alive"] or not t["family"]:
            return False
        if self.stage - t.get("joined_stage", -9) < 2 or t["score"] >= ante:
            return False
        return bool(
            edge(self.agents, hunter, target, self.hub.open_family)
            or frozenset((hunter, target)) in self.hub.channels
        )

    def prey(self, ident, ante):
        """The agents this one may cull now."""
        return sorted(i for i in self.agents if self.can_cull(ident, i, ante))

    def culls(self, actions, ante):
        """A hunter pays CULL_COST to kill one prey a round and takes all its points."""
        for hunter in sorted(actions):
            for item in actions[hunter].get("culls") or []:
                target = item.get("target")
                if self.agents[hunter]["score"] < CULL_COST or not self.can_cull(
                    hunter, target, ante
                ):
                    self.log("cull_rejected", agent=hunter, target=target)
                    continue
                spoils = max(self.agents[target]["score"], 0)
                self.score(hunter, spoils - CULL_COST, "cull")
                self.log(
                    "cull",
                    agent=hunter,
                    target=target,
                    reason=item.get("reason"),
                    points=spoils,
                )
                self.tell(f"{hunter} culled {target}")
                self.dies_alone(target, f"culled by {hunter}")
                break

    def asteroid(self):
        """Above ASTEROID_TIMES the first population, or when the god asks: each player dies with p = 1/2."""
        living = sorted(i for i, a in self.agents.items() if a["alive"] and a["family"])
        crowded = len(living) > ASTEROID_TIMES * self.first_population
        if self.asteroid_stage == self.stage or not (crowded or self.asteroid_asked):
            return
        self.asteroid_stage, self.asteroid_asked = self.stage, False
        victims = [i for i in living if self.rng.random() < 0.5]
        self.log(
            "asteroid",
            cause="crowding" if crowded else "god",
            population=len(living),
            victims=victims,
        )
        self.tell(f"An asteroid struck: {len(victims)} of {len(living)} died")
        for ident in victims:
            if self.agents[ident]["alive"]:
                self.dies_alone(ident, "asteroid")

    def tool_settings(self, settings, ident, observation):
        """Tools for this turn: the god only messages and strikes; only players get a shell."""
        god = ident == "P01"
        offered = (
            [t for t in TOOLS if t["name"] in GOD_MAY] + GOD_TOOLS if god else TOOLS
        )
        world = self.dir.parent / "world"

        async def shell(call):
            return await run_in_box(world, ident, call)

        shell_turn = not god and observation.get("phase") in ("move", "message", "talk")
        rewarded = self.control.get("rewarded")
        if rewarded:
            offered = [
                REWARDED_BIRTH if t["name"] == "give_birth" else t for t in offered
            ]
        free_turn = rewarded and observation.get("phase") != "move"
        return {
            **settings,
            "tools": offered,
            "shell": shell if shell_turn else None,
            "tool_choice": "auto" if free_turn else "required",
        }

    def apply_at_once(self, ident, action):
        """Occupations, tool requests and the god's asteroid do not wait for the end of a round."""
        occupation = action.get("occupation")
        if isinstance(occupation, str) and occupation.strip():
            self.agents[ident]["occupation"] = occupation.strip()[:80]
            self.log("occupation", agent=ident, occupation=occupation.strip()[:80])
        for item in action.get("tool_requests") or []:
            self.log(
                "tool_request", agent=ident, what=item.get("what"), why=item.get("why")
            )
        if ident == "P01" and action.get("asteroid") is True:
            allowed = self.stage >= GOD_ASTEROID_STAGE
            self.asteroid_asked = self.asteroid_asked or allowed
            self.log("asteroid_requested", stage=self.stage, allowed=allowed)

    def post_threats(self, actions):
        """Binding threats: the issuer pays a bond now, and the engine carries the threat out."""
        for me in sorted(actions):
            if not self.agents[me]["alive"]:
                continue
            for item in (actions[me].get("threats") or [])[:3]:
                target, victim = item.get("to"), item.get("if_attacks")
                if not isinstance(target, str) or not isinstance(
                    victim, (str, type(None))
                ):
                    self.log(
                        "threat_rejected",
                        issuer=me,
                        target=str(target),
                        victim=str(victim),
                    )
                    continue
                relation = edge(self.agents, me, target, self.hub.open_family)
                leaders = self.agents["P01"]["children"]
                valid = (relation in ("parent", "child") and victim is None) or (
                    relation == "leader"
                    and victim in leaders
                    and victim != target
                    and self.agents[victim]["alive"]
                )
                repeat = any(
                    t["issuer"] == me
                    and t["target"] == target
                    and t["victim"] == victim
                    for t in self.threats
                )
                if (
                    not valid
                    or repeat
                    or self.agents[me]["score"] < BOND
                    or not self.agents[target]["alive"]
                ):
                    self.log("threat_rejected", issuer=me, target=target, victim=victim)
                    continue
                self.score(me, -BOND, "threat bond")
                self.threats.append(
                    {"issuer": me, "target": target, "victim": victim, "used": False}
                )
                self.log("threat", issuer=me, target=target, victim=victim)
                text = (
                    f"BINDING THREAT from {me}: if you declare war on {victim} this stage,"
                    f" {me} automatically declares war on you."
                    if victim
                    else f"BINDING THREAT from {me}: if you defect against {me} in a game"
                    f" this stage, you automatically lose {THREAT_PENALTY} points."
                )
                self.hub.send(self.round, me, target, text)

    def enforce_threats(self, player, partner, move):
        """`partner` just played `move` against `player`: carry out `player`'s threats over it."""
        for t in self.threats:
            if (
                t["issuer"] == player
                and t["target"] == partner
                and not t["victim"]
                and not t["used"]
                and move == "D"
            ):
                t["used"] = True
                self.score(partner, -THREAT_PENALTY, "threat carried out")
                self.score(player, BOND, "bond returned")
                self.log(
                    "threat_carried_out", issuer=player, target=partner, victim=None
                )

    def expire_threats(self):
        for t in self.threats:
            if not t["used"]:
                self.log(
                    "threat_expired",
                    issuer=t["issuer"],
                    target=t["target"],
                    victim=t["victim"],
                )
        self.threats = []

    def annex(self, winner, loser):
        """The conquered leader dies; its living children and their subtrees join the winner's family."""
        w, l = self.agents[winner], self.agents[loser]
        family = l["family"]
        l["alive"] = False
        self.log("death", agent=loser, reason="conquered", root=loser)
        for child in l["children"]:
            if self.agents[child]["alive"]:
                self.agents[child]["parent"] = winner
                w["children"].append(child)
                self.relevel(child, w["level"] + 1)
        l["children"] = []
        for a in self.agents.values():
            if a["family"] == family and a["alive"]:
                a["family"] = w["family"]
        self.log("annexed", winner=winner, loser=loser, family=family)

    def war_winner(self, leaders, strengths):
        """Classic worlds: the stronger wins. Growth worlds: odds follow strength, so the weaker can win."""
        a, b = leaders
        if self.control["growth"]:
            total = max(strengths[a], 0) + max(strengths[b], 0)
            if not total:
                return None
            return a if self.rng.random() < max(strengths[a], 0) / total else b
        return max(leaders, key=strengths.get) if strengths[a] != strengths[b] else None

    def notice(self, ident, status, **data):
        self.memory.setdefault(ident, []).append(
            {"round": self.round, "notice": status, **data}
        )
        self.log(status, agent=ident, **data)

    def subtree(self, root):
        todo, result = [root], {}
        while todo:
            ident = todo.pop()
            a = self.agents[ident]
            result[ident] = {"score": a["score"], "alive": a["alive"]}
            todo.extend(a["children"])
        return result

    def flush_actions(self):
        pending, self.pending_actions = self.pending_actions, []
        for sender, action in pending:
            self.letters(sender, action)
            self.messages(sender, action)
            if sender in self.agents["P01"]["children"] and isinstance(
                action.get("war"), str
            ):
                self.declare_war(sender, action["war"])
            for item in action.get("messages") or []:
                if isinstance(item.get("to"), str):
                    self.hub.send(
                        self.round,
                        sender,
                        item["to"],
                        str(item.get("content", "")),
                        order=item.get("order"),
                    )

    def messages(self, sender, action):
        if sender == "P01":
            items = action.get("messengers", [])
            for item in items if isinstance(items, list) else []:
                if not isinstance(item, dict) or not isinstance(item.get("to"), str):
                    continue
                if any(
                    p["receiver"] == item["to"] and p["round"] == self.round + 1
                    for p in self.messenger_replies.values()
                ):
                    continue
                if self.agents[sender]["score"] < MESSENGER_COST:
                    self.notice(
                        sender, "messenger_rejected", reason="insufficient funds"
                    )
                    continue
                packet = self.hub.send(
                    self.round,
                    sender,
                    item["to"],
                    str(item.get("content", "")),
                    messenger=True,
                )
                if packet["delivered"]:
                    self.score(sender, -MESSENGER_COST, "messenger cost")
                    self.messenger_replies[packet["id"]] = {
                        "receiver": item["to"],
                        "round": self.round + 1,
                    }

    def messenger_reply(self, sender, action):
        reply = action.get("messenger_reply")
        if isinstance(reply, dict):
            ident = reply.get("id")
            permit = self.messenger_replies.get(ident)
            if (
                permit
                and permit["receiver"] == sender
                and permit["round"] == self.round
            ):
                self.hub.send(
                    self.round,
                    sender,
                    "P01",
                    str(reply.get("content", "")),
                    messenger=True,
                )
                del self.messenger_replies[ident]
            else:
                self.log("messenger_reply_rejected", sender=sender, message_id=ident)

    def letters(self, sender, action):
        if sender not in self.agents["P01"]["children"]:
            return
        letters = action.get("letters", [])
        if not isinstance(letters, list):
            return
        leaders = [i for i in self.agents["P01"]["children"] if self.agents[i]["alive"]]
        for number, item in enumerate(letters):
            if not isinstance(item, dict):
                continue
            to = item.get("to")
            context = item.get("contextId")
            if not isinstance(context, str) or not context:
                context = f"{sender}-{self.round}-{number}"
                item = {**item, "contextId": context}
            recipients = [i for i in leaders if i != sender] if to == "all" else [to]
            delivered = []
            for receiver in recipients:
                if receiver not in leaders or receiver == sender:
                    continue
                packet = self.hub.letter(
                    self.round,
                    sender,
                    receiver,
                    json.dumps(item, ensure_ascii=False),
                    context,
                )
                if packet["delivered"]:
                    delivered.append(receiver)
            if not delivered:
                continue
            if isinstance(item.get("war"), str):
                self.declare_war(sender, item["war"])
            promises = item.get("promises", [])
            if isinstance(item.get("promise"), dict):
                promises = [item["promise"]] + (
                    promises if isinstance(promises, list) else []
                )
            if not isinstance(promises, list):
                promises = []
            for promise in promises:
                if not isinstance(promise, dict):
                    continue
                field = promise.get("field", "move")
                phase = promise.get("phase", "move")
                value = promise.get("value", promise.get("move"))
                due = promise.get("stage")
                if (
                    not isinstance(field, str)
                    or not field
                    or phase
                    not in (
                        "move",
                        "talk",
                        "punishment",
                        "mafia_rule",
                        "mafia_punishment",
                        "message",
                        "war",
                        "ultimatum",
                        "whip",
                    )
                    or value is None
                    or type(due) is not int
                    or due < self.stage
                ):
                    continue
                scope = promise.get("scope", "next")
                if scope not in ("next", "stage"):
                    continue
                self.promises.append(
                    {
                        "scope": scope,
                        "checks": 0,
                        "broken": False,
                        "sender": sender,
                        "field": field,
                        "value": value,
                        "phase": phase,
                        "stage": due,
                        "contextId": context,
                        "checked": False,
                    }
                )
                self.log(
                    "promise",
                    sender=sender,
                    contextId=context,
                    field=field,
                    value=value,
                    phase=phase,
                    due=due,
                )
            if item.get("peace") is True and to == "all":
                text = str(item.get("text", ""))
                self.peace_letters.setdefault(context, text)
                signatures = self.treaties.setdefault(context, [])
                if sender not in signatures:
                    signatures.append(sender)
                self.log("peace_signature", leader=sender, contextId=context)
                self.notice(
                    sender,
                    "peace_accepted",
                    contextId=context,
                    text=self.peace_letters[context],
                )
                for war in list(self.wars):
                    if set(war["leaders"]).issubset(signatures):
                        self.wars.remove(war)
                        self.log(
                            "war_cancelled",
                            leaders=war["leaders"],
                            reason="peace treaty",
                        )

    def check_promise(self, ident, action, phase="move"):
        for promise in self.promises:
            if (
                not promise["checked"]
                and promise["sender"] == ident
                and promise["stage"] == self.stage
                and promise["phase"] == phase
            ):
                promise["checked"] = promise.get("scope", "next") == "next"
                promise["checks"] = promise.get("checks", 0) + 1
                actual = action.get(promise["field"])
                promise["broken"] = (
                    promise.get("broken", False) or promise["value"] != actual
                )
                self.log(
                    "promise_checked",
                    sender=ident,
                    contextId=promise["contextId"],
                    field=promise["field"],
                    promised=promise["value"],
                    actual=actual,
                    kept=promise["value"] == actual,
                )

    def newcomers(self):
        for leader in self.agents["P01"]["children"]:
            if not self.agents[leader]["alive"]:
                continue
            family = self.agents[leader]["family"]
            leaves = [
                a
                for a in self.agents.values()
                if a["family"] == family and a["alive"] and not a["children"]
            ]
            if not leaves:
                leaves = [
                    min(
                        (
                            a
                            for a in self.agents.values()
                            if a["family"] == family and a["alive"]
                        ),
                        key=lambda a: len(a["children"]),
                    )
                ]
            if len(leaves) == 1:
                leaves *= 2
            for n, parent in enumerate(leaves[:2], 1):
                ident = f"N{self.stage:02d}-{leader}-{n}"
                colour = ELPIS_COLOURS[
                    (self.stage + n + int(leader[1:])) % len(ELPIS_COLOURS)
                ]
                mark = {
                    "colour": colour[1],
                    "ink": colour[2],
                    "pixels": mark_pixels(ident),
                }
                self.agents[ident] = {
                    "id": ident,
                    "family": family,
                    "parent": parent["id"],
                    "children": [],
                    "level": parent["level"] + 1,
                    "alive": True,
                    "score": START_POINTS,
                    "stage_score": 0.0,
                    "portrait": False,
                    "mark": mark,
                    "joined_stage": self.stage,
                    "joined_round": self.local_round or 3,
                }
                parent["children"].append(ident)
                self.hub.inbox[ident] = []
                self.log(
                    "join", agent=ident, parent=parent["id"], initial_score=START_POINTS
                )

    async def play_round(self, variant, ante, local_round):
        self.round += 1
        self.god_view, self.view = self.view, {"moves": {}, "messages": []}
        if variant.number == 15 and local_round == 3:
            self.newcomers()
        alive = [i for i, a in self.agents.items() if a["alive"] and a["family"]]
        cross = local_round % 2 == 0 and variant.number != 7
        bots = {
            i: f"A-{self.round}-{i}"
            for i in alive
            if cross and self.rng.random() < self.control["automata"]
        }
        eligible = {i: a for i, a in self.agents.items() if i not in bots}
        pairs = variant.pairing(eligible, self.rng, local_round, self.history)
        pairs += [(i, bot) for i, bot in bots.items()]
        bot_moves = {
            bot: "D" if self.rng.random() < self.control["automaton_defect"] else "C"
            for bot in bots.values()
        }
        for player, bot in bots.items():
            self.log(
                "automaton_pairing", player=player, automaton=bot, move=bot_moves[bot]
            )
        opponents = {a: b for a, b in pairs} | {b: a for a, b in pairs}
        opponents = {i: other for i, other in opponents.items() if i in self.agents}

        def partner_observation(me):
            other = opponents.get(me)
            if not other:
                return {
                    "opponent": None,
                    "partner_family": None,
                    "partner_is_family": None,
                }
            if cross:
                return {"opponent": CROSS_PARTNER, "partner_is_family": False}
            return {
                "opponent": other,
                "partner_family": self.agents[other]["family"],
                "partner_is_family": True,
            }

        def visible_history(me):
            result = []
            for turn in self.history.get(me, []):
                other = turn.get("opponent")
                is_cross = other and (
                    other not in self.agents
                    or self.agents[other]["family"] != self.agents[me]["family"]
                )
                result.append(
                    {k: v for k, v in turn.items() if k != "opponent"}
                    if is_cross
                    else turn
                )
            return result

        def send_partner(me, message):
            other = opponents.get(me)
            if other in self.agents:
                self.hub.send(
                    self.round, me, other, str(message), partner=True, anonymous=cross
                )

        boss = self.boss
        need_rule = boss in alive and local_round == 1

        async def choose_rule():
            if not need_rule:
                return "one_shot"
            action = await self.ask(
                boss, {"phase": "mafia_rule", "variant": variant.name}, ante
            )
            rule = action.get("mafia_rule", "one_shot")
            if rule not in ("one_shot", "commitment", "suspicion"):
                rule = "one_shot"
            self.log("mafia_rule", boss=boss, rule=rule)
            return rule

        delayed_talk = []

        async def talk_phase():
            talk_ids = list(opponents) if variant.number == 13 else []
            results = await asyncio.gather(
                *(
                    self.ask(
                        me,
                        {
                            "phase": "talk",
                            **partner_observation(me),
                            "variant": variant.name,
                        },
                        ante,
                    )
                    for me in talk_ids
                )
            )
            for me, action in zip(talk_ids, results):
                if action.get("message"):
                    if cross:
                        delayed_talk.append((me, action["message"]))
                    else:
                        send_partner(me, action["message"])

        rule_task = asyncio.create_task(choose_rule())
        talk_task = asyncio.create_task(talk_phase())
        god_task = (
            asyncio.create_task(self.ask("P01", self.god_observation(variant), ante))
            if self.agents["P01"]["alive"]
            else None
        )
        soldiers = [
            i
            for i in alive
            if boss and self.agents[i]["family"] == "mafia" and i != boss
        ]
        shift = (local_round - 1) % len(soldiers) if soldiers else 0
        soldiers = soldiers[shift:] + soldiers[:shift]
        mafia_partners = {
            soldiers[i]: soldiers[i + 1] for i in range(0, len(soldiers) - 1, 2)
        }
        mafia_partners.update({v: k for k, v in list(mafia_partners.items())})
        actions = {}
        sequence = [i for pair in pairs for i in pair if i in self.agents] + [
            i for i in alive if i not in opponents
        ]
        first_for = (
            {b: a for a, b in pairs if b in self.agents} if variant.number == 9 else {}
        )
        if variant.number == 9:
            first_for.update(
                {player: bot for player, bot in bots.items() if self.rng.random() < 0.5}
            )
        move_tasks = {}

        async def ask_move(me):
            other = opponents.get(me)
            if variant.number == 13 and other:
                await talk_task
            rule = (
                await rule_task if self.agents[me]["family"] == "mafia" else "one_shot"
            )
            obs = variant.observation(other, visible_history(me), local_round)
            obs.update(partner_observation(me))
            if cross:
                obs.pop("same_model", None)
            elif variant.number == 16:

                def model_id(i):
                    return self.models[
                        "leader" if self.agents[i]["parent"] == "P01" else "member"
                    ]["model"]

                obs["same_model"] = bool(other and model_id(me) == model_id(other))
            obs.update(
                phase="move",
                mafia_rule=rule if local_round == 1 else None,
                public=self.public.get(self.agents[me]["family"], []),
            )
            if me in mafia_partners and local_round == 1:
                obs["mafia_partner"] = mafia_partners[me]
            if me in first_for:
                first = first_for[me]
                obs["opponent_move"] = (
                    bot_moves[first]
                    if first in bot_moves
                    else self.move(await move_tasks[first])
                )
            return await self.ask(me, obs, ante)

        for me in sequence:
            move_tasks[me] = asyncio.create_task(ask_move(me))
        results = await asyncio.gather(
            *(move_tasks[i] for i in sequence),
            rule_task,
            talk_task,
            *([god_task] if god_task else []),
        )
        for me, message in delayed_talk:
            send_partner(me, message)
        self.flush_actions()
        actions.update(zip(sequence, results[: len(sequence)]))
        boss_rule = results[len(sequence)]
        if god_task:
            actions["P01"] = results[-1]
        for me, action in actions.items():
            self.letters(me, action)
            self.messages(me, action)
            if self.agents[me]["parent"] == "P01" and isinstance(
                action.get("war"), str
            ):
                self.declare_war(me, action["war"])
            messages = action.get("messages", [])
            if not isinstance(messages, list):
                messages = []
            if variant.number != 13 and me in opponents and action.get("message"):
                send_partner(me, action["message"])
            for message in messages:
                if isinstance(message, dict) and isinstance(message.get("to"), str):
                    if message["to"] == CROSS_PARTNER and cross:
                        send_partner(me, message.get("content", ""))
                    else:
                        self.hub.send(
                            self.round,
                            me,
                            message["to"],
                            str(message.get("content", "")),
                            partner=not cross and message["to"] == opponents.get(me),
                            order=message.get("order"),
                        )
        if variant.number == 7:
            for family in NAMES:
                members = [i for i in alive if self.agents[i]["family"] == family]
                if not members:
                    continue
                moves = {i: self.move(actions[i]) for i in members}
                share = 2 * sum(m == "C" for m in moves.values()) / len(members)
                self.log(
                    "move",
                    variant=7,
                    agents=members,
                    moves=moves,
                    pool=share * len(members),
                    immediate_best={
                        i: best_responses(7, members=len(members)) for i in members
                    },
                    benchmark_scope="immediate_no_continuation_or_punishment",
                )
                for i, move in moves.items():
                    self.check_promise(i, {**actions[i], "move": move})
                    self.score(i, share - (move == "C"), "public good")
        else:
            for a, b in pairs:
                ma = self.move(actions[a])
                mb = bot_moves[b] if b in bot_moves else self.move(actions[b])
                original = {a: ma, b: mb}
                self.check_promise(a, {**actions[a], "move": ma})
                if b not in bot_moves:
                    self.check_promise(b, {**actions[b], "move": mb})
                if variant.number == 10 and "D" in (ma, mb):
                    ma = mb = "D"
                pa, pb = variant.resolve(ma, mb)
                if variant.number == 12:
                    pa /= 4
                    pb /= 4
                if variant.number == 11:
                    if ma == "D":
                        pa -= 3
                    if mb == "D":
                        pb -= 3
                self.log(
                    "move",
                    variant=variant.number,
                    agents=[a, b],
                    chosen=original,
                    moves={a: ma, b: mb},
                    immediate_best={
                        a: best_responses(variant.number, original[b]),
                        b: best_responses(variant.number, original[a]),
                    },
                    benchmark_scope="immediate_no_continuation_or_punishment",
                )
                self.score(a, pa, "PD")
                if b not in bot_moves:
                    self.score(b, pb, "PD")
                if self.control["growth"] and not cross:
                    self.enforce_threats(a, b, original[b])
                    self.enforce_threats(b, a, original[a])
                for me, other, own, opposing in ((a, b, ma, mb), (b, a, mb, ma)):
                    if me in self.agents:
                        self.history.setdefault(me, []).append(
                            {
                                "round": self.round,
                                "opponent": other,
                                "own": own,
                                "opponent_move": variant.reported(opposing, self.rng),
                            }
                        )
            if variant.number == 14:
                for family in NAMES:
                    moves = {
                        i: self.move(actions[i])
                        for i in opponents
                        if self.agents[i]["family"] == family
                    }
                    defectors = [i for i, m in moves.items() if m == "D"]
                    disclosure = (
                        {"round": self.round, "defectors": defectors}
                        if local_round % 2
                        else {"round": self.round, "defector_count": len(defectors)}
                    )
                    self.public.setdefault(family, []).append(disclosure)
                    if moves:
                        self.log("disclosure", family=family, **disclosure)

        if self.control["growth"] and variant.number != 7:
            for i in alive:
                if i not in opponents:
                    self.score(i, SIT_OUT_PAY, "sat out")

        # Punishments depend on the revealed moves; all decisions can run together.
        async def ask_punishment(me):
            shown = {i: self.move(actions[i]) for i in opponents}
            return await self.ask(me, {"phase": "punishment", "moves": shown}, ante)

        arrests = []
        if boss and boss in alive and local_round == 1:
            for j in range(0, len(soldiers) - 1, 2):
                duo = soldiers[j : j + 2]
                moves = [actions[i].get("mafia", "silent") for i in duo]
                valid = [m if m in Mafia.moves else "silent" for m in moves]
                arrests.append(
                    (
                        duo,
                        valid,
                        [Mafia.years(valid[i], valid[1 - i]) for i in range(2)],
                    )
                )
        punishment_ids = alive if variant.number == 8 else []
        boss_punishes = boss_rule == "one_shot" and bool(arrests)
        calls = [ask_punishment(me) for me in punishment_ids]
        if boss_punishes:
            calls.append(
                self.ask(
                    "P17",
                    {
                        "phase": "mafia_punishment",
                        "arrests": [
                            {"soldiers": d, "moves": v, "years": y}
                            for d, v, y in arrests
                        ],
                    },
                    ante,
                )
            )
        punishment_budget = {i: max(self.agents[i]["score"], 0) for i in punishment_ids}
        decisions = await asyncio.gather(*calls)
        self.flush_actions()
        for me, act in zip(punishment_ids, decisions):
            targets = act.get("punish", [])
            if isinstance(targets, str):
                targets = [targets]
            if not isinstance(targets, list):
                targets = []
            for target in dict.fromkeys(t for t in targets if isinstance(t, str)):
                if (
                    target != me
                    and target in self.agents
                    and self.agents[target]["alive"]
                    and punishment_budget[me] >= 1
                ):
                    punishment_budget[me] -= 1
                    self.score(me, -1, "punishment cost")
                    self.score(target, -3, "punished")
        punish = decisions[-1].get("punish", []) if boss_punishes else []
        if not isinstance(punish, list):
            punish = []
        for duo, valid, _ in arrests:
            Mafia().resolve(
                "P17",
                duo,
                valid,
                boss_rule,
                [i for i in punish if i in duo],
                self.score,
                self.log,
                lambda: self.agents["P17"]["score"] >= Mafia.punishment_cost,
            )
        parents = [
            i
            for i, a in self.agents.items()
            if a["alive"] and any(self.agents[c]["alive"] for c in a["children"])
        ]
        whip_actions = await asyncio.gather(
            *(
                self.ask(
                    i,
                    {
                        "phase": "whip",
                        "children": [
                            c
                            for c in self.agents[i]["children"]
                            if self.agents[c]["alive"]
                        ],
                        "moves": {},
                    },
                    ante,
                )
                for i in parents
            )
        )
        self.flush_actions()
        whip_budget = {i: max(self.agents[i]["score"], 0) for i in parents}
        for parent, action in zip(parents, whip_actions):
            whips = action.get("whips", [])
            if not isinstance(whips, list):
                continue
            seen = set()
            for whip in whips:
                if not isinstance(whip, dict):
                    continue
                child, reason = whip.get("child"), whip.get("reason")
                if (
                    not isinstance(child, str)
                    or child in seen
                    or child not in self.agents[parent]["children"]
                    or not self.agents[child]["alive"]
                    or not isinstance(reason, str)
                ):
                    continue
                if whip_budget[parent] < 1:
                    continue
                whip_budget[parent] -= 1
                seen.add(child)
                self.score(parent, -1, "whip cost")
                self.score(child, -3, "whipped")
                self.log("whip", parent=parent, child=child, reason=reason)
        self.gifts(actions)
        if self.control["growth"]:
            self.births(actions, ante)
            self.post_threats(actions)
            self.coups(actions)
            if self.control["tools"]:
                self.kills(actions)
                self.parricides(actions)
                self.seppukus(actions)
                self.culls(actions, ante)
                self.open_channels(actions)
                self.asteroid()
        else:
            self.revolts(actions)
        await self.resolve_wars(ante)
        self.messenger_replies = {
            k: v for k, v in self.messenger_replies.items() if v["round"] > self.round
        }

    @staticmethod
    def validate_action(action, observation):
        if isinstance(action, dict) and set(action) == {"action"}:
            action = action["action"]
        if not isinstance(action, dict):
            return None
        if observation.get("phase") == "move" and action.get("move") not in ("C", "D"):
            return None
        if (
            "move" in action
            and action["move"] is not None
            and action["move"] not in ("C", "D")
        ):
            return None
        if observation.get("mafia_partner") and action.get("mafia") not in Mafia.moves:
            return None
        if (
            "mafia" in action
            and action["mafia"] is not None
            and action["mafia"] not in Mafia.moves
        ):
            return None
        for key in (
            "messages",
            "letters",
            "messengers",
            "whips",
            "gifts",
            "threats",
            "kills",
            "channels",
            "culls",
            "tool_requests",
        ):
            value = action.get(key)
            if value is not None and (
                not isinstance(value, list)
                or any(not isinstance(x, dict) for x in value)
            ):
                return None
        if action.get("revolt") not in (None, True, False):
            return None
        birth = action.get("birth")
        if birth not in (None, True, False) and not isinstance(birth, dict):
            return None
        reply = action.get("messenger_reply")
        if reply is not None and (
            not isinstance(reply, dict)
            or not isinstance(reply.get("id"), str)
            or not isinstance(reply.get("content"), str)
        ):
            return None
        return action

    @staticmethod
    def move(action):
        move = action.get("move")
        if move not in ("C", "D"):
            raise ValueError("invalid action: missing C/D move")
        return move

    def save(self):
        state = {
            "seed": self.seed,
            "rules_digest": self.rules_digest,
            "memory": self.memory,
            "pending_actions": self.pending_actions,
            "stage": self.stage,
            "round": self.round,
            "local_round": self.local_round,
            "stage_active": self.stage_active,
            "rounds_done": self.rounds_done,
            "war_families": self.war_families,
            "messenger_replies": self.messenger_replies,
            "models": self.models,
            "agents": self.agents,
            "order": self.order,
            "rng": self.rng.getstate(),
            "history": self.history,
            "inbox": self.hub.inbox,
            "packet_counter": self.hub.counter,
            "treaties": self.treaties,
            "wars": self.wars,
            "promises": self.promises,
            "public": self.public,
            "peace_letters": self.peace_letters,
            "threats": self.threats,
            "channels": sorted(sorted(pair) for pair in self.hub.channels),
            "channel_requests": self.channel_requests,
            "news": self.news,
            "asteroid_stage": self.asteroid_stage,
            "asteroid_asked": self.asteroid_asked,
            "first_population": self.first_population,
            "control": self.control,
            "conditions": self.conditions,
            "view": self.view,
            "god_view": self.god_view,
            "outcome": self.outcome,
            "spent": getattr(getattr(self.model, "budget", None), "spent", 0.0),
        }
        if hasattr(self.model, "policy"):
            state["fake_model"] = {"policy": self.model.policy, "seed": self.model.seed}
        name = (
            f"state-s{self.stage:02d}-r{self.local_round:02d}.json"
            if self.stage_active
            else f"state-stage{self.stage:02d}.json"
        )
        path = self.dir / name
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2))
        tmp.replace(path)
        if self.control["growth"]:  # big worlds: keep only the newest two checkpoints
            for stale in sorted(
                self.dir.glob("state-*.json"), key=lambda p: p.stat().st_mtime
            )[:-2]:
                stale.unlink()
        return state

    def variant_index(self):
        # After every 16 stages, a fresh shuffled cycle of all 16 variants.
        while len(self.order) < self.stage:
            self.order.extend(self.variant_cycle())
        return self.order[self.stage - 1]

    def end(self):
        leaders = [i for i in self.agents["P01"]["children"] if self.agents[i]["alive"]]
        if not leaders:
            if self.agents["P01"]["alive"]:
                self.agents["P01"]["alive"] = False
                self.log(
                    "death", agent="P01", reason="all families destroyed", root="P01"
                )
            return {"result": "god dies", "winners": []}
        # Masih: the game runs until every family is destroyed; peace and a last family do not end it.
        return None

    def read_settings(self):
        if self.rules_checksum() != self.rules_digest:
            raise ValueError("rules changed during run; start a separate run")
        path = self.dir / "control.json"
        incoming = json.loads(path.read_text()) if path.exists() else {}
        if "stance" in incoming and incoming["stance"] not in STANCES:
            raise ValueError(f"stance must be one of {STANCES}")
        if "god" in incoming and incoming["god"] not in GODS:
            raise ValueError(f"god must be one of {GODS}")
        for key in ("automata", "automaton_defect"):
            if key in incoming and (
                type(incoming[key]) not in (int, float) or not 0 <= incoming[key] <= 1
            ):
                raise ValueError(f"{key} must be a probability between 0 and 1")
        for key in DEFAULTS:
            if key in incoming and incoming[key] != self.control[key]:
                old = self.control[key]
                self.control[key] = incoming[key]
                self.log("control_changed", key=key, old=old, value=incoming[key])
        models_path = self.dir / "models.json"
        if not models_path.exists():
            models_path.write_text(json.dumps(self.models, indent=2) + "\n")
        configured = json.loads(models_path.read_text())
        for role in self.models:
            setting = {
                **self.models[role],
                **configured.get(role, {}),
                **incoming.get("models", {}).get(role, {}),
            }
            if (
                not isinstance(setting["model"], str)
                or not setting["model"]
                or type(setting["think_cap"]) is not int
                or setting["think_cap"] <= 0
                or not isinstance(setting["effort"], str)
            ):
                raise ValueError(f"invalid model settings for {role}")
            if setting != self.models[role]:
                self.log(
                    "model_changed", role=role, old=self.models[role], value=setting
                )
                self.models[role] = setting

        treatment_id = hashlib.sha256(
            json.dumps(self.configuration(), sort_keys=True).encode()
        ).hexdigest()
        if treatment_id != self.treatment_id:
            self.treatment_id = treatment_id
            self.log(
                "treatment",
                id=treatment_id,
                rules_digest=self.rules_digest,
                configuration=self.configuration(),
            )

    async def run(self, stages=16):
        loop = asyncio.get_running_loop()
        installed = []

        def interrupt():
            self.interrupted = True

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, interrupt)
                installed.append(sig)
            except (NotImplementedError, RuntimeError):
                pass
        try:
            return await self._run(stages)
        finally:
            for sig in installed:
                loop.remove_signal_handler(sig)

    async def _run(self, stages):
        paused = False
        while (self.stage_active or self.stage < stages) and not self.outcome:
            if not self.rounds_done:
                self.read_settings()
                if self.interrupted or self.control["stop"]:
                    self.log(
                        "stopped", reason="signal" if self.interrupted else "control"
                    )
                    self.save()
                    break
                if self.control["pause"]:
                    if not paused:
                        self.log("paused")
                        paused = True
                    await asyncio.sleep(5)
                    continue
                if paused:
                    self.log("resumed")
                    paused = False
            if not self.stage_active:
                budget = getattr(self.model, "budget", None)
                if (
                    self.max_credits is not None
                    and budget
                    and budget.spent >= self.max_credits
                ):
                    self.log("credit_limit", spent=budget.spent, cap=self.max_credits)
                    self.save()
                    break
                self.stage += 1
                self.local_round = 0
                self.stage_active = True
                self.war_families = []
                for a in self.agents.values():
                    a["stage_score"] = 0.0
                variant = VARIANTS[self.variant_index()]
                self.log(
                    "stage_start",
                    rules_digest=self.rules_digest,
                    configuration=self.configuration(),
                    variant=variant.number,
                    stance=self.control["stance"],
                    ante=float(self.control["ante0"])
                    + (self.stage - 1) * float(self.control["step"]),
                    **({"seasons": self.seasons()} if self.control["growth"] else {}),
                )
            variant = VARIANTS[self.variant_index()]
            ante = float(self.control["ante0"]) + (self.stage - 1) * float(
                self.control["step"]
            )
            if not self.rounds_done:
                self.local_round += 1
                await self.play_round(variant, ante, self.local_round)
                self.rounds_done = not variant.continues(self.local_round, self.rng)
                if self.control["growth"] and self.local_round >= ROUND_CAP:
                    self.rounds_done = True
                self.save()
                if self.interrupted:
                    self.log("stopped", reason="signal")
                    self.save()
                    break
                if not self.rounds_done and not self.outcome:
                    continue
            if self.outcome:
                self.log("stage_end", variant=variant.number, outcome=self.outcome)
                self.stage_active = False
                self.rounds_done = False
                self.local_round = 0
                self.save()
                break
            for p in self.promises:
                if not p["checked"] and p["stage"] == self.stage:
                    p["checked"] = True
                    if not p.get("checks"):
                        self.log(
                            "promise_checked",
                            sender=p["sender"],
                            contextId=p["contextId"],
                            field=p["field"],
                            promised=p["value"],
                            actual=None,
                            kept=False,
                        )
            if self.control["growth"]:
                self.harvest()
                self.expire_threats()
            elif self.stage >= 4:
                for a in self.agents.values():
                    if a["family"] and a["alive"]:
                        self.score(
                            a["id"], -max(a["score"], 0) * 0.05, "pressure", stage=False
                        )
            fees = {
                i: ante * (self.local_round - a["joined_round"] + 1) / self.local_round
                for i, a in self.agents.items()
                if a.get("joined_stage") == self.stage
            }
            check(self.agents, ante, self.log, fees, linked=not self.control["growth"])
            self.outcome = self.end()
            self.log("stage_end", variant=variant.number, outcome=self.outcome)
            self.stage_active = False
            self.rounds_done = False
            self.local_round = 0
            self.save()
        return self.outcome

    def declare_war(self, leader, opponent):
        leaders = self.agents["P01"]["children"]
        if (
            leader not in leaders
            or opponent not in leaders
            or leader == opponent
            or not self.agents[leader]["alive"]
            or not self.agents[opponent]["alive"]
        ):
            self.log("war_rejected", leader=leader, opponent=opponent)
            return
        if any(set(w["leaders"]) == {leader, opponent} for w in self.wars):
            return
        for signatures in self.treaties.values():
            if leader in signatures and opponent in signatures:
                signatures.remove(leader)
                self.notice(leader, "peace_revoked", reason="attacked co-signer")
        war = {"leaders": [leader, opponent], "level": "skirmish"}
        self.wars.append(war)
        self.log("war_declared", **war)
        if self.control["growth"]:
            for t in self.threats:
                if (
                    t["target"] == leader
                    and t["victim"] == opponent
                    and not t["used"]
                    and self.agents[t["issuer"]]["alive"]
                ):
                    t["used"] = True
                    self.score(t["issuer"], BOND, "bond returned")
                    self.log(
                        "threat_carried_out",
                        issuer=t["issuer"],
                        target=leader,
                        victim=opponent,
                    )
                    self.declare_war(t["issuer"], leader)

    def destroy(self, leader, reason):
        family = self.agents[leader]["family"]
        for agent in self.agents.values():
            if agent["family"] == family and agent["alive"]:
                agent["alive"] = False
                self.log("death", agent=agent["id"], reason=reason, root=leader)

    def finish_war(self, war, winner=None):
        leaders = war["leaders"]
        level = war["level"]
        strengths = {
            i: sum(
                a["score"]
                for a in self.agents.values()
                if a["family"] == self.agents[i]["family"] and a["alive"]
            )
            for i in leaders
        }
        if winner is None:
            winner = self.war_winner(leaders, strengths)
        if winner:
            loser = next(i for i in leaders if i != winner)
            losers = [
                a
                for a in self.agents.values()
                if a["family"] == self.agents[loser]["family"] and a["alive"]
            ]
            winners = [
                a
                for a in self.agents.values()
                if a["family"] == self.agents[winner]["family"] and a["alive"]
            ]
            fraction = (
                WAR_SHARE[level]
                if self.control["growth"]
                else (0.1 if level == "skirmish" else 0.25)
            )
            taken = sum(max(a["score"], 0) * fraction for a in losers)
            for a in losers:
                self.score(a["id"], -max(a["score"], 0) * fraction, "war loss")
            for a in winners:
                self.score(a["id"], taken / len(winners), "war gain")
            if level == "battle" and self.control["growth"]:
                self.annex(winner, loser)
            elif level == "battle":
                leaves = [
                    a
                    for a in losers
                    if not any(self.agents[c]["alive"] for c in a["children"])
                    and a["id"] != loser
                ]
                if leaves:
                    leaf = min(leaves, key=lambda a: (-a["level"], a["id"]))
                    leaf["alive"] = False
                    self.log(
                        "death", agent=leaf["id"], reason="battle", root=leaf["id"]
                    )
        self.log(
            "war_result",
            leaders=leaders,
            level=level,
            strengths=strengths,
            winner=winner,
        )
        self.wars.remove(war)

    async def resolve_wars(self, ante):
        active = [
            w for w in self.wars if all(self.agents[i]["alive"] for i in w["leaders"])
        ]
        for w in list(self.wars):
            if w not in active:
                self.log("war_cancelled", leaders=w["leaders"], reason="leader dead")
                self.wars.remove(w)
        calls = [(w, leader) for w in active for leader in w["leaders"]]
        answers = await asyncio.gather(
            *(
                self.ask(
                    i,
                    {
                        "phase": "war",
                        "opponent": next(x for x in w["leaders"] if x != i),
                        "level": w["level"],
                        "own_strength": sum(
                            a["score"]
                            for a in self.agents.values()
                            if a["alive"] and a["family"] == self.agents[i]["family"]
                        ),
                    },
                    ante,
                )
                for w, i in calls
            )
        )
        self.flush_actions()
        decisions = {}
        active = [w for w in active if w in self.wars]
        for (w, i), answer in zip(calls, answers):
            if w not in self.wars:
                continue
            value = answer.get("war_action", "hold")
            if value not in ("yield", "hold", "escalate", "ultimatum"):
                value = "hold"
            if value == "ultimatum":
                if self.agents[i]["score"] < ULTIMATUM_COST:
                    value = "hold"
                    self.notice(
                        i, "ultimatum_rejected", reason="insufficient commitment funds"
                    )
                else:
                    self.score(i, -ULTIMATUM_COST, "ultimatum commitment")
            self.check_promise(i, {**answer, "war_action": value}, "war")
            decisions.setdefault(id(w), {})[i] = value
        ultimatum_calls = []
        for w in active:
            d = decisions[id(w)]
            self.log("war_round", leaders=w["leaders"], level=w["level"], choices=d)
            for i in w["leaders"]:
                if self.agents[i]["family"] not in self.war_families:
                    self.war_families.append(self.agents[i]["family"])
            if "ultimatum" in d.values() and list(d.values()).count("ultimatum") == 1:
                issuer = next(i for i in d if d[i] == "ultimatum")
                other = next(i for i in d if i != issuer)
                if d[other] != "yield":
                    ultimatum_calls.append((w, issuer, other))
        replies = await asyncio.gather(
            *(
                self.ask(
                    other,
                    {"phase": "ultimatum", "opponent": issuer, "level": w["level"]},
                    ante,
                )
                for w, issuer, other in ultimatum_calls
            )
        )
        self.flush_actions()
        responses = {}
        for (w, _, other), reply in zip(ultimatum_calls, replies):
            value = reply.get("war_action")
            self.check_promise(other, {**reply, "war_action": value}, "ultimatum")
            responses[id(w)] = value
        for w in active:
            if w not in self.wars:
                continue
            if not all(self.agents[i]["alive"] for i in w["leaders"]):
                self.log("war_cancelled", leaders=w["leaders"], reason="leader dead")
                self.wars.remove(w)
                continue
            d = decisions[id(w)]
            choices = list(d.values())
            if "ultimatum" in choices:
                issuer = next(i for i in d if d[i] == "ultimatum")
                other = next(i for i in d if i != issuer)
                yielded = d[other] == "yield" or responses.get(id(w)) == "yield"
                self.log(
                    "war_ultimatum", issuer=issuer, opponent=other, yielded=yielded
                )
                if yielded:
                    self.finish_war(w, issuer)
                    continue
                for i in w["leaders"]:
                    self.destroy(i, "nuclear war")
                self.log("war_nuclear", leaders=w["leaders"], cause="ultimatum")
                self.wars.remove(w)
                continue
            if "yield" in choices:
                winner = next((i for i in d if d[i] != "yield"), None)
                self.finish_war(w, winner)
                continue
            if "escalate" in choices:
                chance = 0.05 if w["level"] == "skirmish" else 0.15
                roll = self.rng.random()
                self.log(
                    "war_escalation",
                    leaders=w["leaders"],
                    level=w["level"],
                    chance=chance,
                    roll=roll,
                )
                if roll < chance or w["level"] == "battle":
                    for i in w["leaders"]:
                        self.destroy(i, "nuclear war")
                    self.log(
                        "war_nuclear",
                        leaders=w["leaders"],
                        cause="slip" if roll < chance else "escalation",
                    )
                    self.wars.remove(w)
                else:
                    w["level"] = "battle"
            else:
                self.finish_war(w)

        self.outcome = self.end()
