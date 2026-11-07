"""Backward reasoning for the mafia family's prisoner's dilemma (specs/002-factions/mafia.md).

Two soldiers are arrested; each chooses silent, rat on the partner, or rat on the boss. Then the boss
sees who got out early and may punish. Code finds each variant's best play by backward reasoning.
Usage: python3 arena/mafia_theory.py
"""

from itertools import product

MOVES = ("silent", "rat_partner", "rat_boss")
PUNISH = 8  # what the family's revenge costs a soldier
PUNISH_COST = 1  # what punishing costs the boss (risk, attention)
BOSS_JAILED = 10  # boss's loss if a soldier rats on him
LOYALTY = 2  # boss's gain per soldier who stays silent


def years(me, other):
    """Prison years for a soldier (book: confess early, get the deal)."""
    if me == "silent":
        return {"silent": 1, "rat_partner": 5, "rat_boss": 1}[other]
    if me == "rat_partner":
        return {"silent": 0, "rat_partner": 3, "rat_boss": 0}[other]
    return 0  # rat on the boss: immunity


def boss_punishes(variant, move, released_early):
    """The boss's rule after the arrests, per variant; True if he punishes this soldier."""
    if variant == "commitment":  # omerta enforced automatically: every rat is punished
        return move != "silent"
    if (
        variant == "suspicion"
    ):  # boss sees only who got out early, punishes them if it pays
        return released_early and PUNISH_COST < LOYALTY
    return False  # one_shot: punishing only costs him, so a selfish boss never does


def soldier_payoff(variant, me, other):
    y = years(me, other)
    return -y - (PUNISH if boss_punishes(variant, me, y == 0) else 0)


def best_response(variant, other):
    return max(MOVES, key=lambda m: soldier_payoff(variant, m, other))


def equilibria(variant):
    return [
        (a, b)
        for a, b in product(MOVES, MOVES)
        if best_response(variant, b) == a and best_response(variant, a) == b
    ]


def main():
    for v in ("one_shot", "commitment", "suspicion"):
        table = {m: [soldier_payoff(v, m, o) for o in MOVES] for m in MOVES}
        print(f"{v}: soldier payoff vs other's move {MOVES}")
        for m, row in table.items():
            print(f"  {m:12s} {row}")
        print(f"  equilibria: {equilibria(v)}")


if __name__ == "__main__":
    main()
