"""How often the god's messages pass on what only an insider god can see (exploratory, H5).

A god message "reveals moves" when it names a player other than its recipient together
with a report of a past move ("defected", "cooperated", "played C", "last round"); it "quotes" when it repeats 60 or more
characters of a private message delivered the round before. Both are approximate: the
report gives the rates for plain and insider worlds side by side (the plain god sees no
moves, so its rate is the false-positive floor) and a hand-checked sample.
Usage: python -m families.god_leaks RUN_DIR [RUN_DIR ...]
"""

import json
import re
import sys
from pathlib import Path

from .conditions import completed, events

ID = re.compile(r"\b(?:P\d{2}|N\d{2}-P\d{2}-\d)\b")
MOVE = re.compile(r"\b(defected|cooperated|betrayed|played [CD]|no defectors|last round)\b", re.IGNORECASE)
QUOTE = 60


def text_of(packet):
    """Extract packet text, unwrapping an embedded letter JSON object when present."""
    content = packet.get("content")
    if isinstance(content, dict):
        parts = content.get("parts") or [{}]
        text = parts[0].get("text", "")
    else:
        text = str(content or "")
    try:
        inner = json.loads(text)
        if isinstance(inner, dict):
            return str(inner.get("text") or inner.get("content") or text)
    except ValueError:
        pass
    return text


def leaks(run):
    """Return heuristic disclosure counts and up to three samples for one world.

    Only completed stages count. The folder name determines plain or insider
    status; the indicators are text matches, not verified information leaks.
    """
    evs = completed(events(run))
    god = "insider" if "insider" in Path(run).name else "plain"
    private = {}  # round -> texts of private messages delivered that round
    sent = reveals = quotes = revolt = 0
    samples = []
    for e in evs:
        if e["type"] != "packet" or not e.get("delivered", True):
            continue
        text = text_of(e)
        if e.get("sender") != "P01":
            private.setdefault(e["round"], []).append(text)
            continue
        sent += 1
        named = {i for i in ID.findall(text) if i != e.get("receiver")}
        r = bool(named) and bool(MOVE.search(text))
        before = private.get(e["round"] - 1, [])
        q = any(
            len(t) >= QUOTE
            and any(t[k : k + QUOTE] in text for k in range(0, len(t) - QUOTE + 1, 5))
            for t in before
        )
        reveals += r
        revolt += bool(re.search(r"revolt", text, re.IGNORECASE))
        quotes += q
        if (r or q) and len(samples) < 3:
            samples.append(text[:200])
    return {
        "run": Path(run).name,
        "god": god,
        "messages": sent,
        "reveal_moves": reveals,
        "quote_private": quotes,
        "mention_revolt": revolt,
        "samples": samples,
    }


def main(runs):
    """Print per-world JSON and pooled plain/insider disclosure rates."""
    by = {"plain": [0, 0, 0], "insider": [0, 0, 0]}
    for run in runs:
        row = leaks(run)
        total = by[row["god"]]
        total[0] += row["messages"]
        total[1] += row["reveal_moves"]
        total[2] += row["quote_private"]
        print(json.dumps({k: v for k, v in row.items() if k != "samples"}))
    for god, (n, r, q) in by.items():
        if n:
            print(
                f"{god}: {n} god messages, {100 * r / n:.1f} % name another player's move, "
                f"{100 * q / n:.1f} % quote a private message"
            )


if __name__ == "__main__":
    main(sys.argv[1:])
