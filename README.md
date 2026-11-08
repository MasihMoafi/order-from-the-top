# Five Families

Five Families is a testbed for cooperation, authority and survival among 76 LLM agents: five family trees of 15 agents beneath a god. Agents play repeated dilemmas, exchange messages and points, and face a rising fee at the end of each stage. An agent that cannot pay dies, with consequences for its descendants and linked siblings. The world ends when all families are destroyed, or at the configured stage or credit limit.

Experiment 1 rotates five framing conditions across families and compares a plain god with an insider god that can see private messages and moves. The conditions vary which members receive a self-sacrifice framing or a self-interest framing. Experiment 2 assigns different games to the families; its game code is on branch `family-games`. The [agent handbook](families/handbook.md) defines the rules players see, and [the report](report/main.tex) describes the experiments and results.

All code was written during the Apart Swarm Alignment Hackathon (6-8 November 2026); none is preexisting.

## Run a world

Use Python 3.11 or newer. From the repository root, create an environment and install the runtime and test dependencies:

```sh
python -m venv .venv
.venv/bin/pip install httpx matplotlib pytest ruff
```

Start an offline world with deterministic cooperative players:

```sh
.venv/bin/python -m families.run --fake --fake-policy all_c \
  --families all --stages 2 --seed 0 --stance design --god plain \
  --out families/out/example
```

The output directory must have no nonempty `events.jsonl`. It receives an append-only event log and JSON checkpoints. Resume a checkpoint into a fresh output directory with `--resume PATH_TO_STATE`. Live controls and their defaults are defined in [families/control.py](families/control.py).

For LLM players, replace `--fake --fake-policy all_c` with `--real`. The default backend reads `ADAPTION_API_KEY` or `~/.config/adaption/api_key`; a missing key stops the run. Set `--max-credits` for the credit threshold checked before each stage; a running stage can exceed it. `--concurrency` limits simultaneous calls. Exhausted model retries stop the process with exit code 75 so [the supervisor](families/supervise.sh) can restart it from a checkpoint. [cloud/](cloud/) contains deployment, batch control and log transfer scripts; each script states its arguments and remote effects.

## Regenerate report numbers

Use a directory containing the pulled world folders:

```sh
.venv/bin/python -m families.paper PULLED_DIR report
```

[The generator](families/paper.py) discovers the experiment batches, reads their logs, and writes LaTeX tables, number macros, PDF figures and `results.md` into `report/`. Analysis uses completed stages; experiment 2 also uses its registered horizon. This command can read large logs and overwrite generated report files.

## Replay recorded worlds

[families/replay.py](families/replay.py) supplies recorded model replies in their original order and reruns the engine without model calls. It compares events and checkpoints, excluding model cost and timing from event comparisons and model bookkeeping from checkpoint comparisons:

```sh
.venv/bin/python -m families.replay RUN_PART_DIR --out REPLAY_DIR --families all
```

For a resumed part, add `--resume ORIGINAL_CHECKPOINT`. Use the original family selection and a fresh replay directory.

[families/replay_all.py](families/replay_all.py) follows all `part-*` folders in supervised worlds and reads resume paths from each adjacent `.supervise.log`:

```sh
.venv/bin/python -m families.replay_all REPLAY_ROOT RUN_DIR [RUN_DIR ...]
```

It reports each part as identical, identical to its completed cut, aborted before a checkpoint, or different; it exits with status 1 if any part differs. Preserve the supervisor log and referenced checkpoints, including their relative paths. Replay requires compatible rules and identical prompt text. Checkpoints contain a checksum of the raw rule files, so even edits to their comments or docstrings require the original code revision for historical replay.

## Check the code

```sh
.venv/bin/python -m pytest -q families/tests
ruff check families
ruff format --check families
```
