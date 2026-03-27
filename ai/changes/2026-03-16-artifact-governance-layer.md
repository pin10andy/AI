# Change Record: Artifact Governance Layer

- **Date**: 2026-03-16
- **Status**: validated
- **Task**: Establish artifact governance for Google Ads outputs
- **Decision**: N/A (operational, not architectural)

---

## Summary

Introduced a formal artifact governance layer for Google Ads workflow outputs.
This addresses inconsistent naming, scattered storage, and lack of artifact
traceability across multiple agents (Claude, Codex, Gemini, OpenClaw).

## What changed

### New files created

| File | Purpose |
|------|---------|
| `ai/registry/storage-map.yaml` | Canonical storage paths for every artifact type |
| `ai/registry/artifacts.yaml` | Artifact registry with full field definitions and existing artifact inventory |
| `ai/policies/artifact-naming-policy.md` | Deterministic filename patterns for all artifact types |
| `ai/policies/artifact-write-policy.md` | Write rules, classification, multi-agent coordination |
| `ai/migration/2026-03-16-artifact-migration-plan.md` | Phased plan to migrate existing scattered files |

### New directories created

```
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/
├── golden/
├── approved-references/
├── pipeline/
└── deliverables/

scratch/google-ads/
```

### Files updated

| File | Change |
|------|--------|
| `ai/playbooks/lovefu-hillbed-pmax-runbook.md` | Added artifact governance reference section |

### Files NOT changed

- `ai/registry/canonical-briefs.yaml` — path updates deferred to migration execution
- `ai/registry/supported-matrix.yaml` — kept focused on support/readiness per policy decision
- All existing output files — no moves or deletes in this change

## Design decisions

1. **Scratch separated from outputs**: `scratch/google-ads/` is outside `ai/outputs/` to prevent governance confusion.
2. **Pipeline files grouped by task_id**: Each pipeline run gets its own subdirectory under `pipeline/`, not flat files.
3. **Lane includes message scope**: `evergreen-purchase-pmax` not just `purchase-pmax`.
4. **Storage concerns separated from supported-matrix**: `storage-map.yaml` owns paths; `supported-matrix.yaml` owns readiness.
5. **Migration is a separate document**: Not embedded in long-term policy.

## Impact

- All future Google Ads outputs must follow the new policies.
- Existing files remain in place until migration is approved and executed.
- All four agents must reference the governance layer before producing outputs.

## Verification

- [x] Directory structure created and accessible
- [x] Storage map covers all artifact types
- [x] Artifact registry documents all known existing artifacts
- [x] Naming policy covers all artifact types with examples
- [x] Write policy defines classification, rules, and workflow
- [x] Migration plan is phased with human checkpoints
- [x] No existing files moved or deleted
