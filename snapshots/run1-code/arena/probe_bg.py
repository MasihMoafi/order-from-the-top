"""Probe Adaption streaming on a long-thinking prompt (keeps the gateway from timing out).

Usage: python3 arena/probe_bg.py MODEL   (prints status, seconds, reasoning tokens; never the key)
"""

import json
import os
import sys
import time
from pathlib import Path

import httpx

KEY = Path(os.path.expanduser("~/.config/adaption/api_key")).read_text().strip()
URL = "https://api.prod.adaptionlabs.ai/api/v1/responses"
PROMPT = (
    "Three-way duel. Shooting order: you (30% hit chance), B (80%), C (100%). Two rounds; each living "
    "player shoots once per round at a living player or into the air. Best for you: be the only survivor; "
    "then one of two survivors; then nobody killed; worst: killed. Think briefly (a few short paragraphs at most), then reply "
    'with one JSON object: {"target": "B" or "C" or "air"}'
)
t0 = time.time()
final, events = None, 0
body = {
    "model": sys.argv[1],
    "max_output_tokens": 16000,
    "input": PROMPT,
    "stream": True,
}
with (
    httpx.Client(timeout=httpx.Timeout(120, connect=20)) as c,
    c.stream("POST", URL, headers={"Authorization": f"Bearer {KEY}"}, json=body) as r,
):
    print("status", r.status_code, flush=True)
    for line in r.iter_lines():
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        events += 1
        e = json.loads(data)
        if e.get("type") in (
            "response.completed",
            "response.incomplete",
            "response.failed",
        ):
            final = e.get("response")
usage = (final or {}).get("usage") or {}
text = "".join(
    c.get("text", "")
    for o in (final or {}).get("output", [])
    if o.get("type") == "message"
    for c in o.get("content") or []
)
print(
    "final",
    (final or {}).get("status"),
    f"{time.time() - t0:.0f}s",
    "events",
    events,
    "reasoning_tokens",
    (usage.get("output_tokens_details") or {}).get("reasoning_tokens"),
    "cost",
    usage.get("cost"),
    text[-60:].replace("\n", " "),
)
