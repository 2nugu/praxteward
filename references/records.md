# Records

Write standard records in the formats of [VOLUME](../assets/templates/VOLUME.md) and [INDEX](../assets/templates/INDEX.md); the checker parses those formats. Minimal records use only [LOG](../assets/templates/LOG.md). On read-only tasks, inspect and report without writing.

## Work record `W-NNN`

A work unit is whatever the project produces and later needs to find again: a feature, a document section, a group of slides, an analysis, a reverse-engineering finding.

| Field | Must contain | Fails if |
|---|---|---|
| Status | planned, active, done, or superseded by W-x | — |
| Intent | What the unit must achieve and for whom, with acceptance criteria | Task wording ("make slides on X") |
| How | Method, technique, tools and versions, sources, data shape, structure or interfaces | "Done as planned" |
| Alternatives | Each option compared, how it was compared, observed result (numbers when measured) | "Considered others" |
| Rationale | Why the choice fits this project's constraints; reversal condition or D-ID | Generic virtues without evidence |
| Verification | Command, procedure, or source check; observed result; commit or date; what was not checked | "Checked", "works" |
| Locators | One line per `path::anchor` — what it confirms | Bare file lists |
| Use | How the reader or user applies, configures, inspects, or recovers it; or `internal: <reason>` | Empty |
| Limits | Known gaps, assumptions, deferred IDs | Empty |
| Supersedes | Earlier W-ID this record replaces, or — | — |

Anchors: a symbol in code (`src/sched.py::retry`), a heading in a document (`report.md::Results`), a slide or page (`deck.pptx::slide 7`), a cell (`model.xlsx::Sheet1!B12`), an address or offset (`firmware.bin::0x1F40`). The checker confirms the file exists and, for text files, that the anchor text occurs in it.

Use specific names, values, paths, and measurements; no narrative padding. When a field would be long, keep the evidence in the log and point to the entry. When a unit changes, write a new or revised W with `Supersedes`, mark the old one `superseded by W-x`, and update the registry.

## Decision record `D-NNN` and comparison note `C-NNN`

- **D**: Context, Options (at least two, including keep-current), Choice, Evidence, `invalidated_if`, Affects (W-IDs), Supersedes. A reversal is a new D; never rewrite an old decision. Add every D to the index's Decisions table.
- **C**: Hypothesis, Setup, Result (numbers), Conclusion, Feeds (D/W IDs). Write one whenever a comparison or experiment runs. Raw outputs stay in the log or artifacts, referenced by path.

## Volumes

- Number volumes by phase of progress (Vol 01, 02, …), not by topic. Each holds only what its phase needed to decide, produce, and verify, in detail. Keep one active volume.
- Open a new volume when the phase's exit criteria are met at a milestone, when a shift in objective or approach makes the phase objective obsolete, or when the volume can no longer be oriented from its header and exit summary (about 1,500 lines). Split only at a completed milestone, never mid-unit.
- To close a volume: set its Status to `closed`, write the exit summary (W/D IDs established), and give every open item a disposition: **carried** (listed under the next volume's Carried in), **deferred** (added to the index's Deferred table with a revisit condition), or **dropped** (with reason). Update the index's Volumes table and Active volume.
- Closed volumes are append-only except for supersession pointers and locator fixes.

## Minimal records

The LOG alone: recovery summary at the top, dated entries below. Each entry that completes something states what was produced, how it was checked, and where it is. Promote to standard records by copying the other templates; earlier entries stay in the LOG.

## Checker errors

The checker is structural: it cannot tell whether a rationale is true. Spot-check How and Locators against the artifacts at Reconcile. To accept an uncovered file deliberately, add a log line `no-record: <path> — <reason>`.
