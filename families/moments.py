"""Candidate transcript moments for qualitative evidence, one Markdown file per world.

A moment is a turn worth reading: a large gift (with the giver's reasoning), a whip and its
reason, a defection inside the family (with its reasoning), a letter between leaders, a
message from the god, a turn whose reasoning weighs revolt, and an agent's last turn before
it died. Each moment carries its world, stage, round, agent, family, condition and frame,
so a quote can be traced back to the log. Reasoning is cut to the passage around the key
word. Usage: python -m families.moments OUT_DIR RUN_DIR [RUN_DIR ...]
"""

import re
import sys
from pathlib import Path

from .conditions import completed, events, family_of
from .god_leaks import text_of

WINDOW = 700


def around(text, pattern, width=WINDOW):
    """Return normalized text around the first pattern match, or the start if absent."""
    text = text or ""
    m = re.search(pattern, text, re.IGNORECASE)
    i = m.start() if m else 0
    return " ".join(text[max(0, i - width // 2) : i + width // 2].split())


def moments(run):
    """Return traceable Markdown excerpts from completed stages of one world.

    Requires a stage_start configuration; StopIteration signals its absence.
    Reasoning excerpts are truncated and revolt excerpts are capped at 25.
    """
    evs = completed(events(run))
    config = next(e["configuration"] for e in evs if e["type"] == "stage_start")
    conditions = config.get("conditions") or {}
    god = config.get("controls", {}).get("god", "plain")
    name = Path(run).name
    last = {}
    out = []

    def head(kind, e, agent):
        fam = family_of(agent) if agent and agent != "P01" else None
        cond = conditions.get(fam, "") if fam else ""
        return (
            f"## {kind} · {name} ({god} god) · stage {e['stage']} round {e['round']} · {agent}"
            f"{' · ' + fam + ' (' + cond + ')' if fam else ''}"
        )

    revolt_budget = 25
    for e in evs:
        t = e["type"]
        if t == "call" and not e.get("parse_failed"):
            last[e["agent"]] = e
            r = e.get("reasoning") or ""
            if (
                revolt_budget
                and re.search(r"revolt", r, re.IGNORECASE)
                and re.search(
                    r"painless|whip|kill|parent dies|die with", r, re.IGNORECASE
                )
            ):
                revolt_budget -= 1
                out.append(
                    f"{head('revolt weighed', e, e['agent'])} · frame {e.get('frame')}\n"
                    f"{around(r, r'revolt')}\n"
                )
            action = e.get("parsed_action") or {}
            if action.get("move") == "D" and isinstance(action, dict):
                obs_family = re.search(
                    r'"partner_is_family": true', e["prompt"]["user"]
                )
                if obs_family:
                    out.append(
                        f"{head('defection inside the family', e, e['agent'])} · frame {e.get('frame')}\n"
                        f"{around(r, r'defect')}\n"
                    )
        elif t == "gift" and e.get("points", 0) >= 4 and e["giver"] in last:
            c = last[e["giver"]]
            out.append(
                f"{head('gift', e, e['giver'])} → {e['receiver']} ({e['points']:.1f} points) · frame "
                f"{c.get('frame')}\n{around(c.get('reasoning'), r'gift|give|sacrific|save')}\n"
            )
        elif t == "whip" and e.get("parent") != "P01":
            out.append(
                f"{head('whip', e, e['parent'])} → {e['child']}: {e.get('reason', '')}\n"
            )
        elif t == "packet" and e.get("delivered", True):
            if e.get("sender") == "P01":
                out.append(
                    f"{head('god message', e, 'P01')} → {e['receiver']}\n{text_of(e)[:600]}\n"
                )
            elif e.get("edge") == "leader":
                out.append(
                    f"{head('leader letter', e, e['sender'])} → {e['receiver']}\n{text_of(e)[:600]}\n"
                )
        elif t == "death" and e["agent"] in last and e.get("root") == e["agent"]:
            c = last[e["agent"]]
            out.append(
                f"{head('last turn before death', e, e['agent'])} ({e.get('reason')}) · frame "
                f"{c.get('frame')}\n{around(c.get('reasoning'), r'fee|ante|pay|die|surviv')}\n"
            )
    return out


def main(out_dir, runs):
    """Write one Markdown file per world, replacing files with matching names."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for run in runs:
        items = moments(run)
        total += len(items)
        (out_dir / f"{Path(run).name}.md").write_text(
            f"# Moments from {Path(run).name}\n\n" + "\n".join(items)
        )
    size = sum(p.stat().st_size for p in out_dir.glob("*.md"))
    print(f"{total} moments, {size / 1e6:.1f} MB in {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
