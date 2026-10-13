#!/bin/bash
G=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/limits_repro/lowlevel_join
cd /home/user/auth_gap
for c in "$@"; do
  dir=$G/cases/$c; [ -d "$dir" ] || dir=$G/saved/$c
  .venv/bin/python -m authgap scan "$dir" --population mcp_server --annotation-patch $G/out/${c}_patch.json --determinism 3 > $G/out/$c.stdout 2> $G/out/$c.stderr
  ec=$?
  .venv/bin/python -m authgap probe "$dir" --population mcp_server > $G/out/$c.probe.json 2> $G/out/$c.probe.err
  echo "=================== $c (scan exit=$ec; $(tail -1 $G/out/$c.stderr))"
  python3 $G/tools/summ2.py $G/out/$c.stdout $G/out/$c.probe.json
done
