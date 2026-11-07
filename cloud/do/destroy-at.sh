#!/usr/bin/env bash
# Make the droplet destroy itself at a set time (Masih's choice: no bill if his internet is cut).
# The DigitalOcean token (scopes: droplet read + delete) travels on stdin and is never printed.
# Usage: cloud/do/destroy-at.sh HOST "2026-11-08 20:00:00 UTC"
set -euo pipefail
host="$1"; when="$2"
case "$host" in *hetzner*) echo "refused: not our server"; exit 1;; esac
r=(bash "$(dirname "$0")/remote.sh" "$host")
"${r[@]}" 'umask 077 && cat > /root/.do_token' < "$HOME/.config/do/token"
"${r[@]}" "cat > /root/destroy.sh && chmod 700 /root/destroy.sh" <<'EOF'
#!/bin/sh
# Wipe the keys, then ask DigitalOcean to delete this droplet.
id=$(curl -s http://169.254.169.254/metadata/v1/id)
t=$(cat /root/.do_token)
shred -u /root/.config/adaption/api_key 2>/dev/null
curl -s -o /dev/null -w '%{http_code}\n' -X DELETE -H "Authorization: Bearer $t" \
  "https://api.digitalocean.com/v2/droplets/$id"
EOF
# Check the token can see this droplet (read scope) without deleting anything.
"${r[@]}" 'id=$(curl -s http://169.254.169.254/metadata/v1/id); curl -s -o /dev/null -w "token check: HTTP %{http_code}\n" -H "Authorization: Bearer $(cat /root/.do_token)" https://api.digitalocean.com/v2/droplets/$id'
"${r[@]}" "systemctl stop ff-stop.timer 2>/dev/null; systemctl reset-failed ff-stop.service 2>/dev/null; \
  systemd-run --quiet --unit=ff-stop --on-calendar='$when' /root/destroy.sh && \
  systemctl list-timers ff-stop --no-pager | sed -n 2p"
