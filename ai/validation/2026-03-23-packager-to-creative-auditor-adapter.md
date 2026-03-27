# Validation Record: Packager to Creative Auditor Adapter and Sample Preflight Audit

## Related Task

`gads-creative-audit-002` / `ai/tasks/2026-03-23-packager-to-creative-auditor-adapter.yaml`

## Related Decision

`ai/decisions/ADR-006-google-ads-creative-auditor-sidecar.md`

## What Was Validated

1. adapter script 是否可編譯並成功消費既有 `packager.json`
2. `audit-input` 是否具備 creative-audit input schema 的必填欄位
3. `audit-output` 是否具備 creative-audit output schema 的必填欄位
4. sample markdown report 是否成功寫入 `ai/reports/`
5. skill sync 後 `.agents/skills/` 是否包含新的 handoff 說明
6. governance check 是否維持 PASS

## Result

PASS

## Evidence

### Source Artifact

- `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-2-uat/packager.json`

### Script Checks

1. compile
   - command: `python3 -m py_compile scripts/google_ads_packager_to_creative_audit.py`
   - result: pass

2. audit-input contract
   - command: inline `python3` wrapper calling `scripts/google_ads_packager_to_creative_audit.py --mode audit-input`
   - result:
     - `audit_input_missing=none`
     - `campaign_type=search_rsa`
     - `lane_id=evergreen-purchase-pmax`

3. audit-output contract
   - command: inline `python3` wrapper calling `scripts/google_ads_packager_to_creative_audit.py --mode audit-output`
   - result:
     - `audit_output_missing=none`
     - `upload_status=needs_manual_review`
     - `health=76/B`

### Report Output

- generated report: `ai/reports/2026-03-23-lovefu-hillbed-packager-preflight-audit.md`
- key lines confirmed:
  - `Upload decision: needs_manual_review`
  - `Generic LOVEFU / 飄雲 language still dilutes hillbed focus`
  - `gap angles: entry_value`
  - `path / payload campaign_type drift`

### Skill Sync

- command: `bash scripts/sync-skills.sh`
- result: `Sync Complete`
- synced evidence:
  - `.agents/skills/google-ads/creative-auditor/SKILL.md` 包含 adapter command
  - `.agents/skills/google-ads/upload-packager/SKILL.md` 包含 optional creative-auditor handoff

### Governance

- command: `python3 scripts/check_artifact_governance.py`
- result: `Overall: PASS`
- note: 仍有既有 legacy flat outputs 警告，但非本次整合新增問題

## Notes

- sample source artifact 本身存在 path / payload drift：
  - lane: `evergreen-purchase-pmax`
  - payload `campaign_type`: `search_rsa`
- 此問題是本次 sample audit 主動揭露出的上游 metadata 漂移，不是 adapter 寫錯欄位。
- sample report 的內文 `generated_at` 為 `2026-03-24T00:05:41+08:00`，屬於 3 月 23 日任務延伸到本地午夜後的正常時間戳。
