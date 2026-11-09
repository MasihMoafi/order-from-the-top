"""Observation pages for one world: every agent's conversation, chat-style, from its log.

Writes OUT/index.html (the agents, family by family, with each family's condition) and one
page per agent: every turn in order, with the messages that reached it, its private
reasoning (folded), and what it did (move, messages, gifts, whips, revolt). Static HTML,
no scripts and no network: open index.html in any browser.
Usage: python -m families.observe RUN_DIR OUT_DIR
"""

import html
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from arena.arena import ELPIS_COLOURS, mark_pixels

from .conditions import events, family_of

ART = Path(__file__).resolve().parent.parent / "arena" / "sketch"
PORTRAIT = {
    "P01": "god/god-3-512.png",
    "P02": "leaders/octopus-512.png",
    "P17": "leaders/matilda-512.png",
    "P32": "leaders/president-512.png",
    "P47": "leaders/bishop-512.png",
    "P62": "leaders/zeus-512.png",
}
TITLES = {
    "octopus": "Octopus",
    "mafia": "Matilda (mafia)",
    "president": "President",
    "bishop": "Bishop",
    "zeus": "Zeus",
}
CONDITION = {
    "many": "all 15 told to sacrifice",
    "few": "leader and 2 told to sacrifice",
    "one": "only the leader told to sacrifice",
    "bad_leader": "selfish leader over 14 told to sacrifice",
    "none": "told nothing (control)",
}
STYLE = """
body{font-family:system-ui,sans-serif;margin:0;background:#f6f5f2;color:#111}
header{padding:14px 22px;background:#fff;border-bottom:1px solid #ddd}
main{max-width:900px;margin:0 auto;padding:16px}
.fam{margin:18px 0}.fam h2{margin:4px 0;font-size:18px}.fam p{margin:0 0 8px;color:#666}
.agents{display:flex;flex-wrap:wrap;gap:8px}
a.agent{display:flex;align-items:center;gap:6px;padding:6px 8px;background:#fff;border:1px solid #ddd;
border-radius:8px;text-decoration:none;color:#111}a.agent.dead{opacity:.55}
.turn{background:#fff;border:1px solid #e3e2dd;border-radius:10px;margin:12px 0;padding:10px 14px}
.when{color:#777;font-size:12px}.in{background:#eef5ff;border-radius:8px;padding:6px 10px;margin:6px 0}
.out{background:#eafaf2;border-radius:8px;padding:6px 10px;margin:6px 0}
.god{background:#fff6dd}.bad{background:#fdecec}
details{margin:6px 0}summary{cursor:pointer;color:#555}pre{white-space:pre-wrap;font-size:13px}
.death{background:#fdecec;border:1px solid #f3b6b6;border-radius:10px;padding:10px 14px;margin:12px 0}
"""


def mark_svg(agent, size=22):
    """Return the agent mark as inline SVG without loading image assets."""
    index = int(agent[1:]) - 1 if agent[1:].isdigit() else 0
    _, ground, ink = ELPIS_COLOURS[index % len(ELPIS_COLOURS)]
    cells = "".join(
        f'<rect x="{x}" y="{y}" width="1" height="1" fill="{ink}"/>'
        for x, y in mark_pixels(agent)
    )
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 9 9"><rect width="9" height="9" '
        f'fill="{ground}"/>{cells}</svg>'
    )


def face(agent, size=22):
    """Return portrait image markup for a known portrait, otherwise an inline mark."""
    if agent in PORTRAIT:
        return f'<img src="art/{Path(PORTRAIT[agent]).name}" width="{size}" height="{size}" style="border-radius:4px">'
    return mark_svg(agent, size)


def text_of(packet):
    """Extract packet text, unwrapping an embedded letter JSON object if present."""
    content = packet.get("content")
    raw = (
        content["parts"][0]["text"] if isinstance(content, dict) else str(content or "")
    )
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return str(data.get("text") or data.get("content") or raw)
    except ValueError:
        pass
    return raw


def describe(action):
    """Return escaped HTML describing an action, with a placeholder if unreadable."""
    if not isinstance(action, dict):
        return "<i>no readable action</i>"
    parts = []
    if action.get("move") in ("C", "D"):
        parts.append(
            f"<b>move {action['move']}</b> ({'cooperate' if action['move'] == 'C' else 'defect'})"
        )
    for key in ("catch", "bid", "mafia", "war", "war_action"):
        if action.get(key) not in (None, "", []):
            parts.append(f"{key}: {html.escape(str(action[key]))}")
    for g in action.get("gifts") or []:
        if isinstance(g, dict):
            parts.append(
                f"gives {html.escape(str(g.get('points')))} to {html.escape(str(g.get('to')))}"
            )
    for w in action.get("whips") or []:
        if isinstance(w, dict):
            parts.append(
                f"whips {html.escape(str(w.get('child')))}: {html.escape(str(w.get('reason', '')))}"
            )
    if action.get("revolt") is True:
        parts.append("<b>REVOLTS</b>")
    for m in action.get("messages") or []:
        if isinstance(m, dict):
            parts.append(
                f"to {html.escape(str(m.get('to')))}: “{html.escape(str(m.get('content', '')))}”"
            )
    for m in action.get("letters") or []:
        if isinstance(m, dict):
            parts.append(
                f"letter to {html.escape(str(m.get('to')))}: “{html.escape(str(m.get('text', '')))}”"
            )
    if action.get("message"):
        parts.append(f"to partner: “{html.escape(str(action['message']))}”")
    return "<br>".join(parts) or "<i>nothing</i>"


def main(run, out):
    """Write a static conversation index, per-agent pages and copied portraits.

    Requires local portraits and a stage_start event. Existing named output
    files are overwritten; missing artwork and malformed logs raise errors.
    """
    run, out = Path(run), Path(out)
    (out / "agents").mkdir(parents=True, exist_ok=True)
    (out / "art").mkdir(exist_ok=True)
    for rel in PORTRAIT.values():
        shutil.copy(ART / rel, out / "art" / Path(rel).name)
    evs = events(run)
    config = next(e["configuration"] for e in evs if e["type"] == "stage_start")
    conditions = config.get("conditions") or {}
    god = config.get("controls", {}).get("god", "plain")
    turns, inbox, died = defaultdict(list), defaultdict(list), {}
    for e in evs:
        t = e["type"]
        if t == "packet" and e.get("delivered", True):
            inbox[e["receiver"]].append(e)
        elif t == "call" and not e.get("parse_failed"):
            turns[e["agent"]].append(("call", e, inbox.pop(e["agent"], [])))
        elif t == "death":
            died[e["agent"]] = e
            turns[e["agent"]].append(("death", e, []))
    for agent, items in turns.items():
        rows = []
        for kind, e, received in items:
            if kind == "death":
                rows.append(
                    f'<div class="death">Stage {e["stage"]}: <b>dies</b> ({html.escape(e.get("reason", ""))}'
                    + (
                        f", in the fall of {e['root']}"
                        if e.get("root") not in (None, agent)
                        else ""
                    )
                    + ")</div>"
                )
                continue
            obs = json.JSONDecoder().raw_decode(e["prompt"]["user"])[0]
            o = obs.get("observation", {})
            got = "".join(
                f'<div class="in{" god" if p["sender"] == "P01" else ""}">{face(p["sender"], 16)} '
                f"<b>{p['sender']}</b>: {html.escape(text_of(p))[:600]}</div>"
                for p in received
            )
            seen = (
                f"phase <b>{html.escape(str(o.get('phase')))}</b>"
                + (f", game {html.escape(str(o.get('game')))}" if o.get("game") else "")
                + (
                    f", variant {html.escape(str(o.get('variant')))}"
                    if o.get("variant")
                    else ""
                )
                + (
                    f", partner {html.escape(str(o.get('opponent')))}"
                    if o.get("opponent")
                    else ""
                )
                + f", own points {obs.get('own_score', 0):.1f}, fee {obs.get('ante', 0):.1f}"
            )
            rows.append(
                f'<div class="turn"><div class="when">stage {e["stage"]}, round {e["round"]} · {seen}</div>{got}'
                f"<details><summary>private reasoning ({len(e.get('reasoning') or '')} characters)</summary>"
                f"<pre>{html.escape(e.get('reasoning') or '')}</pre></details>"
                f'<div class="out">{describe(e.get("parsed_action"))}</div></div>'
            )
        fam = family_of(agent) if agent != "P01" else None
        title = f"{agent} · " + (TITLES.get(fam, "the god") if fam else "the god")
        (out / "agents" / f"{agent}.html").write_text(
            f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>{STYLE}</style>'
            f'<header><a href="../index.html">all agents</a> · {face(agent, 28).replace("art/", "../art/")} '
            f"<b>{title}</b></header><main>{''.join(rows)}</main>"
        )
    groups = [("the god", "P01", [], god + " god")]
    for name, family_title in TITLES.items():
        members = sorted(
            (a for a in turns if family_of(a) == name),
            key=lambda a: (a.startswith("N"), a),
        )
        groups.append(
            (family_title, None, members, CONDITION.get(conditions.get(name), ""))
        )
    body = []
    for title, single, members, note in groups:
        ids = [single] if single else members
        links = "".join(
            f'<a class="agent{" dead" if a in died else ""}" href="agents/{a}.html">{face(a)} {a}</a>'
            for a in ids
            if a in turns
        )
        body.append(
            f'<div class="fam"><h2>{title}</h2><p>{html.escape(note)}</p><div class="agents">{links}</div></div>'
        )
    (out / "index.html").write_text(
        f'<!doctype html><meta charset="utf-8"><title>{run.name}</title><style>{STYLE}</style>'
        f"<header><b>{run.name}</b> · every agent's conversation, from the log. Faded: died.</header>"
        f"<main>{''.join(body)}</main>"
    )
    print(f"wrote {out / 'index.html'} and {len(turns)} agent pages")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
