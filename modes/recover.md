# Recover

Goal: resume from the last verified point without repeating non-idempotent actions.

- V1. Read the recovery summary and the latest log entries only.
- V2. Inspect actual artifacts (working tree, outputs, test results) and classify each recorded in-flight action as completed, partially applied, not started, or unknown.
- V3. Re-run only the checks needed to establish consistency. Treat unconfirmed persistence, tests, and side effects as unknown, not done.
- V4. Choose the latest verified resume point. Irreversible recovery steps need operator approval.
- V5. When taking over another agent's work, adopt its records, not its conclusions; re-verify the claims you depend on.
- V6. Update the recovery summary to the confirmed state, then continue in the appropriate mode.
