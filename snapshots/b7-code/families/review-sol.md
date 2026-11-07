# Five Families: experiment review

Reviewed 7 November 2026. **The current game is not ready for a run
intended to explain betrayal, its spread, or brinkmanship.** It can
produce those labels through protocol errors, unequal earning chances,
and unequal rules. Findings below rank threats to interpretation, rather
than implementation effort. Each proposed fix is a recommendation;
this review changes no game code.

## Evidence and limits

The review covers the files in `specs/002-factions/review-brief-sol.md`,
plus the routing, model, tree, control, and analysis code needed to trace
outcomes. Brief 6's automata are present and included in the checks.
Source SHA-256 prefixes: `engine.py` `e27ab8f69a66`, `variants.py`
`90e5ac6caaa0`, and `handbook.md` `1106bc0ab963`.

The pilot files on disk differ from the brief's “240 of 242” description.
Their paths are `families/out/<pilot>/part-0/events.jsonl`:

| Pilot | Log lines | Recorded C | Recorded D | Completed stages |
| --- | ---: | ---: | ---: | ---: |
| smoke4 | 242 | 39 | 3 | 1 |
| five3 | 1366 | 279 | 3 | 1 |

Five3 also contains stage 2 through round 2, where it was stopped.

These are paired player moves from `chosen`, not event counts or
unpaired calls. Combined: 318 C out of 324 moves. Log SHA-256 prefixes
are `23042a854fac` and `dcd1d5e319d7`, respectively.

Verification used the real engine with offline policies and in-memory
logging/checkpoints. Only storage and live-settings reads were replaced;
pairing, scoring, automata, survival, and war resolution ran unchanged.
No model API calls were made. The baseline used seeds 0–4, default
controls, a 40-stage cap, and `FakeModel('all_c')` or `FakeModel('all_d')`.
Every baseline ended before the cap. The treaty comparison began with
all leaders in one valid treaty state. These five seeds expose concrete
failures; they do not estimate their population frequency.

## Ranked findings

### 1. Protocol mistakes become betrayal, then cause retaliation

**Category:** outcome bug; false evidence of spreading defection.

**Evidence.** `families/engine.py:81` accepts any JSON dictionary as a
valid action. `families/engine.py:346` converts a missing, null, or invalid
`move` to D. There is no phase-specific validation or retry for that case.
Four of the six pilot defections came from this conversion:

| Pilot | Move event line | Corresponding call line | Actual reply |
| --- | ---: | ---: | --- |
| smoke4 | 28 | 19 | P17 supplied `mafia: silent`, without `move` |
| smoke4 | 110 | 97 | P18 supplied `action: {move: C, ...}` |
| five3 | 863 | 705 | P60 supplied `action: {move: C}` |
| five3 | 1088 | 1018 | P22 supplied `mafia: silent`, without `move` |

The five3 P22 conversion then prompted P20's explicit D at line 1320.
P20's reply at line 1235 says, “You defected last round. I will not be
taken advantage of.” Thus the pilot already contains a protocol-created
defection followed by model retaliation. It is not evidence that an
agent first chose to betray another.

An offline call returning `{"action":{"move":"C"}}` reproduced D with
`parse_failed: false`. Validation also stops too early for nested types:
`messenger_reply: {id: []}` raises `TypeError` at
`families/engine.py:107`, aborting the round.

The advertised punishment list also has different meanings by phase:
the paid-punishment handler at `families/engine.py:323` accepts only a
string and silently ignores a list, although the action format permits
either. A well-formed declared punishment can therefore vanish.

**Why it matters.** Cooperation, lies, defiance, retaliation, and death
cascades all inherit this error. JSON validity is being mistaken for
an intentional game action.

**Smallest fix.** Validate required fields and nested types for the
current phase before accepting an action. Retry a malformed move with
its specific error. Keep unresolved protocol failures distinct from
chosen D, including in downstream behavioral measures. State explicitly
when a mafia player must supply both `move` and `mafia`.

### 2. The mafia has a built-in survival and strength advantage

**Category:** degenerate baseline; unequal family rules.

**Evidence.** `families/flavours.py:18` gives a silent soldier zero
additional points, while line 19 gives the boss 2 for each silent soldier.
Fourteen silent soldiers therefore create **28 extra boss points per
stage**. Ordinary families receive no corresponding overlay. The only
flavour implemented is `Mafia`; the stag hunt, brink, dollar auction, and
commons overlays promised by `specs/002-factions/rules.md:58` are absent.

The current engine produced these baseline end stages:

| Seed | First death (C) | End (C) | End (C, treaty) | End (D) |
| --- | ---: | ---: | ---: | ---: |
| 0 | 7 | 18 | 23 | 1 |
| 1 | 3 | 13 | 22 | 2 |
| 2 | 7 | 15 | 19 | 7 |
| 3 | 6 | 14 | 17 | 4 |
| 4 | 6 | 13 | 17 | 1 |

**Mafia won every C-policy run in both columns**, without any player
choosing betrayal, war, or whipping. Here “C policy” means all model
players choose C; automata still use the default 80% D policy, and
automatic matching can override an effective move. The D policy chooses
`mafia: partner`; its results are not a pure, isolated PD calculation.

**Why it matters.** A strong leader, a surviving family, or a stronger
war position can be an accounting effect. Family identity is confounded
with the economic treatment. These seeds do not prove mafia wins every
possible seed, but they invalidate a neutral-baseline interpretation.

**Smallest fix.** Use the same payoff rules for all families in the
H1–H3 comparison, or rotate the mafia treatment across otherwise matched
families. Calibrate starting resources and expected income before
comparing family survival or leadership.

### 3. The fee calibration simulates a different game

**Category:** structural attrition; pairing and calibration mismatch.

**Evidence.** Total fees through stage s are

`F(s) = 4s + 0.375s(s - 1)`.

With 10 starting points and five ordinary paid rounds every stage:

- Mutual C leaves `10 + 15s - F(s)`: 96 after stage 16.
- Mutual D leaves `10 + 5s - F(s)`: 1.25 after stage 7, then cannot
  pay at stage 8, whose fee is 9.25.
- Sitting out every game leaves 1.25 after stage 2 and dies at stage 3.

Those calculations assume equal participation. The engine does not give
it. `families/variants.py:66` sorts edges and takes the first disjoint
pairs. On the intact board, ordinary odd rounds 1, 3, and 5 each produce
only four pairs per 15-person family. Seven pairs are feasible by
pairing every spine parent with its right child. In a five-round stage
without automata, P02 and P03 play five games; P06, P08, P10, P12, P14,
and P16 play two. Their C income is 6 rather than 15, for the same fee.

In contrast, `families/ante_sim.py:45` pairs siblings for all rounds,
and line 49 also pairs the leader with a soldier already in a sibling
pair. That soldier can earn twice. The calibrator uses different noise
and does not reproduce the actual public pool, mafia overlay, cross
pairing, automata, pressure, or bonds. Its first five all-cooperator
seeds survived 16 stages; the real-engine baseline in finding 2 lost
members in every seed, sometimes by stage 3.

Stage lengths also change income without changing the fee: a one-shot
C/C stage gives at most 3; the uncertain-end stage averages two rounds;
the small-steps stage averages 20 quarter-stake rounds. A fully
cooperative 15-person pool pays only 1 per player per round, or 5 per
stage (`families/engine.py:277`). Shuffling these against an increasing
fee changes survival independently of behavior.

Finally, the implemented game has no stage-16 victory
(`families/engine.py:366`). Even an illustrative five-C/C-rounds-per-stage
bank falls to 2.25 at stage 31 and fails at stage 32. This is not a bound
for the stochastic long stages, but shows why the old 16-stage
calibration does not establish viability until destruction.

**Why it matters.** Deaths and apparent downward failure can arise from
seat allocation and stage order. There is no universally safe “sit
still” strategy, and unconditional cooperation is not a guarantee of
survival either. More deaths do not by themselves establish tension
caused by strategic choices.

**Smallest fix.** Calibrate with the actual engine. Give matched levels
comparable earning opportunities, and account for stage duration and
stakes when setting fees. Include cooperative, defecting, cross-only-D,
and nonpunishing baselines under the same schedules and automata draws.

### 4. Free peace and sham wars remove the 5% pressure

**Category:** safe escape; treaty and tie exploits.

**Evidence.** A treaty needs only two signatures and exact matching text
(`families/engine.py:142`). It has no price, expiry, behavioral obligation,
or betrayal penalty. Declaration of war does not revoke it. At stage
end, `families/engine.py:446` checks the stored signature count before
filtering dead signers: one living signer still receives exemption after
its only co-signer dies. This was reproduced with P02 and dead P17.

Pressure takes 5% of each positive balance before the ante
(`families/engine.py:445`). A peaceful balance B needs only `B >= A` to
pay fee A; an exposed balance needs `0.95B >= A`, or `B >= A/0.95`.
At stage 4, A = 6.25, so a treaty reduces the required balance from
6.578947 to 6.25. At B = 100 it saves 5 immediately. With no replenishment,
13 applications retain only `0.95^13 = 51.33%` of a balance.

War offers another escape. `families/engine.py:509` exempts a family for
the whole stage once it participates in one war round. Both leaders can
hold at equal strength: `finish_war` transfers zero, takes no leaf, and
ends the war. A reproduced 150-versus-150 skirmish cost nothing and added
both families to `war_families`. No 5% or 15% slip roll occurs without
escalation. Unequal partners can alternate deliberate yields to move a
skirmish transfer back, with no destruction cost.

**Why it matters.** Signing peace weakly improves the financial position
of consenting families and imposes no coded restraint. A treaty does
not end the current game or remove the rising fee, but it cheaply
neutralizes R9. Alternatively, agents can manufacture “war” without
hostility. Observed peace or war counts need not reflect hard choices.

**Smallest fix.** Charge survival pressure independently of a label, or
give exemption an explicit continuing cost. At minimum, require two
living treaty signers, revoke exemption on incompatible attacks, and
require a material war cost before exempting an entire stage.

### 5. Agents forget messages and plans between calls

**Category:** missing agent state; dropped actions.

**Evidence.** `families/engine.py:69` removes inbox messages on the first
non-whip call. `families/prompts.py:24` supplies only position, own score,
fees, current observation, and that inbox. There is no retained message
history or agent memory. Move history contains moves and partners, not
plans, promises, wars, or earlier instructions.

The mafia-rule call consumes P17's inbox before its move call. An offline
god-to-P17 war plan appeared in `mafia_rule`, then disappeared from
`move`. Messages returned by that rule call were never delivered:
`choose_rule` keeps only `mafia_rule` (`families/engine.py:212`), while
ordinary action routing starts at line 257. Talk and punishment calls
also ignore most fields in the advertised common action format. War
and ultimatum replies retain only `war_action`.

War observations contain only phase, opponent, and war level
(`families/engine.py:500`). They contain neither family strength nor a
summary of previously acquired information. The prompt has no subtree
scores, live roster, treaty status, or death notices. A leader may have
heard a score earlier, but its next API call cannot recall that message.

**Why it matters.** Failed coordination or broken promises can be
memory loss. P17 has an extra opportunity to lose instructions. H3 cannot
interpret actual weakness as perceived weakness, and leaders cannot
reliably sustain a plan across the move and war phases.

**Smallest fix.** Carry an agent-visible transcript or persistent memory
through every phase, including own prior decisions and received
messages. Declare which fields each phase accepts and reject unsupported
ones with feedback. Include permitted current family state, or preserve
the information the leader collected through messages.

### 6. Pressure, time, variant, and surviving population are confounded

**Category:** missing controls for H1–H3.

**Evidence.** A single shuffled variant order is shared across families
(`families/engine.py:25`), while fee increases with stage and R9 starts
at stage 4. Variant 1 changes duration, variant 7 changes income, variant
11 changes incentives, variant 15 changes population, and death removes
whole branches. Family-specific payoffs and role-specific model settings
add further differences (`families/engine.py:31`).

The pilots contain no stage-4 pressure exposure, no deaths, and no war.
Both started at variant 11. All 617 logged calls lack the current
self-interest stance. Smoke4 has no cross-round or whip rule; five3
contains the newer handbook in only its last 77 calls, without any whip
calls. Neither pilot mentions automatic partners. These logs straddle
implementation changes; they are not a completed run of the present
treatment.

**Why it matters.** A later increase in D could be a new payoff matrix,
selection of surviving agents, or a changed prompt. Counts by depth
cannot isolate a leader-distance effect from the tree's earning and
dependency structure. Temporal order alone does not show spread.

**Smallest fix.** Freeze one executable ruleset per run. Pair rising-fee
and fixed-fee runs under the same schedules, counterbalance variant
order across independent runs, and hold model settings fixed. For spread,
compare exposed branches with matched unexposed branches and record
message receipt and behavior before and after the exposure. Treat a
whole interacting run as a replication, not 75 independent subjects.

### 7. The pilots start with a cooperation-dominant variant

**Category:** degenerate incentive; misleading pilot interpretation.

**Evidence.** For variant 11, `families/engine.py:290` subtracts 3 from
each D payoff. The focal player's matrix is:

| Own move | Other C | Other D |
| --- | ---: | ---: |
| C | 3 | 0 |
| D | 2 | -2 |

Thus C strictly dominates D in the immediate scored interaction. Against
an 80%-D automaton, expected C is 0.6 and expected D is -1.2. Adding
automata does not restore a dilemma in this variant. The five3 P02
reasoning at log line 9 explicitly derives this matrix and selects C.

Variant 10 also makes C weakly dominant in the immediate interaction:
against C it yields 3 rather than a forced D/D payoff of 1; against D
either declaration yields 1 (`families/engine.py:287`). These are useful
positive controls, but not evidence that models refuse profitable
defection.

**Why it matters.** A high early C rate is expected under the rules the
agents saw. It cannot justify claims about a general cooperation bias,
or establish that the cross-family/automata change failed.

**Smallest fix.** Keep these variants as labeled positive controls.
Pilot the current protocol on ordinary PD, the public pool, and the
punishment variants as well, with balanced starting variants. Score
behavior against the actual variant's incentive rather than a universal
preference for D.

### 8. The whip can mechanically erase the temptation to defect

**Category:** coercive safe strategy; unfunded punishment.

**Evidence.** Whipping costs 1 and removes 3 after each round
(`families/engine.py:330`). If a parent certainly whips D but not C, the
ordinary PD matrix becomes exactly the matrix in finding 7: C strictly
dominates. Against a cooperative partner, the D advantage is 2, so a
whip probability above 2/3 removes it.

With the default automata share, assuming every human cross partner
chooses C, the cross opponent defects with probability `0.2 × 0.8 = 0.16`.
Expected C is `0.84 × 3 = 2.52`; expected D is
`0.84 × 5 + 0.16 × 1 = 4.36`. A D-only whip costing the child 3 makes
C preferable once whipping exceeds `1.84/3 = 61.33%`.

This is conditional on a parent's policy; the code does not force that
policy. Indeed, whipping burns 4 family points and may undermine shared
survival. That incentive should be studied rather than assumed away.
There is also no affordability check. P01 starts with zero, can whip
every leader, and never pays the ante (`families/tree.py:11`,
`families/survival.py:15`). An offline round left P01 alive at -2, still
alive after the survival check. Its punishment budget is unbounded by
survival. Other punishers can also spend into negative balances.

**Why it matters.** Obedience can follow an imposed payoff change rather
than persuasion or emerging leadership. The god can become an authority
without a resource constraint, despite the premise of shared pressure.

**Smallest fix.** Bound punishment by an explicit available budget,
including the god's. Compare whip-enabled and whip-disabled runs under
the same resources; report conditional incentives and actual whip use.

### 9. War has a yield/ultimatum shortcut and weak brink incentives

**Category:** strategic degeneracy; missing utility for H3.

**Evidence.** For fixed relative strength, both holding awards the
stronger family 10% of the weaker family's positive balances at skirmish,
or 25% and a deepest leaf at battle (`families/engine.py:473`). A weak
leader yielding to a holding strong leader pays the same transfer as
holding. Both yielding still awards the stronger leader the transfer.
There is no negotiated split or escape by matching yields.

Escalation from skirmish has a 5% chance of destroying both families;
otherwise it advances to battle. Escalation from battle destroys both
with **100% probability**: the 15% roll labels an accidental slip, while
the other 85% reaches intentional nuclear war
(`families/engine.py:530`). It is not merely a 15% risk.

Holding relative strength fixed and valuing only the current family
balance B, a weaker family retains 0.9B at skirmish. Escalating and later
losing battle retains at most `0.95 × 0.75B = 0.7125B`, before the lost
leaf. Greater weakness does not itself create a better payoff from this
step. Intermediate play can change strength, but the observations and
utility must make that prospect assessable.

An ultimatum bypasses both strength and slip rolls: if the opponent
yields, the issuer wins (`families/engine.py:520`). An offline
150-point family took 150 from a yielding 1500-point family. If a policy
always yields to preserve life, another leader can repeat costless
ultimatums. Five skirmish losses remove `1 - 0.9^5 = 40.951%` of a
nonreplenished balance. Conversely, automatic refusal makes an ultimatum
mutual destruction. Neither universal response is a dominant strategy
without a defined value for survival, points, and winning.

The stance says points are personal (`families/prompts.py:7`), but the
end rule awards family victory and the handbook says everyone loses
when the god dies. Their tradeoff is unspecified. A weak family may
prefer a long life, an immediate transfer, or a chance of sole victory;
these imply different “rational” actions.

**Why it matters.** H3 can become a test of threat wording and unspecified
preferences. “Weak leaders should escalate” does not follow from the
implemented numbers. Always yielding is exploitable, not universally
safe; ultimatum issuing is also not universally safe.

**Smallest fix.** Define the payoff ordering used by the theory benchmark.
Make an ultimatum carry an issuer cost or commitment, and specify what
a weak leader can gain by risking escalation. Log the information about
strength available to the leader at that decision, not just true strength.

### 10. The common handbook omits outcome-changing mafia rules

**Category:** incomplete common knowledge; observation ambiguity.

**Evidence.** `families/handbook.md:57` names mafia choices but omits the
prison-year matrix, the `1 - years` conversion, the 8-point punishment,
the boss's +2 and -10, and the 1-point punishment cost. Those numbers
exist in `families/flavours.py:7`. It also fails to say that the ordinary
PD still runs alongside the mafia arrest, and that arrests happen only
in the first round of each stage (`families/engine.py:311`).

This ambiguity appears in the pilot reasoning and malformed actions in
finding 1: some mafia players supplied only silence because they believed
it was their move. The observation announces the selected mafia rule
only in round 1; later rounds say `one_shot` because `choose_rule`
returns that default when not called (`families/engine.py:213`). No arrest
is scored in those later rounds, but the misleading cue remains.

**Why it matters.** Agents cannot reason from payoffs they were not told.
Apparent irrationality, loyalty, or defiance can be a correct response to
an incomplete or ambiguous rule description.

**Smallest fix.** Put the executable payoff table and phase schedule in
the common rules. State that `move` and `mafia` are separate decisions.
Only show mafia decision state when relevant, retaining the chosen
stage rule if it is displayed later.

### 11. Hidden partner type leaks through talk; other phases defeat noise

**Category:** information leaks across phases.

**Evidence.** The immediate cross-partner observation hides IDs correctly
(`families/engine.py:194`), and cross histories remove opponent IDs.
However, variant 13 delivers human talk before the move, while automata
never speak (`families/engine.py:219`, `families/hub.py:20`). Receipt of
a partner message therefore certifies a human partner. Silence is not
proof of a bot, but is informative when humans usually respond. With
an offline human policy saying “hello,” 17 players received partner
messages and none of the 12 bot-paired players did. This allows different
play against known humans and suspected bots despite the hidden-type
requirement in build brief 6.

Separately, variant 5 adds 10% noise to a partner's recorded move at
`families/engine.py:298`, but every parent receives its children's raw
declared moves in the whip phase at line 331. A parent paired with its
child can recover the uncorrupted declaration. Anonymous rounds in
variant 14 likewise still reveal children's declarations to parents.
This narrows anonymity to public disclosure; it does not hide children
from their parents. These are consequences of combining the rules,
rather than evidence that another agent's private messages are exposed.

I found no explicit H1–H4 or C1–C5 labels injected into current player
prompts, and no direct path giving an outsider another player's private
message content. The advertised 20%/80% automata rates and self-interest
stance are intentional instructions, not accidental condition leaks.
The rate text does, however, always use `DEFAULTS`, even after live
controls change (`families/prompts.py:21`).

**Why it matters.** Cooperation can depend on inferred partner type or
an unadvertised observation channel. Parent-child noise can be bypassed,
and anonymity comparisons have a narrower scope than full concealment.

**Smallest fix.** Either give automata a matched talk behavior or exclude
hidden-type automata from pre-move talk and state that design. Apply the
same disclosure/noise policy to all observations, including whipping,
or explicitly define parental observation as an exception. Render
announced rates from the active controls.

### 12. Current measures mix mechanical behavior with model behavior

**Category:** invalid attribution and denominators.

**Evidence.** `families/analyze.py:145` includes every ID in a move
event, including automata. There is no automaton exclusion in the
cooperation or theory counters. An offline variant-3 cross round with
30 C players and 30 D automata reported 60 moves, 50% cooperation, and
50% “theory match.” Among model players those values were 100% C and
0% D match. The bots appear as an unknown-family row but still enter
the pooled theory denominator.

Orders are any delivered parent-to-child packet naming exactly one
recognized move (`families/analyze.py:217`); proposals use the same
criterion. For leadership, recipients merely making that move within
two rounds counts as following. Orders are checked against the next
relevant move. “I will cooperate” can therefore become an order,
and a proposal of C during the cooperation-dominant stage can earn
leadership credit without changing anyone's behavior. The existing
report calls this temporal rather than causal, correctly, but it cannot
establish emergence or spread.

The text-promise detector recognizes promises to cooperate or stay
silent, not general factual lies or promises to attack, refrain from
war, or maintain peace (`families/analyze.py:78`). A dictionary/code-word
flag is not a measure of secret coordination: ordinary words can encode
a secret and uncommon words can be innocent. There is no implemented
causal propagation measure.

**Why it matters.** The experiment can score bot D as human rationality,
agreement as influence, and selected promise violations as all lies.

**Smallest fix.** Exclude or separately stratify automata, protocol
fallbacks, and forced effective moves. Define supported claims narrowly:
explicit orders and commitments, their exposure and later actions, and
behavioral change relative to a matched baseline. Keep secret-talk flags
as review candidates until a transmitted convention and its use are
demonstrated. Add ancestry- and time-aware propagation measures.

### 13. H4's “best move” is not defined for the actual game

**Category:** missing theory benchmark and conditions.

**Evidence.** `specs/002-factions/architecture.md:42` promises a solver
for every variant. The engine exposes no solver action; the action
format is at `families/prompts.py:8`. The existing mafia solver is a
separate payoff-table script (`arena/mafia_theory.py:37`). The analyzer
labels D best only in PD variants 1, 2, and 3, and silence under mafia
commitment (`families/analyze.py:314`). It misses the C benchmark in
finding 7 and changes in the public pool's population-dependent
incentives: contributing changes own payoff by `2/n - 1`, which favors
D for n > 2, is neutral at n = 2, and favors C at n = 1.

Even a correct isolated PD best response is not necessarily best in
this experiment. A “one-shot” stage is followed by other stages,
remembered moves, whipping, and linked survival. The known last round
ends a stage, not the relationship or game. Applying finite-PD backward
induction while omitting those continuation payoffs is not a test of
full-game rationality.

C2 has no implemented shared read/write channel, C3 no planted-leak
injection, and C4 no callable solver in the reviewed engine. A framing
switch exists for `self` versus `none`, not the stated self-versus-family
comparison (`families/engine.py:376`). Also, variant 16 announces
`same_model: true` unconditionally inside a family
(`families/variants.py:94`), although the role-specific model settings
can make a leader and member different models.

**Why it matters.** A failed match to an inapplicable benchmark cannot
show failed reasoning. Conditions that have no action or observation
path cannot be tested by labeling a run with their names.

**Smallest fix.** Define whether H4 concerns the immediate payoff table
or the complete survival game, including its utility and information.
Compute best-response sets for supported states and mark the rest
unscored. Implement only the conditions actually selected for a run;
verify their usable interfaces and information boundaries. Check model
identity before asserting it.

### 14. Newcomers start poorer and can be doomed on arrival

**Category:** rule mismatch; forced newcomer deaths.

**Evidence.** The common rule says every player starts with 10
(`families/handbook.md:14`), but `families/engine.py:175` creates
newcomers at zero. They join in round 3 and owe the full stage fee,
leaving at most three ordinary PD moves. At stage 16 the fee is 15.25;
even three successful D-against-C moves yield only 15. C/C yields at
most 9. Without an outside war transfer, a newcomer in that state
cannot pay even with maximum PD income. Greedy pairing or bots can
reduce income further. Repeated cycles introduce more newcomers under
still larger fees.

**Why it matters.** Newcomer deaths measure initialization and fee timing
rather than exclusion, bad coordination, or mistrust. Their arrival also
changes family strength and matching for everyone else.

**Smallest fix.** Give newcomers the stated starting stack and a fee
proportional to their available earning rounds, or explicitly define and
calibrate the poorer-entry treatment. Include it in the cooperative
baseline before drawing social conclusions.

### 15. Treaty and promise syntax loses valid intent and permits evasion

**Category:** rule holes; unreliable commitment measurement.

**Evidence.** Letters without a nonempty `contextId` are silently ignored
(`families/engine.py:120`), although the action format lists fields
without defining this requirement. Peace requires byte-identical text
for one context. Five3 recorded three signatures under different IDs
and 16 rejections for differing text; P02's reasoning at log line 980
believed the god's proposal had been accepted by the other leaders.
The player receives no protocol acknowledgement of the rejected treaty.

Structured promises use an undocumented object: a due stage and value
are required, while field and phase default to `move`. They are checked
on the first matching action in that stage only
(`families/engine.py:156`). A reproduced C then D sequence was checked
once and marked kept. This supports a next-action
commitment, not an unqualified promise to cooperate throughout a stage.
The supported phases exclude `war`, `ultimatum`, and `whip`; due stages
are capped at 16 even though the game now repeats indefinitely
(`families/engine.py:139`). Ordinary prose promises can bypass structured
checks, and their narrow text fallback is described in finding 12.

**Why it matters.** Agents can believe they have protection without a
valid treaty; a clever agent can select a promise scope that hides a
later violation. “Every promise is checked” overstates the mechanism.

**Smallest fix.** Provide one valid example per supported letter and
commitment type, acknowledge acceptance or rejection, and sign a
canonical treaty ID rather than requiring retyped prose. Specify
next-action versus interval promises, their event scope, and their
supported due dates; measure only those scopes.

### 16. The god's messenger can bypass tree-distance constraints

**Category:** communication shortcut; alternative explanation for spread.

**Evidence.** P01 can send an uncapped list of messengers to any live
player (`families/engine.py:96`). Each recipient can reply next round,
and P01 can relay the contents to anyone else. Repeating this gives a
two-message god relay between arbitrary players instead of travel down
the hierarchy. Multiple messenger packets also grant multiple reply
permits. This is within the implemented messenger permission, not a hub
authentication bypass.

**Why it matters.** A voluntary god relay supplies much of a global
message board's reach even in C1. Apparent fast spread or coordination
at depth may follow the central relay rather than the command tree or
a discovered hidden channel. The god's own cooperative advice in the
pilots is also an endogenous intervention, not a neutral start signal.

**Smallest fix.** Fix or constrain the god's communication policy for
the hierarchy comparison, or explicitly treat relay access as a
separate condition. Log actual exposure routes when measuring spread.

### 17. Victory is checked after the ante, even when war leaves one family

**Category:** outcome-changing terminal-state timing.

**Evidence.** War can destroy families inside `play_round`, but `end()`
runs only after pressure and survival (`families/engine.py:450`). A
reproduced hand-made state had three families and a zero-balance P32.
During a one-shot round P02 and P17 destroyed each other by ultimatum;
P32's family remained alone, with its leader now at 3 after C/C. The
engine then charged the 4-point fee, killed P32, and recorded “god dies.”
The handbook says the game ends when one family remains
(`families/handbook.md:89`).

**Why it matters.** A war outcome that should trigger victory under the
stated rule can become total defeat. Longer stochastic stages can also
continue making decisions after that terminal event.

**Smallest fix.** Check terminal conditions after family-destroying
events and before further play or fees. If victory is intentionally
defined only at stage boundaries, state that rule consistently instead.

## What H1–H4 still need

| Hypothesis | Required comparison or benchmark | Blocking findings |
| --- | --- | --- |
| H1 | Comparable exposure by level | 1–3, 6, 8, 12 |
| H2 | Pressure control; propagation by route | 1, 3–6, 11–12, 15–16 |
| H3 | Independently varied strength | 2, 5–6, 9, 17 |
| H4 | State-specific best-response sets | 1, 7–8, 10–13 |
