#!/usr/bin/env bash
# Queue a batch on the droplet from a given code folder: it waits until batch WAIT has no game
# left running (the provider's rate limit is shared per account), then plays each seed with a
# plain god. The key is held in memory from now on; the code's commit is recorded.
# Usage: cloud/do/batch-after.sh HOST NAME DIR WAIT[:N] "SEEDS" COMMIT [run.py args...]
#   e.g. cloud/do/batch-after.sh root@1.2.3.4 b9 ff2 b7r "0 1 2 3 4" 1a2b3c4 --games family
set -euo pipefail
host="$1"; name="$2"; dir="$3"; wait_for="$4"; seeds="$5"; commit="$6"; shift 6
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $name $dir $wait_for '$seeds' $commit $*" <<'REMOTE'
set -euo pipefail
name="$1"; dir="$2"; wait_for="$3"; seeds="$4"; commit="$5"; shift 5
# WAIT may be NAME:N: start once at most N games of batch NAME are still running.
left="${wait_for#*:}"; [ "$left" = "$wait_for" ] && left=0; wait_for="${wait_for%%:*}"
cd ~/"$dir"
echo "$commit" > "families/out/$name.commit"
cat > "families/out/$name.sh" <<EOF
cd ~/$dir
export ADAPTION_API_KEY="\$(cat ~/.config/adaption/api_key)"
while [ "\$(pgrep -fc "supervise.sh families/out/$wait_for-")" -gt $left ]; do sleep 60; done
echo "\$(date -u +%T) $wait_for finished; starting $name"
for seed in $seeds; do
  families/supervise.sh families/out/$name-plain-s\$seed --families all --stance design --god plain --seed \$seed $* &
  sleep 20
done
wait
shred -u ~/.config/adaption/api_key 2>/dev/null
echo "batch finished"
EOF
tmux new-session -d -s "$name" "bash families/out/$name.sh; bash"
echo "queued $name in $dir (seeds $seeds, commit $commit) after $wait_for"
REMOTE
