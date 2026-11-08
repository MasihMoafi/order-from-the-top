#!/usr/bin/env bash
# Resume a paused batch once another batch is down to N running worlds: a watcher on the
# droplet sets {"pause": false} in each paused world's newest part (logged by the engine).
# Usage: cloud/do/resume-when.sh HOST DIR BATCH WAIT:N   e.g. ... root@1.2.3.4 ff b7r b7:4
set -euo pipefail
host="$1"; dir="$2"; batch="$3"; wait_for="${4%%:*}"; left="${4#*:}"
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $dir $batch $wait_for $left" <<'REMOTE'
set -euo pipefail
dir="$1"; batch="$2"; wait_for="$3"; left="$4"
cat > "$dir/families/out/$batch.resume.sh" <<EOF
cd ~/$dir/families/out
while [ "\$(pgrep -fc "supervise.sh families/out/$wait_for-")" -gt $left ]; do sleep 60; done
for world in $batch-*-s?; do
  newest=\$(ls -d "\$world"/part-* | awk -F'part-' '{print \$2, \$0}' | sort -n | tail -1 | cut -d' ' -f2)
  printf '{"pause": false}\n' > "\$newest/control.json.tmp" && mv "\$newest/control.json.tmp" "\$newest/control.json"
  echo "\$(date -u +%T) resumed \$world"
done
