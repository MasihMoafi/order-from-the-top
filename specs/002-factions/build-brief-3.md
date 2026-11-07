# Build brief 3: live control, wars, messengers, models per role (for Codex Terra)

Work in `~/Desktop/p/swarm-hackathon/families/` and its tests only. Same limits as
before: no paid calls, never read key files. Tests: `.venv/bin/python -m pytest
families/tests -q`. Since brief 2 I changed (keep these): leaders' fates are not linked;
the mafia leader is P17; START_POINTS = 10; ante step 0.75; the mafia arrest happens once
per stage on the PD scale (points = 5 - years) with one boss call; `RealModel` caps
thinking and falls back to no thinking; `call_stream(..., extra=None)`.
Rules: `specs/002-factions/rules.md`; what agents are told: `handbook.md` (update it for
anything agents must know, in the same plain style; never mention measures or conditions).

1. Pause and fix mid-game without losing anything.
   - Save a checkpoint after every round (`state-sNN-rMM.json`), not only every stage.
   - Read `control.json` before every round: `pause` (wait, polling every 5 s, logged
     once), `stop` (save and exit cleanly), `ante0`, `step`, and model settings (item 4).
   - `--resume` from any round checkpoint continues mid-stage; a test shows a resumed run
     equals a straight run (fake model).
   - SIGINT/SIGTERM: finish writing the current event, save, exit.
2. Wars (R7), replacing the stub. A leader may declare war on another family in its
   letter phase. Each war round both leaders choose yield, hold or escalate; levels:
   skirmish (winner takes 10% of the loser family's points, spread evenly), battle (25%
   and the loser's lowest live leaf dies), nuclear (both families destroyed). Each
   escalation raises the chance of an accidental slip to nuclear (5% at skirmish, 15% at
   battle). A leader may issue a nuclear ultimatum at any time: the other yields (war
   lost at the current level) or both are destroyed. Strength = the family's total points;
   higher strength wins a level, ties split. A war at a level counts as "at war" for R9.
   All rolls by code with the engine rng; every step logged.
3. Messengers. The god may send messengers: `messengers: [{to: any live agent id,
   content}]`, delivered with edge `messenger`. Members may reply to a messenger once,
   in the next round, and the reply goes to the god.
4. Models per role. `models.json` in the run folder: `{god: {...}, leader: {...},
   member: {...}}`, each `{model, think_cap, effort}`; default all `deepseek-v4-flash`,
   think_cap 8000. Read at start and before each round (changes logged).
5. Speed: within a round, ask every independent call at once (gather); list in the
   report every place a call still waits on another call, and why it must.

Done when: tests pass (including the resume-mid-stage equality and a war test with
fixed rolls); a fake five-family 16-stage run finishes with at least one war in the log.
Report outputs and every rule reading you chose.
