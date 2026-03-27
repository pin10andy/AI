# Change Record: PMax 文案生成 MVP

## Related Task

`ai/tasks/2026-03-14-google-ads-pmax-mvp.yaml` (`gads-copy-002`)

## Summary

在既有 Search RSA MVP 基礎上，將 `google-ads-writer` 升級為共用 brief、依 `campaign_type`
分流到 Search / PMax 的文案生成 skill。新增 PMax output schema、playbook、human review checklist、
3 份 PMax testcase、3 份 PMax 輸出樣本，並補強 validator 以支援 exact PMax 檢查。

## Files Created

- `ai/tasks/2026-03-14-google-ads-pmax-mvp.yaml`
- `ai/schemas/google-ads-pmax-output.schema.json`
- `ai/playbooks/google-ads-pmax.md`
- `ai/evals/google-ads-pmax-human-review.md`
- `ai/testcases/google-ads/lovefu-mattress-pmax.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-pmax.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-pmax.yaml`
- `ai/testcases/google-ads/outputs/lovefu-mattress-pmax.output.json`
- `ai/testcases/google-ads/outputs/lovefu-mattress-pmax.output.md`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-pmax.output.json`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-pmax.output.md`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-pmax.output.json`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-pmax.output.md`
- `ai/reports/2026-03-14-pmax-human-review.md`

## Files Updated

- `ai/inputs/google-ads-brief.schema.json`
  - 從 Search-only 改為共用 brief schema
  - 依 `campaign_type` 分別約束 Search / PMax 的 character policy
- `ai/skill-src/google-ads-writer/SKILL.md`
  - 升級為 Search / PMax 雙路徑文案生成 skill
  - 依 `campaign_type` 切換 playbook、schema、review checklist、template
- `ai/skill-src/google-ads/SKILL.md`
  - 路由新增「從 brief 直接產生 PMax」
- `ai/playbooks/google-ads.md`
  - 補上 PMax 專用 playbook 導引
- `ai/evals/ads-rubric.yaml`
  - 從 Search RSA rubric 擴成通用 Google Ads copy rubric
- `ai/skill-src/google-ads/ad-copy-builder/SKILL.md`
  - 明確說明全新 Search / PMax 文案都應優先走 `google-ads-writer`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
  - 支援 `google-ads-pmax-output.schema.json` 的 JSON 結構
  - 新增 `--exact-pmax-output`

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

- 目前 PMax 只處理文字資產，不含圖片、影片與 feed
- PMax human review 仍屬內部快速評估，尚未經 PM / 投放端最終複核
- 目前尚未加入批次生成腳本，仍以 skill + testcase 驗證為主
