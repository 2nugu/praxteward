# Automate

Goal: automate only where it pays, at the lowest level that captures the value.

- M1. Consider a standard card, a stable recurring task type, or an explicit operator request. Otherwise stop.
- M2. Estimate value over the card's review period: `V = N × (C_manual − C_auto) − C_build − C_maint − E[C_failure]`, with N from the task-type tally. Count operator attention (reviews, answers) as cost alongside time and compute. Use conservative numbers and state them. Without a tally, apply the fallback rule in [practice](../references/practice.md).
- M3. Rate determinism of inputs and outputs, how often requirements change, whether results can be checked automatically, failure cost, and how easily a failure is undone.
- M4. Pick the lowest level that captures most of V: documented steps, checklist, decision rule, script, agent workflow. Add an operator approval gate where checks are weak or failures costly. If V is near zero, document only.
- M5. Build it with its own check: asserted outputs, a dry-run mode, and a rollback path where state changes.
- M6. When failure cost is not trivial, run it once alongside the manual way and compare before relying on it.
- M7. Record the level, location, and check in the card's Automation field; add review triggers for scale changes and repeated failures. Without authority to build, deliver this as a proposal with the estimate.
