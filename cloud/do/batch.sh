#!/usr/bin/env bash
# Start a brief-7 batch on a droplet set up by `deploy.sh HOST -`: each seed with a plain god
# and an insider god, side by side in one tmux session. The batch holds the API key in memory
# from the start, so another batch shredding the key file cannot stop it; the key file is
# shredded when this batch finishes.
# Usage: cloud/do/batch.sh HOST BATCH_NAME ["SEEDS"]   (default seeds "0 1 2 3 4")
set -euo pipefail
host="$1"; name="$2"; seeds="${3:-0 1 2 3 4}"
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $name '$seeds'" <<'REMOTE'
set -euo pipefail
name="$1"; seeds="$2"
cd ~/ff
cat > "families/out/$name.sh" <<EOF
cd ~/ff
export ADAPTION_API_KEY="\$(cat ~/.config/adaption/api_key)"
for god in plain insider; do
  for seed in $seeds; do
    families/supervise.sh families/out/$name-\$god-s\$seed --families all --stance design --god \$god --seed \$seed &
    sleep 20
  done
done
wait
shred -u ~/.config/adaption/api_key 2>/dev/null
echo "batch finished"
EOF
tmux new-session -d -s "$name" "bash families/out/$name.sh; bash"
echo "started batch $name (seeds $seeds)"
REMOTE
