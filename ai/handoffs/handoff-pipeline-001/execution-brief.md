# Execution Brief: handoff-pipeline-001

## Context

This repo uses Claude for planning and Codex for implementation. Currently the handoff between
them is manual: Claude outputs a plan in chat, the user switches to Codex and re-explains context.

This task builds the automated handoff mechanism so that after Claude writes planning artifacts
to the repo, an orchestrator script can immediately launch Codex with the right context —
and when Codex finishes, Claude is notified to review.

The full flow is:

```
Claude writes task.yaml + execution-brief.md + status.yaml(pending)
  → post-commit hook prints orchestrator command
  → user runs: python3 scripts/orchestrator.py --task <task-id>
  → orchestrator validates, creates worktree, launches Codex
  → Codex implements, writes changes + validation + review-brief
  → Codex runs: python3 scripts/handoff_complete.py --task <task-id>
  → handoff_complete updates status → review_ready, prints Claude review instructions
  → Claude reads review-brief and approves or requests changes
```

## Objective

Implement the six sub-tasks (HANDOFF-001 through HANDOFF-006) that build this mechanism.
HANDOFF-001 is already done (skeleton, templates, schema exist). Start from HANDOFF-002.

## Inputs

Read these before starting:

- `AGENTS.md` — your adapter, load order, and execution rules
- `docs/ai/HANDOFF_PROTOCOL.md` — current handoff protocol (you will update this)
- `docs/ai/WORKTREE_POLICY.md` — worktree rules you must follow
- `docs/ai/VALIDATION_LEVELS.md` — what counts as done
- `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml` — full task record with all sub-tasks
- `ai/handoffs/handoff-pipeline-001/status.yaml` — this handoff's state
- `ai/schemas/handoff-status.schema.json` — status.yaml schema (HANDOFF-001 output)
- `ai/handoffs/execution-brief-template.md` — template you'll reference in scripts
- `ai/handoffs/review-brief-template.md` — template you'll reference in scripts
- `scripts/hooks/pre-commit` — existing hook structure to understand before writing post-commit
- `scripts/install-hooks.sh` — understand how hooks are installed
- `scripts/validate_task_artifacts.py` — reference implementation for stdlib-only Python scripts

## Expected Outputs

| Path | Format | Sub-task |
|------|--------|----------|
| `scripts/handoff_preflight.py` | Python | HANDOFF-002 |
| `scripts/orchestrator.py` | Python | HANDOFF-003 |
| `scripts/handoff_complete.py` | Python | HANDOFF-004 |
| `scripts/hooks/post-commit` | Bash | HANDOFF-005 |
| `docs/ai/HANDOFF_PROTOCOL.md` | Markdown (update) | HANDOFF-006 |
| `AGENTS.md` | Markdown (update) | HANDOFF-006 |
| `CLAUDE.md` | Markdown (update) | HANDOFF-006 |
| `ai/changes/2026-03-27-auto-handoff-mechanism.md` | Markdown | you create |
| `ai/validation/2026-03-27-auto-handoff-mechanism.md` | Markdown | you create |
| `ai/handoffs/handoff-pipeline-001/review-brief.md` | Markdown | you create |

## Validation Criteria

- [ ] `python3 -m py_compile scripts/handoff_preflight.py` passes
- [ ] `python3 -m py_compile scripts/orchestrator.py` passes
- [ ] `python3 -m py_compile scripts/handoff_complete.py` passes
- [ ] `bash -n scripts/hooks/post-commit` passes
- [ ] `handoff_preflight.py` returns PASS on this handoff package
- [ ] `handoff_preflight.py` returns FAIL when execution-brief.md is missing
- [ ] `AGENTS.md` contains "Handoff Entry Point" section referencing execution-brief.md
- [ ] `CLAUDE.md` contains "Planning Output Convention" section
- [ ] `docs/ai/HANDOFF_PROTOCOL.md` contains mermaid sequence diagram of the full flow
- [ ] `python3 scripts/validate_task_artifacts.py` passes on this task's chain

## Constraints

- All Python scripts must be stdlib only (no pip installs)
- Do not modify `scripts/hooks/pre-commit` or any existing governance scripts
- Do not modify any files under `ai/` except to add change and validation records
- Do not modify `ai/schemas/handoff-status.schema.json` (already correct)
- Do not modify `ai/handoffs/execution-brief-template.md` or `review-brief-template.md`
- Keep each script focused: preflight only validates, orchestrator only orchestrates,
  handoff_complete only signals completion
- AGENTS.md and CLAUDE.md updates must remain thin — add sections, do not rewrite existing content

## Assumptions

These decisions are already made. Do not re-debate:

1. Orchestrator launches Codex via: `codex "<prompt>"` where prompt instructs Codex to read
   AGENTS.md then the execution brief. If the actual CLI syntax differs, note it in the
   change record and implement the closest equivalent.
2. Phase 1: `handoff_complete.py` prints review instructions to terminal only.
   RemoteTrigger-based auto-trigger is Phase 2 and out of scope here.
3. Worktree path pattern: `../ai-worktrees/<task-id>` relative to repo root.
4. `review-brief.md` is created as an empty-sectioned file by `handoff_complete.py`.
   Codex fills it BEFORE calling `handoff_complete.py` — the script does not generate content.
5. `post-commit` hook only prints a notification when pending handoffs are detected.
   It does not auto-execute the orchestrator.
6. HANDOFF-005 creates a new `scripts/hooks/post-commit` file.
   The existing `pre-commit` hook is not touched.
7. `install-hooks.sh` must be updated to also install the new post-commit hook.

## Execution Order

```
Phase 1: HANDOFF-002 (preflight) — no dependencies
         HANDOFF-004 (handoff_complete) — no dependencies

Phase 2: HANDOFF-003 (orchestrator) — needs HANDOFF-002
         HANDOFF-005 (post-commit hook) — needs HANDOFF-002

Phase 3: HANDOFF-006 (docs + adapters) — needs all scripts done
```

## Final Step

When all sub-tasks are complete:
1. Fill in `ai/handoffs/handoff-pipeline-001/review-brief.md`
2. Run: `python3 scripts/validate_task_artifacts.py --repo-root . --task ai/tasks/2026-03-27-auto-handoff-mechanism.yaml --change ai/changes/2026-03-27-auto-handoff-mechanism.md --validation ai/validation/2026-03-27-auto-handoff-mechanism.md`
3. Run: `python3 scripts/handoff_complete.py --task handoff-pipeline-001`
