# Artifact Migration Plan

> **Date**: 2026-03-16
> **Status**: proposed
> **Scope**: Migrate existing Google Ads artifacts to governed structure
> **Policy references**:
> - `ai/registry/storage-map.yaml`
> - `ai/registry/artifacts.yaml`
> - `ai/policies/artifact-naming-policy.md`
> - `ai/policies/artifact-write-policy.md`

---

## Principle

- **No files are moved or deleted without explicit human approval.**
- Migration is a copy-then-verify-then-remove process.
- All moves are tracked in this document and in `artifacts.yaml`.

---

## Phase 1: Migrate `ai/outputs/` flat files → governed hierarchy

These files are already in `ai/outputs/` but need to move into the
`ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/` hierarchy.

### Golden outputs

| Current path | Target path | Action |
|-------------|-------------|--------|
| `ai/outputs/lovefu-pmax-hillbed.output.json` | `.../evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.json` | copy → verify → update registry → remove original |
| `ai/outputs/lovefu-pmax-hillbed.output.md` | `.../evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.md` | same |

### Approved references

| Current path | Target path | Action |
|-------------|-------------|--------|
| `ai/outputs/lovefu-pmax-hillbed.approved-reference-03.output.json` | `.../approved-references/lovefu-pmax-hillbed.ref-03.output.json` | copy → rename → verify → remove original |
| `ai/outputs/lovefu-pmax-hillbed.approved-reference-03.output.md` | `.../approved-references/lovefu-pmax-hillbed.ref-03.output.md` | same |

### ~~Dry-runs~~ → Approved references (reclassified 2026-03-16)

| Current path | Target path | Action |
|-------------|-------------|--------|
| `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json` | `.../approved-references/lovefu-pmax-hillbed.ref-02.output.json` | copy → rename → verify → remove original |
| `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.md` | `.../approved-references/lovefu-pmax-hillbed.ref-02.output.md` | same |

### Pipeline v1.2 UAT

| Current path | Target path | Action |
|-------------|-------------|--------|
| `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json` | `.../pipeline/2026-03-15-pipeline-v1-2-uat/builder.json` | copy → rename → verify |
| `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.interpreter.json` | `.../pipeline/2026-03-15-pipeline-v1-2-uat/interpreter.json` | same |
| `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.json` | `.../pipeline/2026-03-15-pipeline-v1-2-uat/packager.json` | same |
| `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.md` | `.../pipeline/2026-03-15-pipeline-v1-2-uat/packager.md` | same |
| `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.input.json` | `.../pipeline/2026-03-15-pipeline-v1-2-uat/input.json` | same |

### Performance interpretation

| Current path | Target path | Action |
|-------------|-------------|--------|
| `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.json` | `.../pipeline/2026-03-15-performance-interpretation/interpretation.json` | copy → rename → verify |
| `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.md` | `.../pipeline/2026-03-15-performance-interpretation/interpretation.md` | same |

---

## Phase 2: Triage repo root scattered files

> **Status**: ready for human approval
> **Updated**: 2026-03-16 (post-normalization, refined analysis)

These 13 files were written to the repo root by agents that did not follow output path conventions.
Each file has been individually examined for content, duplication, and classification.

### Group A — v1.1 Pipeline: MIGRATE (5 files)

These are legitimate pipeline outputs from the v1.1 rerun. No governed version exists.

| # | Source file | Target path | Action |
|---|-----------|-------------|--------|
| 1 | `LoveFu_pipeline_v1-1_rerun_builder.json` | `.../pipeline/2026-03-15-pipeline-v1-1/builder.json` | copy → rename → register |
| 2 | `LoveFu_pipeline_v1-1_rerun_interpreter.json` | `.../pipeline/2026-03-15-pipeline-v1-1/interpreter.json` | same |
| 3 | `LoveFu_pipeline_v1-1_rerun_packager.json` | `.../pipeline/2026-03-15-pipeline-v1-1/packager.json` | same |
| 4 | `LoveFu_pipeline_v1-1_rerun_packager.md` | `.../pipeline/2026-03-15-pipeline-v1-1/packager.md` | same |
| 5 | `LoveFu_pipeline_v1-1_full_rerun_report.md` | `ai/reports/2026-03-15-pipeline-v1-1-full-rerun-report.md` | copy → rename |

Notes:
- Pipeline files go to `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-1/`
- Report goes to `ai/reports/` (reports are not registered in artifacts.yaml)
- New artifact registry entry needed for the pipeline run

### Group B — v1.2 Pipeline: ARCHIVE (6 files, earlier run)

> **Updated**: Group B action changed from DELETE to ARCHIVE per Phase 2 approval.
> **Finding**: These are NOT exact duplicates. They are from the v1.2 *initial* run
> (portfolio_id=`lovefu-hillbed-search-rsa-2026q1-portfolio-v1-2`, generated 2026-03-15T16:09).
> The governed versions are from the *UAT rerun* (portfolio_id=`lovefu-hillbed-search-rsa-real-uat-v1-2`,
> generated 2026-03-16T00:28). Different run IDs, different sizes, different checksums.

| # | Source file | Archive target | Archived MD5 | Governed MD5 | Relationship |
|---|-----------|----------------|-------------|-------------|-------------|
| 6 | `LoveFu_pipeline_v1-2_builder.json` | `scratch/google-ads/archive/2026-03-15-pipeline-v1-2-initial-run/` | `acf278f9...` | `3bb2fb63...` | Earlier run |
| 7 | `LoveFu_pipeline_v1-2_interpreter.json` | same | `7f2aa8a9...` | `2f31a3dc...` | Earlier run |
| 8 | `LoveFu_pipeline_v1-2_packager.json` | same | `59638d9e...` | `f3a430b5...` | Earlier run |
| 9 | `LoveFu_pipeline_v1-2_packager.md` | same | `d1919b34...` | `19f7fabc...` | Earlier run |
| 10 | `LoveFu_pipeline_v1-2_UAT_validation.md` | same | `57b4f9e3...` | `3ac2f4ee...` | Earlier draft |
| 11 | `LoveFu_pipeline_v1-2_input_sufficiency.md` | same | `52ffdf0b...` | n/a (subsumed) | Subset |

Notes:
- Files preserved in scratch — NOT deleted
- Original filenames preserved in archive for traceability
- Future hard deletion requires separate human approval

### Group C — RSA Deliverables: ARCHIVE (2 files)

These are ad-hoc strategy proposal documents predating the pipeline, not pipeline-produced deliverables.
They contain CJK filenames which violate naming policy.

| # | Source file | Target path | Action |
|---|-----------|-------------|--------|
| 12 | `LoveFu_山丘樂眠床_RSA新文案.md` | `scratch/google-ads/archive/2026-03-15-hillbed-rsa-proposals/` | copy (preserve original name) |
| 13 | `LoveFu_山丘樂眠床_RSA新文案.xlsx` | `scratch/google-ads/archive/2026-03-15-hillbed-rsa-proposals/` | same |

Notes:
- These are not formal deliverables — they're strategy brainstorm documents
- Archived to scratch with original filenames preserved (scratch has no naming governance)
- Not registered in artifacts.yaml (scratch is excluded from registry)

### Summary

| Action | Count | Files |
|--------|-------|-------|
| MIGRATE to governed path | 5 | v1.1 pipeline (4) + report (1) |
| ARCHIVE to scratch (earlier run) | 6 | v1.2 pipeline (4) + validation (2) |
| ARCHIVE to scratch (proposals) | 2 | RSA proposals (2) |
| **Total** | **13** | |

### Status

- [x] Phase 1 completed and validated
- [x] Normalization completed (dry-run → approved-reference, stage names updated)
- [x] Human approval received for Phase 2 (archive instead of delete)
- [x] Phase 2 executed — all 13 root files handled
- [x] Governance check re-run — see `ai/validation/2026-03-16-artifact-migration-phase-2.md`

### Pending: future hard deletion of Group B archive

Before Group B scratch files can be permanently deleted, the following must be true:
1. Human sign-off confirms the initial v1.2 run data is no longer needed
2. No references to those files remain in active docs
3. Separate approval explicitly authorizing deletion

---

## Phase 3: Handle `.tmp/` and testcases

| Location | Recommendation | Reason |
|----------|---------------|--------|
| `.tmp/google-ads-batch/` | Leave as-is or move to `scratch/google-ads/batch/` | Scratch by nature; no governance needed |
| `ai/testcases/google-ads/outputs/` | Leave as-is | Test outputs, governed by testcase structure |

---

## Phase 4: Update references after migration

After physical files are moved, update these references:

1. **`ai/registry/canonical-briefs.yaml`**
   - `golden_output_json` → new path
   - `golden_output_md` → new path

2. **`ai/registry/artifacts.yaml`**
   - Update `migration_status` from `pending` to `completed`
   - Remove `legacy_path` fields (or keep for audit trail)

3. **Any playbook/runbook** that hardcodes old paths

4. **Scripts** — check `scripts/google_ads_copy_pipeline_v12_real_uat_rerun.py` for hardcoded paths

---

## Execution checklist

- [ ] Phase 1: Human approves migration of `ai/outputs/` flat files
- [ ] Phase 1: Execute copy + verify + remove
- [ ] Phase 1: Update `artifacts.yaml` migration_status
- [ ] Phase 1: Update `canonical-briefs.yaml` golden output paths
- [ ] Phase 2: Human reviews root file triage recommendations
- [ ] Phase 2: Execute approved moves/archives/deletes
- [ ] Phase 3: Decide on `.tmp/` handling
- [ ] Phase 4: Update all references
- [ ] Phase 4: Verify no broken references remain
- [ ] Final: Human sign-off on migration completion
