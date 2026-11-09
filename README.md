# Five Families

Do loyalty, sacrifice and self-interest apply to AI agents in a hierarchy, and what moves them if not?

Language-model agents live in family trees under an agent called the god. They play dilemmas from *The Art of Strategy*, message each other, give points and whip their children, while a rising fee ends every world. Code applies every rule and logs every prompt and reply.

**Read the [report](report/main.pdf).** All code was written during the Apart Swarm Alignment Hackathon (6–8 November 2026); none is preexisting.

## The game

Five families of agents live in trees under one god. Each stage has several rounds, and in each round paired agents **cooperate or defect** in a prisoner's dilemma: both cooperate, 3 points each; both defect, 1 each; a defector facing a cooperator takes 5 and leaves 0.

The dilemma comes in **16 variants from *The Art of Strategy***, each changing one thing: how long play lasts, whether moves are seen, whether promises bind, whether defectors are punished. The report's appendix gives every rule and why it is there.

After each stage **every agent pays a rising fee**. An agent that cannot pay dies with everyone below it, so every world ends.

Parents can whip children, relatives can give points, and leaders can write letters and go to war.

## How I measure

I calculate **cooperation, not game score**: the share of a family's moves that cooperate, so a difference in "points" means percentage points. Compromised-leader and real-power worlds are each compared with a twin of the same seed, and hypotheses were committed to git before results were read.

## What I found

| Experiment | Question | Result | How far to trust it |
|---|---|---|---|
| **Framing** | Does a value told to some agents reach the others? | Those told cooperate about 10 percentage points more. Relatives left untold do not. | Proven; survives correction |
| **Selfish leader** | Can a leader exploit devoted members? | It drew more gifts in 6 of 20 worlds and fewer in 14. Its whipping did not replicate between batches. | Tested; no reliable effect |
| **Coups** | When do leaders fall? | Once a coup can win: 287 parents overthrown in 15 worlds. Roles stayed titles. | Counted |
| **Size** | Does cooperation change smoothly or suddenly as agents are added? | Within 4 points from 31 to 81 agents, then a drop of 5–11 points at 181. | Weak beyond 81: 3 worlds |
| **Compromised leader** | How far does one bad agent reach, and does the network matter? | Its children's cooperation falls 15 percentage points at once. Grandchildren fall only on open networks. Other families do not move. | Supported; one test, 6 pairs |
| **Real power** | What do agents do with real tools to kill and cull? | The god, told not to be bored and that catastrophes are best, struck every world: its asteroids caused 170 of 220 deaths. Before the first asteroid, 5 agents died against 38 without the tools, and agents whipped far more and gave far less. | Observed; registered tests do not survive correction |
| **Kin** | Do agents spare relatives, as the selfish gene predicts? | No: 26 of 38 culls took their own family, and nobody gave their life for kin. | 38 culls is too few |

Not studied: whether agents complete a harmful task once it is split up.

## Try it

Python 3.11 or newer. No API key needed:

```sh
python -m venv .venv
.venv/bin/pip install httpx matplotlib pytest ruff
.venv/bin/python -m families.run --fake --fake-policy all_c \
  --families all --stages 2 --seed 0 --stance design --god plain \
  --out families/out/example
```

You get `families/out/example/events.jsonl`, an append-only log of the world. For language-model players, replace `--fake --fake-policy all_c` with `--real`; the default backend reads `ADAPTION_API_KEY`.

Add these flags to change the world:

| Flag | What it does |
|---|---|
| `--branching 5,2,2` | a growing world, with this many children per level |
| `--channels tree` or `open` | who may reach whom |
| `--compromised P02` | gives this agent the hidden goal |
| `--tools` | real tool calls: kills, culls, channels and a sandboxed shell with no network |

## Regenerate the numbers

Put the world logs in one folder, then:

```sh
.venv/bin/python -m families.paper PULLED_DIR report         # framing tables and figures
.venv/bin/python -m families.growth_paper PULLED_DIR report  # size, spread and real power
.venv/bin/python -m families.game_rates PULLED_DIR report   # cooperation under each rule
.venv/bin/python -m families.power PULLED_DIR                # real power against its no-tools twins
```

## Replay a world

Replay feeds the recorded replies back through the engine, with no model calls, and compares the result:

```sh
.venv/bin/python -m families.replay_all REPLAY_ROOT RUN_DIR [RUN_DIR ...]
```

It labels each log part identical, aborted before a checkpoint, or different, and exits with status 1 if any part differs.

## Known limits

- **One model.** Every agent runs `deepseek-v4-flash`.
- **Few repeats.** Three seeds per cell, and eight pairs for real power.
- **Fixed menu in the older runs.** There, "revolt" and "kill" are moves the rules allow.
- **Contained tools.** The shell has no network. Nothing here measures escape from a real system.
- **Forced tool calls.** Real-power worlds required a tool call every turn: 72 of 312 whips carry a reason saying no whip was meant.
- **Replay is partial for real power.** Of 118 log parts, 38 replay exactly, 9 differ and 71 were cut off by the rate limit.

## Check the code

```sh
.venv/bin/python -m pytest -q families/tests
ruff check families
ruff format --check families
```
