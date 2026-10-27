# Checkpoint

Goal: another session, model, or agent can resume without this context.

- K1. Overwrite, do not append, the log's recovery summary: objective and scope, last verified state with evidence reference, in-flight partial changes with paths, blockers and unknowns, next safe action and the checks to run first.
- K2. Point to durable evidence (commit, file, test output), not prose assertions.
- K3. Mark every unconfirmed side effect `unknown`.
- K4. If a versioned snapshot is available and authorized, create it and record its reference. Without one, assume a crash can leave in-flight side effects partially applied.
- K5. Keep the summary under about 15 lines; details belong in log entries.
