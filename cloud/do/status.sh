# Runs ON the droplet (fed by watch.sh over stdin). Prints: calls starts exits free_MB newest_state
name="$1"
cd ~/ff/families/out || exit 1
calls=$(cat "$name"/part-*/events.jsonl 2>/dev/null | rg -c '"type": "call"')
starts=$(rg -c '^\d\d:\d\d:\d\d start ' "$name.supervise.log")
exits=$(rg -c '^\d\d:\d\d:\d\d exit ' "$name.supervise.log")
mem=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
state=$(ls "$name"/part-*/state-s*.json 2>/dev/null | sort -V | tail -1 | xargs -r basename)
echo "${calls:-0} ${starts:-0} ${exits:-0} $mem ${state:-none}"
