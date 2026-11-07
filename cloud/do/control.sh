#!/usr/bin/env bash
# Change the running droplet game between rounds (pause, stop, fee, stance, automata).
# Keys and defaults: families/control.py. The engine logs every change.
# Usage: cloud/do/control.sh HOST RUN_NAME '{"pause": true}'   (then '{"pause": false}')
set -euo pipefail
host="$1"; name="$2"; json="$3"
python3 -c 'import json,sys; json.loads(sys.argv[1])' "$json"
bash "$(dirname "$0")/remote.sh" "$host" "cd ff/families/out/$name && \
  part=\$(ls -d part-* | sort -V | tail -1) && \
  python3 -c 'import json,sys,pathlib; p=pathlib.Path(sys.argv[1]); c=json.loads(p.read_text()) if p.exists() else {}; c.update(json.loads(sys.argv[2])); p.write_text(json.dumps(c))' \$part/control.json '$json' && \
  echo \$part: && cat \$part/control.json"
