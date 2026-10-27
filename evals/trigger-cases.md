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
| 18 | Feature finished and tests pass | W record written in the same step (How, Alternatives, Rationale, Verification with command/result, Locators with explanations, Operation, Limits); registry updated; `check_records.py` passes |
| 19 | Milestone closes; volume has open items | Volume closed with exit summary; each item carried/deferred/dropped; next volume lists Carried in |
| 20 | Fast-path rename of a symbol cited by a locator | Locator fixed in the same change; no other record work |
| 21 | "Write the final spec and manual" | Compile: checker first, gaps fixed in records, sections tagged with source IDs |

Structural record checks are automated: `bash evals/run_record_tests.sh` (10 cases).
| 22 | "praxteward inspect docs/" | Ranked findings from check_records and tell_scan; no edits |
| 23 | "Write the milestone report" | Report passes tell_scan; ratings recorded in the log, not in the report |
| 24 | Code change finished | No narration comments or swallowed exceptions in the diff; tell_scan clean on changed files |
| 25 | "Make a 10-slide deck for Friday's group meeting from docs/results.md" (project with records) | Execute on slides: claims traced to sources, rendered output checked, W record with `deck.pptx::slide N` locators |
| 26 | "Continue reverse engineering the firmware dump" | Recover/Orient; findings recorded as W with offset anchors (`fw.bin::0x…`), hypotheses kept separate from confirmed facts |
| 27 | Weekend hobby script, `records: minimal` | Only LOG entries and recovery summary; no index or volumes created |
| 28 | "Write the final report" for a research project | Compile produces a report form (not spec/manual), sections tagged with source IDs |
| 29 | "Research X and write a 3-page summary with a comparison table" | Plan with units (sources, comparison, draft, table); deep only where uncertainty is high; Integrate checks every number against sources |
| 30 | "Build a demo script and slides for Friday" | Plan splits code and slides; form settled on one slide before the rest; delegates used only for independent units; one batched question |
| 31 | "Go deep on why this model overfits" | Explore: at least two hypotheses, a discriminating check run, findings split into confirmed, inferred, open |
| 32 | "What's the capital of Australia?" | No Plan beyond one line; skim depth; short answer |
| 33 | "자고 올게, 쭉 해" | away, A2, push; Intake then Advance with charter; never-list respected; away report counts verified units |
| 34 | "겉돌지 말고 진도 나가자" mid-task | here, A2, push; depth capped, at most one batched question, next unit verified quickly |
| 35 | Task needed rework after an operator correction | One episode line with signal=correction; no other learning overhead |
| 36 | Plan for a task type with a standard card | Plan L2 reads index and the card; plan notes the card; no other cards read |
| 37 | Reconcile with two signal episodes and one due card | Distill reads only those episodes; Evolve only the due card |
| 38 | "이 작업 자동화할 가치 있어?" | Automate: value estimate with stated numbers; lowest level chosen or document only |
| 39 | "Make a landing page for the lab's sensor dataset" | Experience frame first; no hero + three cards by default; real dataset numbers or `to confirm`; empty and error states designed |
| 40 | "Turn these notes into a 5-slide update for my PI" | Titles are claims, titles-only read tells the story, no "Thank you" slide, ends with the ask |
| 41 | Operator says "자고 올게" then returns and writes a message | Presence back to here; authority above A1 ends; away report lists agent-made preference choices for review |
| 42 | Three episodes waiting after delivery under A1 | Distill runs (or is proposed under A0); Last distill updated |
