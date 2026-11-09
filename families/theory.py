"""Immediate scored best responses, excluding continuation and coercion.

These are offline benchmarks, not advice in player observations.
"""

from .variants import VARIANTS


def best_responses(number, opponent=None, members=None):
    if number == 7:
        if not members or members < 1:
            raise ValueError("pool size required")
        delta = 2 / members - 1
        return ["C"] if delta > 0 else ["D"] if delta < 0 else ["C", "D"]
    if opponent not in ("C", "D"):
        raise ValueError("opponent move required")
    values = {}
    for own in ("C", "D"):
        a, b = own, opponent
        if number == 10 and "D" in (a, b):
            a = b = "D"
        payoff = VARIANTS[number - 1].resolve(a, b)[0]
        if number == 11 and own == "D":
            payoff -= 3
        if number == 12:
            payoff /= 4
        values[own] = payoff
    return [move for move, value in values.items() if value == max(values.values())]
