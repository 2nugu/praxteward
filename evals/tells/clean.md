# Results

The pipeline processes 1,200 records per second on one core, up from 310 before the change (`bench/run.sh`, commit 3f2a1c9).

Retries stop after five attempts; see `src/scheduler.py::RETRY_MAX`.
