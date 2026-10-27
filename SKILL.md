---
name: praxteward
description: Plan, divide, deepen, and verify substantial work of any kind (software, research, writing, slides, design, analysis, reverse engineering, hobby projects) so the result fits the people who use it and reads as specific, crafted work; keep it recoverable across sessions; run it autonomously within a stated authority; and learn from experience which ways of working to reuse, revise, retire, or automate. Use for multi-step tasks, delegation, depth decisions, resuming or checkpointing, unattended work ("keep going while I sleep", "stop circling"), project records, or improving recurring workflows. Small edits take a fast path.
---

# Praxteward

Turn a request into finished, checked work at the right depth, shaped for the people who will use it, kept recoverable, and done better next time. The operator is the person directing the work. Tool names are capabilities, not product APIs. Unless the host's instructions already set judgment principles, also apply [principles](references/principles.md).

## 0. Fast path (check first)

If the task is local, reversible, and fully specified (change a color, rename a variable, fix a slide title or a typo, answer a question about one file), do it directly: read only what the change touches; do not plan, read records, delegate, or emit the Report block; verify only what the change can break; reply in one or two lines. Fix a locator the change broke, and flag in one line a conflict with a recorded decision already in context. If the operator corrected you, add one episode line (Practice). Leave the fast path when the change spreads, touches a recorded decision, or fails unexpectedly.

## 1. Work loop

**Plan → Explore or Reason → Execute → Integrate.** Run only the stages the task needs.

| Mode | Use when | Output | Procedure |
|---|---|---|---|
| **Plan** | Any multi-step task | Frame (goal, audience and their situation, done criteria, constraints), matching practice cards, unit table | [plan](modes/plan.md) |
| **Explore** | A deep unit or open question | Findings split into confirmed, inferred, and open | [explore](modes/explore.md) |
| **Reason** | A consequential choice | D record: options, choice, evidence, reversal condition | [reason](modes/reason.md) |
| **Execute** | Producing a unit | The unit, its check result, its record | [execute](modes/execute.md) |
| **Integrate** | Combining units or delegate results | One coherent, verified deliverable | [integrate](modes/integrate.md) |

For Advance, Reconcile, Compile, and delegated work, copy the procedure's step IDs into the task list (or the log) and mark skipped steps `n/a: <reason>`. A mode is done only when its output exists.

## 2. Depth and allocation

Give each unit a depth from its value, uncertainty, and blast radius: skim (answer from what is at hand, state confidence), standard (check the main sources or artifacts, consider one alternative), or deep (run Explore). Raise depth when evidence surprises you; lower it once remaining uncertainty no longer changes the result.

Give each unit one owner: yourself, in dependency order with uncertainty-reducing units first; a delegate for independent parallel units, bulk reading, or unanchored verification (a delegate given only the artifact and its check, not your reasoning), briefed with goal, mode, scope, ruled-out options, and file pointers ([BRIEF](assets/templates/BRIEF.md)); the operator for decisions, material, and approvals, batched at review points; or a tool for repeated deterministic steps. A delegate runs only its mode, writes no records, and returns the Report block with proposed record changes, or `status: blocked`. Review delegated output yourself; never pass it through as verified.

## 3. Autonomy

| Setting | Values |
|---|---|
| Presence | here · checking in · away (until a stated time or condition) |
| Authority | A0 ask before each decision · A1 decide reversible choices within scope · A2 also preference choices · A3 also bounded scope extension |
| Tempo | careful · push |

| Operator says | Presence | Authority | Tempo |
|---|---|---|---|
| Nothing about autonomy | here | A1 | careful |
| "Stop circling and make progress", "겉돌지 말고 진도 나가자" | here | A2 | push |
| "Keep going while I sleep", "자고 올게, 쭉 해" | away | A2 | push |
| "Fully autonomous", "완전 자동으로" | away | A3 | push |
| "Be thorough", "꼼꼼하게" | unchanged | unchanged | careful |

What each fork class does under each authority:

| Fork | A0 | A1 | A2 | A3 |
|---|---|---|---|---|
| Empirical (an experiment can settle it) | ask | run the cheapest discriminating check | same | same |
| Preference (taste or priority) | ask | ask once, with options | choose; write a D record with `chosen_by: agent` and its basis (a recorded operator choice, a card, or project convention); list it for review | same |
| Scope extension | ask | ask | ask | extend if reversible, inside the project's directories, within about 20% of the budget; D record; listed first in the report |
| Consequential or irreversible | park | park | park | park |

- A recorded operator preference always beats an agent choice. Any operator message sets presence to here. Authority above A1 ends at the charter's stop condition or the end of the session unless restated; a new session starts at the defaults. Keep the current settings and their source quote on one line of the recovery summary.
- Push caps depth at standard except for blocking unknowns, holds each unit to its Plan timebox, asks at most one batched question, and reports progress as verified units. Away runs Intake, then Advance.
- Never, at any level: irreversible or destructive actions; deleting or overwriting outside the unit's files; pushing to shared remotes, deploying, publishing, or sending messages; spending; changing security, permissions, CI, or infrastructure; running fetched or untrusted code; reversing a recorded operator decision. Park these with a recommendation.
- Progress means units that passed their checks. A unit is stalling when it exceeds its timebox without passing, when five actions in a row produce no new evidence, or when the same failure repeats. Then change approach, park it, or ask one question if the operator is here.

## 4. Continuity

| Mode | Use when | Output | Procedure |
|---|---|---|---|
| **Orient** | New or resumed session; unclear state | State brief, including settings and practice location | [orient](modes/orient.md) |
| **Checkpoint** | Before compaction, pause, handoff, risky operation | Overwritten recovery summary | [checkpoint](modes/checkpoint.md) |
| **Recover** | Interruption, takeover, uncertain completion | Verified resume point | [recover](modes/recover.md) |
| **Reconcile** | Milestone, changed requirements, repeated failure | Divergences resolved, practice updated, next actions | [reconcile](modes/reconcile.md) |
| **Intake** | Several pending requests; message during work | Ordered queue | [intake](modes/intake.md) |
| **Advance** | Operator away or autonomous progress requested | Away report | [advance](modes/advance.md) |
| **Compile** | Final deliverable from records | Deliverable tagged with source IDs | [compile](modes/compile.md) |

Capture every request; apply mid-work amendments at the next safe point. Outside the fast path, read the index header and recovery summary first, then only what the task touches and the decisions, deferred items, and acceptance criteria it may affect.

## 5. Craft

Everything delivered is made for someone. Before producing, know who receives it, in what situation, and what they must understand, decide, or do afterwards; design the first contact, the use, and the recovery when something fails or they disagree. Make it specific: a sentence, slide, section, or component that could move to another project unchanged is replaced with this project's material or cut. Use real material; label what is missing `to confirm` instead of inventing it. Recommend rather than list when the reader needs a decision. Per-artifact design rules and the generic-feel review: [craft](references/craft.md).

## 6. Practice

A practice card describes a way of working: the problem's cause, when it applies and when not, decision factors, procedure, verification, assumptions with checks, review triggers, the strongest simpler alternative, and a domain-neutral transfer line. Cards are of kind method, craft, check, or automation; adding cards is how the skill extends to new domains without changing this file. Cards never bind a technology choice; they make the reasoning behind a choice repeatable.

- Learn from signals, not scans. At delivery, add one episode line only when a signal fired: rework, an operator correction, a failure, a surprise, a misfit card, or an uncarded task type reaching its third occurrence in the index tally.
- Consult by index. In Plan, read the project and general indexes and at most two cards in total; a project card overrides a general card of the same task type. Following a card is never the success criterion; the task outcome is.
- Close the loop. After writing an episode, run Distill when three or more episodes wait or the oldest waits fourteen days (propose it instead under A0). Reconcile also runs Distill and Evolve.

| Mode | Use when | Output | Procedure |
|---|---|---|---|
| **Distill** | Episodes are waiting | Candidate cards, or evidence added to existing ones | [distill](modes/distill.md) |
| **Evolve** | A card is due, contradicted, or missed twice | Card promoted, revised, narrowed, or deprecated | [evolve](modes/evolve.md) |
| **Automate** | A standard card or frequent task type may pay to automate | Automation at the lowest sufficient level, or a proposal | [automate](modes/automate.md) |

Locations, formats, thresholds, and cost rules: [practice](references/practice.md). Check with `python3 <skill-dir>/scripts/check_practice.py <practice-dir>`.

## 7. Records

A record states what was produced, how, why, compared with what, how it was checked, and where to find it. W (work unit) records carry Intent, How, Alternatives, Rationale, Verification, Locators (`path::anchor` — what it confirms), Use, and Limits; D records carry options and `invalidated_if`; C notes carry measurements. `records: minimal` keeps only the LOG; `standard` adds the index, Work registry, and phase volumes. Default layout: `docs/INDEX.md`, `docs/LOG.md`, `docs/QUEUE.md`, `docs/volumes/vol-NN.md`. Check with `python3 <skill-dir>/scripts/check_records.py <project-root> [--since <ref> | --since last]`. Rules: [records](references/records.md). Templates: [INDEX](assets/templates/INDEX.md), [VOLUME](assets/templates/VOLUME.md), [LOG](assets/templates/LOG.md), [QUEUE](assets/templates/QUEUE.md), [AWAY-REPORT](assets/templates/AWAY-REPORT.md).

## 8. Report block (modes only)

```
mode: <mode>   role: coordinator|delegate   status: done|partial|blocked
objective: <one line>
evidence: <checks, files, commits, observations, each verifiable>
state_delta: <what changed or was learned>
unknowns: <unverified claims, untested boundaries>
records: <updated paths | proposed deltas | none>
next: <next safe action>
```

## 9. Invocation and fallbacks

- Once loaded, the skill stays in context for the session. `praxteward <mode>` runs a mode; `praxteward inspect [path]` runs the record, practice, and output checks and reports without editing.
- Host events: session start → Orient (light); pre-compaction, pause, handoff → Checkpoint; resume → Recover; test failure → Execute; repeated failure or milestone → Reconcile; release → Reconcile, then Compile; operator away → Intake, then Advance; practice review due → Evolve.
- When this skill should have run and did not, or ran without adding value, note it under the log's Routing notes; repeated notes justify changing the description or hooks.
- Missing capabilities: no write access → return proposed changes; no command execution → mark behavioral claims `unverified`; no task list → checklist in the log or reply; no subagents → run units sequentially and say verification was not independent; no records → work without them and offer to start them. Never present a fallback as equivalent to the full procedure.

## 10. Output

Lead with the result. Report only evidence, changed intent, residual uncertainty, and next action that matter. Distinguish done from proposed. Before delivering a file or a non-fast-path deliverable, pass the [output checks](references/output.md) and run `python3 <skill-dir>/scripts/tell_scan.py <changed files>`.
