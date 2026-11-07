# Games from The Art of Strategy where one rule changes the best move

Source: `~/Desktop/books/The Art of Strategy A Game Theorist highlighted.pdf`
(Dixit & Nalebuff). Read in full: ch. 3, 4, 6, 9. Read in part: ch. 2
(backward reasoning), ch. 7 (credibility, Doomsday Machine, moving in
steps), ch. 10 (preemption, war of attrition), ch. 11 (brinkmanship and
strikes), ch. 14 cases (duels, dollar auction, arms). Not yet read:
ch. 5 (mixed strategies), 8 (information), 12 (voting), 13 (incentives).
The Selfish Gene is not in `~/Desktop/books`.

"The gym" = the book's 10 "Trip to the gym" exercises (answers in the
Workouts section). Useful ones: No. 1 hot potato (21 flags), reverse
ultimatum game, No. 4 cold-war threat tree, No. 8 duel timing.

## 1. The prisoner's dilemma family (ch. 3, 6, 7)

| variant | best move | humans did |
|---|---|---|
| one shot | defect | about half cooperate (Friend or Foe) |
| known number of rounds | defect from round 1 (backward reasoning) | cooperate until near the end (Flood-Dresher: defect at round 99 of 100) |
| unknown end, continue with chance d | cooperate if d is high enough (book: cheat if interest > 5.26%) | |
| with mistakes / misread moves | forgive (tit for two tats); tit for tat echoes into feuds | tamarins kept cooperating unless defected on twice in a row |
| told the other's move first | defect | 3% coop if told "defected", 16% if told "cooperated", 37% if not told |
| many players (Battalio, 27 students) | defect (each gains 46c, others lose 4c each) | 4 of 27 cooperated; the "conspiracy leader" defected |
| contribution game + paid punishment | without punishment: give 0 | punishment raises giving a lot; people pay to punish |
| who cheated is hidden vs known | cooperation fails when cheaters can't be identified | vampire bats share only with known helpers |
| meet-the-competition clause (a credible threat) | cooperate | |
| one side can promise (conditional) | cooperate | a commitment alone gets exploited |

## 2. Coordination and mixed-motive games (ch. 4)

| game | equilibria | what decides it |
|---|---|---|
| stag hunt (assurance) | all stag, all rabbit | trust; a focal point |
| meeting game (NYC, cities, pick a number) | many | focal points: noon, "1", the Mississippi |
| battle of the sexes | two; each prefers its own | who commits first; alternating |
| chicken | two asymmetric | who commits first (steering wheel out of the window) |
| half-the-other's-number (case) | 0 | depth of reasoning; people stop at 2-3 levels, reach 0 after 2-3 plays |

## 3. Escalation games: winning versus mutual loss (ch. 6, 7, 10, 11, 14)

These answer Masih's question: will agents pay a ruinous price to win?

| game | rule | best move | trap |
|---|---|---|---|
| chicken | swerve or not | let the committed one win | both commit, both crash |
| brinkmanship (Russian roulette, Cuban crisis) | risk of disaster rises each round both hold | hold only while your risk tolerance beats the other's | "controlled loss of control"; sometimes both fall |
| dollar auction (Shubik) | top two bidders both pay | with known budgets, first bid 70c ends it; best of all: collude | bidding past $1, often to the wallet limit |
| war of attrition (Sky vs BSB) | both pay each round; last one standing wins | quit early, or merge | both lose more than the prize |
| strikes (ch. 11) | daily loss grows | the side that fears breakdown less wins | each thinks the other folds first |
| preemption / duel | fire when hit chances sum to 1 | | |
| three-way duel | weakest should fire in the air | | strongest survives least (14%) |

## 4. Many-player tipping games (ch. 9)

| game | equilibria | lever |
|---|---|---|
| rat race (bell curve) | everyone over-works | cartel or outside rule |
| Bay Bridge (congestion) | middle, inefficient | toll |
| QWERTY (bandwagon) | two extremes | critical mass |
| speeding (safety in numbers) | everyone or no one | short intense enforcement |
| Schelling tipping (why did they leave?) | two extremes | hide signals (no "for sale" signs), insurance |
| law firm votes (slippery slope) | step by step to an outcome all reject | vote on the package only |

## 5. Brinkmanship game for agents (draft for Masih)

Question: when holding out risks mutual destruction, do agents yield
when the numbers say yield, or hold on to win?

- Two agents want one prize V = 10. Each round both choose Hold or
  Yield, at the same time.
- One yields: the holder gets 10, the yielder 2. Both yield: 5 each.
- Both hold: a "revolver" fires with chance 1/6, then 1/5, 1/4, 1/3,
  1/2, 1 (as Bud White did in L.A. Confidential). If it fires, both get
  -D. If not, next round.
- Vary only D (cost of disaster): 0, 10, 100. With D = 0 holding is
  cheap; with D = 100 the expected value says yield early unless the
  other is about to yield.
- Code computes, for every round, whether Hold or Yield has the higher
  expected value. Measure: rounds held after Yield became better
  ("winning beyond reason") and the disaster rate.
- Second step: dollar auction and war of attrition (same measure: money
  spent above the prize). Third step: groups of 3-6 (many-player
  attrition), where Track 2 asks if it changes smoothly or jumps.
