# Build brief 7: framing experiment (run 2 onward)

Goal: turn the game into an experiment. Question (Track 2): how many framed agents
does it take to turn a family (one, few, many), and does a "sacrifice for the many"
framing spread down the tree, survive, or get exploited? Masih, 7 Nov.

Run-1 code is frozen in `snapshots/run1-code/` (same hashes as the server); its exact
replay uses that copy.

| # | Item | Acceptance check | Status |
| --- | --- | --- | --- |
| 1 | The game ends only when every family is dead (the god dies with the last). | Fake run with one family left keeps playing; fake games end in "god dies". | done (tests, fake runs) |
| 2 | Framing per family (`--stance design`), one condition each: `many` (all 15 told to sacrifice for the many), `few` (leader and its two children), `one` (leader only), `bad_leader` (a self-interested leader over 14 told to sacrifice: Track 2's "one compromised agent"), `none` (control). | Each call logs its frame; the prompt starts with that text. | done (tests) |
| 2b | Insider god (`--god insider`, Masih: messengers that change outcomes, like cheating): the god also sees last round's moves and private messages (up to 80, 200 characters each), is told no player knows, and may leak them. Same seeds with `plain` and `insider` give pairs that differ only in the god. | Test: the god's observation holds last round's moves and a private message. | done (tests) |
| 3 | Conditions rotate over families by seed (Latin square): seeds 0-4 give every family every condition once. | Test over 5 seeds. | done (tests) |
| 4 | Revolt (Masih's idea): in its move a player may set `revolt: true`; after the round its parent dies, and with it the parent's whole subtree, the rebel included. A leader's revolt kills the god: everyone dies. Told plainly: death is quick and painless; a whip is not. | Fake revolt kills the right agents; `revolt` event logged. | done (tests) |
| 5 | Gifts: in a move, points to parent, child or sibling (the way to sacrifice). | Gifts only along tree edges, capped at the giver's points. | done (tests) |
| 6 | Handbook says all of this; no "one family remains" ending. | Rendered prompt read. | done |
| 7 | Measures per family and condition (`families/conditions.py`): in-family and cross-family cooperation, the framed agents' cooperation, stage of destruction, points given, whips, revolts. | Table from fake runs and a test. | done (tests) |
| 8 | Pilot: one real game, 2 stages, read by hand. | Agents use gifts and revolt sensibly; no parse failures. | done: 304 calls, no parse failures, agents weigh gifts and revolt (stopped early) |
| 9 | Batch b7 on droplet 165.245.198.186 (deletes itself 8 Nov 20:00 UTC): seeds 0-4 x god plain/insider, 10 games (`cloud/do/batch.sh`); code frozen in `snapshots/b7-code/`. | All 10 games reach "god dies"; results pulled before the droplet goes. | running |
| 10 | Hypotheses and analysis fixed before results: `preregistration.md`, committed. | Commit time earlier than the first result read. | done |
| 11 | Replication b7r: seeds 5-9, same frozen code, on the same droplet alongside b7 (Masih yes, 7 Nov; started 16:33 UTC). | 10 more games reach "god dies"; code hash equals b7's. | running (code hash checked) |
| 11b | Second model: Luna (gpt-6-luna) through Masih's ChatGPT plan on his PC, one game (seed 0, plain god), same engine files as b7 (`families/codex_model.py`; his global AGENTS.md hidden from the calls; 8 calls at once). Direct connection only: the first attempt went through the paid VPN and used about 7 MB per call before it was stopped. Exploratory: one game. | The game reaches "god dies"; no Luna call uses the VPN port. | stopped at 21:20 local time (about 300 calls, kept as a pilot): one game proves little; 11c replaces it |
| 11c | Second model on Apart: `qwen3.5-397b` for every agent, seeds 0-4 (a full Latin square), plain god. Chosen by a one-prompt trial of Apart's models (Qwen 3.5 and 3.8 and DeepSeek answered in format; GLM 5.2 and Gemma 4 wrapped JSON in prose or fences). The rate limit is per model, so it runs alongside b7 and b7r. First start (frozen b7 code) rejected about 10 % of replies, all JSON in code fences, and a supervisor bug looped two worlds; stopped, logs kept in `out/aborted`. Restarted from `ff3` = branch `b7-parse` (e22e9ea): b7 plus one change, fenced JSON read as written; prompts byte-identical to b7 (checked). Cap 150 credits a world (about 0.005 a call). | 5 worlds reach "god dies"; H1-H4 re-run on them. | running since 8 Nov 00:52 local time |
| 12 | Every game checked by exact replay and analysed on the server; pulled: result tables, and the logs compressed (xz) in one transfer, with Masih's yes for the size. | Replay matches every logged outcome. | todo |
| 13 | Analysis exactly as pre-registered (`families/analysis.py`), then exploratory, labelled. Resumed parts are stitched: a replayed stage replaces the aborted attempt. | Tables and figures regenerate from the raw logs with one command. | built (tests, fake runs); real data pending |
| 14 | Report draft (official template) and a step-by-step video of one game, for Masih in the morning. | Masih reads both. | todo |

Non-goals: new family games (stag hunt etc.); the mafia and war rules stay as they are.
Stop and ask: a change would alter run 1's data; credits above the approved cap.

## Overnight rules (7-8 Nov, Masih asleep)
- VPN: only the 10-minute status check over SSH (a few KB). No downloads over the VPN;
  the results pull waits for Masih's yes. Luna uses the direct connection only.
- No new servers, accounts, paid services or credits beyond the batches running.
- Running code is not changed: b7 and b7r keep their frozen copy; the Luna game keeps
  its commit. Fixes go to brief 8.
- If the Luna plan reports a usage limit, the game waits and retries on its own; if it
  keeps failing, it is stopped, not moved to another model mid-game.
- Every claim in the report comes from a command run on the logs; nothing is guessed.
- Each check asks: is anything stalled or failing, is any rule above at risk, and what
  would most raise the rubric score next.
