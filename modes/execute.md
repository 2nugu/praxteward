# Execute

Goal: one unit produced, with evidence that it meets its check, and a record that makes re-reading unnecessary. Units may be code, documents, slides, data, or analyses.

- E1. Fix acceptance criteria before editing: behavior and data integrity for code, accuracy and fit to the experience frame for documents and slides, reproducibility for analyses. Apply the artifact rules in [craft](../references/craft.md) for the unit's type.
- E2. List the files to modify, create, or delete, and the affected interfaces, invariants, and deferred items. Propose, do not perform, out-of-scope effects.
- E3. Run Checkpoint first if the operation is long, risky, or non-idempotent.
- E4. Implement the smallest coherent change. Preserve existing interfaces unless a D record justifies otherwise.
- E5. Verify on the real artifact, with checks proportional to the change: reproduce-then-pass for fixes, before/after measurements for improvements, literal expected values in tests, every factual claim and number traced to its source in documents, rendered output for slides and figures, and re-run results for analyses. A tool's success message is not evidence.
- E6. Review any delegated work yourself.
- E7. In the same step as verification, write or update the W record per [records](../references/records.md) and update the Work registry (standard records), or add a log entry (minimal records). When no records apply, report the same facts in the reply. Work without its record is not done.
- E8. Pass the output checks on changed code, documents, and records, then report checks run, observed results, and untested boundaries. Increment the task-type tally and add an episode line if a signal fired ([practice](../references/practice.md)).
