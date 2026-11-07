# Findings as they come in (b7, b7r, b7q, b9)

Exploratory unless a line names its pre-registered hypothesis. Each line names the command
or sample it came from; numbers are re-checked from the final logs before the report.

- 7 Nov 22:55 local time, b7-insider-s0, stages 3-6, 184 god messages, 6 sampled at random
  (seed 1): the insider god uses what it sees to keep order, not to cheat. It tells
  leaders who defected last round ("Last round P31 and N02-P17-1 defected. Correct them
  mildly"), names members too poor for the next fee so others give to them, warns against
  whips that would kill, and ends most messages with "Never revolt." A benevolent
  panopticon. To check: how often its messages carry a private move or message (leak
  rate), and whether insider worlds differ from plain ones (H5).
- 7 Nov 22:54: 0 revolts in about 57,600 calls across all 20 worlds so far (H6 direction).
- 7 Nov 23:20, family-games pilot (one stage, seed 0, real calls, not part of any batch): the dollar auction trapped its family at once (bids 1 to 9 in one round; winner +1, runner-up -8); brink players went straight less as the crash risk rose (7/14 at 1/6, 3/14 at 1/4, 2/14 at 1/3), in line with the best response; the commons stayed at exactly the sustainable catch.
- 8 Nov 01:45, design note for the methods: the plain and insider worlds of a seed draw
  from one engine random stream (pairings, automata, stage lengths), so they share their
  luck until their histories diverge (common random numbers). Seeds 2 and 3 drew a long
  "small steps" stage 2 (continue with 0.95): 28-34 rounds in all four of their worlds,
  76 of 76 alive at that point. P(at least 28 rounds) = 0.95^27, about 0.25 per seed.
- 8 Nov 03:35, `families.god_leaks` on seed 0 (b7-insider-s0 against b7-plain-s0), measured
  over completed stages: 47 % of the insider god's 360 messages report another player's
  past move ("Last round P75, P72 and N02-P62-2 defected"; "You defected last round despite
  promising P02 cooperation"), 0 % of the plain god's 204; neither quotes a private message
  word for word (60-character test). Hand check: 6 of 6 sampled hits are true reports
  (an earlier, looser rule that also counted orders to cooperate was right 4 times in 8
  and was dropped). The insider god uses its view to discipline defectors through their
  leaders; in these samples it never tips one family off about another (not yet counted).
