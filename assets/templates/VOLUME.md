# Vol 01 — <phase name>

- **Status:** active
- **Phase objective:** <what this phase must establish>
- **Entry state:** <verified state at phase start, with commit>
- **Exit criteria:** <observable conditions that close the phase>

## Carried in

- <ID — item> — from Vol <NN>

## Decisions

### D-001 — <title>
- **Context:** <problem and constraints>
- **Options:** <A: … ; B: … ; keep current: …>
- **Choice:** <option>
- **Evidence:** <measurements, references, C-IDs>
- **invalidated_if:** <condition>
- **Affects:** W-001
- **Supersedes:** <D-ID or —>

## Work units

### W-001 — <title>
- **Status:** planned  (planned | active | done | superseded by W-x)
- **Intent:** <what it must achieve, for whom, and acceptance criteria>
- **How:** <method, tools and versions, sources, data shape, structure or interfaces>
- **Alternatives:** <option — how compared — result>
- **Rationale:** <why it fits here; reversal condition or D-ID>
- **Verification:** <command, procedure, or source check — observed result — commit/date; what was not checked>
- **Locators:**
  - `path/to/file::anchor` — <what to check here>
- **Use:** <how the reader or user applies, configures, inspects, or recovers it, or "internal: reason">
- **Limits:** <known gaps, assumptions, deferred IDs>
- **Supersedes:** <W-ID or —>

## Comparisons

### C-001 — <title>
- **Hypothesis:** <…>
- **Setup:** <data, environment, commands>
- **Result:** <numbers>
- **Conclusion:** <…>
- **Feeds:** D-001, W-001

## Open items

- [ ] <ID — item> — disposition: <carried | deferred X-NNN | dropped: reason>  (required before close)

## Exit summary

- **Established:** <F/D IDs>
- **Carried forward:** <IDs>
- **Risks:** <…>
