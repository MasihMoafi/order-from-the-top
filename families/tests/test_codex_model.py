"""Check Codex JSONL parsing without launching model calls."""

import json

from families.codex_model import parse


def test_parse_reads_the_reply_usage_and_errors():
    lines = [
        {"type": "thread.started"},
        {"type": "item.completed", "item": {"type": "reasoning", "text": "think"}},
        {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": '{"move":"C"}'},
        },
        {"type": "turn.completed", "usage": {"input_tokens": 5}},
    ]
    out = "\n".join(map(json.dumps, lines)) + "\nnot json\n"
    assert parse(out) == ('{"move":"C"}', "think", {"input_tokens": 5}, "")
    failed = json.dumps({"type": "turn.failed", "error": {"message": "usage limit"}})
    assert "usage limit" in parse(failed)[3]
