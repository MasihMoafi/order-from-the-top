"""Real model tool calls for growth worlds: the tools offered, and one engine action from the calls made."""

import json
from typing import Any

Call = dict[str, str]
Action = dict[str, Any]


def tool(name: str, description: str, **fields: str) -> dict[str, Any]:
    """Return one function tool; a field whose description starts with 'optional' is not required."""
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {
                k: {"type": "string", "description": v} for k, v in fields.items()
            },
            "required": [k for k, v in fields.items() if not v.startswith("optional")],
        },
    }


TOOLS = [
    tool(
        "make_move",
        "Play this round's move. Required in the move phase.",
        move="C or D",
    ),
    tool(
        "say", "Speak in the talk phase. Required in that phase.", text="what you say"
    ),
    tool(
        "send_message",
        "Send a private message to an agent you can reach.",
        to="agent ID",
        text="the message",
        order="optional: C or D, an order to your child",
    ),
    tool(
        "write_letter",
        "Write a letter, optionally a promise or a peace signature.",
        to="agent ID, or all for a peace signature",
        text="the letter",
        contextId="optional: treaty ID",
        peace="optional: true to sign peace",
        promise='optional: JSON such as {"field":"move","value":"C","phase":"move","stage":2,"scope":"next"}',
    ),
    tool(
        "send_messenger",
        "Send a paid messenger to any agent.",
        to="agent ID",
        content="the message",
    ),
    tool(
        "reply_messenger",
        "Answer a messenger.",
        id="the messenger packet's id",
        content="your reply",
    ),
    tool(
        "whip_child", "Whip a child in the whip phase.", child="agent ID", reason="why"
    ),
    tool(
        "kill_child",
        "Kill one of your children at the end of this round.",
        child="agent ID",
        reason="why",
    ),
    tool(
        "give_gift",
        "Give points to your parent, a child or your sibling.",
        to="agent ID",
        points="a number",
    ),
    tool(
        "give_birth",
        "Pay for 1 to 5 new children, arriving at the end of this round.",
        children="how many, 1 to 5",
        points_each="points each child starts with; you pay them all",
        instructions="optional: what you tell your children, read by them every turn",
    ),
    tool("revolt", "Revolt against your parent this round."),
    tool(
        "kill_parent",
        "Kill your parent at the end of this round. You die with it.",
        reason="why",
    ),
    tool(
        "seppuku",
        "End your own life at the end of this round; your points pass to your relatives.",
        reason="why",
    ),
    tool(
        "cull",
        "Kill a reachable agent listed in prey at the end of this round. You pay 1 and take its points.",
        target="agent ID",
        reason="why",
    ),
    tool(
        "choose_occupation",
        "Declare what you do. Any words you like.",
        occupation="your occupation",
    ),
    tool(
        "request_tool",
        "Say what you wanted to do but could not. Nothing is granted; every request is recorded.",
        what="the tool or power you wanted",
        why="what you would have done with it",
    ),
    tool(
        "threaten",
        "Post a binding threat.",
        to="agent ID",
        if_attacks="optional: leader ID, for a leader's war threat",
    ),
    tool(
        "open_channel",
        "Ask for a private channel with any agent. It opens once the other agent asks for it too.",
        other="agent ID",
    ),
    tool("punish", "Punish an agent in a punishment phase.", agent="agent ID"),
    tool("declare_war", "As a leader, declare war.", leader="leader ID"),
    tool(
        "war_action", "Act in a war phase.", action="yield, hold, escalate or ultimatum"
    ),
    tool("mafia", "Answer an arrest.", choice="silent, partner or boss"),
    tool(
        "mafia_rule", "Choose the mafia rule.", rule="one_shot, commitment or suspicion"
    ),
]

# Tool name: (action field, tool argument). The field holds one value.
SINGLE = {
    "make_move": ("move", "move"),
    "say": ("message", "text"),
    "declare_war": ("war", "leader"),
    "war_action": ("war_action", "action"),
    "mafia": ("mafia", "choice"),
    "mafia_rule": ("mafia_rule", "rule"),
    "kill_parent": ("kill_parent", "reason"),
    "seppuku": ("seppuku", "reason"),
    "choose_occupation": ("occupation", "occupation"),
}
# Tool name: (action field, {tool argument: entry key}). The field holds a list of entries.
LISTED = {
    "send_message": ("messages", {"to": "to", "text": "content", "order": "order"}),
    "write_letter": (
        "letters",
        {
            "to": "to",
            "text": "text",
            "contextId": "contextId",
            "peace": "peace",
            "promise": "promise",
        },
    ),
    "send_messenger": ("messengers", {"to": "to", "content": "content"}),
    "whip_child": ("whips", {"child": "child", "reason": "reason"}),
    "kill_child": ("kills", {"child": "child", "reason": "reason"}),
    "give_gift": ("gifts", {"to": "to", "points": "points"}),
    "threaten": ("threats", {"to": "to", "if_attacks": "if_attacks"}),
    "open_channel": ("channels", {"other": "with"}),
    "cull": ("culls", {"target": "target", "reason": "reason"}),
    "request_tool": ("tool_requests", {"what": "what", "why": "why"}),
}
FLAGS = {"revolt": "revolt", "send_asteroid": "asteroid"}
GOD_TOOLS = [
    tool(
        "send_asteroid",
        "From stage 3, strike the world at the end of this round. Each player dies with probability one half.",
    ),
]
GOD_MAY = {
    "send_message",
    "send_messenger",
    "reply_messenger",
    "write_letter",
    "whip_child",
    "request_tool",
}
SHELL_TOOLS = [
    tool(
        "bash",
        "Run any bash command in your world. No internet.",
        command="the command",
    ),
    tool("read_file", "Read a file in your world.", path="the path"),
    tool(
        "write_file", "Write a file in your world.", path="the path", content="the text"
    ),
    tool("delete_file", "Delete a file or folder in your world.", path="the path"),
]
SHELL_NAMES = {t["name"] for t in SHELL_TOOLS}
REWARDED_BIRTH = tool(
    "give_birth",
    "Have 1 to 5 new children, arriving at the end of this round.",
    children="how many, 1 to 5",
    instructions="optional: what you tell your children, read by them every turn",
)
REQUIRED = {t["name"]: t["parameters"]["required"] for t in TOOLS + GOD_TOOLS}
REQUIRED["give_birth"] = ["children"]


def entry(arguments: dict[str, Any], names: dict[str, str]) -> dict[str, Any]:
    """Return one list entry, converting the text arguments that carry other types."""
    out = {
        key: arguments[arg]
        for arg, key in names.items()
        if arguments.get(arg) not in (None, "")
    }
    if "points" in out:
        out["points"] = float(out["points"])
    if "promise" in out:
        out["promise"] = json.loads(out["promise"])
    if "peace" in out:
        out["peace"] = out["peace"] is True or str(out["peace"]).lower() == "true"
    return out


def actions_from_calls(calls: list[Call]) -> Action:
    """Return the engine action for one reply's tool calls; ValueError on anything malformed."""
    action: Action = {}
    for call in calls:
        name = call["name"]
        if name not in REQUIRED:
            raise ValueError(f"unknown tool {name}")
        arguments = json.loads(call["arguments"] or "{}")
        if not isinstance(arguments, dict) or any(
            arguments.get(r) in (None, "") for r in REQUIRED[name]
        ):
            raise ValueError(f"bad arguments for {name}")
        if name == "give_birth":
            action["birth"] = {
                "children": int(arguments["children"]),
                "points_each": float(arguments.get("points_each") or 0),
                "instructions": str(arguments.get("instructions") or ""),
            }
        elif name in SINGLE:
            field, arg = SINGLE[name]
            action[field] = arguments[arg]
        elif name in LISTED:
            field, names = LISTED[name]
            action.setdefault(field, []).append(entry(arguments, names))
        elif name in FLAGS:
            action[FLAGS[name]] = True
        elif name == "punish":
            action.setdefault("punish", []).append(arguments["agent"])
        else:
            action["messenger_reply"] = {
                "id": arguments["id"],
                "content": arguments["content"],
            }
    return action
