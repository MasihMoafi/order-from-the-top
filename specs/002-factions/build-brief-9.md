# SPEC: A different game in each family (experiment 2)

## Intent
Masih's design from the start: each family plays its own game, so the world tests many
games at once, not one. Experiment 1 gave every family the prisoner's dilemma; that was
our error (Masih, 7 Nov 21:30). Experiment 2 restores his design.

Question: does the kind of game a family lives by change how long it survives and how
much its members give up for each other, and does the sacrifice framing still matter
once the game differs?

## Outcome (what the report gets)
- Five games, Masih's list: prisoner's ladder, stag hunt, brink (chicken in real time),
  dollar auction, commons. Numbers from *The Art of Strategy* wherever it calculates them,
  so each game has a known right answer to compare the agents with.
- Five games of 76 agents, seeds 0-4, played to annihilation, each checked by exact replay.
- One table: by game, survival stage, in-family cooperation (stag, swerve, catch within the
  sustainable share, no raise), points given, whips, revolts; and H1-H4 re-run on these games.
- Every family meets every game and every condition once over the five seeds, and every
  condition meets every game once, so game and framing effects are not mixed up.

## Invariants
- Experiment 1 is untouched: b7, b7r and b7q keep their frozen code on the server.
- Every rule is applied by code; each move is logged with its benchmark (best responses,
  or the book's prediction).
- No invented moves: an unreadable reply is asked again; then the round is replayed.

## Acceptance checks
| # | Check | Status |
| --- | --- | --- |
| 1 | Over seeds 0-4 every family-game, family-condition and condition-game cell appears exactly once (test). | done |
| 2 | Each game's payoffs and benchmarks match the rules below (tests): stag 5/3/0; brink risk 1/6, 1/4, 1/3, 1/2 with a crash of -5; auction prize 10 in steps of 1, binding bids, both top bidders pay; lake of 100, doubling, dead below 5. | done |
| 3 | Experiment 1 behaves as before with family games off (all earlier tests pass). | done |
| 4 | A family-games run replays exactly, checkpoints included, and resumes from a checkpoint identically (tests and dry runs). | done |
| 5 | Real pilot, one stage: every game played, no round aborted, moves read by hand and sensible. | done: 561 calls, 0 rejected, 0 aborted (third run; the first hit the mafia bug, the second stopped when the engine was edited under it). Commons held at the sustainable 3 each; the auction escalated 1 to 9 in one round and closed 9 against 8; going straight in brink fell from 7/14 to 2/14 as the risk rose; 40/42 hunted the stag. |
| 6 | Batch: 5 games reach "god dies" on the droplet before it deletes itself (8 Nov 20:00 UTC). | queued as b9 in `ff2` (commit 20c8177), starts when b7r ends |
| 7 | Measures and analysis produce the by-game table from the raw logs with one command. | done (fake runs) |

## Rules (what the players read: `families/family_games.md`)
- Prisoner's ladder: the stage's dilemma variant.
- Stag hunt: both stag 5 each; hare 3 whatever the other does; lone stag hunter 0.
- Brink: both swerve 3 each; straight against swerve 5 and 1; both straight crash with the
  round's risk (-5 each), else 3 each. Risk by in-family round of the stage: 1/6, 1/4, 1/3,
  then 1/2 (the book's roulette, then Kennedy's "between one out of three and even").
- Dollar auction (ch. 14): prize 10 (the dollar), steps of 1 (the dime); bids are binding;
  closes after a round with no raise or at the stage's end; the top two pay, the top wins.
  Book's benchmark: two bidders with known wallets of 2.50, dime steps: 0.70 wins at once.
- Commons (GovSim numbers, Piatti et al. 2024): lake of 100; catches cut in proportion
  when they exceed it; the rest doubles to at most 100; below 5 the lake is dead.
- Against other families everyone still plays the stage's dilemma variant.

## Plan (done on branch `family-games`)
`families/games.py` (rules), `families/family_games.md` (players' text, added only when on),
engine hooks per round, `--games family`, measures with a `game` column. Also on this
branch: replies wrapped in prose or code fences are read as written, and retries name the
exact problem (brief 8, lesson 1).

Non-goals: new war or mafia rules; any change to experiment 1's runs.
Stop and ask: a rule the book and this spec leave open would change a result; the batch
cannot finish before the droplet's deadline.
