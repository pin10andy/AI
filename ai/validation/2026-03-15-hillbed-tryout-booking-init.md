# Validation Record: Hillbed Tryout Booking Initialization

## Related Task

`lane-002` / `ai/tasks/2026-03-15-hillbed-tryout-booking-init.yaml`

## What Was Tested

1. draft brief 是否成功從 purchase canonical brief fork 出來
2. draft brief 是否通過正式 brief schema validation
3. lane spec 是否明確定義與 purchase lane 的差異
4. supported-matrix 是否保持不變
5. validation plan 是否清楚列出 support 前的 gates

## Agents / Tools Involved

- Codex
- `.tmp/jsonschema-venv/bin/python` + `jsonschema`

## Source of Truth Files

- `ai/inputs/briefs/lovefu-pmax-hillbed.json`
- `ai/inputs/briefs/lovefu-pmax-hillbed-tryout-booking-draft.json`
- `ai/inputs/google-ads-brief.schema.json`
- `ai/specs/lovefu-hillbed-tryout-booking-pmax-lane-spec.md`
- `ai/reports/2026-03-15-hillbed-tryout-booking-validation-plan.md`
- `ai/registry/supported-matrix.yaml`

## Result

通過（初始化完成，但尚未成為 supported lane）

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| draft brief file 建立 | ✓ | 已建立獨立 JSON，不覆寫 purchase canonical brief |
| draft brief schema validation | ✓ | 通過 `google-ads-brief.schema.json` |
| goal mapping clarity | ✓ | 文件明確標示 `tryout booking -> store_visit` |
| differences vs purchase lane | ✓ | lane spec 有完整 diff 表格 |
| validation plan exists | ✓ | support 前 gate 已分成 4 個 phase |
| supported-matrix unchanged | ✓ | 尚未新增 lane entry |

## Issues Found

1. 最終 landing page 與 booking 承接路徑尚未確定
2. 尚無 golden output，因此還不能做 regression baseline

## Conclusion

`hillbed × tryout booking` 已完成初始化，
但仍屬 draft candidate。下一步應先確認 landing page 與預約流程，
再進入 output 生成與 human review。
