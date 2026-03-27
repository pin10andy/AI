# ADR-005: Google Ads Copy Pipeline v1.2 Data / Observe / Taxonomy Contracts

## Status

accepted

## Background

Google Ads copy pipeline v1.1 已經修正：

1. legacy 三分模型
2. decision basis / confidence
3. builder / packager field-level handoff

但 full rerun 仍顯示三個結構問題：

1. 上游仍缺 asset-level click / conversion / placement / duration 資料層
2. observe 堆積過高，Builder 難以收斂到真實上稿規模
3. candidate generation 與 angle_key 仍不夠像可跨 skill 運作的正式 contract

## Decision

採用 v1.2 contract：

- input schema 顯式描述 click / conversion / placement / duration layers
- interpreter 輸出 observe 子類別與 active-duration downgrade 結果
- `new_candidate_assets` 升級為 candidate supply layer，必帶 `angle_key / risk_level / rewrite_mode`
- angle taxonomy 固定為 10 個標準 key，且必須由上游顯式提供
- builder / packager handoff 繼續維持 field-level validation，並擴充到 taxonomy / observe / rewrite metadata

## Rationale

這個方案延續 v1.1 的 contract-first 路線，但把真正造成「會跑、卻不夠像可上稿系統」的三個瓶頸一起打掉：

- 資料 basis
- observe 收斂
- candidate 與 taxonomy 的跨模組語意一致性

## Impact

- 影響的檔案：
  - interpreter / builder / packager 的 input/output schema
  - 三個 skill 的 decision rules / sample run / templates
  - creative interpretation playbook
  - 三份 rubric
  - LoveFu / 山丘樂眠床 sample input
- 影響的 agent：
  - claude / codex / gemini / openclaw
- 影響的流程：
  - LoveFu rerun
  - builder / packager field-level handoff
  - 後續 brief generator 接入 candidate pipeline

## Related

- Task: `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-2.yaml`
- Change: `ai/changes/2026-03-15-google-ads-copy-pipeline-v1-2.md`
- Previous ADR: `ai/decisions/ADR-004-google-ads-copy-pipeline-v1-1-contracts.md`
