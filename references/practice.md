# Practice

## Where cards live

Use the first location that is writable and persists between sessions, and state it in Orient:

1. `practice_dir` in `.praxteward.yaml`.
2. `~/.praxteward/practice`, created only with the operator's approval; record the approval by writing `practice_dir` into `.praxteward.yaml`.
3. `docs/practice` in the project. General cards written here use `Scope: general (staged)` until moved to a user-level directory.
4. Nowhere: report episodes in the reply and say that learning is not persisted.

Project-only cards always live in `docs/practice`. Each directory holds `INDEX.md` and `cards/P-NNN.md`. In Plan, read both the project and general index; a project card overrides a general card of the same task type; read at most two cards in total.

## Index

[PRACTICE-INDEX](../assets/templates/PRACTICE-INDEX.md) holds the card table (first table, parsed by the checker), `Last distill: YYYY-MM-DD`, optional `Processed on last distill date: <episode IDs or none>`, and the task-type tally. The processed IDs prevent replay while allowing later episodes on the same date. Task types come from the tally; reuse one before adding another. At delivery, increment its count; an uncarded type reaching three triggers the `repeat` signal.

## Episode line

Written in the project LOG entry at delivery, only when a signal fired:

```
- Episode E-<project>-<YYYYMMDD>-<n>: type=<task type>; card=<P-NNN@version|none>; outcome=<met|partial|missed>; rework=<n>; corrections=<n>; signal=<rework|correction|failure|surprise|repeat|misfit|check>; note=<one line>
```

`outcome` judges the task goal, not whether steps ran. `corrections` counts operator redirections. Without project records, report the episode in the reply.

`signal=check` names the check ID in the note and goes to the check, not to a card. Two episodes on one pattern justify narrowing it (a genre profile or threshold) or removing it. A missed defect justifies a new pattern only when the pattern separates the defect from correct text on material not written for the test, as in the Korean calibration; samples written to fit the pattern do not count. Checks are shared, so a project proposes the change to the skill instead of editing it.

## Card fields

| Field | Must contain |
|---|---|
| Version | `major.minor`, starting at 1.0; revisions raise it |
| Status | candidate, trial, standard, or deprecated |
| Kind | method, craft, check, or automation |
| Scope | `general`, `general (staged)`, or `project:<name>` |
| Task type | One type from the index tally |
| Objective | The outcomes the way of working protects, not the steps |
| Applies when / Not when | Observable conditions; Not when lists known misfits |
| Decision factors | What to weigh; no fixed answer |
| Procedure | Numbered steps |
| Verification | How to tell the outcome was met |
| Assumptions | One line each: claim — how to check it |
| Review triggers | Events that reopen the card, plus `review_by: YYYY-MM-DD` |
| Simpler alternative | The strongest simpler way, then `— untested` or `— <result when tried>` |
| Transfer | cause → conditions → mechanism → verification, in domain-neutral words |
| Automation | Level (none, checklist, decision rule, script, agent workflow, with or without approval gate) and its basis |
| Evidence | One line each: `<project>/<deliverable> — met|partial|missed — E-id`; source episode and check result must be retrievable through the project log or a source pointer in the card |
| History | One line per version: date, version, change, reason |
| Replacement | Deprecated cards only: the card or way that replaces it, or `none` |

## Lifecycle thresholds

| Status | Enter when | Use |
|---|---|---|
| candidate | Distilled from one episode | Suggestion only |
| trial | Two or more evidence lines | On low-stakes, reversible work; note "trial" in the plan |
| standard | `met` in two or more distinct project/deliverable pairs, simpler alternative tried, every assumption has a check | By default, unless a Not when condition holds |
| deprecated | An assumption failed its check, two misses where it applied, or a cheaper way met the same outcome twice | Never; kept for history with its Replacement |

Narrowing scope (adding to Not when) is usually better than deprecating. Promotion also requires inspecting the source episodes, observed checks, and simpler-alternative result; counts alone do not establish that a method helped. The checker validates structure, not effectiveness. Unavailable evidence leaves the card at its current status.

## At plan time

When Plan reads a card: if `review_by` has passed or an assumption is visibly false in this context, send the card to Evolve and do not rely on it. If its simpler alternative is `untested` and this task is low-stakes and reversible, try the alternative on this task or a slice of it and record the result as evidence.

## Cost rules

- Normal work adds at most one tally increment and, only on a signal, one episode line.
- Distill reads from `Last distill` inclusive and skips processed IDs; Evolve reads only due or contradicted cards; Plan reads two indexes and at most two cards. Nothing scans all logs or cards.
- Automate takes N (expected runs) from the tally rate over the card's review period. Without a tally, use the rule: automate only if the card is standard, the type has occurred three or more times, and the output can be checked automatically.
