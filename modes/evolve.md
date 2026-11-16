# Evolve

Goal: keep each card true to current conditions, and prefer cheaper ways that reach the same outcome.

- Y1. Take only cards that are due (`check_practice.py` lists them), contradicted by an episode, or flagged by Plan.
- Y2. Re-check the assumptions the trigger touches, using each assumption's own check.
- Y3. Inspect source episodes and check results before comparing outcomes, rework, and corrections across project/deliverable pairs. Ask whether success came from the method or its conditions, and inspect the simpler-alternative result. Unavailable evidence prevents promotion; leave a specific evidence gap.
- Y4. Decide one action: promote (thresholds in [practice](../references/practice.md)), keep and move `review_by`, revise (raise the version, add a History line), narrow (add to Not when), or deprecate (History reason and Replacement).
- Y5. When another task type shares the card's cause and conditions, add it to Applies when only after one trial there succeeds.
- Y6. Update the card and the index row; log the decision with its evidence.
