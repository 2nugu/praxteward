# Praxteward

An agent skill for long-running software and research projects. It keeps intent, architectural decisions, roadmap, verified progress, and recoverable continuity coherent across sessions, models, subagents, and hosts, and stays out of the way on trivial edits.

Standard `SKILL.md` format. Works with Claude (claude.ai, Claude Code, API), OpenAI Codex and ChatGPT, and custom agent workbenches.

Self-contained: no other skills or packages are required. The scripts need Python 3.8+ (standard library only), and changed-file coverage needs git.

## What it does

| Need | How |
|---|---|
| Stay light on small tasks | A fast path at the top of `SKILL.md` handles local, reversible, fully specified changes directly |
| Choose depth deliberately | Gate on uncertainty × blast radius; forks classified as empirical, preference, or consequential |
| Follow procedures, not vibes | Nine modes (Orient, Reason, Execute, Reconcile, Checkpoint, Recover, Intake, Advance, Compile), each a procedure of numbered steps with an exit artifact; `praxteward inspect` reports without editing |
| Records worth reading | Feature records state technique, alternatives compared, rationale, verification evidence, and `path::symbol` locators, so later work does not re-read the implementation |
| Documents that grow with the project | Volumes are numbered by phase; closing one forces every open item to be carried, deferred, or dropped |
| Nothing missed | `scripts/check_records.py` checks fields, locators, registry, volume closure, and changed-file coverage since a git ref |
| Queues and unattended work | Intake orders pending and mid-task requests; Advance works within a charter while you are away and parks decisions |
| One final document | Compile assembles a specification, operator manual, and project report from the records |
| Output without machine tells | Block and Fix checks for prose and code, scanned by `scripts/tell_scan.py`, with inline overrides that require a reason |
| Subagents and workbenches | Coordinator and delegate roles, a common report block, and `contract.json` for deterministic routing |

## Repository layout

```
SKILL.md              entry point: fast path, gate, modes, rules
contract.json         machine-readable modes, events, report, record, and output-check schema
modes/                one file per mode, numbered steps
references/           records rules, output checks, principles
assets/templates/     INDEX, VOLUME, LOG, QUEUE, AWAY-REPORT, BRIEF
scripts/              check_records.py, tell_scan.py (run by the agent)
agents/openai.yaml    Codex and ChatGPT presentation and policy
--- repository only (not packaged) ---
docs/integration.md   hooks, activation policy, workbench responsibilities
tools/                validate.py, package.py
evals/                trigger cases and regression tests for both scripts
```

## Install

| Host | Steps | Explicit call |
|---|---|---|
| claude.ai / Claude desktop | Download `praxteward.zip` from Releases (or run `python tools/package.py`) and upload it under Settings → Capabilities/Features → Skills. Requires code execution. | `praxteward <mode>`, `praxteward inspect` |
| Claude Code | `git clone https://github.com/2nugu/praxteward.git ~/.claude/skills/praxteward` (personal) or into `<project>/.claude/skills/praxteward` | `/praxteward` |
| Claude API | Upload the zip via the Skills API (`/v1/skills`); reference its `skill_id` in the container with the code execution tool | — |
| Codex CLI / IDE | `git clone https://github.com/2nugu/praxteward.git ~/.agents/skills/praxteward` (user) or into `<repo>/.agents/skills/praxteward`; restart Codex if it does not appear | `$praxteward` or `/skills` |
| ChatGPT | Distribute as a plugin, or create with `@skill-creator` from this folder | `@praxteward` |
| Custom workbench | Load `name` and `description` always, `SKILL.md` on trigger, a procedure per mode; route events via `contract.json` | `praxteward <mode>` |

Update git installs with `git pull`. Uploaded copies do not sync; re-upload after changes.

### Codex notes

- Skills are read from `.agents/skills` (searched from the working directory up to the repo root) and `~/.agents/skills`. Older Codex versions used `~/.codex/skills`.
- The initial skills list is capped at about 2% of the context window, and descriptions are shortened first when many skills are installed.
- Use `~/.codex/AGENTS.md` or a repo `AGENTS.md` for the global instructions below.
- Disable without deleting: add `[[skills.config]]` with `path = ".../praxteward/SKILL.md"` and `enabled = false` to `~/.codex/config.toml`.

## Project setup

Optional `.praxteward.yaml` at the project root:

```yaml
index: docs/INDEX.md
log: docs/LOG.md
queue: docs/QUEUE.md
volumes_dir: docs/volumes
activation: session      # auto | session | explicit
coverage_ignore:
  - "*.lock"
```

`activation: session` loads the skill once per session in projects with records; `auto` relies on description matching; `explicit` loads only when named. See [docs/integration.md](docs/integration.md) for hooks and trade-offs.

## Recommended global instructions

The skill holds procedures. Global instructions should hold the rules that apply even when the skill is not loaded, and say when to load it. Add or merge into your personal preferences (Claude) or `AGENTS.md` (Codex):

```markdown
# Adaptive Workflow & Learning (add or merge)

- Match workflow complexity to uncertainty and blast radius: handle local, reversible, fully specified changes directly, even when a project skill is loaded.
- Optimize for verified objective completion and total expected effort, including rework, not minimal immediate token usage.
- Act autonomously within authorized boundaries. Escalate consequential decisions rather than routine implementation details. Never drop a queued or mid-task request; apply amendments at the next safe point. When unattended, park decisions that need the operator and continue independent work.

# Project Continuity

Maintain two canonical records: **Project Documents** (intent, design rationale, indexed roadmap, acceptance criteria; each verified completion records the technique used, alternatives compared, rationale, verification evidence, and code locators, so later work need not re-read the implementation and the records can compile into a specification, operator manual, and report) and **Project Logs** (execution evidence, decisions, successful and failed procedures, and a compact recovery summary).

- Record work when it is verified, not at session end. Keep records concise and actionable rather than transcripts.
- On project start, session restart, or orientation requests, read the index and recovery summary before extensive code exploration.
- Before context loss, checkpoint; after interruption, reconcile records with actual artifacts and resume from the last verified checkpoint.
- In sessions working on a project with Praxteward records, load the Praxteward skill once at session start; it exits quickly for trivial tasks. If the skill is unavailable, apply the rules above minimally.
```

General judgment rules (objective reconstruction, evidence over agreement, scope discipline, verification) can live in your own instructions; otherwise the skill applies `references/principles.md`.

## Development

```bash
python tools/validate.py                  # package consistency
bash evals/run_record_tests.sh            # record-checker regression tests
bash evals/run_tell_tests.sh              # output-check regression tests
python scripts/tell_scan.py <files>       # check docs or code before delivery
python scripts/check_records.py <project-root> --since <git-ref>
python tools/package.py                   # dist/praxteward.zip
```

After changing the description or procedures, run the cases in `evals/trigger-cases.md` in fresh sessions.

## License

MIT. See [LICENSE](LICENSE).
