"""Watch a game back on the Love Spot page "Families replay", one round every few seconds.

Each round shows who played C or D, who wrote to whom and what, points, deaths and wars.
Frames come from a local run folder, or from the server (built there; only the frames,
gzipped, cross the network).
Usage: python3 -m families.board_replay RUN_DIR [--every 4] [--from-stage 1]
       python3 -m families.board_replay --host root@IP RUN_NAME [--follow 60]   (then stays live)
"""

import argparse
import base64
import gzip
import json
import subprocess
import tempfile
import time
from pathlib import Path

from .board_frames import frames

HERE = Path(__file__).resolve().parent
SSH = HERE.parent / "cloud/do/remote.sh"
REMOTE = (
    "cd ff && PYTHONPATH=. .venv/bin/python - families/out/{name}/part-*/events.jsonl"
    " | gzip -9 | base64 -w0"
)


def server_frames(host, name):
    """Build frames remotely and decode the gzipped JSON returned over SSH.

    Raise on command failure, timeout, invalid compressed data or invalid JSON.
    """
    script = (HERE / "board_frames.py").read_text()
    r = subprocess.run(
        ["bash", str(SSH), host, REMOTE.format(name=name)],
        input=script,
        capture_output=True,
        text=True,
        timeout=600,
        check=True,
    )
    return json.loads(gzip.decompress(base64.b64decode(r.stdout.strip())))


def paint(frame):
    """Update the board through board_live.cjs and return its printed output.

    The temporary snapshot is removed after the subprocess returns; its nonzero
    exit status is not raised, and stderr is returned when stdout is empty.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(frame, f)
    r = subprocess.run(
        ["node", str(HERE / "board_live.cjs"), f.name],
        capture_output=True,
        text=True,
        check=False,
    )
    Path(f.name).unlink()
    return (r.stdout or r.stderr).strip()


def main():
    """Play local or remote frames on the named board page, optionally following."""
    p = argparse.ArgumentParser()
    p.add_argument("run", help="local run folder, or the run name with --host")
    p.add_argument("--host")
    p.add_argument("--every", type=float, default=4, help="seconds per round")
    p.add_argument("--from-stage", type=int, default=1)
    p.add_argument("--page", default="Families replay")
    p.add_argument(
        "--follow",
        type=float,
        metavar="SECONDS",
        help="after the replay, keep showing the live game, checking this often",
    )
    a = p.parse_args()

    def load():
        if a.host:
            return server_frames(a.host, a.run)
        run = Path(a.run)
        return frames(
            sorted(
                run.glob("part-*/events.jsonl"), key=lambda p: int(p.parent.name[5:])
            )
            or [run / "events.jsonl"]
        )

    shown = {}  # (stage, round) -> the frame as last painted; a round still being played changes
    first = True
    while True:
        for f in load():
            key = (f["stage"], f["round"])
            if f["stage"] < a.from_stage or shown.get(key) == f:
                continue
            shown[key] = f
            painted = dict(
                f,
                page=a.page,
                alive=sum(x["alive"] for x in f["agents"].values()),
                total=len(f["agents"]),
            )
            print(f"stage {key[0]} round {key[1]}: {paint(painted)}", flush=True)
            if first:
                time.sleep(a.every)
        first = False
        if not a.follow:
            return
        time.sleep(a.follow)


if __name__ == "__main__":
    main()
