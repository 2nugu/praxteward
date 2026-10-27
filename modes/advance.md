# Advance

Goal: advance the queue and roadmap while the operator is away, then hand back a decision-ready report.

- A1. Set the charter: objective, authorized scope, stop predicates (queue empty, budget, time, failure threshold), and what must never happen unattended. Without one from the operator, derive a conservative charter from the queue and current authority and state it at the top of the report.
- A2. Checkpoint.
- A3. Loop: take the next ready item, run its path (fast or mode), verify, update its queue status, and checkpoint after each completed item.
- A4. Park items that need a decision, are irreversible, or fall outside scope: record options, evidence, and a recommendation, then continue with the next independent item. Never wait idle and never exceed the charter.
- A5. Stop an item after the same failure twice; record the failing layer and continue with others.
- A6. When the queue is exhausted and budget remains, rank up to three next actions by expected value (unblocked roadmap items, `done` without evidence, deferred items now due, record drift) and execute only those the charter covers.
- A7. On a stop predicate, checkpoint and write the away report from [AWAY-REPORT](../assets/templates/AWAY-REPORT.md); it passes the output checks.

If the host supports scheduled resumption, schedule a check-in rather than ending long unattended work in one turn.
