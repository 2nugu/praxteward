# Reconcile

Goal: records and plan match reality, and the ways of working improve.

- N1. For standard records, run `python3 <skill-dir>/scripts/check_records.py <project-root> --since last` (omit `--since` outside git) and resolve every error: add records, fix locators, or log `no-record: <path> — <reason>`.
- N2. Compare roadmap and acceptance criteria against actual artifacts for the milestone or affected area, and spot-check at least one record's How and Locators against the artifacts.
- N3. For each divergence, state evidence, impact, and whether intent or implementation should change. Supersede decisions with new D records; never rewrite history.
- N4. Re-examine deferred and temporary items whose revisit conditions may now hold. Do not turn vague possibilities into tasks.
- N5. Run Distill on episodes with signals since the last run.
- N6. Run `python3 <skill-dir>/scripts/check_practice.py <practice-dir>` and run Evolve on the cards it lists as due, plus cards whose review triggers this milestone fired.
- N7. If the phase is complete or the volume can no longer be oriented from its header and exit summary, close it and open the next one per the volume rules in [records](../references/records.md). Compact redundant notes without destroying unique evidence. Without write authority, return proposed deltas.
- N8. Review routing notes and Automate candidates among standard cards, then rank up to three next actions by expected value (unblocked roadmap items, `done` without evidence, deferred items now due, record drift). Propose them; execute only under a charter or approval. Set the index's `Last reconcile:` to the current commit.
