# Praxteward

An agent skill for substantial work of any kind: software, research, reports and presentations, data analysis, reverse engineering, or hobby projects. It plans the work, splits it into units, sets how deep each one goes, assigns owners (itself, parallel subagents, you, or a script), integrates and verifies the result, runs on its own within an authority you set, keeps the work recoverable across sessions, and learns from experience which ways of working to reuse, revise, retire, or automate. Small edits take a fast path.

Standard [Agent Skills](https://agentskills.io/specification) format. The scripts need Python 3.8+ (standard library only), and changed-file coverage needs git.

## What it does

| Area | Contents |
|---|---|
| Work loop | Plan, Explore, Reason, Execute, Integrate; a depth per unit (skim, standard, deep); one owner per unit |
| Autonomy | Presence, authority A0 to A3, and tempo, read from what you say ("keep going while I sleep", "stop circling"); fixed limits; a stalling rule |
| Continuity | Orient, Checkpoint, Recover, Reconcile, Intake, Advance, Compile; work and decision records with `path::anchor` locators, or a log only with `records: minimal` |
| Craft | An experience frame, a swap test against generic content, form by genre and medium, design principles and visual rules with measured contrast checks |
| Practice | Cards that capture ways of working with their conditions and evidence; Distill, Evolve, and Automate run on signals, never by scanning everything |
| Output checks | Block and Fix checks for prose and code, English and Korean; a change rate when revising someone's text |
| Lean code | `praxteward lean lite\|full\|ultra\|off`, `review`, `audit`, `debt`: the smallest complete change, never cutting validation, data-loss handling, security, or accessibility |
| Web pages | `praxteward web`: copy first, a dealt palette, type pairing, and hero, a starter page, static and four-width browser checks |
| Korean prose | `praxteward humanize`: pattern diagnosis by severity and genre, revision routes, and meaning gates on numbers, quotations, and change rate |

## Repository layout

```
SKILL.md              entry point
modes/                one procedure per mode (5 work, 7 continuity, 3 practice), numbered steps
references/           craft, design, output checks, records, practice, principles, lean, web, korean
assets/templates/     INDEX, VOLUME, LOG, QUEUE, AWAY-REPORT, BRIEF, CARD, PRACTICE-INDEX
assets/web/           palettes, type pairings, starter page and stylesheet
scripts/              check_records, check_practice, tell_scan, contrast, ko_scan, debt_scan, page_check, deal
--- repository only (not packaged) ---
docs/integration.md   activation policy and session hooks
tools/                validate.py, package.py
evals/                eval_queries.json (triggering), evals.json (behavior), trigger-cases.md,
                      regression tests per script, Korean calibration, recorded results
```

## Install

| Host | Steps | Explicit call |
|---|---|---|
| claude.ai / Claude desktop | Run `python tools/package.py` and upload `dist/praxteward.zip` under Settings → Capabilities → Skills. Requires code execution. | `praxteward <mode>`, `praxteward inspect` |
| Claude Code (plugin) | `claude plugin marketplace add 2nugu/praxteward` then `claude plugin install praxteward@praxteward` | `/praxteward:praxteward` |
| Claude Code (plain skill) | `git clone https://github.com/2nugu/praxteward.git ~/.claude/skills/praxteward` (personal) or into `<project>/.claude/skills/praxteward` | `/praxteward` |
| Claude API | Upload the zip via the Skills API (`/v1/skills`); reference its `skill_id` in the container with the code execution tool | — |
| Codex CLI / IDE | `git clone https://github.com/2nugu/praxteward.git ~/.agents/skills/praxteward` (user) or into `<repo>/.agents/skills/praxteward` | `$praxteward` |

The skill directory must be named `praxteward`, matching `name` in `SKILL.md`. Update git installs with `git pull`. Uploaded copies do not sync; re-upload after changes.

## Project setup

Optional `.praxteward.yaml` at the project root:

```yaml
index: docs/INDEX.md
log: docs/LOG.md
queue: docs/QUEUE.md
volumes_dir: docs/volumes
records: standard        # minimal | standard
activation: session      # auto | session | explicit
practice_dir: ~/.praxteward/practice   # general practice cards (optional)
coverage_ignore:
  - "*.lock"
```

`activation: session` loads the skill once per session in projects with records; `auto` relies on description matching; `explicit` loads only when named. See [docs/integration.md](docs/integration.md) for the hooks.

## Recommended global instructions

The skill holds procedures. Global instructions only need the rules that apply when the skill is not loaded, and when to load it. Add to your personal preferences (Claude) or `AGENTS.md` (Codex):

```markdown
- Long-running projects: use the Praxteward skill, loaded once per session. Without it, read the project index and recovery summary first, and record verified work with evidence and locators.
- Handle local, reversible, fully specified changes directly, even when a project skill is loaded.
- Never drop a queued or mid-task request. When unattended, park decisions that need me and continue independent work.
```

## Development

```bash
python tools/validate.py                  # spec frontmatter, links, mode and template consistency, manifests, fingerprint
bash evals/run_record_tests.sh            # check_records
bash evals/run_tell_tests.sh              # tell_scan
bash evals/run_practice_tests.sh          # check_practice
bash evals/run_design_tests.sh            # contrast
bash evals/run_toolkit_tests.sh           # ko_scan, debt_scan, deal, page_check
python evals/korean/calibrate.py --ids    # ko_scan on human vs generated Korean
python tools/package.py                   # dist/praxteward.zip
```

Every script prints its usage with `--help`.

A change to the description or the procedures is kept on measurement, not on argument:

- Triggering: `evals/eval_queries.json` holds queries with `should_trigger` and a fixed `train` or `validation` split. Run each query three times in a fresh session; it passes when the trigger rate is at least 0.5 for a positive and below 0.5 for a negative. Edit the description from train failures only, and choose the version by its validation pass rate.
- Behavior: `evals/evals.json` holds a prompt, fixture files, and assertions per case. Run the affected cases with the skill and without it (or against the previous version), and grade each assertion with its evidence. Give the grader the request and the raw artifacts, never the expected answer, and run the task checks yourself. An assertion that passes in both configurations measures nothing: drop it or sharpen it.
- Keep or discard: keep a change that raises the pass rate. At an equal pass rate, keep the shorter version. Try deletions as readily as additions; text whose removal changes no result goes.
- Record each run under `evals/results/` as `YYYY-MM-DD-<topic>.json` with the package fingerprint from `validate.py`, the model, observed results, operator interventions, and unchecked boundaries. A passing script regression suite is not behavioral evidence.

`validate.py <installed-skill-dir>` fingerprints an installed copy for comparison.

## Privacy and code execution

- Praxteward collects no personal data and sends nothing off the machine. It reads the project files the user points it to and writes its records (`docs/`, and practice cards in `practice_dir` when set) inside the user's own directories.
- The skill tells the agent to run the Python scripts bundled in `scripts/`, locally, on the files being checked. They use the standard library only, make no network requests, and read no credentials. `check_records.py` runs read-only `git` commands; `page_check.py --render` uses a locally installed Playwright when one exists.
- The plugin declares no MCP servers and no hooks.
- Development files outside the skill (`evals/`, `tools/`) are not run by the skill. `evals/korean/calibrate.py`, when a developer runs it, downloads public Korean Wikipedia and Wikinews text for calibration.

## License

MIT. See [LICENSE](LICENSE).
