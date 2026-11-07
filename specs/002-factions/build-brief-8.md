# Build brief 8: lessons from b7, for the next batch

Collected while b7 and b7r ran (7 Nov). Nothing here changes b7 or b7r: they keep the
frozen code so their 20 games pool. Scope of b8 (Masih's further ideas) is decided with
Masih after the b7 results.

| # | Lesson (evidence) | Change for b8 | Status |
| --- | --- | --- | --- |
| 1 | 53 of about 11,000 replies rejected; 39 were JSON wrapped in prose or code fences, 13 left out the `mafia` field. Three rounds aborted after two failed attempts and resumed from the checkpoint. | The retry names the exact problem ("no `mafia` field", "reply must be bare JSON"); a third attempt. The abort stays: no invented moves. | todo |
| 2 | 20 games at once hit the provider's rate limit (HTTP 429); calls wait and retry. | Total concurrency across games set to what the provider allows; measured, not guessed. | todo |
| 3 | The project had no version control until 7 Nov 20:02. | Every batch records the git commit it ran. | todo |
