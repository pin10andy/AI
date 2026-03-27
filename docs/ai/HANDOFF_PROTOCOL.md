# Handoff Protocol

## Purpose

Define how execution moves between agents or between sessions without relying on
 chat history as the official handoff channel.

## Core Rule

**Handoff happens through artifacts, not through chat logs.**

The minimum handoff chain is:

```
task -> decision (optional) -> change -> validation
```

## Required Handoff Package

For any non-trivial execution, the outgoing owner should leave:

1. a task record in `ai/tasks/`
2. a change record in `ai/changes/`
3. a validation record in `ai/validation/`
4. an ADR in `ai/decisions/` when the change alters architecture or canonical boundaries

## Handoff Read Order

The incoming owner should read in this order:

1. `docs/ai/PRD-multi-agent-operating-system.md`
2. `docs/ai/SSD-multi-agent-operating-system.md`
3. `docs/ai/WORKTREE_POLICY.md`
4. `docs/ai/VALIDATION_LEVELS.md`
5. task-specific records under `ai/tasks/`, `ai/changes/`, `ai/validation/`

## Mandatory Handoff Fields

Every non-trivial handoff should leave evidence for:

- objective
- touched files
- assumptions
- known risks
- follow-ups
- validation evidence

## Status Semantics

Use the task status values already defined by the canonical task template:

- `proposed`
- `in_progress`
- `blocked`
- `validated`
- `shipped`
- `archived`

Do not infer `validated` or `shipped` from discussion alone.

## Chat Usage Rule

Chat can explain context, but cannot replace:

- a task record
- a change record
- a validation record

If a decision matters later, it must be written into the repo.

## Review and Validation

When work is ready for review:

1. update the change record
2. draft or complete the validation record
3. attach review notes using the review template when needed

## Exceptions

If an execution owner must proceed with incomplete information:

1. make the smallest conservative assumption
2. record it in the change record
3. leave a follow-up item for review
