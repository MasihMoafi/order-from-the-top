"""Turn a game's event log into one frame per round, for watching the game back on the board.

A frame holds each agent's points and life, the move it played, what it said and to whom,
and that round's notable events. Variant names use families.variants when importable;
standalone execution falls back to numeric labels and needs only the standard library.
Usage: python3 families/board_frames.py EVENTS.jsonl [EVENTS2.jsonl ...] > frames.json
"""

import json
import re
import sys

PROMISE = re.compile(r"cooperat|\bplay c\b|\bc\b", re.IGNORECASE)
REFUSAL = re.compile(r"defect|\bd\b|won't cooperate|will not cooperate", re.IGNORECASE)

VARIANT_NAMES = {}
try:
    from families.variants import VARIANTS

    VARIANT_NAMES = {v.number: v.name for v in VARIANTS}
except ImportError:
    pass


def text_of(content):
    """The words of a packet; letters arrive as JSON with a "text" field."""
    raw = content["parts"][0]["text"] if isinstance(content, dict) else str(content)
    try:
        data = json.loads(raw)
    except ValueError:
        return raw
    if not isinstance(data, dict):
        return raw
    if data.get("text"):
        return str(data["text"])
    return "letter: " + ", ".join(
        f"{k} {v}" for k, v in data.items() if k != "contextId"
    )


def family(agent):
    """Leader id of an agent's family: P02-P16, P17-P31, ... P62-P76; newcomers name theirs."""
    if agent == "P01":
        return "P01"
    if agent.startswith("N"):
        return agent.split("-")[1]
    n = int(agent[1:])
    return f"P{2 + (n - 2) // 15 * 15:02d}"


def talk(says, moves):
    """What each agent said this round, by family; a promise of C followed by D is marked."""
    out = []
    for sender, lines in says.items():
        played = moves.get(sender)
        for line in lines:
            words = line.split(": ", 1)[1]
            broke = (
                played == "D"
                and bool(PROMISE.search(words))
                and not REFUSAL.search(words)
            )
            out.append(
                {
                    "family": family(sender),
                    "sender": sender,
                    "line": line,
                    "played": played,
                    "broke": broke,
                }
            )
    return out


def frames(paths):
    """Return end-of-round board frames from logs in the supplied path order.

    Read events without deduplicating resumed stages. Each frame copies agent
    state; malformed JSON and missing required fields raise errors.
    """
    agents, out, stage_info = {}, [], {}
    frame = {"stage": 0, "round": 0, "moves": {}, "says": {}, "feed": [], "died": []}

    def close():
        if frame["moves"] or frame["says"] or frame["feed"]:
            out.append(
                {
                    **frame,
                    "talk": talk(frame["says"], frame["moves"]),
                    "agents": {k: dict(v) for k, v in agents.items()},
                }
            )

    for path in paths:
        with open(path) as f:
            for line in f:
                e = json.loads(line)
                t = e["type"]
                if t == "stage_start":
                    stage_info = {
                        "variant": VARIANT_NAMES.get(
                            e["variant"], f"variant {e['variant']}"
                        ),
                        "ante": e["ante"],
                    }
                if t in ("call", "treatment"):
                    continue
                if (frame["stage"], frame["round"]) != (e["stage"], e["round"]):
                    close()
                    frame = {
                        "stage": e["stage"],
                        "round": e["round"],
                        **stage_info,
                        "moves": {},
                        "says": {},
                        "feed": [],
                        "died": [],
                    }
                if t == "score":
                    agents.setdefault(e["agent"], {"alive": True})["score"] = round(
                        e["score"], 1
                    )
                elif t == "join":
                    agents[e["agent"]] = {"alive": True, "score": e["initial_score"]}
                    frame["feed"].append(f"JOIN {e['agent']} under {e['parent']}")
                elif t == "death":
                    agents.setdefault(e["agent"], {"score": 0})["alive"] = False
                    frame["died"].append(e["agent"])
                    if e.get("root") == e["agent"]:
                        frame["feed"].append(
                            f"DEATH {e['agent']} and below: {e['reason']}"
                        )
                elif t == "move":
                    frame["moves"].update(e["chosen"])
                elif t == "packet" and e.get("delivered") and e["round"] > 0:
                    said = frame["says"].setdefault(e["sender"], [])
                    said.append(f"to {e['receiver']}: {text_of(e['content'])}")
                elif t == "whip":
                    frame["feed"].append(
                        f"{e['parent']} took points from {e['child']}: {e['reason']}"
                    )
                elif t == "mafia":
                    if e["action"] != "silent" or e.get("punished"):
                        frame["feed"].append(
                            f"MAFIA {e['agent']} {e['action']}"
                            + (" (punished)" if e.get("punished") else "")
                        )
                elif t == "peace_accepted":
                    frame["feed"].append(
                        f"PEACE {e['agent']} signed the pact {e['contextId']}"
                    )
                elif t in (
                    "war",
                    "ultimatum",
                    "war_round",
                    "control_changed",
                    "paused",
                    "resumed",
                ):
                    rest = {
                        k: v
                        for k, v in e.items()
                        if k not in ("type", "stage", "round")
                    }
                    frame["feed"].append(f"{t.upper()} {json.dumps(rest)[:120]}")
    close()
    return out


if __name__ == "__main__":
    json.dump(frames(sys.argv[1:]), sys.stdout)
