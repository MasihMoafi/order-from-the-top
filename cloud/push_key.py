"""Copy the Adaption key into a Cloudroom sandbox without printing it.

Usage: python3 cloud/push_key.py THREAD_ID
The key travels on stdin to `room-cli vm run --stdin` and lands in the sandbox at the
same path the game reads (~/.config/adaption/api_key, mode 600).
Missing local keys and subprocess startup errors raise. Remote failures are printed
as an exit field; they do not set this script's exit status or print remote stderr.
"""

import subprocess
import sys
from pathlib import Path

key = (Path.home() / ".config/adaption/api_key").read_bytes()
cmd = "mkdir -p ~/.config/adaption && umask 077 && cat > ~/.config/adaption/api_key && wc -c < ~/.config/adaption/api_key"
r = subprocess.run(
    ["room-cli", "vm", "run", "--thread", sys.argv[1], "--stdin", cmd],
    input=key,
    capture_output=True,
    check=False,
)
print(
    "bytes in sandbox:",
    r.stdout.decode().strip(),
    "| local bytes:",
    len(key),
    "| exit",
    r.returncode,
)
