# Change Record: Claude vs Codex Google Ads Copy Pipeline v1.2 Rerun Comparison

## Related Task

`gads-pipeline-014` / `ai/tasks/2026-03-16-claude-vs-codex-v1-2-rerun-comparison.yaml`

## Summary

新增一份正式 comparison report，
以 artifact-level review 比較 Claude archived initial-run
與 Codex governed real-UAT rerun 的 Google Ads copy pipeline v1.2 成果，
並給出默認 runner 建議。

## Files Created

- `ai/reports/2026-03-15-claude-vs-codex-v1-2-rerun-comparison.md`
- `ai/tasks/2026-03-16-claude-vs-codex-v1-2-rerun-comparison.yaml`
- `ai/changes/2026-03-16-claude-vs-codex-v1-2-rerun-comparison.md`
- `ai/validation/2026-03-16-claude-vs-codex-v1-2-rerun-comparison.md`

## Files Updated

- 無

## Key Findings

1. Claude 的 artifact schema 外觀完整，但 `replacement_map`、retirement handoff、observe 語意保留都偏弱，實際更像 schema pass 而非 execution-ready handoff。
2. Codex 在同樣弱資料前提下，能更清楚區分 source-data fail 與 handoff success，並把 safer rewrite / replacement / coverage / review checklist 串成可操作交付。
3. 若要指定默認 runner，Codex 較適合；Claude 應保留為 challenger / auditor / backup runner。

## Validation Result

比較報告已產出，並包含：

- artifact completeness check
- 五大維度打分
- final verdict
- recommended next steps
