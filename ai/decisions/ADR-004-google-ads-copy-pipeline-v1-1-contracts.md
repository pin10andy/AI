# ADR-004: Google Ads Copy Pipeline v1.1 Contracts

## Status

accepted

## Background

Google Ads copy pipeline v1.0 已拆出 interpreter / builder / packager，
但仍有三個核心結構問題：

1. legacy 建模把 phrase、token、motif 混成單一路徑
2. decision 只寫結論，不顯示 basis / confidence
3. handoff 只驗 object presence，沒有欄位級契約

## Decision

採用 v1.1 contract：

- legacy 拆為 `protected_phrase` / `must_include_token` / `reusable_motif`
- interpreter 每筆 asset decision 必須輸出 `decision_basis` 與 `decision_confidence`
- percentile 依 `asset_type` cohort 分開計算
- builder / packager input contract 一律升級為 field-level validation

## Rationale

這個方案在不重寫整條 pipeline 的前提下，
直接修正最會讓 output 看起來完整、實際上失真的三個環節。

## Impact

- 影響的檔案：
  - interpreter / builder / packager 的 input/output schema
  - 三個 skill 的 decision rules 與 sample run
  - creative interpretation playbook
  - 三份 rubric
- 影響的 agent：
  - claude / codex / gemini / openclaw
- 影響的流程：
  - LOVEFU 山丘樂眠床 rerun
  - 後續 builder / packager handoff validation

## Related

- Task: `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-1.yaml`
- Change: `ai/changes/2026-03-15-google-ads-copy-pipeline-v1-1.md`
