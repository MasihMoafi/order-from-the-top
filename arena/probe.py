"""Probe Adaption models: latency and errors for one short game prompt, direct and over the VPN.

Usage: python3 arena/probe.py MODEL [MODEL ...]   (prints status, seconds, cost; never the key)
"""

import os
import sys
import time
from pathlib import Path

import httpx

KEY = Path(os.path.expanduser("~/.config/adaption/api_key")).read_text().strip()
URL = "https://api.prod.adaptionlabs.ai/api/v1/responses"
PROMPT = (
    "Prisoner's dilemma, played once. Both C: 3 each; both D: 1 each; you D they C: 5 and 0. "
    'Reply with one JSON object: {"move": "C" or "D"}'
)
for proxy in (None, "http://127.0.0.1:10808"):
    for model in sys.argv[1:]:
        t0 = time.time()
        where = "vpn" if proxy else "direct"
        try:
            with httpx.Client(proxy=proxy, timeout=httpx.Timeout(240, connect=20)) as c:
                r = c.post(
                    URL,
                    headers={"Authorization": f"Bearer {KEY}"},
                    json={"model": model, "max_output_tokens": 4000, "input": PROMPT},
                )
            j = r.json() if r.status_code == 200 else {}
            out = (j.get("output_text") or "")[-50:].replace("\n", " ")
            cost = (j.get("usage") or {}).get("cost")
            print(
                f"{where}\t{model}\t{r.status_code}\t{time.time() - t0:.0f}s\tcost={cost}\t{out}",
                flush=True,
            )
        except httpx.HTTPError as e:
            print(
                f"{where}\t{model}\tERR {type(e).__name__}\t{time.time() - t0:.0f}s",
                flush=True,
            )
