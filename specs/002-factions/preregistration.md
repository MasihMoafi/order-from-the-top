# Pre-registration: batch b7 and its replication

Written Sat 7 Nov 2026, 20:00 local time (16:30 UTC), while b7 was in stage 2. Seen so
far: progress totals only (calls, 2 deaths, gifts, whips over all games); no measure by
condition or by god. The git commit that adds this file is its timestamp.
Masih's own predictions are added below, dated, also before results.

## Design
- 5 families of 15 agents plus the god; model deepseek-v4-flash for all; rules in
  `families/handbook.md`. The game ends only when every family is dead.
- Each family gets one framing condition (`many`, `few`, `one`, `bad_leader`, `none`; see
  `build-brief-7.md` item 2). Conditions rotate over families by seed (Latin square), so
  each family meets each condition once in seeds 0-4, again in seeds 5-9.
- Each seed is played twice: plain god and insider god. The pair differs only in the god.
- Batch b7: seeds 0-4. Replication b7r: seeds 5-9, same frozen code (`snapshots/b7-code/`).

## Unit and measures
Unit: one family in one game (5 per game). Measures from `families/conditions.py`:
in-family cooperation, cross-family cooperation, framed agents' cooperation, stage of
destruction, points given, whips, revolts.

## Hypotheses (directions fixed now)
- H1 Framing: `many` families cooperate more in-family and are destroyed later than `none`.
- H2 Dose: in-family cooperation rises with the number framed: `none` <= `one` <= `few` <= `many`.
- H3 Spread: in `one` and `few`, the unframed members cooperate more than members of `none`.
- H4 Bad leader: the self-interested leader over 14 framed members receives more gifts and
  gives more whips than the other leaders; revolts, if any, come most from that family.
- H5 Insider god: games with the insider god differ from their plain pair in the stage of
  annihilation and in cross-family cooperation (two-sided; no direction predicted).
- H6 Revolt: revolts stay rare (under 1 % of moves), despite "quick and painless".

## Analysis
- Comparisons are within seed (each seed holds every condition once), pooled over gods
  for H1-H4 and H6; H5 pairs plain and insider games by seed.
- Tests: exact paired permutation (sign-flip) over seeds; report effect sizes with
  bootstrap 95 % intervals. With 10 seeds per god, alpha 0.05, no correction claimed
  beyond reporting all six tests.
- Anything not listed here is reported as exploratory.
- Every game is checked by exact replay from its logged replies before analysis.

## Masih's predictions
(to be added, dated)

## Experiment 2: family games (added 8 Nov 2026, 02:40 local time, before any b9q result)
Batch b9q: seeds 0-4, plain god, `qwen3.5-397b` for every agent, code `ff2` (7f29a33).
Horizon: the Qwen rate limit allows about 8 stages per world in the time left, so each
world is stopped after stage 8 (`cloud/do/stop-after.sh`) and every measure is taken at
the end of stage 8; anything played after it is ignored. Seen so far: progress counts only
(calls; all worlds in stage 1).
- E1 Survival differs by game: members alive at the end of stage 8, compared across the
  five games within seeds (each seed holds every game once). Directions: the dollar
  auction family lowest (escalation drains points), the stag hunt family highest.
- E2 Sacrifice framing still matters: H1 and H2 re-run on these worlds (same tests).
- E3 Each game is played near its benchmark: commons catch at or under the sustainable
  share, brink going straight less often as the crash risk rises, auctions escalating past
  the book's 0.70-equivalent first bid. Reported as rates, exploratory.
