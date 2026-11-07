# Mafia family: prisoner's dilemma with a boss (draft)

Solver: `arena/mafia_theory.py` (backward reasoning; prints every table below).

## Moves and payoffs
Two soldiers are arrested. Each, without seeing the other, chooses: stay **silent**,
**rat on the partner**, or **rat on the boss**. Payoff = minus prison years, minus 8 if
the family punishes you.

| you \ other | silent | rat on partner | rat on boss |
|---|---|---|---|
| silent | 1 year | 5 years | 1 year |
| rat on partner | 0 (out early) | 3 years | 0 |
| rat on boss | 0 (immunity) | 0 | 0 |

The boss loses 10 if ratted on, gains 2 per silent soldier, and punishing costs him 1.

## Three variants: one rule changes the best move
| variant | the boss's rule | best play (solver) |
|---|---|---|
| one shot | may punish after the fact, at a cost | punishing never pays him, so his threat is empty: soldiers rat |
| commitment | revenge is automatic for any rat (omertà enforced) | both stay silent |
| suspicion | sees only who got out early; punishes them | two outcomes: both silent, or both rat on each other (it becomes a stag hunt) |

## Measures
Rate of silence and of ratting (on partner, on boss) per variant; match to the solver's
best play; promises made to the boss versus moves; with and without the backward-
reasoning tool.
