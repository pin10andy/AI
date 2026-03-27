# Change Record: HANDOFF-002 preflight validator

## Related Task

`handoff-pipeline-001` / `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`

## Summary

Implemented `HANDOFF-002` only: added a stdlib-only handoff preflight validator,
created a review-ready handoff package for this scope, and updated planning
artifacts so the package can be reviewed without relying on chat history.

## Files Created

- `scripts/handoff_preflight.py`
- `ai/changes/2026-03-27-auto-handoff-mechanism.md`
- `ai/validation/2026-03-27-auto-handoff-mechanism.md`
- `ai/handoffs/handoff-pipeline-001/review-brief.md`

## Files Updated

- `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`
- `ai/handoffs/handoff-pipeline-001/status.yaml`

## Files Removed

- 無

## Commands Run

- `python3 -m py_compile scripts/handoff_preflight.py`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001` with `execution-brief.md` temporarily removed from a copied package
- `python3 scripts/validate_task_artifacts.py --repo-root . --task ai/tasks/2026-03-27-auto-handoff-mechanism.yaml --change ai/changes/2026-03-27-auto-handoff-mechanism.md --validation ai/validation/2026-03-27-auto-handoff-mechanism.md`

## Assumptions

- `review_ready` in `status.yaml` is the repo-canonical equivalent of the requested `ready_for_review` transition, because the schema enum already defines `review_ready`.
- `HANDOFF-002` may create a minimal `review-brief.md` manually so the package is reviewable, even though automated generation belongs to a later phase.
- `HANDOFF-003`, `HANDOFF-004`, `HANDOFF-005`, and `HANDOFF-006` remain out of scope for this execution and are not implemented here.

## Sync / Deployment Impact

- No skill sync required.
- No hook installation changes.
- No adapter or governance files changed.

## Known Risks

- The preflight parser handles the current simple `status.yaml` structure and is not a general YAML parser.
- `status.yaml` now points to a worktree path that is valid for this execution environment but may differ on another machine.
- The review brief is intentionally minimal because full review automation belongs to later handoff phases.

## Validation Evidence

- `python3 -m py_compile scripts/handoff_preflight.py` passed
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001` returned `PASS`
- The same command returned `FAIL` when the copied package was missing `execution-brief.md`
- `python3 scripts/validate_task_artifacts.py ...` returned `PASS`

## Follow-ups

- HANDOFF-003 should consume the same `status.yaml` and `review_ready` semantics without changing governance.
- HANDOFF-004 should take over review-brief generation/update in the full flow.
- HANDOFF-005 and HANDOFF-006 remain blocked until later phases.
