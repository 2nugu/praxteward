# Praxteward

An agent skill for doing substantial work of any kind well, and getting better at it: software, research, reports and presentations, data analysis, reverse engineering, or hobby projects. It plans the work, splits it into units, sets how deep each one goes, assigns owners (itself, parallel subagents, you, or a script), integrates and verifies the result, runs on its own within an authority you set, keeps everything recoverable across sessions, and learns from experience which ways of working to reuse, revise, retire, or automate. Small edits take a fast path.

Standard `SKILL.md` format. Works with Claude (claude.ai, Claude Code, API), OpenAI Codex and ChatGPT, and custom agent workbenches.

Self-contained: no other skills or packages are required. The scripts need Python 3.8+ (standard library only), and changed-file coverage needs git.

## What it does

| Need | How |
|---|---|
| Stay light on small tasks | A fast path at the top of `SKILL.md` handles local, reversible, fully specified changes directly |
| Plan before doing | Plan frames the goal, audience, and done criteria, then splits the work into units with output, depth, owner, dependencies, and a check |
| Go as deep as the work needs | Each unit is skim, standard, or deep; deep units run Explore: question ladder, competing hypotheses, primary sources, a discriminating check, a stop rule |
| Divide the work | Owners per unit: self, parallel subagents with briefs, the operator (batched questions at review points), or a script |
| Put it back together | Integrate merges units, resolves conflicts, checks the whole against the goal, and verifies end to end |
| Made for someone, not generated | Craft rules: an experience frame (who receives it, in what situation, what they do next), a swap test against generic content, real material instead of filler, and design rules for writing, slides, guides, charts, interfaces, code, and replies, plus a generic-feel review |
| Decide on purpose | Reason records options, evidence, and the condition that would reverse a decision |
| Work on its own, safely | Three settings (presence, authority A0 to A3, tempo) read from what you say, such as "keep going while I sleep" or "stop circling"; fixed limits it never crosses; a stalling rule; progress counted as verified units |
| Extend without editing the core | New domains arrive as practice cards (kinds: method, craft, check, automation) in a practice directory you own; the skill files stay unchanged |
| Learn how to work better | Practice cards capture ways of working with their conditions, assumptions, simpler alternative, and evidence. Learning fires only on signals (rework, corrections, failures, surprises, repeats, misfits); Distill, Evolve, and Automate promote, revise, retire, or automate cards by evidence, never by scanning everything |
| Keep long work recoverable | Orient, Checkpoint, Recover, Reconcile, Intake, Advance, and Compile handle sessions, interruptions, queues, unattended work, and final deliverables |
| Records worth reading | Work records state method, alternatives, rationale, verification, and `path::anchor` locators (symbol, heading, slide, cell, offset); `records: minimal` keeps only a log for casual work |
| Nothing missed | `scripts/check_records.py` checks fields, locators, registry, volume closure, and changed-file coverage |
| Output without machine tells | Block and Fix checks for prose and code, scanned by `scripts/tell_scan.py` |
| Subagents and workbenches | Coordinator and delegate roles, a common report block, and `contract.json` for deterministic routing |

## Repository layout

```
SKILL.md              entry point: fast path, work loop, depth, allocation, continuity, records, output
contract.json         machine-readable modes, events, report, record, and output-check schema
modes/                one procedure per mode (5 work, 7 continuity, 3 practice), numbered steps
references/           craft, records, practice, output checks, principles
assets/templates/     INDEX, VOLUME, LOG, QUEUE, AWAY-REPORT, BRIEF, CARD, PRACTICE-INDEX
scripts/              check_records.py, check_practice.py, tell_scan.py (run by the agent)
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
| Claude Code (plugin) | `claude plugin marketplace add 2nugu/praxteward` then `claude plugin install praxteward@praxteward`; update with `claude plugin update praxteward@praxteward` | `/praxteward:praxteward` |
| Claude Code (plain skill) | `git clone https://github.com/2nugu/praxteward.git ~/.claude/skills/praxteward` (personal) or into `<project>/.claude/skills/praxteward` | `/praxteward` |
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
records: standard        # minimal | standard
activation: session      # auto | session | explicit
practice_dir: ~/.praxteward/practice   # general practice cards (optional)
coverage_ignore:
  - "*.lock"
```

`activation: session` loads the skill once per session in projects with records; `auto` relies on description matching; `explicit` loads only when named. See [docs/integration.md](docs/integration.md) for hooks and trade-offs.

## Recommended global instructions

The skill holds procedures. Global instructions only need the rules that apply when the skill is not loaded, and when to load it. Add to your personal preferences (Claude) or `AGENTS.md` (Codex):

```markdown
- Long-running projects: use the Praxteward skill, loaded once per session. Without it, read the project index and recovery summary first, and record verified work with evidence and locators.
- Handle local, reversible, fully specified changes directly, even when a project skill is loaded.
- Never drop a queued or mid-task request. When unattended, park decisions that need me and continue independent work.
```

General judgment rules (objective reconstruction, evidence over agreement, scope discipline, verification) can live in your own instructions; otherwise the skill applies `references/principles.md`.

## Development

```bash
python tools/validate.py                  # package consistency
bash evals/run_record_tests.sh            # record-checker regression tests
bash evals/run_tell_tests.sh              # output-check regression tests
bash evals/run_practice_tests.sh          # practice-card regression tests
python scripts/tell_scan.py <files>       # check docs or code before delivery
python scripts/check_records.py <project-root> --since <git-ref>
python tools/package.py                   # dist/praxteward.zip
```

After changing the description or procedures, run the cases in `evals/trigger-cases.md` in fresh sessions.

## License

MIT. See [LICENSE](LICENSE).
