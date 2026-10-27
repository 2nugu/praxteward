# Intake

Goal: no request is lost, merged wrongly, or executed out of order. Not needed for a single request.

- I1. Record each request in the queue (or a persistent task list) with near-verbatim text, time, and source. A batch of fast-path items needs only a one-line list.
- I2. Relate each to in-flight and queued items: amends, supersedes, duplicate, depends_on, or independent. Superseded items stay, with a pointer.
- I3. Apply amendments to the current item at the next safe point, after its current step is verified.
- I4. Assign each item the fast path or a mode, with a depth (SKILL.md Depth and allocation). Mark items needing an operator decision `needs_decision` with the question.
- I5. Order: amendments and blockers, then dependencies, then highest value per effort; batch fast-path items. For conflicting requests, keep both, flag the conflict, and proceed with independent work.
- I6. Acknowledge briefly what was queued and in what order; ask only about real conflicts.
