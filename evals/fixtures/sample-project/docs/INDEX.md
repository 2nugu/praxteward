# Project Index
## Volumes
| Vol | File | Phase | Status | Exit summary |
|---|---|---|---|---|
| 01 | volumes/vol-01.md | Baseline | closed | yes |
| 02 | volumes/vol-02.md | Scale-out | active | — |
## Work registry
| ID | Title | Status | Vol | depends_on |
|---|---|---|---|---|
| W-001 | Job scheduler | done | 01 | — |
| W-002 | Retry policy | planned | 02 | W-001 |
## Decisions
| ID | Decision | invalidated_if | Vol |
|---|---|---|---|
| D-001 | In-process queue | >1 worker host | 01 |
## Deferred
| ID | Item | Revisit when | From Vol |
|---|---|---|---|
| X-001 | Persistent queue | >1 worker host | 01 |
