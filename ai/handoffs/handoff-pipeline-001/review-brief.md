# Review Brief: handoff-pipeline-001 / HANDOFF-002 + HANDOFF-003 + HANDOFF-004 + HANDOFF-005 + HANDOFF-006

## Scope

Review only `HANDOFF-002`, `HANDOFF-003`, `HANDOFF-004`, `HANDOFF-005`, and the scoped `HANDOFF-006` hardening items:

- `scripts/handoff_preflight.py`
- `scripts/orchestrator.py`
- `scripts/handoff_complete.py`
- `scripts/handoff_e2e.py`
- `scripts/hooks/post-commit`
- `scripts/install-hooks.sh`
- `scripts/handoff_status.py`
- `ai/decisions/ADR-009-handoff-status-execution-gates.md`
- `ai/schemas/handoff-status.schema.json`
- `ai/handoffs/handoff-pipeline-001/status.yaml`
- `ai/changes/2026-03-27-auto-handoff-mechanism.md`
- `ai/validation/2026-03-27-auto-handoff-mechanism.md`

## What Was Completed

- Added a stdlib-only preflight validator for handoff packages
- Added a minimal orchestrator that can start only from `handoff_status: pending`
- Canonicalized `handoff_status` as package execution state, not task lifecycle state
- Fixed the blocking `write_status_yaml` bug so valid packages may omit optional artifact keys before execution outputs exist
- Added legal transition enforcement in code, including reviewer-only writeback and the canonical `changes_requested -> pending` loop
- Added auditable `review.*` and `reopen.*` metadata plus `attempt` / `revision` counters
- Added a runnable E2E harness that exercises the canonical happy path, retry path, reviewer-only gate failures, illegal transitions, and `new_package_required` refusal
- Restored the deferred post-commit notification hook and wired it through `install-hooks.sh`
- Fixed the blocking review issue by tracking `scripts/hooks/post-commit` in git with executable mode
- Clarified in `ADR-009` that `planning_owner` or `review_owner` may reopen `changes_requested -> pending`
- Documented that `attempt` and `revision` are currently equivalent counters that increment together
- Verified `PASS` on the real package
- Verified FAIL when `execution-brief.md` is missing from a copied package
- Verified FAIL when a copied package is forced to `handoff_status: review_ready` under `--require-status pending`
- Verified a minimal package can run through orchestrator `--no-launch` without `KeyError` when optional artifact keys are absent
- Verified copied-package transitions for `complete`, `approve`, `request-changes`, `reopen`, and `close`
- Verified a full `PASS` matrix across all canonical E2E scenarios
- Verified the retry path preserves the first-round `review.*` block after the second-round `review_ready`
- Verified the installed post-commit hook surfaces the next action / orchestrator hint for pending packages
- Verified tracked executable state directly from the git index (`100755`) so the hook is reviewable as a real repository artifact, not only via temp-repo copy tests
- Kept the canonical package status at `pending`; this round validates the start gate and does not simulate completion

## Out of Scope

- HANDOFF-006 protocol / adapter updates

## Reviewer Focus

- Is the `handoff_status == pending` start gate explicit enough in both preflight and orchestrator?
- Is the split between handoff package states and task lifecycle states clear and safe?
- Is repo-relative / environment-derived worktree resolution sufficient without reintroducing absolute path coupling?
- Does `write_status_yaml` now tolerate valid packages that have not produced change / validation / review artifacts yet?
- Are reviewer-only transitions and the `changes_requested` reopen loop enforced in code rather than only described in ADRs?
- Is the same-package scope guard clear enough to prevent reusing a package when a new one is required?
- Does the E2E harness give a credible pass/fail matrix for the canonical happy path and retry path without pushing docs debt into this task?
- Is the deferred post-commit hook now sufficient as a notification-only layer without expanding orchestration behavior?
- Is the post-commit hook now correctly tracked and executable in the repo, not just installable after file-copy setup?
- Are reopen actor semantics and attempt/revision semantics now explicit enough in ADR-009?
- Are later sub-tasks still left out of scope?

## Canonical Path Matrix

| Path | Result | Notes |
|------|--------|-------|
| `pending -> in_progress -> review_ready -> approved -> closed` | PASS | `handoff_e2e.py` happy path |
| `pending -> in_progress -> review_ready -> changes_requested -> pending -> in_progress -> review_ready` | PASS | `handoff_e2e.py` retry path |
| non-reviewer approve / request-changes | PASS | both gates rejected `codex` and preserved package state |
| illegal transitions | PASS | invalid `complete`, `close`, and `reopen` attempts all failed |
| `new_package_required` refusal | PASS | package reuse refused and package state preserved |

## Final Review Decision

**Decision: APPROVED**

**Reviewer:** claude
**Date:** 2026-03-27

### Review History

| Sub-task | Review Round | Result | Notes |
|----------|-------------|--------|-------|
| HANDOFF-002 | 1 | APPROVED | preflight validator, stdlib-only |
| HANDOFF-003 | 1 + delta | APPROVED | orchestrator; delta fixed `write_status_yaml` KeyError on optional artifact keys |
| HANDOFF-004 | 1 | APPROVED | shared status helper + handoff_complete.py |
| HANDOFF-005 | 1 | APPROVED | E2E harness; undocumented scope change flagged (post-commit hook deferred to HANDOFF-006) |
| HANDOFF-006 | 1 + delta | APPROVED | post-commit hook, ADR-009 clarifications; delta fixed untracked hook (95fb3a9) |

### Blocking Issues Resolved

1. **HANDOFF-003**: `write_status_yaml` crashed on optional artifact keys → fixed with `.get(key, "")` pattern
2. **HANDOFF-006**: `scripts/hooks/post-commit` was untracked and lacked execute bit → tracked as `100755` in commit 95fb3a9

### Outstanding Debt (Out of Scope)

- AGENTS.md / CLAUDE.md / HANDOFF_PROTOCOL adapter rewrites
- WORKTREE_POLICY branch naming reconciliation (`handoff/<task-id>` vs `feat/<short-scope>`)
- Brief template governance files
- Phase 2 auto-trigger (Claude auto-pickup after review_ready)
- Live Codex launch integration test
