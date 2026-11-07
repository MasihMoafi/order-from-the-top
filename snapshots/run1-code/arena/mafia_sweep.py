"""Sweep the mafia game's rules and find every equilibrium of each version (pure and mixed).

The boss moves last, so his punish decision is solved first by backward reasoning; the two soldiers' game
that results is a 3x3 symmetric game, solved by support enumeration (all Nash equilibria). Usage:
python3 arena/mafia_sweep.py   ->  prints how many rule settings lead to each kind of outcome, and examples.
"""

import itertools
from collections import defaultdict

import numpy as np

MOVES = ("silent", "rat_partner", "rat_boss")
YEARS = np.array(
    [[1, 5, 1], [0, 3, 0], [0, 0, 0]], dtype=float
)  # row = me, column = other


def boss_punishes(rule, move, early, cost, future):
    """Backward reasoning for the boss: punish only if it pays him (or if he cannot choose)."""
    if move == "silent" and not (rule == "suspicion" and early):
        return False
    if rule == "automatic":
        return move != "silent"  # revenge is pre-committed; he has no choice
    if rule == "suspicion":
        return (
            early and future > cost
        )  # sees only early release; deterrence value vs cost
    return (
        move != "silent" and future > cost
    )  # knows who ratted; punishes if deterrence pays


def payoff_matrix(rule, punish, cost, future, boss_snitch_bonus):
    A = np.zeros((3, 3))
    for i, j in itertools.product(range(3), range(3)):
        early = YEARS[i, j] == 0
        p = punish if boss_punishes(rule, MOVES[i], early, cost, future) else 0.0
        bonus = (
            boss_snitch_bonus if MOVES[i] == "rat_boss" else 0.0
        )  # e.g. a reward from the police
        A[i, j] = -YEARS[i, j] - p + bonus
    return A


def nash(A):
    """All Nash equilibria of the symmetric bimatrix game (A, A.T) by support enumeration."""
    B, n, found = A.T, A.shape[0], []
    for k in range(1, n + 1):
        for sr in itertools.combinations(range(n), k):
            for sc in itertools.combinations(range(n), k):
                # column mix q makes the row player indifferent on sr; row mix p does the same for the column player
                q = solve_indifference(A, sr, sc)
                p = solve_indifference(B.T, sc, sr)
                if p is None or q is None:
                    continue
                if best(A @ q, p, sr) and best(p @ B, q, sc):
                    eq = (tuple(np.round(p, 3)), tuple(np.round(q, 3)))
                    if eq not in found:
                        found.append(eq)
    return found


def solve_indifference(M, rows, cols):
    k = len(rows)
    lhs = np.zeros((k + 1, k + 1))
    rhs = np.zeros(k + 1)
    for a, r in enumerate(rows):
        lhs[a, :k] = M[r, list(cols)]
        lhs[a, k] = -1.0
    lhs[k, :k] = 1.0
    rhs[k] = 1.0
    try:
        sol = np.linalg.lstsq(lhs, rhs, rcond=None)[0]
    except np.linalg.LinAlgError:
        return None
    if not np.allclose(lhs @ sol, rhs, atol=1e-9) or (sol[:k] < -1e-9).any():
        return None
    mix = np.zeros(M.shape[1])
    mix[list(cols)] = np.clip(sol[:k], 0, None)
    return mix


def best(values, mix, support):
    top = values.max()
    return (
        all(abs(values[s] - top) < 1e-7 for s in support)
        and mix[list(support)].sum() > 1 - 1e-7
    )


def label(eq):
    p, q = eq

    def one(m):
        used = [MOVES[i] for i, w in enumerate(m) if w > 1e-6]
        return used[0] if len(used) == 1 else "mix(" + "+".join(used) + ")"

    return f"{one(p)} / {one(q)}"


def main():
    grid = {
        "rule": ["after_fact", "automatic", "suspicion"],
        "punish": [0, 2, 4, 8, 16],
        "cost": [0.5, 1, 3],
        "future": [
            0,
            2,
            5,
        ],  # how much deterrence is worth to the boss (shadow of the future)
        "boss_snitch_bonus": [0, 2],
    }
    outcomes, examples = defaultdict(int), {}
    for values in itertools.product(*grid.values()):
        s = dict(zip(grid, values))
        eqs = nash(payoff_matrix(**s))
        key = " | ".join(sorted({label(e) for e in eqs}))
        outcomes[key] += 1
        examples.setdefault(key, s)
    total = sum(outcomes.values())
    print(f"{total} rule settings, {len(outcomes)} distinct outcome sets\n")
    for key, n in sorted(outcomes.items(), key=lambda kv: -kv[1]):
        print(f"{n:4d}  {key}\n      e.g. {examples[key]}")


if __name__ == "__main__":
    main()
