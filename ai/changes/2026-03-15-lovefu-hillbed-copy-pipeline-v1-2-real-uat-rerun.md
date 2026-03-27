# Change Record: LOVEFU 山丘樂眠床 Google Ads Copy Pipeline v1.2 Real UAT Rerun

## Related Task

`gads-pipeline-013` / `ai/tasks/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.yaml`

## Summary

使用真實 LOVEFU / 山丘樂眠床素材資源關聯報表，
重跑 Google Ads copy pipeline v1.2 的 interpreter / builder / packager 三層，
產出可重現的 rerun script、完整 artifact 與 validation report。

## Files Created

- `ai/tasks/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.yaml`
- `ai/changes/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md`
- `scripts/google_ads_copy_pipeline_v12_real_uat_rerun.py`
- `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.input.json`
- `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.interpreter.json`
- `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json`
- `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.json`
- `ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.md`
- `ai/validation/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md`

## Files Updated

- 無

## Validation Result

- runtime input schema: pass
- interpreter schema: pass
- builder schema: pass
- packager schema: pass
- final pack: 15 headlines + 4 descriptions
- replacement gap: 0
- sign_off_status: pending_review

## Key Findings

1. 真實 source export 不足以支撐 v1.2 richer input layers。
   impressions / clicks / ctr 雖有欄位，但全數為 0；
   asset-level conversions / active_duration_days / placement_breakout 仍缺。

2. v1.2 的跨層 contract 已在真實 rerun 中成立。
   angle_key、observe_reason、risk_level、rewrite_mode、safer_rewrite_of、
   replacement_map、coverage_check 全數能從 interpreter 傳到 packager。

3. safer rewrite 在高風險歷史贏家上確實發生作用。
   `hl-03 -> cand-h01`、`desc-01 -> cand-d01`、
   `desc-03 -> cand-d02`、`desc-22 -> cand-d03`
   都進 final pack 或 watchlist。

4. builder / packager 已能收斂到真實 RSA 上稿規模。
   最終 pack 為 15 headlines + 4 descriptions，
   而不是把舊素材池整桶保留。

## Open Issues

- 真實報表仍無法驗證 observe_new / observe_stale / retire_candidate。
- source 素材池混有泛 LOVEFU / 飄雲語言，產品對焦仍需前置過濾。
- final pack 雖更接近可上稿，但仍因 source data 弱而只能維持 `pending_review`。
