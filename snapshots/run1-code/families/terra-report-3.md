# Build brief 3 report

The offline command `.venv/bin/python -m pytest families/tests -q` passed:
29 tests and 10 subtests. The tests include mid-stage resume equality,
fixed war rolls, messenger replies, live settings, concurrency, pause, stop,
and SIGTERM. The real adapter was exercised with a mock; no paid calls were made.

The fake run is in `families/out/brief3-final/`. It used all five families,
seed 8, the `war` fake policy, and `ante0=0`, `step=0` to keep the game
running through all 16 stages. It produced 91 round checkpoints, 8,458 calls,
and 16 declared and resolved skirmishes. All five families reached stage 16
with 17 living players each. `events.jsonl` contains the full trace.

The agent-facing handbook is `families/handbook.md`; the original in `specs/`
was left untouched to respect the brief's `families/` work limit.

## Rule readings

- A round checkpoint records the continuation roll and whether the stage still
  needs its end-of-stage work. A signal completes the current round before the
  checkpoint. Resume into a fresh output directory; the old log is retained.
- The current `ante0` and `step` are applied before each round, including to
  the stage's final payment. A stopped checkpoint retains the stop setting;
  set `stop` to false in the resumed run's control file to continue.
- `models.json` supplies per-role settings; `control.json` may override them
  under `models`. Omitted fields retain their current values. The default
  effort is `medium`. Settings are captured in each call log.
- A declaration names a leader in the action's `war` field or in a delivered
  letter's `war` field. A pair can have one active war. Each war is resolved
  after the round's game and punishment, using the current live points.
- Both leaders hold: the stronger family wins; equal strength means no net
  transfer or death. One yields: the other wins even if weaker. If both yield,
  strength decides. A battle kills the deepest live non-leader leaf, breaking
  depth ties by ID. The losing members each pay the same percentage of their
  nonnegative points; the proceeds are divided equally among living winners.
- An escalation by either leader advances one level, with one slip roll per
  war round. A slip at skirmish or battle destroys both families; advancing
  from battle also reaches nuclear. An ultimatum gives the other leader a
  separate chance to yield unless that leader already yielded. Two simultaneous
  ultimatums destroy both families. A cancelled war whose leader has died ends.
- A family is exempt from that stage's pressure if it participated in a war
  round during the stage, even if the war ended before the stage's payment.
- Messenger replies name the packet ID and are accepted once from the recipient
  in the next global round. An unanswered reply expires after that round.
  God-to-player delivery and the reply both use the `messenger` edge.
- The fake `war` policy cooperates and P02 declares war on P17 in each stage's
  first round. The default fake policies remain available.

## Call dependencies

Independent calls run concurrently. These calls wait for earlier calls:

- In the talk variant, paired players' moves wait for all simultaneous talk
  replies and their delivery, so each player sees the pre-move messages.
- Mafia moves wait for the boss's first-round rule; other families and the god
  do not. In the move-shown-first variant, each second mover waits for that
  pair's first move.
- Punishment calls wait for the moves and arrests they must see. War calls wait
  for declarations and game and punishment effects, so their observations and
  strength use the updated scores. An ultimatum response waits for the initial
  war choices. Independent punishment and war calls are gathered by phase.
- A JSON retry waits for its failed first answer; the no-thinking fallback waits
  for the capped model call. The next round waits for this round's decisions,
  effects, continuation roll, and checkpoint.
