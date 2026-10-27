#!/usr/bin/env bash
# Regression tests for scripts/tell_scan.py.
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
expect 2 latin1.md "not UTF-8"
expect 2 missing.md "not found"
exit $fail
