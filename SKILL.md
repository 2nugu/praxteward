---
name: praxteward
description: Maintain intent, architectural decisions, roadmap, verified progress, and recoverable continuity in long-running software or research projects. Use when orienting to or resuming a project, planning consequential changes, investigating project-specific blind spots, reconciling deferred decisions, reviewing milestones, checkpointing, managing queued or unattended work, or maintaining and compiling project documents and logs. Skip unrelated conversation; trivial edits take a fast path. Explicit use, e.g. "praxteward recover".
---

# Praxteward

Keep a project's intent, actual state, and verified progress coherent across sessions, models, subagents, and hosts. Tool names are capabilities, not product APIs. Unless the host's instructions already set judgment principles, also apply [principles](references/principles.md).

## 0. Fast path (check first)

If the task is local, reversible, and fully specified (change a color, rename a variable, fix a typo, answer a question about one file), do it directly:

- Read only the file being changed. Do not read records, copy procedure steps, delegate, or emit the Report block.
- Verify only what the change can break (the value renders, the file still parses).
- Touch records only to fix a locator the change broke, or to flag in one line that the change contradicts a recorded decision already in context.
- Reply in one or two lines. Batch several pending fast items with a one-line list. Block-level output checks still apply.

Leave the fast path when the change spreads beyond the named location, touches a recorded decision, or fails unexpectedly. Then apply the gate.

## 1. Gate

Choose depth from **uncertainty** (how well intent and state are known) and **blast radius** (what the change can break or invalidate). Optimize expected total effort, including rework.

| | Low blast radius | High blast radius |
|---|---|---|
| **Low uncertainty** | Fast path | Execute |
| **High uncertainty** | Orient (light), then re-gate | Orient → Reason → Execute → Reconcile |

Classify each open fork: **empirical** (run the cheapest discriminating check), **preference** (ask the operator once, with options), **consequential or irreversible** (propose and wait). Stop escalating once remaining uncertainty no longer changes the decision.

## 2. Modes

| Mode | Entry signal | Exit artifact | Procedure |
|---|---|---|---|
| **Orient** | New or resumed session; unclear state | State brief: objective, last verified state, active work, relevant deferred items | [orient](modes/orient.md) |
| **Reason** | Consequential design, research question, suspected blind spot | D record: options, choice, evidence, reversal condition | [reason](modes/reason.md) |
| **Execute** | Authorized change with dependencies | Change, evidence, and a complete F record | [execute](modes/execute.md) |
| **Reconcile** | Milestone, requirement change, repeated failure, major discovery | Divergences resolved or proposed, learned procedures, ranked next actions | [reconcile](modes/reconcile.md) |
| **Checkpoint** | Before compaction, pause, handoff, or risky operation | Overwritten recovery summary pointing to durable evidence | [checkpoint](modes/checkpoint.md) |
| **Recover** | Interruption, compaction, takeover, uncertain completion | Verified resume point; unknowns marked unknown | [recover](modes/recover.md) |
| **Intake** | More than one pending request; message during work; operator leaving | Ordered queue with relations and flagged conflicts | [intake](modes/intake.md) |
| **Advance** | Operator away or asks for autonomous progress | Away report: decisions needed, verified done, partial, proposed next | [advance](modes/advance.md) |
| **Compile** | Release, handoff, or request for spec, manual, or report | One document that is specification, operator manual, and report, tagged with source IDs | [compile](modes/compile.md) |

On entering a mode for non-trivial work, copy the procedure's step IDs into the task list (or a checklist in the log). Mark skipped steps `n/a: <reason>`. A mode is done only when its exit artifact exists.

## 3. Roles and delegation

- **Coordinator** (default) owns the objective, records, and final claims.
- **Delegate** (assigned a mode by another agent or a workbench) runs only that mode within the given scope and writes no records. Its exit artifact is the proposed record delta in the Report block's `records:` field; the coordinator reviews and writes it. If the brief is insufficient, it returns `status: blocked` naming the missing input.

Delegate only separable research, verification that must not be anchored on the current conclusion, or bulk reading that would flood context. Brief with goal, mode, scope, what is ruled out, and file pointers rather than pasted content ([BRIEF](assets/templates/BRIEF.md)). One question per delegate; for a high-stakes decision, a second opinion from a different model on the same brief is allowed, and agreement is the signal. Review delegated diffs and evidence yourself; never pass a delegate's summary through as verified. After an interruption, start a fresh delegate with consolidated scope.

## 4. Queue and autonomy

- Capture every request; never discard silently. Apply mid-work amendments at the next safe point.
- When no one can answer, park the decision with options and a recommendation, and continue independent work. Never exceed the charter; irreversible or out-of-scope actions wait.
- After the queue empties or a milestone closes, propose at most three next actions ranked by expected value. Execute them only under a charter or approval.
- Keep state in the queue and recovery summary so a fresh session can continue.

## 5. Retrieval

Outside the fast path, read the index header and recovery summary first. Read volumes, log entries, and code at cited locators on demand; read full sources, raw logs, and data only when evidence requires. In Orient, Reason, and Reconcile, follow two bounded paths: the **direct** path (what the task names or touches) and the **dependency** path (decisions whose `invalidated_if` the task may trigger, deferred items in the affected area, downstream acceptance criteria).

## 6. Records

A record states what was built, how, why, compared with what, how it was verified, and where to check it, so later work never re-reads the implementation. A checkmark is not a record.

- **F** (feature): Intent, How, Alternatives, Rationale, Verification, Locators (`path::symbol` — what it confirms), Operation, Limits. Written in the same step as verification; a feature without it is not done.
- **D** (decision) with options, evidence, and `invalidated_if`; **C** (comparison) with measurements.
- **Volumes** are numbered project phases, not topics. Closing one requires an exit summary in which every open item is carried, deferred, or dropped.
- The index's **Feature registry** points to each feature's current record.
- Check with `python3 <skill-dir>/scripts/check_records.py <project-root> [--since <ref> | --since last]`: fields, locators, registry, decisions, volume closure, and changed or new files not covered by any record.

**Layout.** Paths come from `.praxteward.yaml` at the project root; without it, use `docs/INDEX.md`, `docs/LOG.md`, `docs/QUEUE.md`, and `docs/volumes/vol-NN.md`. To initialize, copy INDEX, LOG, and QUEUE there and VOLUME as `vol-01.md`; write `.praxteward.yaml` only for non-default paths. Volume paths in the index are relative to the index; locator paths are relative to the project root.

Field and volume rules: [records](references/records.md). Templates: [INDEX](assets/templates/INDEX.md), [VOLUME](assets/templates/VOLUME.md), [LOG](assets/templates/LOG.md), [QUEUE](assets/templates/QUEUE.md), [AWAY-REPORT](assets/templates/AWAY-REPORT.md).

## 7. Report block (modes only)

```
mode: <mode>   role: coordinator|delegate   status: done|partial|blocked
objective: <one line>
evidence: <checks, files, commits, observations, each verifiable>
state_delta: <what changed or was learned>
unknowns: <unverified claims, untested boundaries>
records: <updated paths | proposed deltas | none>
next: <next safe action>
```

Coordinators may render it as prose for the operator; delegates and workbenches use it as-is.

## 8. Capability fallbacks

| Missing | Do instead |
|---|---|
| Write access | Return proposed record deltas in the report |
| Command execution | Mark behavioral claims `unverified` |
| Task list | Checklist under the log's active entry |
| Subagents | Apply lenses sequentially; state that verification was not independent |
| Project records | Say so, give a bounded analysis, offer to initialize from templates |

Never present a fallback result as equivalent to the full procedure.

## 9. Invocation

- Once loaded, the skill stays in context for the session; do not reload it per task.
- `praxteward <mode>` runs that mode directly, skipping the gate.
- `praxteward inspect [path]` runs `check_records.py` and `tell_scan.py` and returns findings ranked by severity without editing anything.
- Host-injected events: session start → Orient (light); pre-compaction, pause, or handoff → Checkpoint; resume after interruption → Recover; test failure → Execute; repeated failure or milestone → Reconcile; release → Reconcile, then Compile; operator away → Intake, then Advance.
- When a mode was missed or added no value, add a line under the log's `Routing notes`.

## 10. Output

Lead with the result. Report only evidence, changed intent, residual uncertainty, and next action that matter. Distinguish done from proposed.

Before delivering a record, report, compiled document, or code, pass the [output checks](references/output.md): Block findings never ship; Fix findings are removed or kept with an inline reason; run `python3 <skill-dir>/scripts/tell_scan.py <changed files>`. Write as a careful engineer would: plain words, specific values, no decoration.
