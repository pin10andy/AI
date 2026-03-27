# Artifact Write Policy — Google Ads

> **Scope**: Google Ads workflow outputs only.
> **Effective**: 2026-03-16
> **Related files**:
> - Storage map: `ai/registry/storage-map.yaml`
> - Artifact registry: `ai/registry/artifacts.yaml`
> - Naming policy: `ai/policies/artifact-naming-policy.md`

---

## 1. Classification

Every file produced by a Google Ads workflow falls into exactly one class:

| Class | Location | Registered | Immutable | Description |
|-------|----------|------------|-----------|-------------|
| **Canonical input** | `ai/inputs/` | In `canonical-briefs.yaml` | Yes (version-controlled) | Briefs, schemas, brand definitions |
| **Formal output** | `ai/outputs/google-ads/...` | In `artifacts.yaml` | Depends on type | Golden, approved-ref, pipeline, deliverable |
| **Validation evidence** | `ai/validation/` | No | No | Verification reports, regression baselines |
| **Report** | `ai/reports/` | No | No | Analysis, drift, audit, review reports |
| **Scratch / temp** | `scratch/google-ads/` | No | No | Test runs, debug output, explorations |

---

## 2. Write rules

### Rule 1: Know your class before writing

Before creating any file, the agent MUST determine which class it belongs to.
If uncertain, default to **scratch**.

### Rule 2: Formal outputs require registration

Every file written to `ai/outputs/google-ads/` MUST have a corresponding entry
in `ai/registry/artifacts.yaml` with all required fields populated.

### Rule 3: Canonical inputs are protected

- Briefs in `ai/inputs/briefs/` MUST NOT be overwritten.
- To update a brief: increment version, record in `version_history`, run drift report first.
- This rule is enforced by `canonical-briefs.yaml` version policy.

### Rule 4: Golden outputs are immutable

- Once a golden output is approved, it MUST NOT be modified.
- To supersede: create a new golden output, mark the old one as `superseded` in the registry.

### Rule 5: Approved references are immutable

- Once approved, reference files MUST NOT be modified.
- New versions get a new sequence number (ref-04, ref-05, etc.).

### Rule 6: Pipeline outputs are grouped by task

- Pipeline stage files MUST be written into `pipeline/{task_id}/` subdirectory.
- Stage filenames are simple: `builder.json`, `interpreter.json`, `packager.json`, `input.json`.
- The task directory name provides all context (date, pipeline version, run type).

### Rule 7: No formal outputs in repo root

Writing any Google Ads output to the repository root directory is **prohibited**.
Agents that produce output must resolve the correct path from `storage-map.yaml`.

### Rule 8: No formal outputs in scratch

Files in `scratch/google-ads/` are never formal.
To promote a scratch file to formal status:
1. Copy (not move) to the governed path
2. Rename according to `artifact-naming-policy.md`
3. Register in `artifacts.yaml`

### Rule 9: Scratch is ephemeral

Files in `scratch/` may be deleted at any time without notice.
Never reference scratch files from formal artifacts, registries, or validation records.

---

## 3. Write workflow

When an agent completes a Google Ads task that produces formal output:

```
1. Determine artifact class
2. Resolve canonical path from storage-map.yaml
3. Generate filename per artifact-naming-policy.md
4. Write file to canonical path
5. Append entry to ai/registry/artifacts.yaml
6. If validation was performed, write to ai/validation/
7. If a report was generated, write to ai/reports/
```

### Pipeline-specific workflow

```
1. Create directory: pipeline/{task_id}/
2. Write each stage file into that directory
3. Register the pipeline run as a single artifact entry
   with a `files` list enumerating all stage files
```

---

## 4. Ownership and responsibility

| Role | Responsibility |
|------|---------------|
| **Agent (any)** | Follow write rules, register artifacts, write to correct path |
| **PM / human** | Approve golden outputs, approve references, trigger drift checks |
| **Governance auditor** | Verify registry completeness, check for unregistered files |

---

## 5. Multi-agent coordination

### Conflict avoidance

- Golden outputs and approved references are immutable — no write conflicts possible.
- Pipeline outputs are scoped by `{task_id}` — different tasks write to different directories.
- Approved references use sequence numbers (ref-01, ref-02) — no conflicts between agents.

### Agent identification

Every artifact entry in `artifacts.yaml` MUST include `generated_by` with the agent name.
Valid values: `claude`, `codex`, `gemini`, `openclaw`, `pipeline-v1.1`, `pipeline-v1.2`, `human`.

### Shared registry writes

When multiple agents need to append to `artifacts.yaml`:
- Each agent appends to the `artifacts` list — do not rewrite existing entries.
- If a conflict is detected, the later agent must re-read and retry.

---

## 6. Enforcement

### Automated enforcement (active)

**Pre-commit hook** — blocks commits that introduce governance violations:
- New Google Ads artifacts in repo root
- Naming violations in `ai/outputs/google-ads/`
- Scratch files inside `ai/outputs/`

Install: `bash scripts/install-hooks.sh`
Source: `scripts/hooks/pre-commit` (versioned, shared across team)

**Governance check script** — validates full compliance:
```bash
python3 scripts/check_artifact_governance.py
```

### Task lifecycle gate

A Google Ads task MUST NOT be marked `validated` or `shipped` unless:
1. `python3 scripts/check_artifact_governance.py` reports zero new FAIL items
2. All formal artifacts are registered in `ai/registry/artifacts.yaml`
3. The task's `validation.governance_check` field is set to `pass`

This gate is codified in:
- Runbook Step 7 (`ai/playbooks/lovefu-hillbed-pmax-runbook.md`)
- Task template (`ai/tasks/task-template.yaml`)

### Setup requirement

All contributors (human and agent) must run `bash scripts/install-hooks.sh` after cloning
or pulling the repo. This is listed in the runbook's prerequisites.

### Future enforcement (proposed)

- CI check for naming policy compliance on PR.
- Automated artifact registry validation on push.

---

## 7. Exceptions

If a legitimate reason exists to deviate from this policy:
1. Document the reason in the artifact's `notes` field.
2. Flag it for human review.
3. Do not use the exception as precedent — fix the policy if the exception is recurring.
