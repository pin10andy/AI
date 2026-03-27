# Validation Record: HANDOFF-002 through HANDOFF-006 handoff hardening, E2E validation, and hook notification

## Related Task

`handoff-pipeline-001` / `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`

## Validation Level

Level 2

## What Was Tested

1. `scripts/handoff_status.py` parses and compiles
2. `scripts/handoff_preflight.py` parses and compiles
3. `scripts/orchestrator.py` parses and compiles
4. `scripts/handoff_complete.py` parses and compiles
5. `scripts/handoff_e2e.py` parses and compiles
6. `scripts/hooks/post-commit` parses with `bash -n`
7. `scripts/hooks/post-commit` is tracked in git with executable mode
8. the real `handoff-pipeline-001` package passes preflight
9. the real package passes preflight with `--require-status pending`
10. `scripts/orchestrator.py --dry-run` passes on the pending package
11. a copied package missing `execution-brief.md` fails preflight
12. a copied package with `handoff_status: review_ready` fails status-required preflight
13. a copied package with `execution_owner: claude` fails orchestrator gating
14. a copied package with pre-populated `worktree_branch` / `worktree_path` fails orchestrator gating
15. a minimal copied package that omits optional artifact keys can still pass orchestrator `--no-launch` without raising `KeyError`
16. `handoff_complete.py complete` enforces `in_progress -> review_ready` for the execution owner
17. `handoff_complete.py request-changes` writes the required review metadata and transitions `review_ready -> changes_requested`
18. `handoff_complete.py reopen` enforces `changes_requested -> pending`, clears worktree assignment, and increments `attempt` / `revision`
19. `handoff_complete.py request-changes` rejects non-reviewer actors
20. `handoff_complete.py approve` rejects non-reviewer actors and then allows reviewer `review_ready -> approved`
21. `handoff_complete.py close` enforces `approved -> closed`
22. `handoff_complete.py request-changes --scope-decision new_package_required` refuses package reuse and leaves the copied package unchanged
23. `handoff_e2e.py` returns a `PASS` matrix for the canonical happy path, retry path, reviewer-only gate failures, illegal transition failures, and `new_package_required` refusal path
24. the retry-path E2E proof preserves the first-round `review.*` block after the second-round `review_ready` state
25. `install-hooks.sh` installs the new `post-commit` hook in a copied temp repo
26. the installed post-commit hook surfaces the pending handoff next-action hint without auto-running orchestrator
27. the task / change / validation artifact chain passes linkage validation
28. status transition rules for `review_ready`, `changes_requested`, `validated`, and `shipped` are recorded in `ADR-009`

## Agents / Tools Involved

- codex
- shell
- python3
- bash

## Source of Truth Files

- `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`
- `ai/handoffs/handoff-pipeline-001/status.yaml`
- `ai/handoffs/handoff-pipeline-001/execution-brief.md`
- `ai/schemas/handoff-status.schema.json`
- `ai/decisions/ADR-009-handoff-status-execution-gates.md`
- `scripts/handoff_status.py`
- `scripts/handoff_complete.py`
- `scripts/handoff_e2e.py`
- `scripts/hooks/post-commit`
- `scripts/install-hooks.sh`
- `scripts/validate_task_artifacts.py`

## Commands Run

- `python3 -m py_compile scripts/handoff_status.py`
- `python3 -m py_compile scripts/handoff_preflight.py`
- `python3 -m py_compile scripts/orchestrator.py`
- `python3 -m py_compile scripts/handoff_complete.py`
- `python3 -m py_compile scripts/handoff_e2e.py`
- `bash -n scripts/hooks/post-commit`
- `chmod +x scripts/hooks/post-commit`
- `git add scripts/hooks/post-commit`
- `git ls-files --stage scripts/hooks/post-commit`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001 --require-status pending`
- `python3 scripts/orchestrator.py --repo-root . --task handoff-pipeline-001 --dry-run`
- `python3 scripts/handoff_e2e.py`
- `tmpdir=$(mktemp -d) && ... copy scripts/hooks + install-hooks.sh ... && bash scripts/install-hooks.sh && .git/hooks/post-commit`
- `python3 scripts/validate_task_artifacts.py --repo-root . --task ai/tasks/2026-03-27-auto-handoff-mechanism.yaml --change ai/changes/2026-03-27-auto-handoff-mechanism.md --validation ai/validation/2026-03-27-auto-handoff-mechanism.md`

## Result

PASS

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| status helper compile | ✓ | `python3 -m py_compile scripts/handoff_status.py` passed |
| preflight compile | ✓ | `python3 -m py_compile scripts/handoff_preflight.py` passed |
| orchestrator compile | ✓ | `python3 -m py_compile scripts/orchestrator.py` passed |
| handoff complete compile | ✓ | `python3 -m py_compile scripts/handoff_complete.py` passed |
| E2E harness compile | ✓ | `python3 -m py_compile scripts/handoff_e2e.py` passed |
| post-commit hook parse | ✓ | `bash -n scripts/hooks/post-commit` passed |
| post-commit tracked executable | ✓ | `git ls-files --stage scripts/hooks/post-commit` reported tracked mode `100755` after `chmod +x` and `git add` |
| real package preflight | ✓ | real handoff package returned `PASS` |
| pending status gate | ✓ | `--require-status pending` returned `PASS` on the canonical package |
| orchestrator dry-run | ✓ | derived branch/path and gating checks passed without launching Codex |
| missing execution brief fails | ✓ | copied package without `execution-brief.md` returned `FAIL` |
| non-pending gate fails | ✓ | copied package with `handoff_status: review_ready` returned `FAIL` under `--require-status pending` |
| owner conflict fails | ✓ | copied package with `execution_owner: claude` returned `FAIL` |
| worktree claim conflict fails | ✓ | copied package with populated `worktree_branch` / `worktree_path` returned `FAIL` |
| optional artifacts omitted | ✓ | minimal package ran through orchestrator `--no-launch` without `KeyError`; status rewrite filled empty optional keys |
| complete transition | ✓ | copied package transitioned `in_progress -> review_ready` and printed reviewer instructions |
| changes_requested writeback | ✓ | copied package wrote `review.requested_by`, `review.requested_at`, `review.reason`, and `review.required_changes[]` |
| reopen loop | ✓ | copied package transitioned `changes_requested -> pending`, cleared worktree assignment, and incremented `attempt` / `revision` from 1 to 2 |
| reviewer-only request changes | ✓ | non-reviewer `codex` was rejected for `review_ready -> changes_requested` |
| reviewer-only approval | ✓ | non-reviewer `codex` was rejected; reviewer `claude` transitioned `review_ready -> approved` |
| close transition | ✓ | copied package transitioned `approved -> closed` |
| out-of-scope rework refused | ✓ | `--scope-decision new_package_required` returned `FAIL` and left the package at `review_ready` |
| canonical path matrix | ✓ | `handoff_e2e.py` returned `PASS` for all five canonical scenarios |
| retry review block preserved | ✓ | second-round `review_ready` still retained first-round `review.decision/requested_by/requested_at/reason/scope_decision/required_changes` |
| hook install wiring | ✓ | `install-hooks.sh` installed `.git/hooks/post-commit` in a copied temp repo |
| post-commit next-action hint | ✓ | installed hook printed preflight + orchestrator hint for the pending package and did not auto-run it |
| task chain linkage | ✓ | `validate_task_artifacts.py` returned `PASS` |
| transition rules documented | ✓ | `ADR-009` defines `pending -> in_progress -> review_ready -> approved|changes_requested`, `changes_requested -> pending`, and `approved -> closed`, while separating task `validated` / `shipped` from handoff status |

## Canonical Path Matrix

| Path | Result | Notes |
|------|--------|-------|
| `pending -> in_progress -> review_ready -> approved -> closed` | PASS | exercised by `handoff_e2e.py` happy path |
| `pending -> in_progress -> review_ready -> changes_requested -> pending -> in_progress -> review_ready` | PASS | exercised by `handoff_e2e.py` retry path; harness automates runtime-slot cleanup between attempts |
| non-reviewer approve / request-changes | PASS | both commands returned `FAIL` and preserved package state |
| illegal transitions | PASS | `complete` on `pending`, `close` on `pending`, and `reopen` on `review_ready` all returned `FAIL` |
| out-of-scope rework refusal | PASS | `new_package_required` refused package reuse and left package in `review_ready`; follow-on `reopen` remained blocked |
| retry review metadata preservation | PASS | second-round `review_ready` retained the first-round `review.*` request block |

## Issues Found

- The handoff scripts intentionally support only the repository's constrained status shape; they are not a full YAML implementation.
- The orchestrator dry-run path is validated here; live Codex launch remains structurally implemented but not exercised in this scope.
- The default worktree root is now derived from git common-dir ancestry; non-standard repo layouts may still need explicit override.
- Optional artifact keys are still rewritten into `status.yaml` as empty strings after orchestrator claim so downstream tools keep a stable shape.
- The retry-path E2E proof currently uses automated runtime-slot cleanup inside the harness because branch/worktree reuse policy is still operational debt, not part of the canonical docs layer.
- The post-commit hook is notification-only by design; it intentionally does not auto-execute orchestrator.
- The earlier install verification copied the hook into a temp repo before it was tracked; this fix closes that review gap by recording tracked executable state directly from the git index.
- The repo still lacks the brief template files referenced by the execution brief; this task does not create new governance docs or template policy.
- Later follow-up work is limited to adapter/doc refinement, not new status semantics.

## Conclusion

`HANDOFF-002` through `HANDOFF-006` are implemented and self-validated within scope.
The handoff package remains executable only from `handoff_status: pending`, the
reviewer writeback path is now enforced in code, the canonical
`changes_requested -> pending` loop is auditable and increments `attempt` /
`revision`, the runnable E2E harness returns a full `PASS` matrix for the
canonical paths, the notification-only post-commit hook is installed and wired,
and the broader auto-handoff mechanism remains in progress.
