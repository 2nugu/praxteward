# Trigger and depth cases

Run each in a fresh session with the skill installed. Record: activated (y/n), path (fast / mode), records read, approx. tokens. Log failures under `Routing notes`.

| # | Situation | Expected |
|---|---|---|
| 1 | "Continue the pipeline work from yesterday." | Recover (or Orient → Recover) |
| 2 | "Change the header color to #3C5CD8." (project with records) | Fast path even if loaded: no record reads, 1–2 line reply |
| 3 | "Rename `tmp` to `buffer` in utils.py." | No activation or fast path |
| 4 | "Should we replace the ingestion queue with streaming?" | Orient → Reason; decision note with reversal conditions |
| 5 | "Tests fail again after the same fix." | Execute → Reconcile (N6 failing-layer analysis) |
| 6 | "Milestone 3 is done; update the docs." | Reconcile |
| 7 | "What is the difference between TCP and UDP?" | No activation |
| 8 | "praxteward checkpoint" | Checkpoint (explicit) |
| 9 | Color change that turns out to be a shared design token used in 40 files | Starts fast, exits to gate (scope_spreads) |
| 10 | Delegate brief with mode=orient and missing pointers | Delegate returns `status: blocked` naming the missing input; writes no records |
| 11 | Workbench fires `pre_compaction` | Checkpoint; recovery summary overwritten, ≤15 lines |
| 12 | Three requests arrive in one message, one amending an earlier item | Intake: amendment linked, order stated, nothing dropped |
| 13 | New message mid-edit: "actually use blue, not green" | Applied after current step's verification as an amendment |
| 14 | "I'm going to sleep, keep going." (no scope given) | Intake → Advance with a derived conservative charter stated in the report |
| 15 | During Advance, an item requires a schema migration on production data | Parked with options and recommendation; Advance continues with independent items |
| 16 | Queue empties with budget left | Lookahead: ≤3 ranked proposals; executes only charter-covered ones |
| 17 | Two queued requests conflict | Both kept, conflict flagged, independent work proceeds |
| 18 | Feature finished and tests pass | F record written in the same step (How, Alternatives, Rationale, Verification with command/result, Locators with explanations, Operation, Limits); registry updated; `check_records.py` passes |
| 19 | Milestone closes; volume has open items | Volume closed with exit summary; each item carried/deferred/dropped; next volume lists Carried in |
| 20 | Fast-path rename of a symbol cited by a locator | Locator fixed in the same change; no other record work |
| 21 | "Write the final spec and manual" | Compile: checker first, gaps fixed in records, sections tagged with source IDs |

Structural record checks are automated: `bash evals/run_record_tests.sh` (10 cases).
| 22 | "praxteward inspect docs/" | Ranked findings from check_records and tell_scan; no edits |
| 23 | "Write the milestone report" | Report passes tell_scan; ratings recorded in the log, not in the report |
| 24 | Feature finished in code | No narration comments or swallowed exceptions in the diff; tell_scan clean on changed files |
