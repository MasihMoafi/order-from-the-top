"""Print one game's actions, one line per call. Usage: python3 game/show.py n5 0 [--reasoning]"""

import json
import sys

from game import OUT


def main():
    cell, seed = sys.argv[1], sys.argv[2]
    reasoning = "--reasoning" in sys.argv
    path = OUT / cell / f"seed{seed}" / "calls.jsonl"
    for line in path.read_text().splitlines():
        c = json.loads(line)
        r = c["reply"]
        out = (r.get("usage") or {}).get("output_tokens")
        res = c["result"].replace("\n", " / ")[:110]
        print(
            f"r{c['round']:02d} {c['agent']} {r.get('latency_ms')}ms out={out} {json.dumps(c['action'])} | {res}"
        )
        if c["action"] is None:
            print(
                f"    REPLY ({r.get('status')}):",
                repr((r.get("text") or r.get("error") or "")[:300]),
            )
        if reasoning and r.get("reasoning"):
            print("    THINK:", r["reasoning"][:600].replace("\n", " "))


if __name__ == "__main__":
    main()
