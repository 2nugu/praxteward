#!/usr/bin/env bash
# Regression tests for scripts/check_practice.py on a fixture practice directory.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; S="$HERE/../scripts/check_practice.py"
BASE="$(mktemp -d)"; fail=0
run(){ # name expected_exit grep_pattern mutation
  rm -rf "$BASE/p"; cp -r "$HERE/fixtures/practice" "$BASE/p"; ( cd "$BASE/p" && eval "$4" )
  out=$(python3 "$S" "$BASE/p" --today 2026-10-27 2>&1); code=$?
  if [ "$code" = "$2" ] && echo "$out" | grep -q "$3"; then echo "PASS $1"; else echo "FAIL $1 (exit $code)"; echo "$out"; fail=1; fi; }
run "valid library, one due"         0 "DUE P-002"  ":"
run "standard with one context"      1 "2+ distinct" "sed -i '/farm\/sensor-archive/d' cards/P-001.md"
run "assumption without check"       1 "every assumption" "sed -i 's/ — measure from production logs monthly//' cards/P-001.md"
run "placeholder left"               1 "placeholder" "sed -i 's/^- \*\*Objective:\*\*.*/- **Objective:** <outcomes>/' cards/P-002.md"
run "index status mismatch"          1 "INDEX Status" "sed -i 's/| P-002 | Slide deck from findings | candidate |/| P-002 | Slide deck from findings | trial |/' INDEX.md"
run "card missing from index"        1 "not in INDEX" "sed -i '/^| P-002 /d' INDEX.md"
run "standard with untested simpler" 1 "simpler alternative" "sed -i 's/^- \*\*Simpler alternative:\*\*.*/- **Simpler alternative:** keep SQLite — untested/' cards/P-001.md"
run "deprecated without replacement" 1 "Replacement field" "sed -i 's/^- \*\*Status:\*\* candidate/- **Status:** deprecated/' cards/P-002.md; sed -i 's/| P-002 | Slide deck from findings | candidate |/| P-002 | Slide deck from findings | deprecated |/' INDEX.md"
run "transfer missing a stage"       1 "Transfer must" "sed -i 's/^- \*\*Transfer:\*\*.*/- **Transfer:** cause → mechanism/' cards/P-002.md"
run "two misses flag review"         0 "2 missed" "sed -i 's/telemetry-store — met/telemetry-store — missed/; s/sensor-archive — met/sensor-archive — missed/' cards/P-001.md; sed -i 's/^- \*\*Status:\*\* standard/- **Status:** trial/' cards/P-001.md; sed -i 's/| P-001 | Data store selection | standard |/| P-001 | Data store selection | trial |/' INDEX.md"
run "same deliverable twice"        1 "2+ distinct" "sed -i 's|farm/sensor-archive — met|robot/telemetry-store — met|' cards/P-001.md"
run "trial with one evidence line"   1 "trial needs" "sed -i 's/^- \\*\\*Status:\\*\\* candidate/- **Status:** trial/' cards/P-002.md; sed -i 's/| candidate | craft |/| trial | craft |/' INDEX.md"
run "invalid review date"            1 "not a valid date" "sed -i 's/review_by: 2027-04-30/review_by: 2027-02-30/' cards/P-001.md; sed -i 's/| 2027-04-30 |/| 2027-02-30 |/' INDEX.md"
run "index review-by mismatch"       1 "INDEX Review by" "sed -i 's/| 2027-04-30 |/| 2027-05-30 |/' INDEX.md"
run "evidence without episode id"    1 "Evidence lines" "sed -i 's/ — E-lab-20260810-1/ — lab log/' cards/P-002.md"
run "comparison text is not a placeholder" 0 "OK" "sed -i 's/^- \\*\\*Decision factors:\\*\\*.*/- **Decision factors:** latency a < b > c in tests; List<int> payloads/' cards/P-001.md"
run "missing last distill"           1 "Last distill" "sed -i '/^Last distill/d' INDEX.md"
rm -rf "$BASE"; exit $fail
