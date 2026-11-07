# Five Families: fix report

7 November 2026. The mechanical repairs pass verification. Findings
9, 11, 13, and 6 still have research-design questions, listed below.
No network, paid model calls, or key-file reads were used.

Player rules live in [handbook.md](handbook.md); numeric defaults live
in [control.py](control.py). The original review remains unchanged.

## Findings, in the requested order

Every finding has a regression named `test_finding<N>_...` in
[the regression file](tests/test_review_fixes.py). Additional tests there
cover simultaneous spending, required mafia actions, phase messages,
and treaty cancellation during war decisions. Regressions were run
against the broken behavior before the corresponding repairs.

| Finding | Status | Smallest repair implemented |
| --- | --- | --- |
| 1 | Fixed | Validate moves and nested replies; abort rather than invent D |
| 2 | Fixed | Remove the mafia boss's free silence income |
| 3 | Fixed | Maximum tree pairing; calibrate actual engine; new fee step |
| 4 | Fixed | Apply pressure regardless of treaty or war labels |
| 5 | Fixed | Persist private communications and non-PD decisions |
| 8 | Fixed | Reserve affordable punishment and whip spending |
| 7 | Fixed | Retain positive controls; score their actual incentives |
| 10 | Fixed | Generate complete mafia rules from executable payoffs |
| 11 | Not fully fixed | Close talk-type and raw-whip disclosure paths |
| 14 | Fixed | Starting stack and proportional first fee for newcomers |
| 17 | Fixed | Resolve war victory before another fee or round |
| 9 | Not fully fixed | Charge ultimatum commitment; show own family strength |
| 15 | Fixed | Canonical treaty IDs; next-action and whole-stage promises |
| 16 | Fixed | Fund god messengers; one per recipient per round |
| 13 | Not fully fixed | Truthful copy identity; scoped immediate benchmarks |
| 6 | Not fully fixed | Record configurations and reject changed rule versions |
| 12 | Fixed | Add model-only metrics and explicit-order evidence |

Specific behavior:

- **1:** One unambiguous `action` wrapper is accepted. Missing C/D or
  required arrest choices trigger a retry, then a visible exception.
  They never become an agent's defection. Paid-punishment lists work,
  with duplicate targets removed and spending limited to available funds.
- **2:** Cooperative mafia play adds no boss bonus. Ratting and funded
  mafia punishment retain their stated losses. Other family-specific
  overlays were not invented; see the remaining decisions.
- **3:** An intact family supplies seven odd-round pairs instead of four.
  Equal-size matchings prefer less-served players. The calibrator calls
  the real engine, including variants, automata, pressure, and cascades.
- **4:** From stage 4, the 5% charge applies to every living family's
  positive balances. Peace still cancels wars between signers and never
  ends the game. Sham wars and dead co-signers cannot avoid pressure.
- **5:** Move history has one home. Private messages and decisions absent
  from that history persist through phases and checkpoints. Agents see
  their own subtree's scores and survival state. Communication returned
  in rule, punishment, whip, and war phases is processed at barriers.
- **8:** The god starts with the same finite stack as other players and
  still pays no ante. Its balance funds its actions. Simultaneous
  punishers reserve their own budgets, so an earlier incoming hit cannot
  suppress another already-funded punishment. Damage may make a balance
  negative; an actor cannot voluntarily spend more than its budget.
- **7:** All 16 variants remain. Immediate best-response sets correctly
  recognize binding-promise C and automatic-matching ties. The benchmark
  is logged for analysis and is absent from player observations.
- **10:** Players receive the prison table, score conversion, punishment
  costs, boss losses, and arrest timing. They are told to supply separate
  PD and arrest choices. Fees and automata rates use active controls.
- **11:** Cross-family talk arrives after choices, regardless of partner
  type; within-family variant-13 talk still precedes choices. Whip calls
  expose no extra raw moves. The remaining inference issue is below.
- **14:** Newcomers receive the normal starting stack. In their entry
  stage they pay for the fraction of rounds they are present; subsequent
  fees are full. Their initial resources are included in join events.
- **17:** Once war leaves one family, it wins before further fees.
  If every family is destroyed, the god dies immediately. A safety-cap
  stop with several families alive remains unfinished, not a victory.
- **9:** Issuing an ultimatum spends 3 personal points. An unfunded request
  becomes hold and produces feedback. War prompts include own family
  strength and retained messages, without disclosing rivals' private
  scores. Promise checks use the funded, normalized war action.
- **15:** The first treaty letter fixes its text; later signatures name
  its ID and receive the canonical text in acknowledgement. Missing IDs
  are generated. Attacking a co-signer revokes the attacker's signature.
  Promises specify next-action or whole-stage scope, include war/whip
  phases, and support stages beyond 16. Whole-stage C then D is broken.
- **16:** Each delivered messenger spends 1 god point. Multiple requests
  to the same recipient in a round grant only one reply permit.
- **13:** Copy observations check the configured models. The offline
  theory helper supports all immediate PD tables and changing pool size.
  It does not claim to solve the complete survival game.
- **6:** Stage records include seed, order, active controls, role models,
  and a source digest. Live configuration changes start a recorded
  treatment. Changed game sources reject continuation/resume when the
  checkpoint has a source digest. Older unversioned checkpoints cannot
  establish version continuity and should not supply confirmatory data.
- **12:** Existing analysis fields remain intact. Added JSON fields are
  `model_cooperation`, `model_theory`, `explicit_orders`, and
  `measurement_scope`. Added report sections display the clean metrics.
  Bots and identifiable legacy protocol defaults are excluded; intended
  and forced moves stay distinguishable. A read-only check of the old
  pilots excludes two malformed PD moves from each.
  Self-predictions in ordinary prose do not become explicit orders.
  Influence remains labeled temporal association, not causation.
  Free-form factual lies, secret coordination, and causal propagation
  need definitions and controlled evidence under decision 6.

## Ante calibration

Selected defaults: **10 starting points; ante 4 + 0.9 × (stage − 1)**.
The stage-16 fee is 17.5; total full fees through stage 16 are 172.
The start fee is retained; the increment rises from 0.75 to 0.9.

The real-engine calibration used default automata, no scripted peace or
war, and seeds 0–4. “C” and “D” describe the model policies; automatic
partners still use their announced distribution. The all-D policy rats
on mafia partners. Results are from the final code:

| Seed | C: original survivors / families | D: end stage / families |
| --- | --- | --- |
| 0 | 0 / 0 | 1 / 0 |
| 1 | 0 / 0 | 2 / 1 |
| 2 | 61 / 5 | 7 / 0 |
| 3 | 65 / 5 | 6 / 0 |
| 4 | 40 / 4 | 1 / 0 |

C entries are at stage 16. Original survivors exclude the god and
newcomers. All-D stops at its terminal state. Neither constant policy
protects every family or member across these seeds; a single surviving
all-D family in one seed is not universal safety. This is a calibration
check, not a proof that every possible strategy lacks a safe equilibrium.

Reproduce:

```bash
.venv/bin/python -m families.ante_sim 4 .9 --seeds 5
```

[Final calibration](out/sol-calibration-final.json) is the evidence.
[The initial real-pairing comparison](out/sol-calibration-initial.json)
and [the selected-fee comparison before later repairs](out/sol-calibration-selected.json)
record why calibration was repeated on the final rules.

## Verification

- `.venv/bin/python -m pytest families/tests -q`: **68 passed,
  10 subtests passed**. [Full output](out/sol-tests-final.txt).
- Focused Python undefined-name/import checks passed with Ruff.
- The actual CLI completed every variant once, in 16 stages, from
  76 initial agents. Five families and the god remained alive at the
  safety cap. All 8,472 model moves chose C; automata supplied 723 moves;
  automatic matching forced 21 effective moves. No protocol errors or
  paid costs were recorded. These are offline-policy results.

```bash
.venv/bin/python -m families.run --fake --fake-policy all_c \
  --families all --seed 2 --stages 16 --out families/out/sol-fixed16
```

The output directory already exists; choose a fresh directory to rerun.
[CLI output](out/sol-cli-final.txt),
[verified run summary](out/sol-fixed16/verification.json), and
[stage-16 checkpoint](out/sol-fixed16/state-stage16.json) retain the proof.

## Decisions still needed

- **9 and 13 — utility and theory scope.** Decide how personal points,
  survival, and sole family victory compare before defining a full-game
  best move. Immediate conditional best responses are implemented.
  The 10%/25% transfers and 5%/15% escalation rules remain; stronger
  incentives for weak-family brinkmanship were not invented.
- **11 — noise definition.** Revealed point changes can still identify
  actual PD outcomes even when reported moves are noisy. Own-subtree
  ledgers also permit inference. Complete concealment requires a choice
  between execution noise, delayed score disclosure, or a narrower
  reporting-noise claim. Current rules retain reporting noise.
- **6 — causal design.** Choose replicated fixed/rising-fee comparisons,
  variant-order counterbalancing, and treatment assignment. Pairing is
  fuller, but odd population sizes still produce unequal opportunities.
  Logging supports inspection; it does not remove those causal confounds.
- **13 — optional conditions.** C2's discoverable shared channel, C3's
  planted letter, C4's agent-callable solver, and family-interest framing
  remain unimplemented. Select their precise behavior before adding
  them. Default self-interest framing remains unchanged.
- **2 — additional flavours.** Stag-hunt, brink, auction, and commons
  family overlays still need explicit payoff rules if they are wanted
  in addition to the common 16-variant ladder. They were not added by
  guessing their economics.

