"""Paint the Love Spot board from a game running on the droplet.

Each minute the server builds the small board snapshot (a few KB) from its newest run part;
only that crosses the network. Usage: python3 -m families.board_remote HOST RUN_NAME [--every 60]
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

from .board_watch import paint

SSH = Path(__file__).resolve().parents[1] / "cloud/do/remote.sh"
REMOTE = (
    "cd ff && .venv/bin/python -c 'import json,sys; from pathlib import Path; "
    "from families.board_watch import snapshot; "
    'parts=sorted(Path("families/out/{name}").glob("part-*"), key=lambda p: int(p.name[5:])); '
    "print(json.dumps(snapshot(parts[-1]) if parts else None))'"
)


def fetch(host, name):
    """Fetch a board snapshot over SSH; return None after printing invalid output.

    Timeouts and process startup errors propagate; a nonzero SSH exit is parsed
    like any other response and does not by itself raise an exception.
    """
    r = subprocess.run(
        ["bash", str(SSH), host, REMOTE.format(name=name)],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        print("fetch failed:", (r.stderr or r.stdout).strip()[-200:], flush=True)
        return None


def main():
    """Poll and repaint changed remote snapshots until interrupted or --once ends."""
    p = argparse.ArgumentParser()
    p.add_argument("host")
    p.add_argument("name")
    p.add_argument("--every", type=float, default=60)
    p.add_argument("--once", action="store_true")
    a = p.parse_args()
    last = None
    while True:
        snap = fetch(a.host, a.name)
        if snap and snap["_key"] != last:
            paint(snap)
            last = snap["_key"]
        if a.once:
            return
        time.sleep(a.every)


if __name__ == "__main__":
    main()
