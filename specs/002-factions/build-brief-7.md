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
| 11 | Replication b7r: seeds 5-9, same frozen code, started when b7 ends (Masih yes, 7 Nov). | 10 more games reach "god dies"; code hash equals b7's. | todo |
| 12 | Pull b7, b7r and run 1 compressed; every game checked by exact replay. | Replay matches every logged outcome. | todo |
| 13 | Analysis exactly as pre-registered (`families/analysis.py`), then exploratory, labelled. Resumed parts are stitched: a replayed stage replaces the aborted attempt. | Tables and figures regenerate from the raw logs with one command. | built (tests, fake runs); real data pending |
| 14 | Report draft (official template) and a step-by-step video of one game, for Masih in the morning. | Masih reads both. | todo |

Non-goals: new family games (stag hunt etc.); the mafia and war rules stay as they are.
Stop and ask: a change would alter run 1's data; credits above the approved cap.
