# Build brief 8: lessons from b7, for the next batch

Collected while b7 and b7r ran (7 Nov). Nothing here changes b7, b7r or b7q: they keep the
frozen code so their games pool. The fixes ship with experiment 2 (brief 9, branch
`family-games`, batch b9).

| # | Lesson (evidence) | Change | Status |
| --- | --- | --- | --- |
| 1 | 53 of about 11,000 replies rejected; 39 were JSON wrapped in prose or code fences, 13 left out the `mafia` field. Rounds aborted after two failed attempts and resumed from the checkpoint. | The JSON the model wrote is read from inside prose or fences; the retry names the exact problem. The abort stays: no invented moves. | done in b9 (tests) |
| 1a | Root cause of the `mafia` failures: the prompt said "use mafia only when an arrest is shown", while the checker required it whenever `mafia_partner` appears. Members who followed the prompt were rejected. b7-insider-s1 replayed stage 5 more than 10 times for it. | The prompt now says to supply mafia exactly when `mafia_partner` appears. | done in b9 |
| 1b | Checkpoints are per stage, so an aborted round replays its whole stage (b7-plain-s2 replayed stage 2 five times). Only stages that ran without an abort are kept: a mild selection on clean rounds, reported. | Fixes 1 and 1a make aborts rare; round checkpoints left for later. | partly |
| 2 | 20 games at once hit the provider's rate limit (HTTP 429); calls wait and retry. | Batches queue one after another (`cloud/do/batch-after.sh`) instead of piling up. | done |
| 3 | The project had no version control until 7 Nov 20:02. | Every batch records the git commit it ran (`families/out/NAME.commit`). | done |
| 4 | The replay tool ignored the run's stance and god, so brief-7 worlds could not replay; the measures table crashed on a whip by the god. | Both fixed on main (commit 1d1ed10); replay checked on a live b7 world: 3,008 calls and 27 of 27 checkpoints identical. | done |
| 5 | The first Luna attempt sent every call through the paid VPN (about 7 MB a call). | Luna and Adaption calls go over the direct connection; only SSH uses the VPN. | done |
| 6 | The supervisor retried a world that failed before its first checkpoint in the same folder, which fails forever (two Qwen worlds looped). | A retry before the first checkpoint starts a new part (branches `b7-parse`, `family-games`; not the running b7 copy). | done |
