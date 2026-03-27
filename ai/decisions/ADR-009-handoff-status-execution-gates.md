# ADR-009: Treat handoff_status as execution-package state, not task lifecycle state

## Status

accepted

## Background

`handoff-pipeline-001` now has a package-level `status.yaml` plus a broader task
record in `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`.

Without a clear boundary between:

- package execution state
- task lifecycle state

the orchestrator can start from the wrong state, reviewers can misread
`review_ready`, `validated`, and `shipped` as interchangeable, and the
`changes_requested` loop has no auditable writeback semantics.

## Decision

`status.yaml.handoff_status` models the **handoff package execution state** only.
It does **not** replace `task.status` in `ai/tasks/`.

Canonical handoff package transitions:

1. `pending`
   - planning artifacts exist
   - orchestrator may start only from this state
2. `in_progress`
   - orchestrator has claimed execution
   - worktree branch and worktree path are assigned
3. `review_ready`
   - execution outputs exist and package is ready for reviewer pickup
4. `approved`
   - reviewer accepts the package
5. `changes_requested`
   - reviewer requests another execution round that still fits the original package scope
6. `closed`
   - handoff package is complete and no further review action is pending

Canonical transition edges:

- `pending -> in_progress`
- `in_progress -> review_ready`
- `review_ready -> approved`
- `review_ready -> changes_requested`
- `changes_requested -> pending`
- `approved -> closed`

`validated` and `shipped` remain **task lifecycle terms** in `ai/tasks/`.

- `validated` means the task has sufficient validation evidence
- `shipped` means the work has been integrated or delivered beyond review

Actor and writeback rules:

- The orchestrator may start only from `handoff_status == pending`
- `changes_requested` is not executable
- Only `review_owner` may write:
  - `review_ready -> approved`
  - `review_ready -> changes_requested`
- Reopening `changes_requested -> pending` must be explicit and auditable
- `planning_owner` or `review_owner` may perform the reopen
- Same-package rework increments both `attempt` and `revision`
- Today `attempt` and `revision` are intentionally equivalent counters; both increment together for auditability while preserving room for future separation if retry semantics diverge
- If requested changes exceed the original package scope, the reviewer must require a new package instead of reusing the old one

Required audit fields:

- For `changes_requested`:
  - `review.requested_by`
  - `review.requested_at`
  - `review.reason`
  - `review.required_changes[]`
- For reopen to `pending`:
  - `reopen.reopened_by`
  - `reopen.reopened_at`
  - `reopen.reopen_reason`

## Rationale

This separation lets the orchestrator gate safely:

- `handoff_status == pending` answers "may execution start?"
- `task.status` answers "what is the broader task lifecycle state?"

It also avoids using `review_ready` as a substitute for `validated` or `shipped`,
and keeps reviewer writeback semantics auditable in repo artifacts instead of chat.

Keeping `attempt` and `revision` equivalent for now makes retry evidence easy to
read in the status file without prematurely introducing a second set of
semantics.

## Impact

- 影響的檔案：
  - `ai/handoffs/handoff-pipeline-001/status.yaml`
  - `scripts/handoff_preflight.py`
  - `scripts/orchestrator.py`
  - `scripts/handoff_complete.py`
  - `scripts/hooks/post-commit`
  - `scripts/install-hooks.sh`
  - `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`
- 影響的 agent：
  - codex
  - claude
- 影響的流程：
  - preflight gating
  - orchestrator start rules
  - review pickup semantics
  - reviewer approval / changes_requested loop

## Related

- Task: `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`
- Change: `ai/changes/2026-03-27-auto-handoff-mechanism.md`
- Validation: `ai/validation/2026-03-27-auto-handoff-mechanism.md`
