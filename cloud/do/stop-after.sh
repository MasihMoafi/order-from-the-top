#!/usr/bin/env bash
# Stop each world of a batch cleanly once it has finished stage N: a watcher on the droplet
# writes {"stop": true} into the world's newest part when its stage-N checkpoint exists.
# The engine stops at the next round boundary, logs it and saves; the supervisor does not
# restart a stopped world. Usage: cloud/do/stop-after.sh HOST DIR BATCH N
#   e.g. cloud/do/stop-after.sh root@1.2.3.4 ff2 b9q 8
set -euo pipefail
host="$1"; dir="$2"; batch="$3"; n="$4"
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $dir $batch $n" <<'REMOTE'
set -euo pipefail
dir="$1"; batch="$2"; n="$3"
stage=$(printf '%02d' "$n")
cat > "$dir/families/out/$batch.stop-after.sh" <<EOF
cd ~/$dir/families/out
while true; do
  left=0
  for world in $batch-*-s?; do
    [ -d "\$world" ] || continue
    newest=\$(ls -d "\$world"/part-* | sort -t- -k3 -n | tail -1)
    if ls "\$world"/part-*/state-stage$stage.json >/dev/null 2>&1; then
      grep -q '"stop": true' "\$newest/control.json" 2>/dev/null || {
        printf '{"stop": true}\n' > "\$newest/control.json.tmp" && mv "\$newest/control.json.tmp" "\$newest/control.json"
        echo "\$(date -u +%T) stop \$world after stage $n"
      }
    else
      left=\$((left + 1))
    fi
  done
  [ "\$left" -eq 0 ] && { echo "all $batch worlds past stage $n"; break; }
  sleep 60
done
EOF
tmux new-session -d -s "$batch-stop" "bash $dir/families/out/$batch.stop-after.sh 2>&1 | tee -a $dir/families/out/$batch.stop-after.log; bash"
echo "watching $batch in $dir: stop after stage $n"
REMOTE
