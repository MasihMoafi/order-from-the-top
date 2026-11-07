#!/usr/bin/env bash
# Copy the game code (no runs, logs or reviews) into a private repo and push it.
# Usage: cloud/gh/push.sh   (repo: MasihMoafi/five-families-run, private)
set -euo pipefail
noproxy=(env -u HTTPS_PROXY -u HTTP_PROXY -u ALL_PROXY -u https_proxy -u http_proxy -u all_proxy)
src="$(cd "$(dirname "$0")/../.." && pwd)"
dst="$HOME/Work/tries/five-families-run"
mkdir -p "$dst/.github/workflows" "$dst/families"
rsync -a --delete --exclude out/ --exclude '*.log' --exclude '*report*.md' \
  --exclude 'review-*.md' --exclude 'sol-*.md' --exclude __pycache__ --exclude .pytest_cache \
  "$src/families/" "$dst/families/"
cp "$src/cloud/gh/run.yml" "$dst/.github/workflows/run.yml"
cd "$dst"
[ -d .git ] || git init -q -b main
git add .github families
git commit -qm "game code $(date +%F-%H%M)" || true
repo=MasihMoafi/five-families-run
"${noproxy[@]}" gh repo view "$repo" >/dev/null 2>&1 \
  || "${noproxy[@]}" gh repo create "$repo" --private --source . --remote origin
"${noproxy[@]}" git -c http.proxy= push -q -u origin main
