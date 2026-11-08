"""Regenerate every number, table and figure the report uses, from the pulled logs.

Usage: python -m families.paper PULLED_DIR REPORT_DIR
Writes REPORT_DIR/tables/prereg.tex (H1-H6), tables/conditions.tex (rates by condition),
tables/games.tex (experiment 2, at its horizon), numbers.tex (\\newcommand macros used in
the text) and figures/*.pdf, plus results.md (the same numbers, readable). Run it after
every pull; the report then compiles with the new numbers and nothing is typed by hand.
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
    return sorted(str(p) for p in Path(pulled).glob(f"{prefix}-*-s?") if p.is_dir())


def pct(c, n):
    return f"{100 * c / n:.1f}" if n else "--"


def fmt_p(p):
    return (
        "$<0.001$"
        if p is not None and p < 0.001
        else (f"{p:.3f}" if p is not None else "--")
    )


def prereg_table(results):
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
    return f"\\newcommand{{\\{name}}}{{{value}}}\n"


def main(pulled, report):
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
    exp2 = worlds(pulled, "b9q")
    if exp2:
        os.environ["HORIZON"] = str(HORIZON2)
        table2 = [r for w in exp2 for r in rows(w)]
        (report / "tables" / "games.tex").write_text(games_table(table2))
        figures.main(report / "figures" / "exp2", exp2)
        md += "\n\n## Experiment 2\n\n" + analysis.report(exp2)
        del os.environ["HORIZON"]
    (report / "numbers.tex").write_text("".join(numbers))
    (report / "results.md").write_text(md + "\n")
    print(md)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
