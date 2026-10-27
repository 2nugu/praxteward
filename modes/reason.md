# Reason

Goal: a decision that serves the program outcome and states what would reverse it. Use the least investigation that settles the consequential question.

- R1. Restate the program outcome, the operator's actual workflow, and the acceptance criteria the decision serves.
- R2. Check that the request targets the causal bottleneck, not a convenient symptom.
- R3. Review prior decisions, temporary solutions, and deferred items in the area, and whether their assumptions still hold. Raise unrecorded gaps only with evidence from code or behavior.
- R4. Classify each open fork: empirical, preference, or consequential (SKILL.md Gate).
- R5. Generate options, including keep, change, and replace. Trace each as `deficiency → mechanism → approach → constraints → discriminating check`. Look into adjacent domains when the mechanism warrants it; prefer primary sources; record provenance and limits; keep facts, inferences, and hypotheses separate.
- R6. Apply only the lenses that could change the choice: **purpose** (advances the outcome or only a local task?), **operator** (can a person inspect, run, and recover it?), **engineering** (interfaces, invariants, data flow, maintainability), **adversarial** (which premise or counterexample breaks it?). For a high-stakes choice, one unanchored delegate or a different-model second opinion is allowed.
- R7. Run the cheapest discriminating check for empirical forks; ask the operator once for preference forks; propose and wait on consequential ones.
- R8. Global check: contradictions with accepted constraints, unnecessary scope, hidden operator friction, a cheaper valid option. Report only findings that change the decision.
- R9. Write the D record (options including keep-current, evidence, `invalidated_if`, affected F-IDs) and any C note with measured results into the active volume; add the decision row to the index.
