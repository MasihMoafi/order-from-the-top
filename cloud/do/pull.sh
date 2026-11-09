#!/usr/bin/env bash
# Pull batches from the droplet, incrementally: each part's events.jsonl is compressed on the
# droplet (xz, only when it changed since the last pull), then rsync fetches the compressed
# files that are new or changed, with the settings and supervisor logs. A finished part is
# fetched once; a refresh fetches only parts still growing. Locally the logs are unpacked
# beside their .xz. Usage: cloud/do/pull.sh HOST DEST DIR:PATTERN [DIR:PATTERN ...]
#   e.g. cloud/do/pull.sh root@1.2.3.4 families/out/pulled ff:b7 ff:b7r ff3:b7q ff2:b9q
set -euo pipefail
host="$1"; dest="$2"; shift 2
mkdir -p "$dest"
here="$(dirname "$0")"
bash "$here/remote.sh" "$host" "bash -s -- $*" <<'REMOTE'
set -euo pipefail
for spec in "$@"; do
  dir="${spec%%:*}"; pat="${spec#*:}"
  for f in "$dir"/families/out/"$pat"-*-s?/part-*/events.jsonl; do
    [ -f "$f" ] || continue
    [ -f "$f.xz" ] && [ "$f.xz" -nt "$f" ] && continue
    nice -n 15 xz -T2 -6 -k -c "$f" > "$f.xz.tmp" && mv "$f.xz.tmp" "$f.xz"
  done
done
echo compressed
REMOTE
key="$HOME/.ssh/do_swarm_ed25519"
proxy="ProxyCommand=${SWARM_PROXY:-none}"
for spec in "$@"; do
  dir="${spec%%:*}"; pat="${spec#*:}"
  rsync -am --partial -e "ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes -o ServerAliveInterval=15 -o '$proxy'" \
    --include "$pat-*-s?/" --include "$pat-*-s?/part-*/" --include "$pat-*-s?/part-*/events.jsonl.xz" \
    --include "$pat-*-s?/part-*/state-*.json" --include "$pat-*-s?/part-*/control.json" --include "$pat-*-s?/part-*/models.json" \
    --include "$pat-*-s?.supervise.log" --include "$pat.commit" --exclude '*' \
    "$host:$dir/families/out/" "$dest/"
done
n=0
while read -r f; do
  if [ ! -f "${f%.xz}" ] || [ "$f" -nt "${f%.xz}" ]; then xz -dkf "$f"; n=$((n + 1)); fi
done < <(find "$dest" -name events.jsonl.xz)
echo "pulled into $dest; unpacked $n changed logs; $(du -sh "$dest" | cut -f1) on disk"
