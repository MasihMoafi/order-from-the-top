#!/usr/bin/env bash
# Run a real game and keep it alive: after an outage (exit 75), a crash or a kill, resume
# from the newest round checkpoint into a new folder part. Stops on a clean finish (exit 0)
# or when control.json says stop.
# Usage: families/supervise.sh RUN_DIR [run.py args...]   e.g. --families all --stages 16
set -uo pipefail
run="$1"; shift
cd "$(dirname "$0")/.."
part=0
dir="$run/part-$part"
resume=()
while true; do
  echo "$(date +%T) start $dir ${resume[*]}" | tee -a "$run.supervise.log"
  .venv/bin/python -m families.run --real --out "$dir" "${resume[@]}" "$@" >>"$run.supervise.log" 2>&1
  code=$?
  echo "$(date +%T) exit $code" | tee -a "$run.supervise.log"
  [ "$code" -eq 0 ] && break
  if rg -q '"stop": *true' "$dir/control.json" 2>/dev/null; then break; fi
  newest=$(ls -t "$run"/part-*/state-*.json 2>/dev/null | head -1)
  [ -z "$newest" ] && { echo "no checkpoint yet; retry from start in 60 s" | tee -a "$run.supervise.log"; sleep 60; continue; }
  part=$((part + 1)); dir="$run/part-$part"; resume=(--resume "$newest")
  [ -f "$run/part-$((part - 1))/control.json" ] && mkdir -p "$dir" && cp "$run/part-$((part - 1))/control.json" "$dir/"
  sleep 30
done
