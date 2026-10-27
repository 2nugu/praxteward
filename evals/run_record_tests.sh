#!/usr/bin/env bash
# Regression tests for scripts/check_records.py on a fixture project.
# Copies the fixture to a temp dir, initializes git, and runs positive and
# negative cases. Exit 1 if any case behaves unexpectedly.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; S="$HERE/../scripts/check_records.py"
BASE="$(mktemp -d)"; cp -r "$HERE/fixtures/sample-project/." "$BASE/fx"
( cd "$BASE/fx" && git init -q && git -c user.email=t@t -c user.name=t add -A && git -c user.email=t@t -c user.name=t commit -qm base )
fail=0
run(){ # name expected_exit mutation [args]
  rm -rf "$BASE/w"; cp -r "$BASE/fx" "$BASE/w"; ( cd "$BASE/w" && eval "$3" ) 
  out=$(cd "$BASE/w" && python3 "$S" . ${4:-} 2>&1); code=$?
  if [ "$code" = "$2" ]; then echo "PASS $1"; else echo "FAIL $1 (exit $code)"; echo "$out"; fail=1; fi; }
G='git -c user.email=t@t -c user.name=t'
run "valid records"                 0 ":"
run "vague verification"            1 "sed -i 's/^- \*\*Verification:\*\*.*/- **Verification:** tested/' docs/volumes/vol-01.md"
run "locator rot"                   1 "sed -i 's/RETRY_MAX/MAX_RETRIES/' src/scheduler.py"
run "unregistered volume"           1 "printf '# Vol 03\n' > docs/volumes/vol-03.md"
run "carried item not carried in"   1 "sed -i '/^- W-002 — retry policy/d' docs/volumes/vol-02.md"
run "open item without disposition" 1 "sed -i 's/- \[x\] persistence — deferred X-001/- [ ] persistence/' docs/volumes/vol-01.md"
run "locator without explanation"   1 "sed -i 's/  - \`src\/scheduler.py::RETRY_MAX\` — retry ceiling/  - \`src\/scheduler.py::RETRY_MAX\`/' docs/volumes/vol-01.md"
run "registry mismatch"             1 "sed -i 's/| W-001 | Job scheduler | done |/| W-001 | Job scheduler | active |/' docs/INDEX.md"
run "uncovered change"              1 "printf 'x=1\n' > src/new_mod.py; $G add -A; $G commit -qm c2" "--since HEAD~1"
run "uncovered change waived"       0 "printf 'x=1\n' > src/new_mod.py; echo '- no-record: src/new_mod.py — scratch' >> docs/LOG.md; $G add -A; $G commit -qm c2" "--since HEAD~1"
run "placeholder left in field"     1 "sed -i 's/^- \\*\\*How:\\*\\*.*/- **How:** <technique>/' docs/volumes/vol-01.md"
run "untracked new file"              1 "printf 'x=1\\n' > src/untracked.py" "--since HEAD"
run "duplicate ID in same file"       1 "printf '\\n### D-001 — dup\\n- **Context:** x\\n' >> docs/volumes/vol-02.md"
run "decision missing from index"     1 "sed -i '/^| D-001 /d' docs/INDEX.md"
run "superseded status documented way" 0 "sed -i 's/^- \\*\\*Status:\\*\\* done/- **Status:** superseded by W-002/' docs/volumes/vol-01.md; sed -i 's/| W-001 | Job scheduler | done |/| W-001 | Job scheduler | superseded by W-002 |/' docs/INDEX.md"
run "since last reconcile"            1 "sed -i \"s/^# Project Index/# Project Index\\nLast reconcile: \\$(git rev-parse HEAD)/\" docs/INDEX.md; printf 'x=1\\n' > src/new2.py; $G add -A; $G commit -qm c3" "--since last"
run "binary locator file exists"   0 "printf 'PK\\0\\0slides' > deck.pptx; python3 \"$HERE/add_locator.py\" docs/volumes/vol-01.md 'deck.pptx::slide 7' 'architecture slide'"
run "markdown heading anchor missing" 1 "printf '# Report\\n## Methods\\n' > report.md; python3 \"$HERE/add_locator.py\" docs/volumes/vol-01.md 'report.md::Results' 'results section'"
run "markdown heading anchor present" 0 "printf '# Report\\n## Results\\n' > report.md; python3 \"$HERE/add_locator.py\" docs/volumes/vol-01.md 'report.md::Results' 'results section'"
run "minimal records"                 0 "printf 'records: minimal\\nlog: docs/LOG.md\\n' > .praxteward.yaml"
rm -rf "$BASE"; exit $fail
