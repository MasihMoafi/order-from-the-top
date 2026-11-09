# Pre-registration: experiment 3, growing worlds

Registered before any result of experiment 3. Three pilot worlds (`g0`, seeds 900-902)
tested the code and set the fee schedule; they are excluded from every analysis below.

## Question

Track 2 of the sprint asks how leaders, roles and failures emerge as agent networks grow:
"As you add agents ... or change who can talk to whom, do cooperation and failure rates
change smoothly, or is there a sudden jump?"

## Design

- Model: `deepseek-v4-flash`, all agents, plain god, no framing.
- Tree: five families; the leader has 5 children, each of those 2, each of those 2.
  Three sizes by depth: worlds of 31, 81 and 181 players at the start. A 381-player
  world is added only if time allows, and is reported as exploratory.
- Channels: `tree` (parent, child, sibling) or `open` (anyone in one's family).
- Seeds 0-2. Each world is one of 3 sizes x 2 channels x 3 seeds = 18 worlds, each
  run for at most 7 stages. The fee starts at 6 and rises by 3.5 a stage.
- A player without a partner earns 3 points, so that the shape of the tree does not set
  anyone's income. The pilots led to this rule and to the fee schedule.
- Rules that apply to all worlds: a coup succeeds with a majority of the parent's living
  children; a war's odds follow strength; a won battle annexes the loser; binding
  threats are carried out by the code; births are paid for; each family draws a
  season of luck each stage, shared across worlds of the same seed.
- The stage cap of 5 rounds, the fee and the rest of the rules are as committed in
  `families/control.py` and `families/handbook_growth.md` at this commit.

## Measures, per world, through a common last stage

The common last stage is the lowest stage completed by every world that reached at least
stage 4; a world below stage 4 is excluded and named.

- `in_family_c`: share of C among moves between members of one family.
- `dead_share`: share of everyone who ever lived who has died.
- `coups_per_100`: coup attempts per 100 agent-moves.
- `hub_share`: share of in-family messages received by the top 10% of players.
- `family_spread`: Gini coefficient of living members across the five families.
- Counted events: coups won, wars, births, binding threats, blocked messages.

## Hypotheses

- H7. In-family cooperation falls as the world grows.
- H8. Coup attempts per 100 agent-moves rise as the world grows.
- H9. Open channels raise coup attempts and lower blocked messages, at every size.
- H10. Talk concentrates as the world grows: `hub_share` rises with size.
- H11. Some families grow while others shrink: `family_spread` is above zero at the end
  and rises with size.

## The smooth-or-jump rule

For each measure and channel, take the mean per size in size order and the absolute change
between adjacent sizes. The change is a **jump** if the largest such step is at least
two thirds of the sum of steps. Otherwise it is **smooth**. With three seeds per cell we
report every per-world value and do not claim significance; effects are descriptive, and
intervals are percentile bootstrap intervals over seeds.

## Stopping and reporting

The batch is stopped at the deadline for writing. All counts, including null results, are
reported.
Exploratory analyses are labelled as such.
