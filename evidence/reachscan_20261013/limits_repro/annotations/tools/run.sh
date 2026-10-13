#!/usr/bin/env bash
# usage: run.sh <case dir> <label>
set -u
SP=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/limits_repro/annotations
in="$1"; n="$2"; o="$SP/out"
cd /home/user/auth_gap || exit 9
.venv/bin/python -m authgap scan "$in" --population mcp_server --sarif "$o/$n.sarif" --annotation-patch "$o/${n}_patch.json" \
  --determinism 3 > "$o/$n.manifest.json" 2> "$o/$n.stderr"; echo "exit=$?" > "$o/$n.exit"
.venv/bin/python -I "$SP/tools/summarize_ag.py" "$o/$n.manifest.json" > "$o/$n.summary.txt"
