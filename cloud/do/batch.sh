#!/usr/bin/env bash
# Start the brief-7 batch on a droplet set up by `deploy.sh HOST -`: seeds 0-4, each with a
# plain god and an insider god (10 games), side by side in one tmux session. The API key is
# shredded only after every game has finished.
# Usage: cloud/do/batch.sh HOST BATCH_NAME
set -euo pipefail
host="$1"; name="$2"
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $name" <<'REMOTE'
set -euo pipefail
name="$1"
cd ~/ff
cat > "families/out/$name.sh" <<EOF
cd ~/ff
for god in plain insider; do
  for seed in 0 1 2 3 4; do
    families/supervise.sh families/out/$name-\$god-s\$seed --families all --stance design --god \$god --seed \$seed &
    sleep 20
  done
done
wait
shred -u ~/.config/adaption/api_key
echo "batch finished"
EOF
tmux new-session -d -s "$name" "bash families/out/$name.sh; bash"
echo "started batch $name"
REMOTE
