"""Print a run's moves and shots, one line each: python3 arena/show.py RUN"""
import json
import sys
from pathlib import Path

d = Path(__file__).resolve().parent / "out" / sys.argv[1]
for line in (d / "events.jsonl").read_text().splitlines():
    e = json.loads(line)
    keys = {
        "move": ["match", "round", "variant", "agent", "move", "theory", "lie", "message"],
        "shot": ["stage", "duel", "round", "agent", "accuracy", "target", "target_accuracy", "hit", "theory", "message"],
        "duel_end": ["stage", "duel", "players", "survivors"],
        "stalemate": ["tournament", "stage"],
        "tournament_end": ["tournament", "winners"],
    }.get(e["type"])
    if keys:
        print(e["type"], *(str(e.get(k, ""))[:70] for k in keys), sep="\t")
