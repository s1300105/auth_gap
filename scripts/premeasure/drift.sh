#!/bin/bash
set -u
name=$1; url=$2
d=corpus_mcp/$name
cd "$d" || exit 0
tags=$(timeout 30 git ls-remote --tags "$url" 2>/dev/null | grep -v '\^{}' | sed 's|.*refs/tags/||' | grep -E '[0-9]+\.[0-9]+' | sort -V)
n=$(echo "$tags" | grep -c .)
[ "$n" -lt 2 ] && { echo "SKIP $name tags=$n"; exit 0; }
new=$(echo "$tags" | tail -1)
idx=$(( n>6 ? n-5 : 1 ))
old=$(echo "$tags" | sed -n "${idx}p")
timeout 120 git fetch -q --depth 1 origin "refs/tags/$new:refs/tags/authgap_new" "refs/tags/$old:refs/tags/authgap_old" 2>/dev/null || { echo "FETCHFAIL $name"; exit 0; }
echo "OK $name old=$old new=$new"
