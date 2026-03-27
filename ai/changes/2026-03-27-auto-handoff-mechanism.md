# Change Record: HANDOFF-002 through HANDOFF-006 handoff hardening, E2E validation, and hook notification

## Related Task

`handoff-pipeline-001` / `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`

## Summary

Implemented `HANDOFF-002` through `HANDOFF-006` within the assigned scope:
added a stdlib-only handoff preflight validator, added a gated orchestrator,
added a shared status parser/writer plus legal transition enforcement,
implemented reviewer writeback semantics in `handoff_complete.py`, codified the
canonical `changes_requested -> pending` loop, and added a runnable end-to-end
validation harness with canonical path coverage. This round also restores the
deferred post-commit notification hook, wires it through `install-hooks.sh`,
clarifies reopen actor and attempt/revision semantics in ADR-009, and keeps the
remaining adapter/doc rewrite debt out of scope.
This fix round only addresses the blocking review issue for `scripts/hooks/post-commit`:
the hook is now tracked in git with executable mode, and the review artifacts
record that index-level verification explicitly.

## Files Created

- `scripts/handoff_preflight.py`
- `scripts/handoff_status.py`
- `scripts/orchestrator.py`
- `scripts/handoff_complete.py`
- `scripts/handoff_e2e.py`
- `scripts/hooks/post-commit`
- `ai/decisions/ADR-009-handoff-status-execution-gates.md`
- `ai/changes/2026-03-27-auto-handoff-mechanism.md`
- `ai/validation/2026-03-27-auto-handoff-mechanism.md`
- `ai/handoffs/handoff-pipeline-001/review-brief.md`

## Files Updated

- `ai/tasks/2026-03-27-auto-handoff-mechanism.yaml`
- `ai/handoffs/handoff-pipeline-001/status.yaml`
- `ai/schemas/handoff-status.schema.json`
- `scripts/install-hooks.sh`

## Files Removed

- 無

## Commands Run

- `python3 -m py_compile scripts/handoff_preflight.py`
- `python3 -m py_compile scripts/handoff_status.py`
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
- `bash scripts/install-hooks.sh` in a copied temp repo and `.git/hooks/post-commit` with a pending package to verify hint output
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001` with `execution-brief.md` temporarily removed from a copied package
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001 --require-status pending` against a copied package with `handoff_status: review_ready`
- `python3 scripts/orchestrator.py --repo-root <copied-repo> --task handoff-pipeline-001 --dry-run` against a copied package with `execution_owner: claude`
- `python3 scripts/orchestrator.py --repo-root <copied-repo> --task handoff-pipeline-001 --dry-run` against a copied package with pre-populated `worktree_branch` / `worktree_path`
- `python3 scripts/orchestrator.py --repo-root <minimal-repo> --task handoff-pipeline-001 --no-launch --worktree-root <tmp-worktrees>` against a package whose `status.yaml` omits optional artifact keys
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> complete --task handoff-pipeline-001 --actor codex`
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> request-changes --task handoff-pipeline-001 --actor claude --reason "..." --required-change "..."`
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> request-changes --task handoff-pipeline-001 --actor codex --reason "..." --required-change "..."` to confirm reviewer-only enforcement
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> reopen --task handoff-pipeline-001 --actor claude --reopen-reason "..."`
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> approve --task handoff-pipeline-001 --actor codex` to confirm reviewer-only enforcement
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> approve --task handoff-pipeline-001 --actor claude --reason "..."`
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> close --task handoff-pipeline-001 --actor claude`
- `python3 scripts/handoff_complete.py --repo-root <copied-repo> request-changes --task handoff-pipeline-001 --actor claude --reason "..." --required-change "..." --scope-decision new_package_required` to confirm package-reuse refusal
- `python3 scripts/validate_task_artifacts.py --repo-root . --task ai/tasks/2026-03-27-auto-handoff-mechanism.yaml --change ai/changes/2026-03-27-auto-handoff-mechanism.md --validation ai/validation/2026-03-27-auto-handoff-mechanism.md`

## Assumptions

- `HANDOFF-002` may create a minimal `review-brief.md` manually so the package is reviewable, even though automated generation belongs to a later phase.
- `status.yaml.handoff_status` models package execution state, while `task.status` continues to model the broader task lifecycle.
- `worktree_path` should be stored repo-relative even when the orchestrator is invoked from a linked worktree.
- `status.yaml` may validly omit optional artifact keys before execution output exists.
- Same-package rework reuses the existing package only when reviewer-requested changes remain within the original package scope.
- The E2E harness may automate runtime-slot cleanup between retry attempts so the validation can prove a full retry loop without human intervention.
- `HANDOFF-005` intentionally delivered `handoff_e2e.py` before the post-commit hook because full flow proof was the blocking safety check; the hook was then recovered in `HANDOFF-006` as notification-only hardening.

## Sync / Deployment Impact

- No skill sync required.
- No hook installation changes.
- No adapter or governance files changed.

## Known Risks

- The preflight parser handles the current simple `status.yaml` structure and is not a general YAML parser.
- `orchestrator.py` currently assumes `codex "<prompt>"` is the closest viable CLI launch syntax and leaves room for later refinement if the CLI contract changes.
- The handoff scripts now depend on the repo's constrained status shape rather than a full YAML parser or JSON Schema runtime.
- The orchestrator default worktree root now derives from `git rev-parse --git-common-dir`; unusual git layouts may still need `AI_WORKTREE_ROOT` or `--worktree-root`.
- `handoff_complete.py` enforces legal transitions and actor ownership, but Phase 2 notification automation remains out of scope.
- `handoff_e2e.py` proves the canonical flows in isolated temp repos, but it is a validation harness rather than a user-facing runtime entry point.
- The post-commit hook is intentionally notification-only; it surfaces next actions but does not auto-run orchestrator.
- The original install test copied the hook into a temp repo before it was tracked; this fix closes that review gap by verifying tracked executable state in the git index.
- The review brief is intentionally minimal because full review automation belongs to later handoff phases.
- The repo still lacks the brief template files referenced by the execution brief; this task does not invent new template governance.

## Validation Evidence

- `python3 -m py_compile scripts/handoff_preflight.py` passed
- `python3 -m py_compile scripts/handoff_status.py` passed
- `python3 -m py_compile scripts/orchestrator.py` passed
- `python3 -m py_compile scripts/handoff_complete.py` passed
- `python3 -m py_compile scripts/handoff_e2e.py` passed
- `bash -n scripts/hooks/post-commit` passed
- `chmod +x scripts/hooks/post-commit` updated the file mode to executable
- `git add scripts/hooks/post-commit` staged the hook for tracking
- `git ls-files --stage scripts/hooks/post-commit` verified tracked mode `100755`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001` returned `PASS`
- `python3 scripts/handoff_preflight.py --repo-root . --task handoff-pipeline-001 --require-status pending` returned `PASS`
- `python3 scripts/orchestrator.py --repo-root . --task handoff-pipeline-001 --dry-run` returned `PASS`
- `python3 scripts/handoff_e2e.py` returned a full `PASS` matrix for the canonical happy path, retry path, reviewer-only gate failures, illegal transition failures, and `new_package_required` refusal path
- `bash scripts/install-hooks.sh` installed both `pre-commit` and `post-commit` in a copied temp repo, and `.git/hooks/post-commit` surfaced the pending handoff next-action hint
- The same command returned `FAIL` when the copied package was missing `execution-brief.md`
- The status-required preflight returned `FAIL` when the copied package was set to `review_ready`
- The orchestrator returned `FAIL` when the copied package was set to `execution_owner: claude`
- The orchestrator returned `FAIL` when the copied package already contained `worktree_branch` / `worktree_path`
- The orchestrator `--no-launch` path no longer raises `KeyError` when optional artifact keys are omitted from a valid minimal package
- `handoff_complete.py complete` transitioned a copied package from `in_progress` to `review_ready`
- `handoff_complete.py request-changes` wrote the required `review.*` fields and transitioned to `changes_requested`
- `handoff_complete.py request-changes` returned `FAIL` for non-reviewer actor `codex`
- `handoff_complete.py reopen` transitioned `changes_requested -> pending`, cleared worktree assignment, and incremented `attempt` / `revision`
- `handoff_complete.py approve` returned `FAIL` for non-reviewer actor `codex`, then `PASS` for reviewer actor `claude`
- `handoff_complete.py close` transitioned `approved -> closed`
- `handoff_complete.py request-changes --scope-decision new_package_required` returned `FAIL` and left the copied package in `review_ready`
- `python3 scripts/validate_task_artifacts.py ...` returned `PASS`

## Follow-ups

- AGENTS / CLAUDE / HANDOFF_PROTOCOL adapter/doc rewrites remain out of scope for this execution.
