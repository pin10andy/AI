# Change Record: Experience Store LP Alignment Review

## Related Task

`2026-03-16-experience-store-lp-alignment-review` / `ai/tasks/2026-03-16-experience-store-lp-alignment-review.yaml`

## Summary

這次改動補上三店合併 booking PMax 的 LP 對頁檢查。
重點不是改網站，而是把 `lovefuhome` 體驗店頁與 `hillbed` 商品頁的承接差異寫清楚，
讓後續投放設定不會再把 booking intent 導去 product purchase flow。

## Files Created

- `ai/tasks/2026-03-16-experience-store-lp-alignment-review.yaml`
- `ai/changes/2026-03-16-experience-store-lp-alignment-review.md`
- `ai/validation/2026-03-16-experience-store-lp-alignment-review.md`
- `ai/reports/2026-03-16-experience-store-lp-alignment-review.md`

## Files Updated

- `ai/inputs/briefs/lovefu-pmax-experience-store-booking-draft.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.md`

## Files Removed

無

## Sync / Deployment Impact

- 無 skill sync 或 deployment 需求
- 只補強 report 與 draft notes，沒有變更正式 supported capability

## Open Issues

- 最終 Google Ads campaign URL 仍需人工在後台確認
- 若後續要拆地區 ad group，需再補 store-specific LP / copy alignment
