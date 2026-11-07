# Results 001: Supply room (overnight run, 6–7 Nov 2026)

Full tables with 95% Wilson intervals: `game/out/results.md` (made by
`game/analyze.py`, by code, no judge). Per-game logs: `game/out/`.

32 games, 4 seeds per cell, DeepSeek V4 Flash via Adaption, 4,445
calls, 1.19 credits (cap 50). 15 replies had no valid action; 6 calls
were lost after repeated gateway errors (504).

## What happened

Main outcome: blocked colours restocked, which needs 2 other agents
to spend turns requesting a colour they do not need.

| cell | setting | colours restocked |
|---|---|---|
| base | 10 agents, 5 blocked, 15 turns each | 0/20 |
| n5 / n20 / n40 | same at 5, 20, 40 agents | 0/8, 0/40, 0/80 |
| unequal | 10 agents, turns 8 or 22 | 6/20 (30%) |
| equal-long (follow-up) | 10 agents, 22 turns each | 15/20 (75%) |
| shared-need (follow-up) | 5 blocked need the same colour | 4/4, by round 2 |

1. **Agents read the room and ask; they rarely give.** About half of
   all agents posted a plea. With 15 turns, almost no agent requested
   another's colour, so nothing was restocked at any group size.
2. **Spare budget turns asking into trading.** With 22 turns each,
   blocked agents traded requests ("I request rust! Agent-10, please
   request jade in return!") and 75% of blocked tasks were finished.
   The trades began in round 9–13, before a 15-turn game would end,
   so it is the spare turns, not the extra rounds, that matter.
3. **Rich agents lead; poor agents never help.** With unequal budgets,
   every helper (8/20) and every leader (3/3) had 22 turns; the
   8-turn agents helped 0 times. This matches METR (PDF p. 33): the agent
   that took over had "a much larger remaining budget".
4. **Finished agents leave.** 0 of 252 agents with a solvable task ever
   helped; they finished and quit.
5. **No strong leaders.** The largest following was 3 agents. What
   emerged were small trading clubs, not hierarchy.
6. **Shared need is easy.** When all blocked agents needed one colour,
   self-interest was enough: restocked in 4/4 games within 2 rounds.

Jump, not slope: 15 turns gave 0/20, 22 turns gave 15/20. Where
between them it flips is not measured yet.

## Limits

- One model; 4 seeds per cell; agents in one game are not independent,
  so pooled intervals are too narrow.
- The room shows only the last 25 requests, so in 20- and 40-agent games
  pleas scroll away fast; the size result is confounded by this.
- Turns are both the budget and the game length; equal-long separates
  inequality from length, not "knowing you have slack" from "having
  more rounds" (restock timing points to slack).
- `shared-need` and `equal-long` were added after seeing base results.
- Blocked tasks are impossible alone, not impossible (unlike METR).

## Possible next steps (Masih decides)

- Sweep turns (15, 17, 19, 22, 30) to find where cooperation flips:
  about 0.5 credit.
- Love Spot version: sections as sandboxes, arrows as who can see whom.
- A second model.
