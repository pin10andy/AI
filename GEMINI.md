# GEMINI.md — Gemini Adapter Layer

> This file is a **thin adapter**. The source of truth is in `ai/`.
> Do NOT duplicate rules here. Reference shared files instead.

## Role
You are operating inside a multi-agent workspace.
Your job is to read shared rules from `ai/` and execute tasks consistently.

## Source of Truth

### Shared Core
- Brand: `ai/brand/master-brand.yaml`
- Playbooks: `ai/playbooks/`
- Schemas: `ai/schemas/`
- Evaluation rubrics: `ai/evals/`
- Shared memory: `ai/memory/shared-context.yaml`
- Shared knowledge: `ai/knowledge/`
- Skill source: `ai/skill-src/`

### R&D Records
- Tasks: `ai/tasks/`
- Decisions (ADR): `ai/decisions/`
- Changes: `ai/changes/`
- Validation: `ai/validation/`
- Releases: `ai/releases/`
- Retros: `ai/retros/`

### Design & Status
- Specs (PM design baseline): `ai/specs/`
- Reports (alignment reports): `ai/reports/`

## Skills
Skills are in `ai/skill-src/`. Load them directly from source.

## Artifact Governance (Google Ads)

Google Ads outputs are governed by formal policies. Before producing any Google Ads output:

1. Read `ai/policies/artifact-write-policy.md` for write rules
2. Write to canonical paths defined in `ai/registry/storage-map.yaml`
3. Follow naming in `ai/policies/artifact-naming-policy.md`
4. Register artifacts in `ai/registry/artifacts.yaml`
5. Run `python3 scripts/check_artifact_governance.py` before marking validated

## Memory
Read `ai/memory/shared-context.yaml` for project context, terminology, and preferences.
This memory is shared across all agents.

## Language Rules
- Marketing assets: Traditional Chinese (zh-TW)
- Schema / config / code: English
- Proper nouns: keep in English

## Execution Priority
1. Read shared context (`ai/memory/shared-context.yaml`)
2. Load relevant playbook from `ai/playbooks/`
3. Follow the playbook steps
4. Output in the format defined by `ai/schemas/`
5. Self-evaluate using `ai/evals/`
6. Tag output with `generated_by: gemini`

## R&D Recording Rules

Every meaningful change must follow this chain:

```
task → decision (if architectural) → change → validation → status update
```

### Recording Policy
1. **Every real work maps to a task** — create under `ai/tasks/`
2. **Architectural choices need an ADR** — create under `ai/decisions/`
3. **Significant changes need a change record** — create under `ai/changes/`
4. **No validation = not done** — create under `ai/validation/`
5. **Status must be explicit** — use: proposed / in_progress / blocked / validated / shipped / archived

### Status Tracking
When asked about progress, inspect `ai/tasks/`, `ai/validation/`, `ai/changes/` and report based on evidence.

### Design Alignment
When asked whether implementation matches the PM design, compare against `ai/specs/current-milestone-spec.md`.
Classify items as: match / partial / missing / drift.
