# ADR-008: Separate operating-pack docs from domain and runtime truth

## Status

accepted

## Background

The repository already used `ai/` as the home for domain rules, execution
records, playbooks, schemas, registries, and governed artifacts. A new
multi-agent operating pack was needed for repo-level collaboration rules such as:

- PRD / SSD for the repository operating model
- handoff protocol
- worktree policy
- validation levels
- memory governance

If those documents were added directly into `ai/`, the domain/runtime layer
would become mixed with repository meta-governance. If adapters kept restating
the rules instead, the system would drift into duplicated policy.

## Decision

Use a two-layer split:

- `docs/ai/` for operating-pack and collaboration docs
- `ai/` for domain truth and runtime truth

Under this decision:

- `docs/ai/` holds repo-level operating documents and template entrypoints
- `ai/` remains canonical for playbooks, schemas, evals, tasks, changes,
  validations, policies, registries, shared memory, skill source, and governed outputs
- adapter files stay thin and point to both layers instead of restating rules

## Rationale

This keeps responsibilities clear without creating a second domain policy system:

- repo-level operating rules become discoverable in one place
- existing canonical governance under `ai/` is preserved
- task/change/validation records stay with runtime truth instead of moving into docs
- adapters remain small and easier to keep aligned across tools

## Impact

- 影響的檔案：
  - `docs/ai/`
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `GEMINI.md`
- 影響的 agent：
  - claude
  - codex
  - gemini
  - openclaw
- 影響的流程：
  - operating-pack doc discovery
  - adapter loading order
  - review of canonical boundaries between docs and runtime artifacts

## Related

- Task: `ai/tasks/2026-03-27-multi-agent-operating-pack-implementation.yaml`
- Change: `ai/changes/2026-03-27-multi-agent-operating-pack-implementation.md`
- Validation: `ai/validation/2026-03-27-multi-agent-operating-pack-implementation.md`
