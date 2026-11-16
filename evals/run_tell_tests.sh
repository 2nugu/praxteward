#!/usr/bin/env bash
# Regression tests for scripts/tell_scan.py.
# Windows: python3 may be the Store stub; fall back to python.
python3 -c "" >/dev/null 2>&1 || { python3(){ python "$@"; }; export -f python3; }
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; S="$HERE/../scripts/tell_scan.py"; fail=0
expect(){ out=$(python3 "$S" "$HERE/tells/$2" 2>&1); code=$?
  if [ "$code" = "$1" ] && { [ -z "${3:-}" ] || echo "$out" | grep -q "$3"; }; then echo "PASS $2"; else echo "FAIL $2 (exit $code)"; echo "$out"; fail=1; fi; }
expect 1 bad.md "T10.*T11\|T11"
expect 1 bad.md "T01"
expect 1 bad.md "T02"
expect 1 bad.md "T13"
expect 1 bad.md "T16"
expect 0 clean.md
expect 0 override.md
expect 1 bad_code.py "T20"
expect 1 bad_code.py "T21"
expect 0 fp.md
expect 1 noreason.md "T11"
expect 1 blockinline.md "T01"
expect 1 comma.md "T13"
expect 1 bad_code.js "T21"
expect 1 bad_code.js "T24"
expect 0 bom.md
T=$(mktemp -d); printf 'caf\351 TODO\n' > "$T/latin1.md"  # non-UTF-8 input, made here so the repo holds text only
out=$(python3 "$S" "$T/latin1.md" 2>&1); code=$?; rm -rf "$T"
if [ "$code" = 2 ] && echo "$out" | grep -q "not UTF-8"; then echo "PASS latin1.md"; else echo "FAIL latin1.md (exit $code)"; echo "$out"; fail=1; fi
expect 2 missing.md "not found"
expect 1 korean_bad.md "T30"
expect 1 korean_bad.md "T31"
expect 1 korean_density.md "T32"
expect 1 korean_density.md "T33"
expect 0 korean_clean.md
base(){ out=$(python3 "$S" "$HERE/tells/$2" --base "$HERE/tells/revise_base.md" 2>&1); code=$?
  if [ "$code" = "$1" ] && echo "$out" | grep -q "$3"; then echo "PASS $2 vs base"; else echo "FAIL $2 vs base (exit $code)"; echo "$out"; fail=1; fi; }
base 0 revise_light.md "(OK;"
base 1 revise_heavy.md "(STOP;"
exit $fail
