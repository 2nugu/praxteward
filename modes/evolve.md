# Evolve

Goal: keep each card true to current conditions, and prefer cheaper ways that reach the same outcome.

- Y1. Take only cards that are due (`check_practice.py` lists them), contradicted by an episode, or flagged by Plan.
- Y2. Re-check the assumptions the trigger touches, using each assumption's own check.
- Y3. Compare the card's evidence across project/deliverable pairs: outcome, rework, corrections. Ask whether the successes came from the card or from conditions, and what the simpler-alternative trials showed.
- Y4. Decide one action: promote (thresholds in [practice](../references/practice.md)), keep and move `review_by`, revise (raise the version, add a History line), narrow (add to Not when), or deprecate (History reason and Replacement).
- Y5. When another task type shares the card's cause and conditions, add it to Applies when only after one trial there succeeds.
- Y6. Update the card and the index row; log the decision with its evidence.
