# Distill

Goal: turn waiting episodes into candidate cards or evidence for existing cards.

- S1. Read episode lines from `Last distill` onward, including that date; skip IDs in `Processed on last distill date`. If this optional field is absent, replay the boundary date and deduplicate against card Evidence and prior distillation entries. Stop without writing when no episodes remain.
- S2. Send `signal=check` episodes to the check they name per [practice](../references/practice.md). For each other episode, find what in the method produced the outcome, and separate it from favorable or unfavorable conditions. For a failure, name the failing layer (missing information, reasoning, tool use, evaluation) and the smallest rule or test that would have caught it.
- S3. Look up the indexes by task type and by cause → mechanism. If a card matches, add the episode to its Evidence (`<project>/<deliverable> — outcome — E-id`), or send the card to Evolve when the episode contradicts it. Do not create a near-duplicate.
- S4. Otherwise draft a candidate card from [CARD](../assets/templates/CARD.md) with kind method, craft, check, or automation.
- S5. Name the strongest simpler alternative; mark it `untested` unless the episode tried it.
- S6. Set scope to `project:<name>` unless the cause and mechanism hold outside this project; write the Transfer line in domain-neutral words.
- S7. Add new cards to the index as candidate with `review_by` about three months out and link the tally row. Set `Last distill` to today; retain the cumulative processed episode IDs dated today in `Processed on last distill date`, including episodes that yielded no card. Log the outcome and source locations.
