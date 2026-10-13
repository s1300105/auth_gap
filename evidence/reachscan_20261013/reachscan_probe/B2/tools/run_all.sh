#!/bin/bash
# Run reachscan and AuthGap on every B2 case. Outputs go to $B/out.
B=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/reachscan_probe/B2
RS=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/rs_venv/bin/reachscan
AG=/home/user/auth_gap/.venv/bin/python
cd /home/user/auth_gap || exit 2
: > $B/out/exit_codes.tsv
for d in $B/cases/*/; do
  n=$(basename $d)
  $RS $d --json > $B/out/rs_$n.json 2> $B/out/rs_$n.json.stderr; echo -e "$n\treachscan --json\t$?" >> $B/out/exit_codes.tsv
  $RS $d > $B/out/rs_$n.txt 2> $B/out/rs_$n.txt.stderr; echo -e "$n\treachscan text\t$?" >> $B/out/exit_codes.tsv
  $RS $d --explain > $B/out/rs_${n}_explain.txt 2> $B/out/rs_${n}_explain.stderr; echo -e "$n\treachscan --explain\t$?" >> $B/out/exit_codes.tsv
  $RS $d --sarif > $B/out/rs_$n.sarif 2> $B/out/rs_$n.sarif.stderr; echo -e "$n\treachscan --sarif\t$?" >> $B/out/exit_codes.tsv
  $AG -m authgap scan $d --sarif $B/out/ag_$n.sarif --annotation-patch $B/out/ag_${n}_patch.json --determinism 3 > $B/out/ag_$n.manifest.json 2> $B/out/ag_$n.stderr; echo -e "$n\tauthgap scan\t$?" >> $B/out/exit_codes.tsv
done
