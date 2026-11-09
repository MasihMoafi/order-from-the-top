#!/usr/bin/env bash
# Start a growth-world batch from a fresh code folder DIR on the droplet: at most PAR worlds
# at once, in manifest order. The API key travels on stdin and is held in memory by the batch.
# MANIFEST lines: NAME SEED BRANCHING CHANNELS   e.g. g1-81-open-s0 0 5,2 open
# Usage: cloud/do/batch-growth.sh HOST BATCH DIR PAR STAGES MANIFEST [run.py args...]
set -euo pipefail
host="$1"; batch="$2"; dir="$3"; par="$4"; stages="$5"; manifest="$6"; shift 6; extra="$*"
case "$host" in *hetzner*) echo "refused: not our server"; exit 1;; esac
src="$(cd "$(dirname "$0")/../.." && pwd)"
key="$HOME/.ssh/do_swarm_ed25519"
proxy="ProxyCommand=${SWARM_PROXY:-none}"
ssh=(ssh -i "$key" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o BatchMode=yes
  -o ConnectTimeout=45 -o ServerAliveInterval=15 -o "$proxy")
"${ssh[@]}" "$host" "mkdir -p $dir/families/out"
rsync -az --delete -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'" \
  --exclude out/ --exclude '*.log' --exclude __pycache__ --exclude .pytest_cache --exclude tests/ \
  "$src/families/" "$host:$dir/families/"
rsync -az -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'" \
  --exclude out/ --exclude sketch/ --include '*/' --include '*.py' --exclude '*' --prune-empty-dirs \
  "$src/game" "$src/arena" "$host:$dir/"
# The key travels on stdin and is stored with mode 600, never printed.
"${ssh[@]}" "$host" 'mkdir -p ~/.config/adaption && umask 077 && cat > ~/.config/adaption/api_key' \
  < "$HOME/.config/adaption/api_key"
"${ssh[@]}" "$host" "cat > $dir/families/out/$batch.manifest" < "$manifest"
"${ssh[@]}" "$host" bash -s -- "$batch" "$dir" "$par" "$stages" "$extra" <<'REMOTE'
set -euo pipefail
batch="$1"; dir="$2"; par="$3"; stages="$4"; shift 4; extra="$*"
cd ~/"$dir"
ln -sfn ~/ff/.venv .venv
cat > "families/out/$batch.sh" <<EOF
cd ~/$dir
export ADAPTION_API_KEY="\$(cat ~/.config/adaption/api_key)"
xargs -P $par -L 1 bash -c 'exec families/supervise.sh families/out/\$0 --families all --stance none --god plain --seed \$1 --branching \$2 --channels \$3 --stages $stages --max-credits 500 --concurrency 30 $extra' < families/out/$batch.manifest
echo "batch finished"
EOF
tmux new-session -d -s "$batch" "bash families/out/$batch.sh; bash"
echo "started $batch: $(wc -l < "families/out/$batch.manifest") worlds, $par at once"
REMOTE
