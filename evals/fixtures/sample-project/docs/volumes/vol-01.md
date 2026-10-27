# Vol 01 — Baseline
- **Status:** closed
## Carried in
## Decisions
### D-001 — Queue placement
- **Context:** single host, <100 jobs/min
- **Options:** A: in-process list; B: Redis; keep current: none
- **Choice:** A
- **Evidence:** C-001 latency 0.4 ms vs 2.1 ms
- **invalidated_if:** more than one worker host
- **Affects:** W-001
## Work units
### W-001 — Job scheduler
- **Status:** done
- **Intent:** run submitted jobs FIFO; accept 100 jobs/min
- **How:** in-process FIFO via `schedule()`; retry ceiling constant
- **Alternatives:** Redis queue — benchmarked C-001 — 5x latency
- **Rationale:** single host; reversal per D-001
- **Verification:** `pytest tests/test_sched.py` — 12 passed — commit abc123
- **Locators:**
  - `src/scheduler.py::schedule` — entry point for job submission
  - `src/scheduler.py::RETRY_MAX` — retry ceiling
- **Use:** set RETRY_MAX in src/scheduler.py; inspect via logs
- **Limits:** no persistence (X-001)
## Comparisons
### C-001 — Queue latency
- **Hypothesis:** in-process is faster
- **Setup:** 1k jobs, local
- **Result:** 0.4 ms vs 2.1 ms
- **Conclusion:** in-process
- **Feeds:** D-001, W-001
## Open items
- [x] W-002 retry policy — carried
- [x] persistence — deferred X-001
## Exit summary
- **Established:** W-001, D-001
- **Carried forward:** W-002
