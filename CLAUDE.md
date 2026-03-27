# CLAUDE.md — Claude Adapter Layer

> Thin adapter only. Do not duplicate canonical rules here.

## Load Order

1. `docs/ai/PRD-multi-agent-operating-system.md`
2. `docs/ai/SSD-multi-agent-operating-system.md`
3. `docs/ai/HANDOFF_PROTOCOL.md`
4. `docs/ai/WORKTREE_POLICY.md`
5. `docs/ai/VALIDATION_LEVELS.md`
6. `docs/ai/MEMORY_GOVERNANCE.md`
7. `ai/memory/shared-context.yaml`

## Canonical Paths

- Domain truth: `ai/`
- Shared memory: `ai/memory/shared-context.yaml`
- Playbooks: `ai/playbooks/`
- Schemas and evals: `ai/schemas/`, `ai/evals/`
- Task chain: `ai/tasks/`, `ai/decisions/`, `ai/changes/`, `ai/validation/`
- Reports and specs: `ai/reports/`, `ai/specs/`
- Skill source: `ai/skill-src/`

## Claude-Specific Notes

- Deployed Claude skills live in `.claude/skills/`
- Canonical skill edits always happen in `ai/skill-src/`
- Sync deployed skills with `bash scripts/sync-skills.sh`
- Install shared git hooks with `bash scripts/install-hooks.sh` when governance enforcement is needed
- For non-trivial changes, use an isolated worktree per `docs/ai/WORKTREE_POLICY.md`

## Governance References

For Google Ads outputs, follow:

1. `ai/policies/artifact-write-policy.md`
2. `ai/policies/artifact-naming-policy.md`
3. `ai/registry/storage-map.yaml`
4. `ai/registry/artifacts.yaml`
5. `python3 scripts/check_artifact_governance.py`

For task linkage validation, use:

- `python3 scripts/validate_task_artifacts.py ...`

## Execution Rule

Implement from canonical docs and repo artifacts.
Do not treat chat history as formal source of truth.
