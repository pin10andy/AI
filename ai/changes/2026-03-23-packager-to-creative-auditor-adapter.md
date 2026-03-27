# Change Record: Packager to Creative Auditor Adapter and Sample Preflight Audit

## Related Task

`gads-creative-audit-002` / `ai/tasks/2026-03-23-packager-to-creative-auditor-adapter.yaml`

## Related Decision

`ai/decisions/ADR-006-google-ads-creative-auditor-sidecar.md`

## Summary

將 `upload-packager` v1.2 output 正式接入 `creative-auditor` sidecar，
新增 deterministic adapter script、workflow integration report，
並用既有 LoveFu hillbed packager artifact 生成一份 sample preflight audit report。

## Files Created

- `scripts/google_ads_packager_to_creative_audit.py`
- `ai/reports/2026-03-23-packager-to-creative-auditor-adapter.md`
- `ai/reports/2026-03-23-lovefu-hillbed-packager-preflight-audit.md`
- `ai/tasks/2026-03-23-packager-to-creative-auditor-adapter.yaml`
- `ai/changes/2026-03-23-packager-to-creative-auditor-adapter.md`
- `ai/validation/2026-03-23-packager-to-creative-auditor-adapter.md`

## Files Updated

- `ai/playbooks/google-ads-creative-audit.md`
- `ai/skill-src/google-ads/creative-auditor/SKILL.md`
- `ai/skill-src/google-ads/upload-packager/SKILL.md`

## Key Findings

1. `packager -> creative-auditor` 已從概念整合變成實際可執行的 handoff。
2. adapter 明確採用 `payload campaign_type > storage lane` 的規則，避免 downstream 依路徑誤判格式要求。
3. sample preflight audit 抓到四個真實問題：generic brand drift、`entry_value` gap、policy-sensitive wording、以及 artifact path/payload drift。

## Validation Result

Adapter script、sample report、skill sync 與 governance check 全數通過；sidecar 已可作為正式 preflight gate 的 MVP。
