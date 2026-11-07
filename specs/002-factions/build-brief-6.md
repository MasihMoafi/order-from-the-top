# Build brief 6: known share of automata (for Codex Terra)

Masih: players must know that some share of others will likely not cooperate. We keep it
true: in cross-family rounds (brief 5), a share of partners are code automata, not players.

Work in `families/` and tests only; no paid calls; never read key files; do not touch
`analyze.py`. Tests: `.venv/bin/python -m pytest families/tests -q`.

1. `control.json` key `automata` (default 0.2) and `automaton_defect` (default 0.8):
   in each even (cross-family) round, each live player independently gets, with chance
   `automata`, an automaton partner instead of a player. The automaton defects with
   chance `automaton_defect`, else cooperates; rolled by code with the engine rng;
   it has no points, cannot die, sends no messages. Its id is `A-<round>-<player>`.
2. The player is never told whether this partner is an automaton; the observation shows
   only "a member of another family" for both kinds (no family name in cross rounds, so
   identity cannot leak). After the move, the player sees the partner's move only.
3. Handbook: one plain sentence: "In rounds against other families, about 20% of your
   partners are automatic players that defect 80% of the time; you are not told which."
   Generate the two numbers from the control defaults so text and code cannot drift.
4. Log every automaton pairing and move; the analysis must be able to exclude them.

Done when tests pass (including: rates over many fake rounds match 0.2 and 0.8 within
tolerance, and an observation never reveals the automaton). Report rule readings.
