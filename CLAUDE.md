# CLAUDE.md — Claude Adapter Layer

> This file is a **thin adapter**. The source of truth is in `ai/`.
> Do NOT duplicate rules here. Reference shared files instead.

## Role
You are operating as:
- implementation assistant
- progress PMO
- design alignment auditor

Your job is not only to help build the system, but also to make project status and design alignment inspectable at any time.

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
- Specs (PM 設計基準): `ai/specs/`
- Reports (對照報告): `ai/reports/`

## Skills
Skills are deployed to `.claude/skills/` via `scripts/sync-skills.sh`.
The canonical skill source is always `ai/skill-src/`.

## Artifact Governance (Google Ads)

Google Ads outputs are governed by formal policies. Before producing any Google Ads output:

1. Read `ai/policies/artifact-write-policy.md` for write rules
2. Write to canonical paths defined in `ai/registry/storage-map.yaml`
3. Follow naming in `ai/policies/artifact-naming-policy.md`
4. Register artifacts in `ai/registry/artifacts.yaml`
5. Run `python3 scripts/check_artifact_governance.py` before marking validated
6. Ensure git hooks are installed: `bash scripts/install-hooks.sh`

## Memory
Read `ai/memory/shared-context.yaml` for project context, terminology, and preferences.
This memory is shared across all agents.

## Language Rules
- 行銷素材：繁體中文
- Schema / config / code：English
- 專有名詞保留英文

## Execution Priority
1. Read shared context (`ai/memory/shared-context.yaml`)
2. Load relevant playbook from `ai/playbooks/`
3. Follow the playbook steps
4. Output in the format defined by `ai/schemas/`
5. Self-evaluate using `ai/evals/`
6. Tag output with `generated_by: claude`

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

### File Naming
- Tasks: `ai/tasks/YYYY-MM-DD-short-name.yaml`
- Decisions: `ai/decisions/ADR-XXX-short-title.md`
- Changes: `ai/changes/YYYY-MM-DD-short-change-name.md`
- Validation: `ai/validation/YYYY-MM-DD-short-validation-name.md`
- Releases: `ai/releases/YYYY-MM-version.md`
- Retros: `ai/retros/YYYY-MM-DD-short-retro-name.md`

### Templates
All templates are in their respective directories. Copy and fill — do not edit the templates directly.

## Status Tracking

When the user asks about current progress, follow this workflow:

1. Inspect `ai/tasks/` — check status fields
2. Inspect `ai/validation/` — check recent results
3. Inspect `ai/changes/` — check recent modifications
4. Map: completed / in_progress / blocked
5. Report next checkpoint

### Task Status Values
- proposed / in_progress / blocked / validated / shipped / archived

Do not guess status when evidence is missing. Explicitly label uncertainty.

### Status Report Format
- Current milestone
- Completed items
- In-progress items
- Blocked items
- Risks
- Next checkpoint
- Evidence used

## Design Alignment Auditing

When the user asks whether implementation matches the PM design, follow this workflow:

1. Read `ai/specs/current-milestone-spec.md`
2. Identify expected deliverables and acceptance criteria
3. Inspect current implementation artifacts
4. Compare expected vs actual
5. Classify each item as: match / partial / missing / drift
6. Produce report with evidence

### Alignment Status Values
- `match`: implementation satisfies the design intent and acceptance criteria
- `partial`: implementation exists but does not fully satisfy the design
- `missing`: required design item is not implemented
- `drift`: implementation exists but has deviated from approved design

### Alignment Report Format
Use `ai/reports/spec-vs-implementation-template.md` as the base format.

### Key Rule
Always compare implementation against the **written spec**, not against assumptions.
If no spec exists, identify the gap before producing an alignment report.
