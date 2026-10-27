# Compile

Goal: one document that is the specification, the operator manual, and the project report, with every claim traceable to a record.

- P1. Run `python3 <skill-dir>/scripts/check_records.py <project-root>` and fix every error in the records first. Never repair gaps only in the final document.
- P2. Fix audience, scope, and output: which current F records and volumes are included, and where to write (default `docs/COMPILED.md`, Markdown, unless the operator names a path or format).
- P3. Specification: per feature, Intent, How, interfaces, constraints from D records; Locators as an appendix table.
- P4. Operator manual: Operation fields grouped by operator task (install, configure, run, inspect, recover); Limits as caveats.
- P5. Project report: per volume in order, phase objective, comparisons with results, decisions with alternatives and evidence, verification evidence, exit summary; then open deferred items.
- P6. Verify a sample of claims, and every numeric claim, against the code at their locators.
- P7. Pass the output checks. When subagents exist, give the document to a delegate with no prior context for review against those checks, and fix what it finds.
- P8. Tag each section with its source IDs (e.g. `[F-012, D-004]`) so the document can be regenerated.
