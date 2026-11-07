#!/usr/bin/env bash
# Copy a worktree's code (families/, and the Python files of game/ and arena/) into its own
# folder on the droplet, share the droplet's Python environment, run the tests there and
# record the commit. Never touches a folder whose games are running (refuses if any are).
# Usage: cloud/do/push-code.sh HOST WORKTREE DIR   e.g. ... root@1.2.3.4 ../.worktrees/x ff3
set -euo pipefail
host="$1"; src="$(cd "$2" && pwd)"; dir="$3"
case "$host" in *hetzner*) echo "refused: not our server"; exit 1;; esac
here="$(dirname "$0")"
if bash "$here/remote.sh" "$host" "pgrep -f '[s]upervise.sh' | xargs -r -I{} readlink /proc/{}/cwd | grep -qx /root/$dir"; then
  echo "refused: games are running in $dir"; exit 1
fi
key="$HOME/.ssh/do_swarm_ed25519"
proxy='ProxyCommand=nc -w 45 -x 127.0.0.1:10808 -X 5 %h %p'
ssh_opt="ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'"
bash "$here/remote.sh" "$host" "mkdir -p $dir/families/out"
rsync -az --delete -e "$ssh_opt" --exclude out/ --exclude '*.log' --exclude __pycache__ \
  --exclude .pytest_cache "$src/families/" "$host:$dir/families/"
rsync -az -e "$ssh_opt" --exclude out/ --exclude sketch/ --include '*/' --include '*.py' \
  --exclude '*' --prune-empty-dirs "$src/game" "$src/arena" "$host:$dir/"
commit=$(git -C "$src" rev-parse --short HEAD)
bash "$here/remote.sh" "$host" "cd $dir && ln -sfn ../ff/.venv .venv && mkdir -p families/out && echo $commit > CODE_COMMIT && .venv/bin/python -m pytest families/tests -q 2>&1 | tail -1"
echo "pushed $commit to $dir"
