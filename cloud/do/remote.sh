#!/usr/bin/env bash
# Run one command on the droplet, directly unless SWARM_PROXY holds an ssh ProxyCommand.
# Usage: cloud/do/remote.sh HOST 'command'
set -euo pipefail
case "$1" in *hetzner*) echo "refused: not our server"; exit 1;; esac
ssh -i "$HOME/.ssh/do_swarm_ed25519" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=45 -o ServerAliveInterval=15 \
  -o "ProxyCommand=${SWARM_PROXY:-none}" "$1" "$2"
