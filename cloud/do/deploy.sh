#!/usr/bin/env bash
# Put the game on Masih's own DigitalOcean droplet and start the full run there.
# Only for a server Masih created and named as ours. Never hetzner-pc / hetzner-gateway.
# Usage: cloud/do/deploy.sh HOST RUN_NAME [run.py args...]   e.g. root@1.2.3.4 full --families all
# SSH goes through the VPN (plain port 22 times out from here).
set -euo pipefail
host="$1"; name="$2"; shift 2
case "$host" in *hetzner*) echo "refused: not our server"; exit 1;; esac
src="$(cd "$(dirname "$0")/../.." && pwd)"
key="$HOME/.ssh/do_swarm_ed25519"
proxy='ProxyCommand=nc -w 45 -x 127.0.0.1:10808 -X 5 %h %p'
ssh=(ssh -i "$key" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o BatchMode=yes
  -o ConnectTimeout=45 -o ServerAliveInterval=15 -o "$proxy")
# 1. Code only (no runs, logs, reviews).
"${ssh[@]}" "$host" "mkdir -p ff"
rsync -az --delete -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'" \
  --exclude out/ --exclude '*.log' --exclude __pycache__ --exclude .pytest_cache \
  "$src/families/" "$host:ff/families/"
# families imports game/ and arena/: their Python files only.
rsync -az -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'" \
  --exclude out/ --exclude sketch/ --include '*/' --include '*.py' --exclude '*' --prune-empty-dirs \
  "$src/game" "$src/arena" "$host:ff/"
# 2. Key: travels on stdin, lands mode 600, never printed.
"${ssh[@]}" "$host" 'mkdir -p ~/.config/adaption && umask 077 && cat > ~/.config/adaption/api_key' \
  < "$HOME/.config/adaption/api_key"
# 3. Swap (512 MB droplet), Python, tests, then the run inside tmux so it outlives SSH.
#    After the run the API key is shredded; the machine powers off 3 days from now regardless.
"${ssh[@]}" "$host" bash -s -- "$name" "$@" <<'REMOTE'
set -euo pipefail
name="$1"; shift
[ -f /swapfile ] || { fallocate -l 1G /swapfile && chmod 600 /swapfile && mkswap -q /swapfile && swapon /swapfile; }
command -v rg >/dev/null || { apt-get update -qq && apt-get install -y -qq ripgrep python3-venv tmux; }
cd ~/ff
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install -q httpx pytest matplotlib
.venv/bin/python -m pytest families/tests -q 2>&1 | tail -3
mkdir -p families/out
shutdown -h +4320 >/dev/null 2>&1 || true
[ "$name" = "-" ] && { echo "set up; no run started (cloud/do/batch.sh starts several)"; exit 0; }
tmux new-session -d -s "$name" "families/supervise.sh families/out/$name $* ; shred -u ~/.config/adaption/api_key; bash"
echo "started $name in tmux"
REMOTE
