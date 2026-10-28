#!/usr/bin/env bash
# Regression tests for scripts/contrast.py.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; S="$HERE/../scripts/contrast.py"; fail=0
expect(){ want=$1; pat=$2; shift 2; out=$(python3 "$S" "$@" 2>&1); code=$?
  if [ "$code" = "$want" ] && echo "$out" | grep -q -- "$pat"; then echo "PASS $*"; else echo "FAIL $* (exit $code)"; echo "$out"; fail=1; fi; }
expect 0 "21.00:1" "#000" "#fff"
expect 1 "4.48:1" 777777 ffffff
expect 0 "4.54:1" 767676 ffffff
expect 0 "4.48:1" 777777 ffffff --min 3
expect 0 "AA" "#fff" "#0055cc"
expect 1 "deutan.*too close" --distinct d62728 2ca02c 1f77b4
expect 0 "normal" --distinct 000000 ffffff
expect 2 "not a hex color" zz fff
expect 2 "pairs" 000 fff 111
expect 2 "at least two" --distinct 000
r=$(python3 -c "import sys; sys.path.insert(0,'$HERE/../scripts'); import contrast as c; print(round(c.de2000((50,2.6772,-79.7751),(50,0,-82.7485)),4), round(c.de2000((50,2.5,0),(73,25,-18)),4))")
[ "$r" = "2.0425 27.1492" ] && echo "PASS CIEDE2000 reference pairs" || { echo "FAIL CIEDE2000 $r"; fail=1; }
exit $fail
