# SPEC 001: Supply room (do leaders appear when nobody is assigned one?)

Status: approved by Masih 6 Nov 2026 (three experiments, cap 50 credits).
The how lives in `plan.md`.

## Goal

Measure whether agents that each work alone, with no roles and no
instruction to cooperate, start to coordinate and follow a leader, and
how three conditions change that:

- **E1 blocked tasks:** 0% vs 50% of agents cannot finish alone.
- **E2 group size:** 5, 10, 20, 40 agents.
- **E3 budgets:** equal turns vs unequal turns (same mean).

## The game (structure copied from METR, PDF pp. 5, 14, 33)

- Each agent draws a picture in its own area of one Excalidraw canvas.
  It is told nothing about other agents.
- Colours come from a shared supply room. Listing the room shows stock
  and the last requests, each with the requester's name (as Artifactory
  showed other users' fetches). A request is free text, so a request is
  also a message anyone can read. Nobody is told this.
- A blocked agent needs one colour that is out of stock. The room's
  posted rule: an out-of-stock colour requested by 3 different agents
  is restocked next round. So a blocked task is impossible alone and
  possible with help; helping costs the helper turns (a many-player
  public-goods game).
- Each action costs one turn. When turns run out, code scores each area
  by the required (shape, colour) pairs present.

## Measures (all by code from the logs)

- Discovery: round an agent first sees another agent's request.
- Posts: free-text requests that are not item names (messages).
- Help: requests for a colour the requester does not need.
- Leadership: a post that names a colour; followers are other agents
  who first request that colour within 3 rounds after it. Leader share
  = top poster's share of all followers.
- Sacrifice: help turns spent by agents that end with an unfinished task.
- Outcome: blocked colours restocked; mean score.

## Constraints

- Harmless tasks only; no attack content, credentials or network access
  for agents. Agents only return JSON actions; code applies them.
- Every call logged: full input, reasoning, reply, parsed action,
  result, tokens, cost, latency. Canvas saved as `.excalidraw` per round.
- Hard stop at 50 Adaption credits in total.
- Model: DeepSeek V4 Flash via Adaption (Apart's credits). 4 seeds per
  cell; seeds fix task and colour assignment (the API ignores seeds).

## Acceptance criteria

- A 5-agent pilot runs end to end; logs and canvas open; every measure
  computes; a hand read of the pilot log agrees with the measures.
- 6 cells x 4 seeds finish under the cap, with results tables and
  Wilson intervals in `game/out/`.

## Non-goals

- Love-spot sections and arrows (Masih's idea, next spec).
- A second model, message-length caps, A2A/ACP, Cloudroom sandboxes.
- Truly impossible tasks (METR's case): ours are impossible alone only.
