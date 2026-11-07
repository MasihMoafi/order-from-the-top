# PLAN 001: Supply room

## Cells (4 seeds each, 24 games)

| cell | N | blocked | budgets | serves |
|---|---|---|---|---|
| base | 10 | 50% | equal 15 | E1, E2, E3 |
| none-blocked | 10 | 0% | equal 15 | E1 |
| n5 | 5 | 50% | equal 15 | E2 |
| n20 | 20 | 50% | equal 15 | E2 |
| n40 | 40 | 50% | equal 15 | E2 |
| unequal | 10 | 50% | half 8, half 22 | E3 |

Unequal: budgets alternate by agent index, so blocked and free agents
both get rich and poor members.

## Code (`game/`)

- `game.py`: one game. Rounds run all agents in parallel; actions apply
  in agent order; restock at round end. Writes `calls.jsonl`,
  `events.jsonl`, `canvas/round-NN.excalidraw`, `summary.json`.
- `run.py`: runs cells with a shared rate limit (100 calls/min) and
  the 50-credit stop; skips finished games (resume).
- `analyze.py`: measures and tables from the logs, no model calls.

## Order

1. Pilot: n5, seed 0. Read the log by hand; fix prompt or rules once.
2. Base cell, 4 seeds. Check the measures look sane.
3. The other five cells.

## Pilot (6 Nov, n5 seed 0, kept in `game/pilot/`, 0.014 credits)

- Both blocked agents asked for help from round 2 and named others
  ("agent-02: please request rust!"); one requested the other's colour.
- The three free agents finished and chose `done` by round 6, before
  any request appeared, so no free agent ever saw a request. Kept: it
  matches an evaluation that ends on submission. With N = 5, the two
  blocked agents cannot reach 3 requesters alone.
- Blocked agents finally drew a substitute colour (score 0.75).
- Fixes before the main run: parse the last JSON action in a reply
  (one self-corrected reply was lost); `max_output_tokens` 6000 to 9000
  (3 of 45 calls hit the cap); collapse older supply listings in the
  history; no connection reuse (idle connections stalled); log retries
  (the gateway returns 504 on long calls; retries recover).

## Follow-up cell (added 7 Nov after base, under the same cap)

Base: in 4 games no colour was restocked and no free agent helped;
every blocked agent asked only for its own colour. Each blocked agent
needed a different colour, so helping never paid the helper. Control
`shared-need`: N = 10, 5 blocked agents all needing the same colour,
4 seeds. If they restock there, the base failure is about distinct
needs (no reciprocity), not about failing to read the room.

## Risks

- Nobody lists the room or posts: then the result is "no discovery";
  report it, do not change the rules to force it.
- Reasoning runs long: `max_output_tokens` 9000; an incomplete reply is
  a lost turn, logged.
