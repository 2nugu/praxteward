# Orient

Goal: know enough of intent and actual state to act, at the lowest reading cost.

- O1. Locate records via `.praxteward.yaml` or project conventions. If none exist, say so and offer to initialize from the templates.
- O2. Read the index header and the log's recovery summary. Nothing else yet.
- O3. Direct path: find the F records the task touches in the Feature registry; read those records and open code only at their locators.
- O4. Dependency path: from the index, collect decisions whose `invalidated_if` the task may trigger, deferred items in the affected area, and downstream acceptance criteria.
- O5. Spot-check the claims the task depends on against actual artifacts (code, tests, outputs). Records state intent; artifacts show state.
- O6. Write the state brief in 3–6 lines. Report contradictions between records and artifacts as findings, not fixes.

Light Orient: O2, O3, O6.
