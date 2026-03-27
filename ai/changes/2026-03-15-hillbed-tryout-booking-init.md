# Change Record: Hillbed Tryout Booking Initialization

## Related Task

`lane-002` / `ai/tasks/2026-03-15-hillbed-tryout-booking-init.yaml`

## Summary

這次改動初始化山丘樂眠床的第二條候選 lane：tryout booking PMax。
做法是從既有 purchase canonical brief fork 出一份 draft brief，
並補上 lane spec 與 validation plan，但不把它加入 supported-matrix。

## Files Created

- `ai/tasks/2026-03-15-hillbed-tryout-booking-init.yaml`
- `ai/inputs/briefs/lovefu-pmax-hillbed-tryout-booking-draft.json`
- `ai/specs/lovefu-hillbed-tryout-booking-pmax-lane-spec.md`
- `ai/reports/2026-03-15-hillbed-tryout-booking-validation-plan.md`
- `ai/validation/2026-03-15-hillbed-tryout-booking-init.md`

## Files Updated

- 無

## Files Removed

無

## Sync / Deployment Impact

- 不影響現行 production lane
- 不更新 supported-matrix
- 不變更 canonical brief registry

## Open Issues

- 最終 booking landing page 尚未定義
- 門市/地區資訊的可用事實尚未核定
- 還沒有 golden output，因此 lane 仍是 draft candidate
