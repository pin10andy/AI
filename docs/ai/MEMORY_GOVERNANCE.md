# Memory Governance

## Purpose

Define which repository artifacts count as durable memory, which count as
execution evidence, and which are explicitly non-canonical.

## Memory Classes

### Shared stable memory

Use for facts and preferences that multiple agents should load by default.

Canonical locations:

- `ai/memory/shared-context.yaml`
- `ai/knowledge/`

### Execution memory

Use for work history that explains what changed and why.

Canonical locations:

- `ai/tasks/`
- `ai/decisions/`
- `ai/changes/`
- `ai/validation/`
- `ai/reports/`

### Domain registries

Use for operational truth that tools must read consistently.

Canonical locations:

- `ai/registry/`
- `ai/policies/`

## Non-Canonical Memory

The following must not be treated as source of truth:

- chat history
- scratch directories
- local settings such as `.claude/settings.local.json`
- generated deployment copies under `.claude/skills/`, `.agents/skills/`, `runtime/openclaw/`

## Write Rules

### Update `ai/memory/shared-context.yaml` only for:

- stable cross-agent preferences
- durable terminology
- project-wide context that should survive across tasks

### Do not put task-specific conclusions into shared memory

Task-specific decisions belong in:

- task records
- change records
- validation records
- reports

## Promotion Rule

If something begins in scratch or chat and later becomes durable:

1. promote it into a canonical file
2. cite the destination artifact in the change record
3. stop treating the original chat or scratch file as authoritative

## Review Rule

When memory boundaries are unclear, prefer:

- execution evidence in task/change/validation
- stable context in shared memory

Do not create a second memory ledger unless a new canonical need is documented.
