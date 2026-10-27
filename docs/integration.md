# Integration guide

For operators and workbench builders. Not part of the installed skill.

Skill selection by description is probabilistic. Anything a host can detect without judgment (session start, compaction, test failure, milestone, operator away) should be routed by the host. `contract.json` lists these events and the mode each runs.

## Integration levels

| Level | Host | What it adds |
|---|---|---|
| 0 | Any skill-capable agent | Description matching, plus `praxteward <mode>` typed by the operator |
| 1 | Hosts with lifecycle hooks | Session-start and pre-compaction hooks inject a short routing line and the recovery summary |
| 2 | Custom workbench | Event routing from `contract.json`, delegate briefs, report validation, queue and wake-up ownership |

## Activation policy

Set `activation` in the project's `.praxteward.yaml`.

| Policy | Cost | Miss risk | Fits |
|---|---|---|---|
| auto | ~100 tokens per session for metadata; body only when matched | The skill may not load when a project-state check was needed | Occasional project work |
| session | Body (~1.6k tokens) once per session in projects with records | Lowest | Long-running projects, heavy agent use, workbenches |
| explicit | Metadata only | Highest | Full manual control |

`session` loads once per session, not per task; the fast path keeps trivial tasks short. Implement it with the hook below or with one line in the global instructions (see README).

## Level 1: Claude Code hooks (`.claude/settings.json`)

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command",
      "command": "test -f .praxteward.yaml || exit 0; LOG=$(sed -n 's/^log: *//p' .praxteward.yaml | head -1 | tr -d '\"'); LOG=${LOG:-docs/LOG.md}; if grep -q '^activation: *session' .praxteward.yaml; then echo 'Load the praxteward skill now (once for this session). Use its fast path for trivial tasks.'; else echo 'This project keeps praxteward records. Load the skill if the task needs project state.'; fi; test -f \"$LOG\" && sed -n '/^## Recovery summary/,/^## Entries/p' \"$LOG\" | head -20" }] }],
    "PreCompact": [{ "hooks": [{ "type": "command",
      "command": "test -f .praxteward.yaml && echo 'Before compaction: run praxteward checkpoint.' || true" }] }]
  }
}
```

Other hosts: use their lifecycle hooks; Codex requires approving hooks via `/hooks`.

## Level 2: workbench responsibilities

1. Route: map events to modes per `contract.json`; on an event, load `SKILL.md` and only that mode's procedure.
2. Delegate: fill `assets/templates/BRIEF.md` with file pointers, not content; set `role: delegate`.
3. Validate: reject reports missing `report.required` fields or claiming `done` with empty `evidence`.
4. Own records: only the coordinator, or the workbench on its behalf, writes the index and log.
5. Queue: append every incoming operator message to the queue file before the model sees it, so mid-task messages survive compaction.
6. Wake: for `operator_away`, schedule resumptions that re-enter Advance from the recovery summary and queue; enforce the charter's budget and stop predicates outside the model.
7. Learn: collect routing misses and false positives from the log's `Routing notes` and adjust the description or hooks from repeated patterns.

## Limits of prompting

Crash-safe recovery needs durable snapshots, transaction boundaries, and idempotent tools in the host. The skill records state and refuses to treat unverified side effects as complete; it cannot make them atomic.
