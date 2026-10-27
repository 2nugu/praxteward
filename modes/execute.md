# Execute

Goal: an authorized change with evidence that the intended outcome holds, and a record that makes re-reading unnecessary.

- E1. Fix behavioral and data-integrity acceptance criteria before editing.
- E2. List the files to modify, create, or delete, and the affected interfaces, invariants, and deferred items. Propose, do not perform, out-of-scope effects.
- E3. Run Checkpoint first if the operation is long, risky, or non-idempotent.
- E4. Implement the smallest coherent change. Preserve existing interfaces unless a D record justifies otherwise.
- E5. Verify on the real artifact, with checks proportional to the change: reproduce-then-pass for fixes, before/after measurements for improvements, assertions on literal expected values, and compatibility and failure behavior where relevant. Compilation or a tool's success message is not evidence.
- E6. Review any delegated work yourself.
- E7. In the same step as verification, write or update the F record per [records](../references/records.md) and update the Feature registry. A feature without a complete record is not done.
- E8. Pass the output checks on changed code and records, then report checks run, observed results, and untested boundaries.
