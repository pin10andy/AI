# Validation: Artifact Governance Enforcement

- **Date**: 2026-03-16
- **Status**: validated
- **Task**: Enforce artifact governance as operational gate for Google Ads lane
- **Script**: `scripts/check_artifact_governance.py`

---

## Test scope

Validated that the artifact governance layer (v1, established 2026-03-16) is
operationally enforceable for the `evergreen-purchase-pmax` production lane.

### What was tested

| Check | Target | Result |
|-------|--------|--------|
| No Google Ads artifacts in repo root | Repo root directory | **FAIL** — 13 legacy files detected |
| Canonical directory structure | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/` | **PASS** — all 4 subdirs present |
| Artifact naming compliance | Files inside canonical paths | **PASS** — dirs empty pre-migration, no violations |
| No scratch in official outputs | `ai/outputs/google-ads/` | **PASS** — clean |
| Registry field completeness | `ai/registry/artifacts.yaml` | **PASS** — all 8 entries have all 12 required fields |
| Legacy flat outputs inventory | `ai/outputs/` flat files | **WARN** — 13 legacy flat files pending migration |
| Validation file naming | `ai/validation/` | **PASS** — all 16 files follow `YYYY-MM-DD-{slug}.md` |
| Write-path test | Write to golden/, pipeline/, deliverables/, scratch/, validation/ | **PASS** — all 5 paths writable |

### Summary

| Metric | Value |
|--------|-------|
| Checks run | 8 |
| Passed assertions | 38 |
| Failed assertions | 13 |
| Warnings | 15 |
| Overall | **FAIL** (expected — legacy files not yet migrated) |

---

## Write-path test details

Simulated a full write cycle for the production lane:

1. **Golden output** → `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/`
   - Write: OK
   - Naming check: pattern `{brief_id}.output.{json|md}` validated

2. **Pipeline stage output** → `.../pipeline/2026-03-16-governance-test/builder.json`
   - Directory creation: OK
   - Stage file naming: OK (matches `{stage}.{json|md}`)
   - Cleanup: OK

3. **Deliverable** → `.../deliverables/`
   - Write: OK

4. **Scratch** → `scratch/google-ads/`
   - Write: OK
   - Confirmed: separate from `ai/outputs/`

5. **Validation evidence** → `ai/validation/`
   - Write: OK

---

## Failures explained

All 13 failures are **legacy repo root files** that predate the governance layer:

| # | File | Classification |
|---|------|---------------|
| 1 | `LoveFu_pipeline_v1-1_rerun_builder.json` | legacy pipeline output |
| 2 | `LoveFu_pipeline_v1-1_rerun_interpreter.json` | legacy pipeline output |
| 3 | `LoveFu_pipeline_v1-1_rerun_packager.json` | legacy pipeline output |
| 4 | `LoveFu_pipeline_v1-1_rerun_packager.md` | legacy pipeline output |
| 5 | `LoveFu_pipeline_v1-1_full_rerun_report.md` | legacy report |
| 6 | `LoveFu_pipeline_v1-2_builder.json` | legacy pipeline output |
| 7 | `LoveFu_pipeline_v1-2_interpreter.json` | legacy pipeline output |
| 8 | `LoveFu_pipeline_v1-2_packager.json` | legacy pipeline output |
| 9 | `LoveFu_pipeline_v1-2_packager.md` | legacy pipeline output |
| 10 | `LoveFu_pipeline_v1-2_UAT_validation.md` | legacy validation |
| 11 | `LoveFu_pipeline_v1-2_input_sufficiency.md` | legacy validation |
| 12 | `LoveFu_山丘樂眠床_RSA新文案.md` | legacy deliverable (CJK filename) |
| 13 | `LoveFu_山丘樂眠床_RSA新文案.xlsx` | legacy deliverable (CJK filename) |

**These are expected failures.** They will be resolved when the migration plan
(`ai/migration/2026-03-16-artifact-migration-plan.md`) is approved and executed.

---

## What is enforced NOW (operational)

| Enforcement | Mechanism | Status |
|-------------|-----------|--------|
| Canonical directory structure exists | `storage-map.yaml` + created dirs | **Active** |
| Write paths are functional | Write-path test proved | **Active** |
| Naming patterns are defined and checkable | `check_artifact_governance.py` | **Active** |
| Registry fields are complete | Script validates all 12 required fields | **Active** |
| Scratch is separated from outputs | `scratch/google-ads/` outside `ai/outputs/` | **Active** |
| Validation files follow naming | Script validates `YYYY-MM-DD-{slug}.md` | **Active** |
| No new violations detectable | Script can run as gate check | **Active** |

## What is documented but NOT yet enforced

| Gap | Reason | Resolution |
|-----|--------|------------|
| Legacy files in repo root | Migration not yet executed | Approve + execute migration plan |
| Legacy flat files in `ai/outputs/` | Migration not yet executed | Same |
| Agents writing to correct paths | Policy exists but no pre-commit hook | Add pre-commit hook or CI check |
| Auto-registration in artifacts.yaml | Manual process only | Future: script or hook to auto-register |
| `canonical-briefs.yaml` golden paths | Still point to legacy flat paths | Update during migration |
| Cross-agent enforcement | Skills don't yet reference policies | Update skill SKILL.md files to reference governance |

---

## Verdict

The governance layer is **structurally complete and operationally testable**.
New outputs CAN be written correctly today. Legacy violations are known and inventoried.

**Next steps** (in priority order):
1. Run `check_artifact_governance.py` after every pipeline execution
2. Approve and execute migration plan for Phase 1 (ai/outputs/ flat → governed hierarchy)
3. Update skill SKILL.md files to reference artifact governance policies
4. Add pre-commit hook for automated enforcement
