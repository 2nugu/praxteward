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
- **Affects:** F-001
- **Supersedes:** <D-ID or —>

## Features

### F-001 — <title>
- **Status:** planned  (planned | active | done | superseded by F-x)
- **Intent:** <needed behavior + acceptance criteria>
- **How:** <technique, algorithm, library@version, data shape, interfaces>
- **Alternatives:** <option — how compared — result>
- **Rationale:** <why it fits here; reversal condition or D-ID>
- **Verification:** <command/procedure — observed result — commit/date; untested boundaries>
- **Locators:**
  - `src/module.py::function_name` — <what to check here>
  - `config/app.yaml::RETRY_MAX` — <what this value controls>
- **Operation:** <how the operator uses/configures/inspects/recovers it, or "internal: reason">
- **Limits:** <known gaps, assumptions, deferred IDs>
- **Supersedes:** <F-ID or —>

## Comparisons

### C-001 — <title>
- **Hypothesis:** <…>
- **Setup:** <data, environment, commands>
- **Result:** <numbers>
- **Conclusion:** <…>
- **Feeds:** D-001, F-001

## Open items

- [ ] <ID — item> — disposition: <carried | deferred X-NNN | dropped: reason>  (required before close)

## Exit summary

- **Established:** <F/D IDs>
- **Carried forward:** <IDs>
- **Risks:** <…>
