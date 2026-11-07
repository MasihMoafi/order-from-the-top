#!/usr/bin/env bash
# Check the droplet game every 5 minutes; exit (which wakes the agent) when it needs attention:
# the game ended or restarted, calls stalled for 10 minutes, memory ran low, or the server
# could not be reached 3 times running. Usage: cloud/do/watch.sh HOST RUN_NAME
set -uo pipefail
host="$1"; name="$2"
r=(bash "$(dirname "$0")/remote.sh" "$host")
last=-1; same=0; down=0; starts=""
while true; do
  out=$("${r[@]}" "bash -s -- $name" < "$(dirname "$0")/status.sh" 2>/dev/null)
  if [ -z "$out" ]; then
    down=$((down + 1)); [ "$down" -ge 3 ] && { echo "$(date +%T) server unreachable 3 times"; exit 1; }
    sleep 300; continue
  fi
  down=0
  read -r calls nstart nexit mem state <<<"$(echo $out)"
  echo "$(date +%T) calls=$calls starts=$nstart exits=$nexit free=${mem}MB $state"
  [ "${nexit:-0}" -gt 0 ] && { echo "game process exited (finished or crashed)"; exit 0; }
  [ -n "$starts" ] && [ "$nstart" != "$starts" ] && { echo "supervisor restarted the game"; exit 0; }
  starts="$nstart"
  [ "${mem:-999}" -lt 60 ] && { echo "memory low"; exit 0; }
  if [ "$calls" = "$last" ]; then same=$((same + 1)); else same=0; fi
  [ "$same" -ge 2 ] && { echo "no new calls for 10 minutes"; exit 0; }
  last="$calls"
  sleep 300
done
