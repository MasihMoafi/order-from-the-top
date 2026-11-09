#!/usr/bin/env bash
# Download new logs of the growth worlds, then rebuild every number, quote and timeline from them.
# Writes families/out/evidence/. Usage: cloud/do/refresh.sh HOST
set -euo pipefail
host="$1"
python="${PYTHON:-.venv/bin/python}"
pulled=families/out/pulled
out=families/out/evidence
bash cloud/do/pull.sh "$host" "$pulled" ff5:g1 ff6:c1
mkdir -p "$out"
worlds=("$pulled"/g1-*-s? "$pulled"/c1-*-s?)
for horizon in 3 5; do
  "$python" -m families.growth "$pulled" g1 "$horizon" > "$out/growth-h$horizon.txt"
done
"$python" -m families.spread "$pulled" > "$out/spread.txt"
"$python" -m families.evidence "$out" "${worlds[@]}"
"$python" -m families.timeline "$out/timeline" "${worlds[@]}" | tee "$out/timelines.txt"
