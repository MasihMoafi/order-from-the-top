# Build brief: Five Families engine (for Codex Terra)

Work in `~/Desktop/p/swarm-hackathon`. Read first: `specs/002-factions/rules.md`
(the rules), `architecture.md` (hub, packets, lockstep, checkpoints), `mafia.md`
(the mafia flavour), and reuse `arena/arena.py` (`call_stream`, Elpis marks) and
`game/game.py` (`Budget`, `BASE`, `MODEL`).

## Hard limits
- No paid model calls. Do not read `~/.config/adaption/api_key` or any key file.
  Every test and demo uses a fake model (seeded random replies in the real format).
- Write only inside `families/` and `families/tests/`. Touch nothing else.
- Code applies every move, chance roll, score and death (invariant I1). No LLM judges.

## Build (a Python package `families/`, one module per job)
1. `tree.py`: god + 5 families x 15 agents (leader, then 7 levels of one spine
   member and one leaf). Ids P01..P76 as on the board (god P01; leaders P02, P17,
   P32, P47, P62). Edges: parent, child, sibling; leaders <-> leaders; god <-> leaders.
2. `hub.py`: every message is a packet {id, round, sender, receiver, edge, content,
   delivered, reason}. Deliver only if R2 allows; log every packet either way.
   Leader letters use the A2A message shape (role, parts, messageId, contextId).
3. `variants.py`: the 16 PD variants of R3 as plugins with one interface: pairing,
   number of rounds (variant 4 rolls continuation d), what each agent sees, how
   moves resolve to points. Payoffs 3/1/5/0.
4. `flavours.py`: plugin interface for R3b; implement the mafia flavour only.
5. `survival.py`: R4-R6, breadth-first from the god; subtree deaths; linked fates.
   Threshold = fraction x family stage average; fraction starts at 0.5 and rises by
   `step` each stage ("blinds"); both from the control file.
6. `engine.py`: lockstep rounds, 16 stages (one variant each, order shuffled by seed),
   checkpoint `state-stageNN.json` after every stage, resume from a checkpoint,
   read `control.json` before each stage (pause, stop, fraction, step).
7. `models.py`: real caller wrapping `call_stream` (not run by you) and `FakeModel`.
8. `prompts.py`: rules (common knowledge), own position, own score, stakes. No goal,
   no persona (I3).
9. `events.jsonl` per run: every call (prompt, reasoning, reply, parsed action,
   timing, cost), packet, move, score, death (I2).
10. `run.py`: `python3 -m families.run --fake --families mafia --stages 1` and
    `--fake --stages 16` for all five families.
Wars (R7), pressure (R9) and end states (R10): implement R9 and R10; leave R7 as a
documented stub with its interface.

## Done when (run these and paste the output in your report)
- `pytest families/tests -q` passes, including hand-made trees whose expected deaths
  under R4-R6 are written out in the test.
- The fake 16-stage, five-family run finishes, and its log has every field above.
- Resume from `state-stage05.json` reproduces the same final state as a straight run.

## Report
Files made, commands, test output, and every place the rules were ambiguous and
which reading you chose (do not silently decide; list them).
