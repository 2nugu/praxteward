# Execute

Goal: one unit produced, with evidence that it meets its check, and a record that makes re-reading unnecessary. Units may be code, documents, slides, data, or analyses.

- E1. Fix acceptance criteria before editing: behavior and data integrity for code, accuracy and fit to the experience frame for documents and slides, reproducibility for analyses. Apply the artifact rules in [craft](../references/craft.md) for the unit's type.
- E2. List the files to modify, create, or delete, and the affected interfaces, invariants, and deferred items. Trace callers, consumers, tests, fixtures, configuration, and exports as applicable; include required updates in the unit. Propose, do not perform, out-of-scope effects.
- E3. Run Checkpoint first if the operation is long, risky, or non-idempotent.
- E4. Apply solution selection and the Code rules in craft. Fix demonstrated causes at their appropriate owner; remove superseded paths within scope rather than leaving parallel implementations. Preserve interfaces unless a recorded decision justifies changing them.
- E5. Verify on the real artifact, with checks proportional to the change: reproduce-then-pass for fixes, before/after measurements for improvements, literal expected values in tests, every factual claim and number traced to its source in documents, rendered output for slides and figures, and re-run results for analyses. Changed non-trivial logic needs a focused check that would detect the relevant wrong behavior; use an existing test when it covers that behavior. Trivial edits need no new test. A tool's success message is not evidence.
- E6. Review any delegated work yourself.
- E7. With verification, update the existing W and registry (standard records), or the log (minimal); create a W only for a distinct work unit. Record what was removed or consolidated and why any new structure is necessary in Rationale. Put shortcut limits and revisit triggers in Limits or the log. When records do not apply, convey these facts in the reply.
- E8. Pass the output checks on changed code, documents, and records, then report checks run, observed results, and untested boundaries. Increment the task-type tally and add an episode line if a signal fired ([practice](../references/practice.md)).
