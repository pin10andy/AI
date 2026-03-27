# Change Record: LOVEFU 山丘樂眠床 Golden Brief

## Related Task

`ai/tasks/2026-03-14-lovefu-hillbed-golden-brief.yaml` (`gads-copy-004`)

## Summary

在不修改既有 schema、playbook、template、validator 與 rubric 的前提下，
補上 `lovefu-pmax-hillbed` 這份產品層級 golden brief，並完成一輪正式 PMax 文案輸出、
格式驗證、rubric 自評、human review、angle coverage / keyword-message fit 檢查，
同時把 brief 欄位分成 A / B 級，作為 Phase 2 brief builder 的設計依據。

## Files Created

- `ai/inputs/briefs/lovefu-pmax-hillbed.json`
- `ai/outputs/lovefu-pmax-hillbed.output.json`
- `ai/outputs/lovefu-pmax-hillbed.output.md`
- `ai/reports/2026-03-14-hillbed-brief-field-grading.md`
- `ai/tasks/2026-03-14-lovefu-hillbed-golden-brief.yaml`
- `ai/changes/2026-03-14-lovefu-hillbed-golden-brief.md`
- `ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md`

## Files Updated

無

## Files Removed

無

## Sync / Deployment Impact

無。  
本次沒有修改 skill、schema 或 sync 流程，只新增基於既有 contract 的實際 brief / output / 記錄檔。

## Open Issues

- 商品頁可驗的促案訊息與規劃草稿中的「購床贈竹眠防水保潔墊」不完全一致，本輪已保守處理並記錄在 brief `notes`
- 本機缺少 `jsonschema` 套件，因此 schema 驗證以 JSON parser + repo-aware structural check 補強
- 若後續 hillbed 也要跑 `store_visit` 導向，建議再開一份獨立 brief，不要直接覆用這份 `purchase` 版
