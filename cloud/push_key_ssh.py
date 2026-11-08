"""Copy the Adaption key to an SSH host without printing it.

Usage: python3 cloud/push_key_ssh.py HOST
The key travels on stdin and lands at ~/.config/adaption/api_key (mode 600) on HOST.
Missing local keys and subprocess startup errors raise. Remote failures are printed
as an exit field; they do not set this script's exit status or print remote stderr.
"""

import subprocess
import sys
from pathlib import Path

key = (Path.home() / ".config/adaption/api_key").read_bytes()
cmd = "mkdir -p ~/.config/adaption && umask 077 && cat > ~/.config/adaption/api_key && wc -c < ~/.config/adaption/api_key"
r = subprocess.run(
    ["ssh", "-o", "BatchMode=yes", sys.argv[1], cmd],
    input=key,
    capture_output=True,
    check=False,
)
print(
    "bytes on host:",
    r.stdout.decode().strip(),
    "| local bytes:",
    len(key),
    "| exit",
    r.returncode,
)
