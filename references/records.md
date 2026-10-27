# Records

Write records in the formats of [VOLUME](../assets/templates/VOLUME.md) and [INDEX](../assets/templates/INDEX.md); the checker parses those formats. On read-only tasks, inspect and report without writing.

## Feature record `F-NNN`

| Field | Must contain | Fails if |
|---|---|---|
| Status | planned, active, done, or superseded by F-x | — |
| Intent | Behavior the operator or program needs, with acceptance criteria | Task wording ("implement X") |
| How | Technique, algorithm, library@version, data shape, key mechanism, interfaces | "Implemented as planned" |
| Alternatives | Each option compared, how it was compared, observed result (numbers when measured) | "Considered others" |
| Rationale | Why the choice fits this project's constraints; reversal condition or D-ID | Generic virtues without evidence |
| Verification | Command or procedure, observed result, commit or date; untested boundaries | "Tested", "works" |
| Locators | One line per `path::symbol` — what it confirms | Bare file lists |
| Operation | How the operator uses, configures, inspects, and recovers it; or `internal: <reason>` | Empty |
| Limits | Known gaps, assumptions, deferred IDs | Empty |
| Supersedes | Earlier F-ID this record replaces, or — | — |

Use specific names, values, paths, and measurements; no narrative padding. When a field would be long, keep the evidence in the log and point to the entry. When a feature changes, write a new or revised F with `Supersedes`, mark the old one `superseded by F-x`, and update the registry.

## Decision record `D-NNN` and comparison note `C-NNN`

- **D**: Context, Options (at least two, including keep-current), Choice, Evidence, `invalidated_if`, Affects (F-IDs), Supersedes. A reversal is a new D; never rewrite an old decision. Add every D to the index's Decisions table.
- **C**: Hypothesis, Setup, Result (numbers), Conclusion, Feeds (D/F IDs). Write one whenever a comparison or experiment runs. Raw outputs stay in the log or artifacts, referenced by path.

## Volumes

- Number volumes by phase of progress (Vol 01, 02, …), not by topic. Each holds only what its phase needed to decide, build, and verify, in detail. Keep one active volume.
- Open a new volume when the phase's exit criteria are met at a milestone, when an objective or architecture shift makes the phase objective obsolete, or when the volume can no longer be oriented from its header and exit summary (about 1,500 lines). Split only at a completed milestone, never mid-feature.
- To close a volume: set its Status to `closed`, write the exit summary (F/D IDs established), and give every open item a disposition: **carried** (listed under the next volume's Carried in), **deferred** (added to the index's Deferred table with a revisit condition), or **dropped** (with reason). Update the index's Volumes table and Active volume.
- Closed volumes are append-only except for supersession pointers and locator fixes.

## Checker errors

The checker is structural: it cannot tell whether a rationale is true. Spot-check How and Locators against code at Reconcile. To accept an uncovered file deliberately, add a log line `no-record: <path> — <reason>`.
