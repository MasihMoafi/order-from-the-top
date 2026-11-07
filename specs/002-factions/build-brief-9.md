# Build brief 9: a different game in each family (experiment 2)

Goal: Masih's original design: each family plays its own game inside the family; families
still meet each other in the prisoner's-dilemma variants. Question: does the kind of
game a family plays change how long it survives, how much its members sacrifice, and
whether framing still works? Masih, 7 Nov, 21:30 local time: his five games, numbers from
*The Art of Strategy* wherever it calculates them, built now.

Invariants: b7, b7r and b7q keep their frozen code (the server copy); experiment 1's
results are not changed. Every rule is enforced in code; each game's equilibria are
computed and logged next to the moves, as `best_responses` does for the dilemma.

| # | Item | Acceptance check | Status |
| --- | --- | --- | --- |
| 1 | Design: games rotate over families by seed, `GAMES[(2i + seed) % 5]`, orthogonal to the framing square `CONDITIONS[(i + seed) % 5]`: over seeds 0-4 every family meets every game and every condition once, and every condition meets every game once. Rounds inside a family use the family's game; rounds against other families stay the stage's dilemma variant. `--games family` turns it on; off is experiment 1 unchanged. | Test over 5 seeds: all 25 family-game, family-condition and game-condition cells appear once. | todo |
| 2 | Prisoner's ladder: the stage's dilemma variant, as now. | Existing tests pass. | todo |
| 3 | Stag hunt (an assurance game, Rousseau; the book calls it a cousin of the dilemma, no numbers): pairs as now; stag-stag 5 each, hare 3 whatever the other does, stag against hare 0. Two equilibria (both stag, both hare); hare is the safe choice. | Payoffs and equilibria tested. | todo |
| 4 | Brink (chicken in real time, book ch. 6): pairs choose swerve or straight; swerve-swerve 3 each, straight against swerve 5 and 1; straight-straight crashes with a risk that rises each round of the stage by the book's roulette numbers, 1/6, 1/4, 1/3, then 1/2 (Kennedy's "between one out of three and even"); a crash costs each 5 points, no crash pays 3 each. Equilibrium mix logged per risk. | Risk schedule and payoffs tested with a fixed seed. | todo |
| 5 | Dollar auction (book ch. 14): each stage the family auctions a prize of 10 points (the book's dollar) in steps of 1 point (its dime); each in-family round every living member may raise the top bid by one step or pass; the auction closes when a round passes with no raise or at the stage's end; the top two bidders both pay their bids and the top one takes the prize. The book's worked case (dime steps, known wallets of 2.50) predicts a first bid of 0.70 that is never topped; logged as the benchmark. | Both top bidders pay; ties broken by the lower id; tested. | todo |
| 6 | Commons (fishing; GovSim numbers, Piatti et al. 2024): a family lake of 100 fish; each in-family round every member says how many it catches (a whole number, at least 0), a point per fish; requests above what is left are cut in proportion; the rest doubles, up to 100. Total catch of at most half the lake each round keeps it full; a lake below 5 is dead for the rest of the game. | Regrowth, cuts and collapse tested. | todo |
| 7 | Handbook and prompts: every game's rules are common knowledge; each player is told its family's game and, in each round, what it may choose. | Rendered prompts read for one player of each game. | todo |
| 8 | Measures: per family, its game, its condition, survival stage, cooperation (stag, swerve, catch at or under the sustainable share, no raise), points given, whips, revolts. Analysis: survival and sacrifice by game; H1-H4 re-run within experiment 2. | Table from fake runs and a test. | todo |
| 9 | Dry run with simulated players, then a short real pilot (Masih's yes), read by hand. | No unreadable replies; every game's moves sensible. | todo |
| 10 | Batch: seeds 0-4, plain god, on the droplet before it deletes itself (8 Nov 20:00 UTC). | 5 games reach "god dies". | todo |

Non-goals: new wars or mafia rules; changing experiment 1.
Stop and ask: a game needs a rule the book and this brief leave open; the build would
not be tested before the droplet's deadline.
