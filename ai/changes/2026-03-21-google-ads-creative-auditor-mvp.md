# Change Record: Google Ads Creative Auditor MVP

## Related Task

`gads-creative-audit-001` / `ai/tasks/2026-03-21-google-ads-creative-auditor-mvp.yaml`

## Related Decision

`ai/decisions/ADR-006-google-ads-creative-auditor-sidecar.md`

## Summary

新增 `creative-auditor` sidecar MVP，
讓現有 Google Ads copy pipeline 具備 creative preflight / challenger review 的正式骨架。

## Files Created

- `ai/inputs/google-ads-creative-audit-input.schema.json`
- `ai/schemas/google-ads-creative-audit-output.schema.json`
- `ai/evals/google-ads-creative-audit-rubric.yaml`
- `ai/playbooks/google-ads-creative-audit.md`
- `ai/skill-src/google-ads/creative-auditor/SKILL.md`
- `ai/skill-src/google-ads/creative-auditor/references/audit-criteria.md`
- `ai/skill-src/google-ads/creative-auditor/templates/audit-report.md`
- `ai/decisions/ADR-006-google-ads-creative-auditor-sidecar.md`
- `ai/tasks/2026-03-21-google-ads-creative-auditor-mvp.yaml`
- `ai/changes/2026-03-21-google-ads-creative-auditor-mvp.md`
- `ai/validation/2026-03-21-google-ads-creative-auditor-mvp.md`

## Files Updated

- `ai/skill-src/google-ads/SKILL.md`

## Key Findings

1. creative-auditor 被定義為 report / validation sidecar，而不是 generator 或 packager。
2. 新 schema 明確區分 evidence level、health score、findings、upload decision 與 integration handoff。
3. skill suite routing 已新增 creative audit 類需求的對應入口。

## Validation Result

MVP 骨架已建立並完成語法、sync、governance 檢查；adapter 與 sample run 留待下一階段。
