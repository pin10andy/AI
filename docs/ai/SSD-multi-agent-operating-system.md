# SSD: Multi-Agent Operating System

## Purpose

Describe how the repository implements the multi-agent operating model without
redefining domain governance that already exists in `ai/`.

## System Boundary

The operating system spans:

- canonical operating docs in `docs/ai/`
- domain source of truth in `ai/`
- thin adapters at repo root and `openclaw/agents/`
- minimal execution scripts in `scripts/`

## Source-of-Truth Split

### `docs/ai/`

Repository-level operating pack:

- PRD / SSD
- handoff protocol
- worktree policy
- validation levels
- memory governance
- template entrypoints

### `ai/`

Execution truth and domain truth:

- shared context, brand, playbooks, schemas, evals
- task / decision / change / validation records
- artifact policies and registries
- skill source and output artifacts

## Execution Flow

1. Read adapter file for the current agent
2. Load `docs/ai/` operating docs
3. Load task-relevant canonical files under `ai/`
4. Execute in an isolated worktree when the change is non-trivial
5. Produce or update task / change / validation artifacts
6. Run minimal validation checks
7. Hand off through artifacts only

## Repo Components

### Adapters

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `openclaw/agents/default-agent.yaml`

Adapters should only specify:

- what canonical docs to load
- agent-specific deployment or routing notes

### Runtime Records

- `ai/tasks/`
- `ai/decisions/`
- `ai/changes/`
- `ai/validation/`
- `ai/reports/`

### Governance

- `ai/policies/artifact-write-policy.md`
- `ai/policies/artifact-naming-policy.md`
- `ai/registry/storage-map.yaml`
- `ai/registry/artifacts.yaml`

### Scripts

- `scripts/sync-skills.sh`
- `scripts/install-hooks.sh`
- `scripts/check_artifact_governance.py`
- `scripts/validate_task_artifacts.py`

## Template Strategy

Canonical templates remain in their existing `ai/` locations when already present.
`docs/ai/templates/` provides stable discovery entrypoints so execution owners do
not need to remember each canonical path.

## Data and Memory Model

### Stable shared memory

- `ai/memory/shared-context.yaml`
- `ai/knowledge/`

### Execution memory

- tasks, changes, validations, reports, and decisions

### Non-canonical memory

- chat history
- scratch files
- local-only tool settings

## Validation Model

Validation is layered:

- structure and file existence
- linkage between task / change / validation artifacts
- tool-specific validation such as governance checks
- task-specific domain validation

Detailed levels are defined in `docs/ai/VALIDATION_LEVELS.md`.

## Conflict Handling

When `docs/ai/` and `ai/` appear to overlap:

1. keep domain/runtime rules in `ai/`
2. keep execution-pack rules in `docs/ai/`
3. record any unresolved boundary in the change record

## Minimal Tooling Rule

Add scripts only when they validate a real repository workflow gap.
No framework scaffolding is introduced without a task-backed need.
