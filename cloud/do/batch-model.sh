#!/usr/bin/env bash
# Queue a second-model batch on the droplet: the same frozen code and design as b7, plain god,
# one model for every agent. It waits until at most N games of batch WAIT are still running
# (WAIT:N; plain WAIT means none; "now" starts at once), then starts. The key is held in
# memory from now on. Extra arguments go to run.py (e.g. --max-credits 150).
# The provider's rate limit is per model: a batch on another model can run alongside.
# Usage: cloud/do/batch-model.sh HOST NAME MODEL "SEEDS" WAIT[:N] [run.py args...]
#   e.g. cloud/do/batch-model.sh root@1.2.3.4 b7q qwen3.5-397b "0 1 2 3 4" now --max-credits 150
set -euo pipefail
host="$1"; name="$2"; model="$3"; seeds="$4"; wait_for="$5"; shift 5
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $name $model '$seeds' $wait_for $*" <<'REMOTE'
set -euo pipefail
name="$1"; model="$2"; seeds="$3"; wait_for="$4"; shift 4
left="${wait_for#*:}"; [ "$left" = "$wait_for" ] && left=0; wait_for="${wait_for%%:*}"
cd ~/ff
cat > "families/out/$name.sh" <<EOF
cd ~/ff
export ADAPTION_API_KEY="\$(cat ~/.config/adaption/api_key)"
while [ "$wait_for" != now ] && [ "\$(pgrep -fc "supervise.sh families/out/$wait_for-")" -gt $left ]; do sleep 60; done
echo "\$(date -u +%T) starting $name with $model"
for seed in $seeds; do
  mkdir -p families/out/$name-plain-s\$seed/part-0
  printf '{"god": {"model": "$model", "think_cap": 8000, "effort": "medium"}, "leader": {"model": "$model", "think_cap": 8000, "effort": "medium"}, "member": {"model": "$model", "think_cap": 8000, "effort": "medium"}}\n' > families/out/$name-plain-s\$seed/part-0/models.json
  families/supervise.sh families/out/$name-plain-s\$seed --families all --stance design --god plain --seed \$seed $* &
  sleep 20
done
wait
shred -u ~/.config/adaption/api_key 2>/dev/null
echo "batch finished"
EOF
tmux new-session -d -s "$name" "bash families/out/$name.sh; bash"
echo "queued $name ($model, seeds $seeds, $*) after $wait_for"
REMOTE
