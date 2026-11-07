Implemented the brief in `families/`. The requested test
command passed: **20 passed, 10 subtests passed**.

A mixed-policy run with seed 8, `ante0=4`, and `step=0.5`
reached stage 16. President, Bishop, and Zeus survived past
stage 4. Deaths occurred in stages 1, 2, 14, 15, and 16.
With the default `step=1`, the same seed ended at stage 15
when Zeus became the only surviving family.

The estimate printed **638 calls** for its seeded cooperative
scenario: stages 1–5 had 420, 83, 50, 50, and 35 calls;
stages 6–16 had zero because that scenario ended. Actual
choices, deaths, round lengths, and retries change the count.

Rule readings used:

- Agents pay from accumulated score; paying exactly is enough.
  The god does not pay, because it has no scoring moves; it
  dies when all leaders are dead.
- Subtree deaths precede linked fates. The existing linked-fate
  rule also applies to paired leaders. Pressure remains before
  the ante.
- Tit-for-tat copies the last observed move by the same opponent.
  Mixed assigns a seeded policy per agent. Fake mafia players
  map cooperation to silence and defection to ratting on a
  partner.
- Credit limits stop at a completed stage checkpoint, so a
  stage can exceed the cap. Checkpoints retain spending and
  fake-policy settings for resume.

The handbook is currently absent. Fake runs use the action
format alone; real calls stop until the handbook exists.
Real-model behavior was tested with a mock; no paid call was
made. The workspace pointer check also reported existing
problems outside this brief’s allowed scope.