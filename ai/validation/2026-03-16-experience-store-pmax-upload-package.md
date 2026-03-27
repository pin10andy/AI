# Validation Record: Experience Store PMax Upload Package

## Related Task

`2026-03-16-experience-store-pmax-upload-package` / `ai/tasks/2026-03-16-experience-store-pmax-upload-package.yaml`

## What Was Tested

1. upload package 是否明確拆出 `主力先上 / 測試保留 / 先不要上`
2. primary + test 的合計是否覆蓋 builder 的 15 short / 5 long / 5 descriptions
3. deliverable 是否帶入正確的 recommended LP 與 risky LP
4. artifact registry 與 governance check 是否完整

## Agents / Tools Involved

- Codex
- `python3` (builder text coverage check)
- `python3 scripts/check_artifact_governance.py`

## Source of Truth Files

- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.json`
- `ai/reports/2026-03-16-experience-store-lp-alignment-review.md`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-upload-package/input.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-upload-package/packager.md`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/deliverables/2026-03-16-experience-store-pmax-upload-package.deliverable.md`

## Result

通過

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| primary / test / do-not-upload 三層拆分 | ✓ | deliverable 與 packager 皆有 |
| short headline 計數 | ✓ | primary 10 + test 5 = 15 |
| long headline 計數 | ✓ | primary 3 + test 2 = 5 |
| description 計數 | ✓ | primary 3 + test 2 = 5 |
| builder text coverage | ✓ | 以 `builder.json` 的 `short_headlines / long_headlines / descriptions` 直接比對，合計文字完全覆蓋 |
| recommended LP 明確 | ✓ | 指定 `https://www.lovefu.tw/pages/lovefuhome` |
| risky LP 明確 | ✓ | 明示避免 `https://www.lovefu.tw/products/hillbed` |
| artifact registry updated | ✓ | 新增 pipeline 與 deliverable entry |
| governance check | ✓ | `python3 scripts/check_artifact_governance.py` pass |

## Command Evidence

1. `python3` coverage check rerun at `2026-03-16T22:07:46+08:00`
   - `short_headlines 15 15 True`
   - `long_headlines 5 5 True`
   - `descriptions 5 5 True`
2. `python3 scripts/check_artifact_governance.py`
   - overall: `PASS`

## Issues Found

1. 目前 deliverable 為 markdown handoff，若團隊要進一步做 bulk import 表，仍需補一份 xlsx / csv
2. generic booking package 尚未拆成 store-specific 版本，不適合直接拿去做地區差異化 A/B

## Conclusion

這份 upload package 已足夠交給投手做第一輪上稿與保守測試；
真正還沒完成的不是文案，而是後續地區拆版與更細的上稿表格式。
