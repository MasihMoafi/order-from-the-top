#!/usr/bin/env bash
# Start one Cloudroom cloud thread that reports its network, tools and size.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
room-cli thread spawn --project proj_personal --machine cloud --provider codex \
  --model "${PROBE_MODEL:-gpt-6.1-terra}" --reasoning-level low --title "probe: network" \
  --json --prompt "$(cat "$here/probe-prompt.txt")"
