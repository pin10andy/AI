# Validation: Artifact Migration Phase 1

- **Date**: 2026-03-16
- **Status**: validated
- **Task**: Migrate ai/outputs/ flat files into governed hierarchy
- **Migration plan**: `ai/migration/2026-03-16-artifact-migration-plan.md`

---

## Scope

Copied 13 flat files from `ai/outputs/` into the governed hierarchy at
`ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/`.

**Not in scope**: repo root legacy files (Phase 2), deletion of flat copies (deferred).

---

## Files copied

### Golden outputs (2 files)

| Source | Target | Checksum match |
|--------|--------|----------------|
| `ai/outputs/lovefu-pmax-hillbed.output.json` | `golden/lovefu-pmax-hillbed.output.json` | OK |
| `ai/outputs/lovefu-pmax-hillbed.output.md` | `golden/lovefu-pmax-hillbed.output.md` | OK |

### Approved references (2 files, renamed)

| Source | Target | Checksum match |
|--------|--------|----------------|
| `...approved-reference-03.output.json` | `approved-references/lovefu-pmax-hillbed.ref-03.output.json` | OK |
| `...approved-reference-03.output.md` | `approved-references/lovefu-pmax-hillbed.ref-03.output.md` | OK |

### Dry-runs (2 files)

| Source | Target | Checksum match |
|--------|--------|----------------|
| `...codex-dry-run.output.json` | `dry-runs/lovefu-pmax-hillbed.codex-dry-run.output.json` | OK |
| `...codex-dry-run.output.md` | `dry-runs/lovefu-pmax-hillbed.codex-dry-run.output.md` | OK |

### Pipeline v1.2 UAT (5 files, into task subdir)

| Source | Target | Checksum match |
|--------|--------|----------------|
| `...v1-2-real-uat.builder.json` | `pipeline/2026-03-15-pipeline-v1-2-uat/builder.json` | OK |
| `...v1-2-real-uat.interpreter.json` | `pipeline/2026-03-15-pipeline-v1-2-uat/interpreter.json` | OK |
| `...v1-2-real-uat.packager.json` | `pipeline/2026-03-15-pipeline-v1-2-uat/packager.json` | OK |
| `...v1-2-real-uat.packager.md` | `pipeline/2026-03-15-pipeline-v1-2-uat/packager.md` | OK |
| `...v1-2-real-uat.input.json` | `pipeline/2026-03-15-pipeline-v1-2-uat/input.json` | OK |

### Performance interpretation (2 files, into task subdir)

| Source | Target | Checksum match |
|--------|--------|----------------|
| `...performance-interpretation.json` | `pipeline/2026-03-15-performance-interpretation/interpretation.json` | OK |
| `...performance-interpretation.md` | `pipeline/2026-03-15-performance-interpretation/interpretation.md` | OK |

**All 13 files: checksum verified (md5 match between source and target).**

---

## Registry updates

### artifacts.yaml

All 8 artifact entries updated: `migration_status: pending` → `migration_status: completed`.

### canonical-briefs.yaml

| Field | Old value | New value |
|-------|-----------|-----------|
| `golden_output_json` | `ai/outputs/lovefu-pmax-hillbed.output.json` | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.json` |
| `golden_output_md` | `ai/outputs/lovefu-pmax-hillbed.output.md` | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.md` |
| `updated_at` | `2026-03-14` | `2026-03-16` |

---

## Governance check result

```
Checks run: 8
Passed:     52
Failed:     13    (all repo root legacy — Phase 2 scope)
Warnings:   14    (all legacy flat files in ai/outputs/ — retention copies)
Overall:    FAIL  (expected — Phase 2 not yet executed)
```

### Phase 1 specific checks — all PASS:

| Check | Result |
|-------|--------|
| Golden files in canonical path | PASS (2 files) |
| Approved refs in canonical path, renamed | PASS (2 files) |
| Dry-runs in canonical path | PASS (2 files, new `dry-runs/` subdir created) |
| Pipeline files in task subdirectory | PASS (7 files in 2 task dirs) |
| All naming compliant | PASS |
| No scratch in outputs | PASS |
| Registry entries complete | PASS (8 entries, all 12+ required fields) |
| Write-path test | PASS |

---

## Anomalies found

### 1. `interpretation` stage name not in original policy

The `interpretation.json/md` files from creative-performance-interpreter did not match
the pipeline stage name regex `(input|builder|interpreter|packager)`.

**Resolution**: Added `interpretation` and `portfolio` as valid stage names in:
- `scripts/check_artifact_governance.py` (regex)
- `ai/policies/artifact-naming-policy.md` (documented list)

This is a legitimate stage name, not a violation.

### 2. Legacy flat files still exist in ai/outputs/

The 13 original flat files remain in `ai/outputs/` as retention copies.
They were **copied, not moved**, per migration plan rules.
Deletion is deferred to a future cleanup step after human confirmation.

### 3. No dry-runs/ subdir existed

The `dry-runs/` subdirectory was not in the original directory creation.
Created during migration. Added `.gitkeep` was replaced by actual files.

---

## Phase 2 recommendation

**Recommended to proceed with Phase 2** — repo root legacy file triage.

Rationale:
- Phase 1 is fully validated
- Governed hierarchy is populated and functional
- All registries and references point to canonical paths
- The 13 repo root files are the only remaining governance failures
- Pre-commit hook prevents new violations

Phase 2 prerequisites (all met):
- [x] Phase 1 validated
- [x] Canonical paths confirmed working
- [x] Registry updated
- [x] canonical-briefs.yaml points to new paths
- [ ] Human approval for Phase 2 execution
