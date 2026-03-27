# Artifact Migration — Phase 2 Validation Report

> **Date**: 2026-03-16
> **Scope**: Repo root legacy file triage (13 files)
> **Status**: validated
> **Executed by**: claude
> **Approval**: human (Phase 2 with archive-instead-of-delete requirement)

---

## Objective

Clear all repo-root Google Ads artifact failures from `check_artifact_governance.py`
without permanently deleting any files. All history must be preserved in a
location outside the official governed output tree.

---

## Migration / Archive Mapping Table

| # | Old path (repo root) | Action | New path | Rationale |
|---|---------------------|--------|----------|-----------|
| 1 | `LoveFu_pipeline_v1-1_rerun_builder.json` | MIGRATE | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-1/builder.json` | No governed version existed; v1.1 pipeline is a legitimate historical artifact |
| 2 | `LoveFu_pipeline_v1-1_rerun_interpreter.json` | MIGRATE | `.../pipeline/2026-03-15-pipeline-v1-1/interpreter.json` | Same |
| 3 | `LoveFu_pipeline_v1-1_rerun_packager.json` | MIGRATE | `.../pipeline/2026-03-15-pipeline-v1-1/packager.json` | Same |
| 4 | `LoveFu_pipeline_v1-1_rerun_packager.md` | MIGRATE | `.../pipeline/2026-03-15-pipeline-v1-1/packager.md` | Same |
| 5 | `LoveFu_pipeline_v1-1_full_rerun_report.md` | MIGRATE | `ai/reports/2026-03-15-pipeline-v1-1-full-rerun-report.md` | Report class; moved to ai/reports/ |
| 6 | `LoveFu_pipeline_v1-2_builder.json` | ARCHIVE | `scratch/google-ads/archive/2026-03-15-pipeline-v1-2-initial-run/` | Earlier run (portfolio_id=v1-2-initial); governed UAT rerun is canonical |
| 7 | `LoveFu_pipeline_v1-2_interpreter.json` | ARCHIVE | same | Same |
| 8 | `LoveFu_pipeline_v1-2_packager.json` | ARCHIVE | same | Same |
| 9 | `LoveFu_pipeline_v1-2_packager.md` | ARCHIVE | same | Same |
| 10 | `LoveFu_pipeline_v1-2_UAT_validation.md` | ARCHIVE | same | Earlier draft; governed validation is ai/validation/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md |
| 11 | `LoveFu_pipeline_v1-2_input_sufficiency.md` | ARCHIVE | same | Content subsumed in governed validation; preserved for reference |
| 12 | `LoveFu_山丘樂眠床_RSA新文案.md` | ARCHIVE | `scratch/google-ads/archive/2026-03-15-hillbed-rsa-proposals/` | Strategy proposal doc; CJK filename violates naming policy; not a pipeline deliverable |
| 13 | `LoveFu_山丘樂眠床_RSA新文案.xlsx` | ARCHIVE | same | Same |

---

## Checksum Verification

### Group A — Migrate (all checksums match source → target)

| File | Source MD5 | Target MD5 | Match |
|------|-----------|-----------|-------|
| builder.json | e66ebcd53a5666b9e1379d80ee6511fc | e66ebcd53a5666b9e1379d80ee6511fc | YES |
| interpreter.json | 2944c634b45661b25376126674d47a40 | 2944c634b45661b25376126674d47a40 | YES |
| packager.json | 145229a3f6e90f53ca182ddea63c0097 | 145229a3f6e90f53ca182ddea63c0097 | YES |
| packager.md | 00b4264f5487f59977a7b188fce8bed6 | 00b4264f5487f59977a7b188fce8bed6 | YES |
| full_rerun_report.md | 8ad9366636651c99f727c1e50b33e3b3 | 8ad9366636651c99f727c1e50b33e3b3 | YES |

### Group B — Archive (not exact duplicates of governed versions)

> These files are from the v1.2 **initial run** (generated 2026-03-15T16:09, portfolio_id=`lovefu-hillbed-search-rsa-2026q1-portfolio-v1-2`).
> The governed versions in `pipeline/2026-03-15-pipeline-v1-2-uat/` are from the **UAT rerun** (generated 2026-03-16T00:28, portfolio_id=`lovefu-hillbed-search-rsa-real-uat-v1-2`).
> They are related but distinct pipeline runs. Checksums intentionally differ.

| File | Archived MD5 | Governed MD5 | Relationship |
|------|-------------|-------------|-------------|
| builder.json | acf278f90edb57e07b19b3d82fb1eb07 | 3bb2fb63361b957f58ccb5d9ff99c524 | Different run (43KB vs 56KB) |
| interpreter.json | 7f2aa8a9a8b53d401b503dabb7400c31 | 2f31a3dc0d6b38fcccfeb497826cdb4d | Different run (217KB vs 265KB) |
| packager.json | 59638d9e6f94687f0d26476258638f30 | f3a430b558b83dafd68d95a10ef93bed | Different run (23KB vs 35KB) |
| packager.md | d1919b34435a5e2bf5041d1a5f53701b | 19f7fabc1ae84f2299940de92423958e | Different run (7.5KB vs 9.0KB) |
| UAT_validation.md | 57b4f9e37a2eb42a34f78a06059d2c40 | 3ac2f4eea02ef8f5a0f3f997f693e549 | Earlier draft (5.1KB vs 7.6KB) |
| input_sufficiency.md | 52ffdf0b66391501c6fba7945d7d7342 | n/a (content subsumed) | Subset |

### Group C — Archive (checksums verified, original filenames preserved)

| File | MD5 |
|------|-----|
| LoveFu_山丘樂眠床_RSA新文案.md | f49eac1d4b37e0c596020a76044b3b1d |
| LoveFu_山丘樂眠床_RSA新文案.xlsx | af876ecacc70c2b880a08d130c4a187b |

---

## Registry Updates

- New formal artifact registered: `2026-03-15-pipeline-v1-1.pipeline`
  - canonical_path: `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-1/`
  - files: builder.json, interpreter.json, packager.json, packager.md
  - status: validated
- `unregistered` section in artifacts.yaml replaced with `archived` section
  - 13 entries with original_path, archived_to, action, md5 checksums recorded

---

## Governance Check Result

```
Checks run: 8
Passed:     62
Failed:     0
Warnings:   14
Overall:    PASS
```

**Repo-root Google Ads artifact failures: 0** (was 13 before Phase 2)

Warnings (14) = 13 legacy flat files in `ai/outputs/` (Phase 1 retention copies) +
1 scratch directory notice. These are expected and not blocking.

---

## Archive Locations

All archived files are in `scratch/google-ads/archive/` — outside the official governed output tree.

```
scratch/google-ads/archive/
├── 2026-03-15-pipeline-v1-2-initial-run/   (6 files — v1.2 initial run)
│   ├── LoveFu_pipeline_v1-2_builder.json
│   ├── LoveFu_pipeline_v1-2_interpreter.json
│   ├── LoveFu_pipeline_v1-2_packager.json
│   ├── LoveFu_pipeline_v1-2_packager.md
│   ├── LoveFu_pipeline_v1-2_UAT_validation.md
│   └── LoveFu_pipeline_v1-2_input_sufficiency.md
└── 2026-03-15-hillbed-rsa-proposals/       (2 files — RSA strategy docs)
    ├── LoveFu_山丘樂眠床_RSA新文案.md
    └── LoveFu_山丘樂眠床_RSA新文案.xlsx
```

---

## What Remains Before Any Future Hard Deletion

### Group B archive (`scratch/google-ads/archive/2026-03-15-pipeline-v1-2-initial-run/`)

Before these 6 files can be permanently deleted:
1. Human sign-off confirming the v1.2 initial run data is no longer needed
2. Verify no active documents reference these specific files
3. Separate explicit approval authorizing deletion (this phase's approval does NOT cover deletion)

### Group C archive (`scratch/google-ads/archive/2026-03-15-hillbed-rsa-proposals/`)

Before these 2 files can be permanently deleted:
1. Confirm RSA strategy proposals are superseded and not referenced in active work
2. Separate explicit approval

### `ai/outputs/` flat files (Phase 1 retention copies — 13 files)

These were preserved during Phase 1 (copy-don't-delete policy).
Deletion requires Phase 3 of the migration plan with explicit approval.
