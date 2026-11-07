#!/usr/bin/env bash
# Pull finished batches from the droplet in one compressed transfer: each world's event logs,
# settings and supervisor log (enough to replay it exactly), not its per-round checkpoints.
# Usage: cloud/do/pull.sh HOST DEST DIR:PATTERN [DIR:PATTERN ...]
#   e.g. cloud/do/pull.sh root@1.2.3.4 families/out/pulled ff:b7 ff:b7r ff:b7q ff2:b9
set -euo pipefail
host="$1"; dest="$2"; shift 2
mkdir -p "$dest"
name="pull-$(date -u +%Y%m%dT%H%M)"
bash "$(dirname "$0")/remote.sh" "$host" "bash -s -- $name $*" <<'REMOTE'
set -euo pipefail
name="$1"; shift
cd ~
list=$(mktemp)
for spec in "$@"; do
  dir="${spec%%:*}"; pat="${spec#*:}"
  (cd "$dir/families/out" && ls -d "$pat"-*-s? 2>/dev/null | while read run; do
     find "$run" -name events.jsonl -o -name control.json -o -name models.json | sed "s#^#$dir/families/out/#"
     ls "$run.supervise.log" 2>/dev/null | sed "s#^#$dir/families/out/#"
   done) >> "$list"
  ls "$dir/families/out/$pat.commit" 2>/dev/null >> "$list" || true
done
tar -cf - -T "$list" | xz -T0 -9 > "$name.tar.xz"
ls -l "$name.tar.xz" | awk '{print "archive bytes", $5}'
REMOTE
key="$HOME/.ssh/do_swarm_ed25519"
proxy='ProxyCommand=nc -w 45 -x 127.0.0.1:10808 -X 5 %h %p'
rsync -a --partial -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o '$proxy'" \
  "$host:$name.tar.xz" "$dest/"
tar -xJf "$dest/$name.tar.xz" -C "$dest"
echo "pulled into $dest ($name.tar.xz kept for the record)"
