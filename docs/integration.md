# Integration guide

Not part of the installed skill.

Skill selection by description is probabilistic. What a host can detect without judgment (session start, compaction) is better routed by a hook; the events and the mode each one runs are listed in `SKILL.md` under Invocation and fallbacks.

## Activation policy

Set `activation` in the project's `.praxteward.yaml`.

| Policy | Cost | Miss risk | Fits |
|---|---|---|---|
| auto | ~250 tokens per session for metadata; body only when matched | The skill may not load when a project-state check was needed | Occasional project work |
| session | Body (~3.7k tokens) once per session in projects with records | Lowest | Long-running projects, heavy agent use |
| explicit | Metadata only | Highest | Full manual control |

`session` loads once per session, not per task; the fast path keeps trivial tasks short. Implement it with the hook below or with one line in the global instructions (see README).

## Claude Code hooks (`.claude/settings.json`)

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

## Limits of prompting

Crash-safe recovery needs durable snapshots, transaction boundaries, and idempotent tools in the host. The skill records state and refuses to treat unverified side effects as complete; it cannot make them atomic.
