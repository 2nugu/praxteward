#!/usr/bin/env bash
# Regression tests for ko_scan.py, debt_scan.py, deal.py, and page_check.py.
# Windows: python3 may be the Store stub; fall back to python.
python3 -c "" >/dev/null 2>&1 || { python3(){ python "$@"; }; export -f python3; }
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; SC="$HERE/../scripts"; fail=0
T="$(mktemp -d)"
check(){ # name expected_exit pattern command...
  name="$1"; want="$2"; pat="$3"; shift 3
  out=$("$@" 2>&1); code=$?
  if [ "$code" = "$want" ] && echo "$out" | grep -q -- "$pat"; then echo "PASS $name"; else echo "FAIL $name (exit $code)"; echo "$out"; fail=1; fi; }
check "ko: S1 stock phrase"       1 "S1 D-2"        python3 "$SC/ko_scan.py" "$HERE/tells/korean_bad.md"
check "ko: translationese"        1 "S2 A-3"        python3 "$SC/ko_scan.py" "$HERE/tells/korean_bad.md"
check "ko: agent passive"         1 "A-9"           python3 "$SC/ko_scan.py" "$HERE/tells/korean_bad.md"
check "ko: comma density"         0 "S3 C-11"       python3 "$SC/ko_scan.py" "$HERE/tells/korean_density.md"
check "ko: generative tells"      1 "S1 K-23"       python3 "$SC/ko_scan.py" "$HERE/tells/korean_genai.md"
check "ko: closing offer"         1 "S1 K-25"       python3 "$SC/ko_scan.py" "$HERE/tells/korean_genai.md"
check "ko: aphoristic close"      1 "K-21"          python3 "$SC/ko_scan.py" "$HERE/tells/korean_genai.md"
check "ko: mixed polite levels"   1 "E-7b"          python3 "$SC/ko_scan.py" "$HERE/tells/korean_genai.md"
check "ko: bold labels"           1 "K-31"          python3 "$SC/ko_scan.py" "$HERE/tells/korean_genai.md"
check "ko: genre legal keeps hedges" 0 "genre legal" python3 "$SC/ko_scan.py" "$HERE/tells/korean_legal.md" --genre legal
check "ko: hedges flagged in general" 0 "G-2"     python3 "$SC/ko_scan.py" "$HERE/tells/korean_legal.md"
check "ko: fiction keeps 그녀"    0 "genre fiction" python3 "$SC/ko_scan.py" "$HERE/tells/korean_fiction.md" --genre fiction
check "ko: 그녀 flagged in general" 1 "S1 A-16a"  python3 "$SC/ko_scan.py" "$HERE/tells/korean_fiction.md"
check "ko: clean text"            0 "route light"   python3 "$SC/ko_scan.py" "$HERE/tells/korean_clean.md"
check "ko: light revision A"      0 "grade: A"      python3 "$SC/ko_scan.py" "$HERE/tells/revise_light.md" --base "$HERE/tells/revise_base.md"
check "ko: heavy revision D"      1 "grade: D"      python3 "$SC/ko_scan.py" "$HERE/tells/revise_heavy.md" --base "$HERE/tells/revise_base.md"
check "ko: lost number caught"    1 "numbers lost \['4'\]" python3 "$SC/ko_scan.py" "$HERE/tells/revise_numbers.md" --base "$HERE/tells/revise_base.md"
check "ko: length target"         1 "outside 5%"    python3 "$SC/ko_scan.py" "$HERE/tells/revise_base.md" --length 200
check "ko: slides keeps labels"    0 "route light, genre slides" python3 "$SC/ko_scan.py" "$HERE/tells/korean_slides.md" --genre slides
check "ko: labels flagged in general" 0 "K-31"      python3 "$SC/ko_scan.py" "$HERE/tells/korean_slides.md"
check "ko: json output"           0 '"route"'       python3 "$SC/ko_scan.py" "$HERE/tells/korean_clean.md" --json
check "ko: voice compare"         0 "sample level polite" python3 "$SC/ko_scan.py" "$HERE/tells/korean_clean.md" --voice "$HERE/tells/revise_base.md"
check "debt: ledger"              0 "2 shortcuts, 1 without" python3 "$SC/debt_scan.py" "$HERE/debt"
check "debt: strict"              1 "MISSING"       python3 "$SC/debt_scan.py" "$HERE/debt" --strict
check "deal: place has no effects" 0 "effects allowed: no" python3 "$SC/deal.py" --kind place --history "$T/h.json"
first=$(python3 "$SC/deal.py" --kind place --history "$T/h.json" | grep '^palette'); second=$(python3 "$SC/deal.py" --kind place --history "$T/h.json" | grep '^palette')
if [ "$first" != "$second" ]; then echo "PASS deal: rotates palettes"; else echo "FAIL deal: same palette twice ($first)"; fail=1; fi
check "deal: korean type"         0 "KR"            python3 "$SC/deal.py" --kind software --lang ko --history "$T/k.json"
check "deal: bad kind"            2 "Usage"         python3 "$SC/deal.py" --kind blog
check "page: good page passes"    0 "OK: 0 fail"    python3 "$SC/page_check.py" "$HERE/web/good.html" --kind place
for rule in "FAIL viewport" "FAIL no placeholder" "FAIL every image has alt" "FAIL no captions" "FAIL no violet" "FAIL nothing animates on scroll" "FAIL no WebGL" "FAIL reduced motion" "WARN at most two hero actions" "WARN contacts generic" "FAIL token contrast"; do
  check "page: bad page $rule" 1 "$rule" python3 "$SC/page_check.py" "$HERE/web/bad.html" --kind place
done
check "page: webgl allowed on tech" 1 "PASS at most 4 live WebGL" python3 "$SC/page_check.py" "$HERE/web/bad.html" --kind tech
check "page: starter markers fail" 1 "FAIL no placeholder" python3 "$SC/page_check.py" "$HERE/../assets/web/starter.html" --kind software
rm -rf "$T"
exit $fail
