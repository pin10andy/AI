# Release: Handoff Pipeline v1

## Version / Milestone

handoff-pipeline-001 v1

## Date

2026-03-27

## Additions

- `scripts/handoff_preflight.py` — stdlib-only handoff package validator with `--require-status` gate
- `scripts/orchestrator.py` — gated orchestrator that starts execution only from `handoff_status: pending`, creates worktrees, and launches Codex
- `scripts/handoff_status.py` — shared status parser/writer with legal transition enforcement (`LEGAL_STATUS_TRANSITIONS`)
- `scripts/handoff_complete.py` — lifecycle subcommands: `complete`, `approve`, `request-changes`, `reopen`, `close`
- `scripts/handoff_e2e.py` — E2E validation harness covering 5 canonical scenarios (happy path, retry, reviewer gates, illegal transitions, scope refusal)
- `scripts/hooks/post-commit` — notification-only hook that surfaces pending handoff packages and next actions
- `scripts/install-hooks.sh` — updated to install both `pre-commit` and `post-commit` hooks
- `ai/decisions/ADR-009-handoff-status-execution-gates.md` — formal separation of package execution state vs task lifecycle state
- `ai/schemas/handoff-status.schema.json` — JSON Schema for `status.yaml`
- `ai/handoffs/handoff-pipeline-001/` — first canonical handoff package (execution-brief, status, review-brief)

## Fixes

- `write_status_yaml` KeyError on optional artifact keys (HANDOFF-003 delta)
- `scripts/hooks/post-commit` untracked and missing execute bit (HANDOFF-006 delta, 95fb3a9)

## Known Limitations

- Codex live launch (`codex "<prompt>"`) is structurally implemented but not exercised in validation
- AGENTS.md / CLAUDE.md / HANDOFF_PROTOCOL adapter rewrites remain deferred
- Brief template governance files not yet created
- WORKTREE_POLICY branch naming (`handoff/<task-id>` vs `feat/<short-scope>`) not yet reconciled
- Phase 2 auto-trigger (Claude auto-pickup after `review_ready`) not implemented
- Retry-path worktree/branch reuse policy is operational debt, automated only inside E2E harness

## Next Focus

- Adapter and protocol doc rewrites (AGENTS.md, CLAUDE.md, HANDOFF_PROTOCOL.md)
- Phase 2: automatic Claude review pickup on `review_ready` transition
- Live Codex integration test with real worktree creation
- Brief template governance and canonical examples
