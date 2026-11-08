"""Write the report's tables, number macros, figures and readable results.

Discovers experiment batches under PULLED_DIR and overwrites generated files
under REPORT_DIR. Experiment 2 analysis sets HORIZON to HORIZON2, then removes
it from the environment. Requires Matplotlib; makes no model calls.
Usage: python -m families.paper PULLED_DIR REPORT_DIR
"""

import os
import statistics
import sys
from pathlib import Path

from . import analysis, figures
from .conditions import rows

CONDITIONS = ("many", "few", "one", "bad_leader", "none")
LABEL = {
    "many": "many",
    "few": "few",
    "one": "one",
    "bad_leader": "bad leader",
    "none": "none",
}
HORIZON2 = 8  # experiment 2 horizon (pre-registered)


def worlds(pulled, prefix):
    """Return sorted matching world directories; the seed suffix is one character."""
    return sorted(str(p) for p in Path(pulled).glob(f"{prefix}-*-s?") if p.is_dir())


def pct(c, n):
    """Return a percentage without its sign, or -- when the denominator is zero."""
    return f"{100 * c / n:.1f}" if n else "--"


def fmt_p(p):
    """Return a TeX p-value, using -- for None and a threshold below 0.001."""
    return (
        "$<0.001$"
        if p is not None and p < 0.001
        else (f"{p:.3f}" if p is not None else "--")
    )


def prereg_table(results):
    """Return the supported registered comparisons as a complete TeX table."""
    names = {
        "H1 in-family cooperation, many - none": "H1 & in-family cooperation, \\textit{many} $-$ \\textit{none}",
        "H1 stage destroyed, many - none": "H1 & stage destroyed, \\textit{many} $-$ \\textit{none}",
        "H2 Spearman(dose, in-family cooperation) > 0": "H2 & Spearman $\\rho$(number framed, cooperation)",
        "H3 unframed cooperation, one/few - none": "H3 & unframed cooperation, \\textit{one}/\\textit{few} $-$ \\textit{none}",
        "H4 gift points to leader, bad_leader - mean of others": "H4 & gift points to the leader, bad $-$ others",
        "H4 whips by leader, bad_leader - mean of others": "H4 & whips by the leader, bad $-$ others",
        "H5 last stage, insider - plain": "H5 & last stage reached, insider $-$ plain",
        "H5 cross-family cooperation, insider - plain": "H5 & cross-family cooperation, insider $-$ plain",
    }
    lines = [
        "\\begin{tabular}{@{}llrrrr@{}}",
        "\\toprule",
        "& Test & $n$ & Mean & 95\\,\\% interval & $p$ \\\\",
        "\\midrule",
    ]
    for name, n, mean, ci, p in results:
        if name not in names:
            continue
        ci_text = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "--"
        mean_text = f"{mean:+.3f}" if mean is not None else "--"
        lines.append(f"{names[name]} & {n} & {mean_text} & {ci_text} & {fmt_p(p)} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


def condition_table(table):
    """Return pooled family counts and rates as a complete TeX table."""
    lines = [
        "\\begin{tabular}{@{}lrrrrrr@{}}",
        "\\toprule",
        "Condition & In-family C (\\%) & Cross C (\\%) & Unframed C (\\%) & Gift points & Whips & Revolts \\\\",
        "\\midrule",
    ]
    for c in CONDITIONS:
        rs = [r for r in table if r["condition"] == c]
        s = {
            k: sum(r[k] for r in rs)
            for k in (
                "in_c",
                "in_n",
                "cross_c",
                "cross_n",
                "unframed_c",
                "unframed_n",
                "gift_points",
                "whips",
                "revolts",
            )
        }
        lines.append(
            f"\\textit{{{LABEL[c]}}} & {pct(s['in_c'], s['in_n'])} & {pct(s['cross_c'], s['cross_n'])} "
            f"& {pct(s['unframed_c'], s['unframed_n'])} & {s['gift_points']:.0f} & {s['whips']} & {s['revolts']} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


def games_table(table):
    """Return family-game summaries as a complete TeX table.

    Games without final survivor counts receive placeholder cells.
    """
    games = sorted({r["game"] for r in table})
    lines = [
        "\\begin{tabular}{@{}lrrrrr@{}}",
        "\\toprule",
        "Family game & Families & In-family C (\\%) & Alive at the end (of 15) & Gift points & Whips \\\\",
        "\\midrule",
    ]
    for g in games:
        rs = [r for r in table if r["game"] == g]
        alive = [r.get("alive_end") for r in rs if r.get("alive_end") is not None]
        lines.append(
            f"{g} & {len(rs)} & {pct(sum(r['in_c'] for r in rs), sum(r['in_n'] for r in rs))} "
            f"& {statistics.fmean(alive):.1f} & {sum(r['gift_points'] for r in rs):.0f} & {sum(r['whips'] for r in rs)} \\\\"
            if alive
            else f"{g} & {len(rs)} & -- & -- & -- & -- \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


def macro(name, value):
    """Return one TeX newcommand definition with a trailing newline."""
    return f"\\newcommand{{\\{name}}}{{{value}}}\n"


def main(pulled, report):
    """Overwrite report tables, macros, figures and Markdown from pulled worlds.

    See the module docstring for output and environment effects. Input,
    analysis and plotting failures propagate and may leave partial output.
    """
    report = Path(report)
    (report / "tables").mkdir(parents=True, exist_ok=True)
    (report / "figures").mkdir(parents=True, exist_ok=True)
    exp1 = worlds(pulled, "b7") + worlds(pulled, "b7r")
    md = analysis.report(exp1)
    results = list(analysis.RESULTS)
    (report / "tables" / "prereg.tex").write_text(prereg_table(results))
    table1 = [r for w in exp1 for r in rows(w)]
    (report / "tables" / "conditions.tex").write_text(condition_table(table1))
    figures.main(report / "figures", exp1)
    by = {name: (n, mean, ci, p) for name, n, mean, ci, p in results}
    moves = sum(r["in_n"] + r["cross_n"] for r in table1)
    revolts = sum(r["revolts"] for r in table1)
    stages = [
        max(r["end_stage"] for r in table1 if r["run"] == Path(w).name) for w in exp1
    ]
    numbers = [
        macro("NWorlds", len(exp1)),
        macro("NMoves", f"{moves:,}"),
        macro("NRevolts", revolts),
        macro("StageMin", min(stages) if stages else 0),
        macro("StageMax", max(stages) if stages else 0),
    ]
    for key, name in (
        ("HOneCoop", "H1 in-family cooperation, many - none"),
        ("HTwoRho", "H2 Spearman(dose, in-family cooperation) > 0"),
        ("HThree", "H3 unframed cooperation, one/few - none"),
        ("HFourGifts", "H4 gift points to leader, bad_leader - mean of others"),
        ("HFiveCross", "H5 cross-family cooperation, insider - plain"),
    ):
        _n, mean, ci, p = by.get(name, (0, None, None, None))
        numbers += [
            macro(key, f"{mean:+.3f}" if mean is not None else "--"),
            macro(key + "P", fmt_p(p)),
            macro(key + "CI", f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "--"),
        ]
    # Worlds that reached total annihilation, and what the god passed on (exploratory).
    from .conditions import completed, events
    from .god_leaks import leaks

    finished = [
        w
        for w in exp1
        if any(
            e["type"] == "stage_end"
            and (e.get("outcome") or {}).get("result") == "god dies"
            for e in events(w)
        )
    ]
    wars = sum(e["type"] == "war_declared" for w in exp1 for e in completed(events(w)))
    numbers += [macro("NFinished", len(finished)), macro("NWars", wars)]
    by_god = {"plain": [0, 0, 0], "insider": [0, 0, 0]}
    for w in exp1:
        row = leaks(w)
        by_god[row["god"]][0] += row["messages"]
        by_god[row["god"]][1] += row["reveal_moves"]
        by_god[row["god"]][2] += row["mention_revolt"]
    for god, (n, r, v) in by_god.items():
        name = "Insider" if god == "insider" else "Plain"
        numbers += [
            macro(f"God{name}Msgs", f"{n:,}"),
            macro(f"God{name}Reveal", f"{100 * r / n:.0f}" if n else "--"),
            macro(f"God{name}Revolt", f"{100 * v / n:.0f}" if n else "--"),
        ]
    md += (
        f"\n\nWorlds ended in annihilation: {len(finished)} of {len(exp1)}. Wars declared: {wars}.\n"
        f"God messages reporting another player's move: insider {by_god['insider'][1]}/{by_god['insider'][0]}, "
        f"plain {by_god['plain'][1]}/{by_god['plain'][0]}.\n"
    )
    exp2 = worlds(pulled, "b9q")
    if exp2:
        os.environ["HORIZON"] = str(HORIZON2)
        table2 = [r for w in exp2 for r in rows(w)]
        (report / "tables" / "games.tex").write_text(games_table(table2))
        figures.main(report / "figures" / "exp2", exp2)
        md += "\n\n## Experiment 2\n\n" + analysis.report(exp2)
        PRIZE = 10  # the auction prize: families/games.py on branch family-games

        brink, commons, closes = {}, [0, 0], []
        for w in exp2:
            for e in completed(events(w), HORIZON2):
                if e["type"] == "move" and e.get("game") == "brink":
                    tally = brink.setdefault(round(e["crash_risk"], 3), [0, 0])
                    tally[0] += sum(m == "D" for m in e["chosen"].values())
                    tally[1] += len(e["chosen"])
                elif e["type"] == "move" and e.get("game") == "commons":
                    commons[0] += sum(m == "C" for m in e["chosen"].values())
                    commons[1] += len(e["chosen"])
                elif e["type"] == "auction_close" and e.get("winner"):
                    closes.append(e["winner"][1])
        low = brink.get(round(1 / 6, 3), [0, 0])
        all_d, all_n = (
            sum(v[0] for v in brink.values()),
            sum(v[1] for v in brink.values()),
        )
        numbers += [
            macro("BrinkStraight", f"{100 * all_d / all_n:.1f}" if all_n else "--"),
            macro(
                "BrinkStraightLow", f"{100 * low[0] / low[1]:.1f}" if low[1] else "--"
            ),
            macro(
                "CommonsWithin",
                f"{100 * commons[0] / commons[1]:.0f}" if commons[1] else "--",
            ),
            macro("AuctionCount", len(closes)),
            macro("AuctionPastPrize", sum(b > PRIZE for b in closes)),
            macro(
                "AuctionMedian", f"{statistics.median(closes):.0f}" if closes else "--"
            ),
        ]
        md += (
            f"\nBrink: straight {all_d}/{all_n}; at risk 1/6 {low[0]}/{low[1]}. Commons within the sustainable "
            f"share {commons[0]}/{commons[1]}. Auctions {len(closes)}, past the prize {sum(b > PRIZE for b in closes)},"
            f" winning bids {sorted(closes)}.\n"
        )
        del os.environ["HORIZON"]
    (report / "numbers.tex").write_text("".join(numbers))
    (report / "results.md").write_text(md + "\n")
    print(md)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
