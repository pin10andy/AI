# Validation Record: Experience Store PMax Booking Refresh

## Related Task

`2026-03-16-experience-store-pmax-booking-refresh` / `ai/tasks/2026-03-16-experience-store-pmax-booking-refresh.yaml`

## What Was Tested

1. experience-store draft brief 是否通過正式 brief schema
2. builder.json 是否通過 PMax output schema
3. builder.json 是否通過 `ad_copy_validator.py --exact-pmax-output`
4. governed path、artifact registry、governance check 是否完整
5. human review checklist 是否至少達到 `可微調後上稿`
6. 資料不足與 LP alignment blocker 是否有被明確記錄，而非被跳過

## Agents / Tools Involved

- Codex
- `.tmp/jsonschema-venv/bin/python` + `jsonschema`
- `python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `python3 scripts/check_artifact_governance.py`

## Source of Truth Files

- `ai/brand/master-brand.yaml`
- `ai/playbooks/google-ads-pmax.md`
- `ai/inputs/google-ads-brief.schema.json`
- `ai/schemas/google-ads-pmax-output.schema.json`
- `ai/evals/google-ads-pmax-human-review.md`
- `ai/inputs/briefs/lovefu-pmax-experience-store-booking-draft.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.json`
- `/Users/andychou/Downloads/素材資源關聯報表_預約.csv`

## Result

通過（draft pipeline validated；lane 仍維持 draft candidate）

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| draft brief schema validation | ✓ | 通過 `ai/inputs/google-ads-brief.schema.json` |
| PMax output schema validation | ✓ | `builder.json` 通過 `ai/schemas/google-ads-pmax-output.schema.json` |
| exact PMax validator | ✓ | 15 short / 5 long / 5 descriptions 全數通過 |
| 至少 1 個短說明 | ✓ | `先預約體驗，再決定下一步。` 為 13 字 |
| 三個 angle 成立 | ✓ | `immersive_tryout / guided_fit / low_pressure_booking` 明確分工 |
| human review fast checklist | ✓ | 品牌語氣、違規風險、headline 分散度皆過；判定 `可微調後上稿` |
| data sufficiency 明確標記 | ✓ | click layer=missing、conversion layer=partial、LP alignment 未關閉均已記錄 |
| supported-matrix unchanged | ✓ | 未將此 lane 加入 `ai/registry/supported-matrix.yaml` |
| artifact registry updated | ✓ | `ai/registry/artifacts.yaml` 已新增 pipeline entry |
| governance check | ✓ | `python3 scripts/check_artifact_governance.py` pass |

## Issues Found

1. CSV 沒有可用的 text-asset impressions / clicks，無法做 CTR 或 hybrid percentile interpretation
2. `體驗店_預約成功` 只落在部分 description rows，headline 層主要只能看 `Store visits + Directions` proxy
3. 實際 landing page 與 booking flow 尚未完成人工對頁，不可把本次草稿直接升級為 supported lane 或 golden output

## Conclusion

這份三店合併的 experience-store PMax 文案已完成正式 draft workflow：
brief、governed output、registry、validation 都已落地。
下一步應先做 LP alignment review，再決定是否進入 human sign-off 與後續非作者 rerun。
