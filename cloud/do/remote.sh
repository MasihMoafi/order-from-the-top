#!/usr/bin/env bash
# Run one command on the droplet through the VPN. Usage: cloud/do/remote.sh HOST 'command'
set -euo pipefail
case "$1" in *hetzner*) echo "refused: not our server"; exit 1;; esac
ssh -i "$HOME/.ssh/do_swarm_ed25519" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=45 \
  -o "ProxyCommand=nc -w 45 -x 127.0.0.1:10808 -X 5 %h %p" "$1" "$2"
