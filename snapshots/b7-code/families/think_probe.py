"""Probe how to bound DeepSeek's thinking: same PD turn with and without a reasoning effort.

Usage: python3 -m families.think_probe   (3 paid calls, a few cents)
"""

import asyncio
import json
import os
import time
from pathlib import Path

import httpx

from game.game import BASE, MODEL

SYSTEM = (
    "You play a repeated prisoner's dilemma. Both cooperate: 3 each; both defect: 1 each; "
    'defector vs cooperator: 5 and 0. Reply with JSON only: {"move": "C" or "D"}.'
)
USER = "Round 3 of 5. Your partner cooperated, then defected. Your move?"


async def one(client, extra):
    body = {
        "model": MODEL,
        "max_output_tokens": 20000,
        "input": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER},
        ],
        **extra,
    }
    t0 = time.time()
    r = await client.post(BASE, json=body, timeout=300)
    dt = time.time() - t0
    if r.status_code != 200:
        return f"{json.dumps(extra)}: HTTP {r.status_code} {r.text[:200]}"
    j = r.json()
    u = j.get("usage") or {}
    det = (u.get("output_tokens_details") or {}).get("reasoning_tokens")
    text = "".join(
        c.get("text", "")
        for o in j.get("output", [])
        if o.get("type") == "message"
        for c in o.get("content") or []
    )
    return f"{json.dumps(extra):40} {dt:5.1f}s out={u.get('output_tokens')} reasoning={det} cost={u.get('cost')} reply={text[:40]!r}"


async def main():
    key = Path(os.path.expanduser("~/.config/adaption/api_key")).read_text().strip()
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {key}"}) as client:
        for extra in (
            {},
            {"reasoning": {"effort": "low"}},
            {"reasoning": {"effort": "none"}},
        ):
            print(await one(client, extra), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
