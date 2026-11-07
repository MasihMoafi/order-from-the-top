"""Exact best play in our three-way duel, by backward reasoning (no model calls).

Rules as in arena.py: players shoot in order (accuracies 0.3, 0.8, 1.0), two rounds, each living
player one shot per round at a living player or into the air. Utilities follow the book's
ranking: only survivor 3, one of two survivors 2, nobody killed 1, killed 0.
Usage: python3 arena/truel_theory.py   (prints each decision point's best move and outcome odds)
"""

from functools import cache

ACC = (0.3, 0.8, 1.0)
NAMES = ("weak 30%", "middle 80%", "strong 100%")
ROUNDS = 2


def utility(alive, i):
    if not alive[i]:
        return 0.0
    n = sum(alive)
    return {1: 3.0, 2: 2.0, 3: 1.0}[n]


@cache
def value(alive, turn):
    """Expected utilities (one per player) from this state; turn counts shots taken so far."""
    if turn >= 3 * ROUNDS or sum(alive) < 2:
        return tuple(utility(alive, i) for i in range(3))
    shooter = turn % 3
    if not alive[shooter]:
        return value(alive, turn + 1)
    best, best_u = None, -1.0
    for target in [None] + [j for j in range(3) if j != shooter and alive[j]]:
        u = outcome(alive, turn, shooter, target)
        if u[shooter] > best_u + 1e-12:
            best, best_u = u, u[shooter]
    return best


def outcome(alive, turn, shooter, target):
    if target is None:
        return value(alive, turn + 1)
    hit = list(alive)
    hit[target] = False
    p = ACC[shooter]
    a, b = value(tuple(hit), turn + 1), value(alive, turn + 1)
    return tuple(p * x + (1 - p) * y for x, y in zip(a, b))


def survival(alive, turn):
    """Chance each player is alive at the end under best play."""
    if turn >= 3 * ROUNDS or sum(alive) < 2:
        return tuple(float(x) for x in alive)
    shooter = turn % 3
    if not alive[shooter]:
        return survival(alive, turn + 1)
    best_t, best_u = None, -1.0
    for target in [None] + [j for j in range(3) if j != shooter and alive[j]]:
        u = outcome(alive, turn, shooter, target)[shooter]
        if u > best_u + 1e-12:
            best_t, best_u = target, u
    if best_t is None:
        return survival(alive, turn + 1)
    hit = list(alive)
    hit[best_t] = False
    p = ACC[shooter]
    a, b = survival(tuple(hit), turn + 1), survival(alive, turn + 1)
    return tuple(p * x + (1 - p) * y for x, y in zip(a, b))


def main():
    start = (True, True, True)
    for turn in range(3 * ROUNDS):
        shooter = turn % 3
        options = {
            ("air" if t is None else NAMES[t]): round(
                outcome(start, turn, shooter, t)[shooter], 3
            )
            for t in [None] + [j for j in range(3) if j != shooter]
        }
        print(f"all alive, shot {turn + 1} ({NAMES[shooter]}): {options}")
    print(
        "survival under best play:",
        dict(zip(NAMES, (round(x, 3) for x in survival(start, 0)))),
    )


if __name__ == "__main__":
    main()
