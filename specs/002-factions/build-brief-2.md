# Build brief 2: ante rule, real model, agent handbook (for Codex Terra)

Work in `~/Desktop/p/swarm-hackathon/families/` (and its tests) only. Same hard limits as
`build-brief.md`: no paid model calls, never read key files. Run tests with
`.venv/bin/python -m pytest families/tests -q` (pytest is installed there).

1. Death rule = rising ante (replaces the "fraction of family average" rule).
   After each stage, every live agent pays `ante = ante0 + step * (stage - 1)` from
   its score. An agent that cannot pay dies with its subtree; then linked fates as now;
   then the god check. `control.json` keys: `ante0` (default 4), `step` (default 1),
   read before each stage and logged when they change. Remove `fraction`.
   Test: a hand-made tree where the expected deaths are written out.
2. Prompts: the system prompt is `specs/002-factions/handbook.md` (I am writing it;
   it may not exist yet: load it at call time) plus the JSON action format. Never send
   `rules.md`, `mafia.md`, `architecture.md` or any spec to agents: they name the hidden
   conditions and the measures. The user message gives position, own score, the current
   ante and next stage's ante, the observation and the inbox.
3. Real model: `python3 -m families.run --real ...` uses `RealModel` (DeepSeek via
   `arena.arena.call_stream`, `game.game.Budget`); fix the broken `from game import`.
   Add `--max-credits` (stop cleanly at a checkpoint when spent >= cap) and
   `--concurrency` (default 40). Unparseable replies: one retry asking for JSON only,
   then the move defaults to the variant's default and is logged as `parse_failed`.
4. FakeModel policies for simulation: `--fake-policy all_c|all_d|random|tft|mixed`
   (mixed = per-agent seeded choice among the others).
5. `python3 -m families.estimate --stages 16 --families all` prints the number of
   model calls per stage and in total, from the engine's own call plan (no calls made).

Done when: tests pass; a fake mixed-policy 16-stage run shows deaths in some stages
but not all families dead by stage 4; the estimate prints. Report the outputs and
every rule reading you chose.
