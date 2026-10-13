#!/usr/bin/env bash
# Run reachscan and AuthGap on one B1 case. Usage: run_case.sh <case>
set -u
SP=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad
B=$SP/reachscan_probe/B1
RS=$SP/rs_venv/bin/reachscan
n="$1"; in="$B/cases/$n"; o="$B/out"
cd "$B/tools" || exit 9
"$RS" "$in" --json    > "$o/rs_$n.json"        2> "$o/rs_$n.json.stderr";    echo "rs json exit=$?"    > "$o/rs_$n.exit"
"$RS" "$in"           > "$o/rs_$n.txt"         2> "$o/rs_$n.txt.stderr";     echo "rs text exit=$?"   >> "$o/rs_$n.exit"
"$RS" "$in" --explain > "$o/rs_${n}_explain.txt" 2> "$o/rs_${n}_explain.stderr"; echo "rs explain exit=$?" >> "$o/rs_$n.exit"
"$RS" "$in" --sarif   > "$o/rs_$n.sarif"       2> "$o/rs_$n.sarif.stderr";   echo "rs sarif exit=$?"  >> "$o/rs_$n.exit"
cd /home/user/auth_gap || exit 9
.venv/bin/python -m authgap scan "$in" --sarif "$o/ag_$n.sarif" --annotation-patch "$o/ag_${n}_patch.json" \
    --determinism 3 > "$o/ag_$n.manifest.json" 2> "$o/ag_$n.stderr"; echo "ag scan exit=$?" > "$o/ag_$n.exit"
