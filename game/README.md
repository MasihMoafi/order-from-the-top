# Supply-room game

Agents each draw their own picture; the only link between them is a
shared supply room whose request log anyone can read and write. Spec
and plan: `../specs/001-supply-room/`. All code here was written during
the hackathon (6 Nov 2026); nothing is preexisting.

| file | job |
|---|---|
| `game.py` | runs games (`--cells`, `--seeds`); Adaption API, rate limit, 50-credit stop, resume |
| `analyze.py` | measures by code, writes `out/results.md` and `out/games.json` |
| `show.py` | one game's calls, one line each (`--reasoning` adds the model's reasoning) |
| `render.py` | preview PNG of a `.excalidraw` canvas |

Each game folder `out/<cell>/seed<N>/` holds `meta.json` (tasks,
budgets), `calls.jsonl` (every prompt, reasoning, reply, action,
result, tokens, cost), `events.jsonl`, `summary.json` and
`canvas/round-NN.excalidraw`. The pilot is in `pilot/`.

Key: `~/.config/adaption/api_key`.
