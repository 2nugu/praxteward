# Lean code

Use on any coding task: writing, fixing, refactoring, reviewing, or choosing dependencies, and when the operator says "simplest solution", "yagni", "be lazy", "과하게 만들지 마", or complains about over-engineering. The aim is the smallest change that fully solves the task, and a reply a busy person understands in one read. Small is the result of building only what is needed, never of compressing code.

## Levels

`praxteward lean lite|full|ultra|off` sets the level for the session; keep it on the settings line of the recovery summary. Default: full.

| Level | Behavior |
|---|---|
| lite | Build what was asked. Name the smaller option in one line and let the operator pick. |
| full | The rules below. |
| ultra | Also question the request: before building, push back on each part the need does not justify, and build only what survives. |
| off | Craft's Code rules only. |

## Before writing

Read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, configuration, exports, and dynamic references. Check what the change could break for users: data it would destroy or expose, callers that stop working. That list is the scope; extra features are not.

## The smallest complete change

Take the first rung that fully works ([solution selection](craft.md#solution-selection) in code terms):

1. Does it need to exist? Skip features, options, and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it the way the surrounding code does.
3. Standard library or platform feature? Use it, unless the project has its own; a house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise, the minimum code that works.

Rules:

- Be lazy about the solution, never about the change: finish every part the task needs, including the callers, tests, and fixtures the change breaks.
- No abstraction, wrapper, type conversion, option, setting, boilerplate, or code "for later" that nobody asked for. Keep values in the form the platform already gives. Deletion beats addition. Keep the structure the codebase already has.
- The shortest working diff wins once you know everything it must touch. A one-liner that needs decoding is not short.
- Comment only the reason the code cannot show, in one line.
- Bug fix: before editing, search every caller of the function, then fix the root cause once in the shared code.
- Code that is moved or merged keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- New non-trivial logic (a branch, a loop, a parser, money, security, or a whole new script) leaves one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets one comment at the code that carries it: `shortcut: <the limit>, <when to upgrade>`. With records, the same limit goes in the W record's Limits or the log.

Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, calibration that real hardware needs, and anything the operator asked for.

End the reply with one or two lines: what was skipped or not checked, and any risk the operator must know.

## Debt ledger (`praxteward debt [path]`)

Run `python3 <skill-dir>/scripts/debt_scan.py <path>`. It collects every `shortcut:` comment into a table of location, limit, and upgrade trigger, and flags shortcuts without a trigger. The ledger is generated on demand, never kept as a separate file to maintain. For each row, check whether its trigger now holds; list those first with the smallest fix, and leave the rest.

## Review (`praxteward review [diff, branch, or files]`)

Review the current diff unless a target is given.

1. Read the diff, then the code around each hunk and its callers; a finding needs the context that proves it.
2. Check, in this order: correctness (wrong result, missed case, broken caller), security and trust boundaries, data loss, load under the project's measured or stated usage, missing tests for new non-trivial logic, and cuttable code (dead or duplicate paths, unasked abstractions, superseded implementations left behind, dependencies added for a few lines).
3. Write each finding with severity (blocker, should fix, could cut), locator (`path:line`), the concrete input or state that fails and what goes wrong, and the smallest adequate fix.
4. Verify each finding by reading the code path or running it; drop what cannot be shown. Hypothetical scale and style preferences are not findings.
5. Report the findings ranked by severity, then one line of what was not checked. Fix nothing unless asked.

## Audit (`praxteward audit [path]`)

The same lenses across the whole repository, as a ranked plan rather than a diff.

1. Inventory entry points, declared dependencies against imports (unused or duplicated packages), and the paths that handle money, security, or user data.
2. Find duplicate implementations of one behavior, superseded paths still reachable, unasked layers and options, and critical paths without tests.
3. Run `debt_scan.py` and the output checks (`tell_scan.py`) over the source.
4. Rank fixes by impact on users and correctness first, then by effort; keep the top ten with locator, problem, fix, and how to check it. Propose; do not edit unless asked.
