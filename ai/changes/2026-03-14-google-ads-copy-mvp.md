# Change Record: Search RSA 文案生成 MVP

## Related Task

`ai/tasks/2026-03-14-google-ads-copy-mvp.yaml` (`gads-copy-001`)

## Summary

將原本偏通用的 Google Ads 文案能力收斂成一條可交付的 Search RSA MVP 流程。
本次新增固定 brief schema、Search RSA output schema、Search playbook、3 份 testcase、
human review checklist，並把 `google-ads-writer` 明確改為 Search RSA only。
同時補強 `ad_copy_validator.py`，讓它能直接讀取新的 Search RSA JSON 結構。

## Files Created

- `ai/tasks/2026-03-14-google-ads-copy-mvp.yaml`
- `ai/inputs/google-ads-brief.schema.json`
- `ai/schemas/google-ads-search-output.schema.json`
- `ai/playbooks/google-ads-search-rsa.md`
- `ai/evals/google-ads-human-review.md`
- `ai/testcases/google-ads/lovefu-mattress-search.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-search.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-search.yaml`
- `ai/testcases/google-ads/outputs/lovefu-mattress-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-mattress-search.output.md`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-search.output.md`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-search.output.md`
- `ai/skill-src/google-ads-writer/templates/search-rsa-output.md`

## Files Updated

- `ai/skill-src/google-ads-writer/SKILL.md`
  - 將 scope 鎖定為 Search RSA MVP
  - 改用固定 brief / output contract
  - 補上 JSON + Markdown 雙輸出流程
- `ai/skill-src/google-ads/SKILL.md`
  - 新增 Search RSA 文案 MVP 路由
  - 將既有 `ad-copy-builder` 明確保留為優化 / PMax 路徑
- `ai/skill-src/google-ads/ad-copy-builder/SKILL.md`
  - 明確說明全新 Search RSA 文案應改走 `google-ads-writer`
- `ai/playbooks/google-ads.md`
  - 補上 Search RSA 專用 playbook 的導引
- `ai/evals/ads-rubric.yaml`
  - 對齊 Search RSA output schema
  - 新增 `angle_coverage` 與 `policy_safety`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
  - 支援新 Search RSA JSON 結構
  - 支援 `--exact-search-output` 契約檢查

## Files Removed

無

## Sync / Deployment Impact

已執行：

```bash
bash scripts/sync-skills.sh
```

已同步更新：

- `.claude/skills/`
- `.agents/skills/`
- `runtime/openclaw/`

## Open Issues

- V1 仍只支援 Search RSA，PMax 尚未進入這條流程
- 第一批輸出已產生，但人工 review 仍屬快速評估，尚未經 PM 或實際投放端最終確認
- 本機環境沒有 `jsonschema` / `pyyaml`，本次 validation 以 Ruby YAML parser 與更新後 validator 完成
