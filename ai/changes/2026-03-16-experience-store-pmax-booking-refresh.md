# Change Record: Experience Store PMax Booking Refresh

## Related Task

`2026-03-16-experience-store-pmax-booking-refresh` / `ai/tasks/2026-03-16-experience-store-pmax-booking-refresh.yaml`

## Summary

這次改動把使用者提供的三店體驗店素材關聯報表，整理成一份 booking-focused 的 PMax draft pipeline。
重點不是直接硬出稿，而是先補上 experience-store draft brief、建立 governed output path、
把 location-specific 舊素材整併成可共享投放的 generic booking copy，
並在 validation 中明確記錄資料只到 association proxy、LP alignment 尚未關閉。

## Files Created

- `ai/inputs/briefs/lovefu-pmax-experience-store-booking-draft.json`
- `ai/tasks/2026-03-16-experience-store-pmax-booking-refresh.yaml`
- `ai/changes/2026-03-16-experience-store-pmax-booking-refresh.md`
- `ai/validation/2026-03-16-experience-store-pmax-booking-refresh.md`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/golden/.gitkeep`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/approved-references/.gitkeep`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/deliverables/.gitkeep`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/input.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.md`

## Files Updated

- `ai/registry/storage-map.yaml`
- `ai/registry/artifacts.yaml`
- `scripts/check_artifact_governance.py`

## Files Removed

無

## Sync / Deployment Impact

- 不影響既有 `hillbed` production lane 的 output 或 supported-matrix 狀態
- governance layer 新增 `experience-store / evergreen-store-visit-pmax` 的 governed path
- 無需 sync skills；本次只使用既有 Google Ads skill 與 validator

## Open Issues

- 實際 landing page 與 booking flow 仍未完成對頁核對
- 素材報表缺少 text-asset impression / click layer，保留與替換判斷只能到 directional confidence
- 若後續要升級為 supported lane，仍需補 human review、LP alignment 與非作者 rerun
