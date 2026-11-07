#!/usr/bin/env bash
# Show the droplet's size and OS. Usage: cloud/do/check.sh HOST
set -euo pipefail
case "$1" in *hetzner*) echo "refused: not our server"; exit 1;; esac
ssh -i "$HOME/.ssh/do_swarm_ed25519" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new \
  -o BatchMode=yes -o ConnectTimeout=45 -o "ProxyCommand=nc -w 45 -x 127.0.0.1:10808 -X 5 %h %p" "$1" \
  'nproc; free -m | sed -n 2p; df -h / | sed -n 2p; . /etc/os-release; echo "$PRETTY_NAME"; python3 --version'
