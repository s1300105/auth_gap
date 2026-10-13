#!/bin/bash
R=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/limits_repro/lowlevel_join_refute
G=/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/limits_repro/lowlevel_join
cd /home/user/auth_gap
for c in "$@"; do
  dir=$R/cases/$c; [ -d "$dir" ] || dir=$G/cases/$c; [ -d "$dir" ] || dir=$G/saved/$c
  .venv/bin/python -m authgap scan "$dir" --population mcp_server --annotation-patch $R/out/${c}_patch.json --determinism 3 > $R/out/$c.stdout 2> $R/out/$c.stderr
  ec=$?
  .venv/bin/python -m authgap probe "$dir" --population mcp_server > $R/out/$c.probe.json 2> $R/out/$c.probe.err
  echo "=================== $c [$dir] (scan exit=$ec; $(tail -1 $R/out/$c.stderr))"
  python3 $R/tools/summ2.py $R/out/$c.stdout $R/out/$c.probe.json
done
