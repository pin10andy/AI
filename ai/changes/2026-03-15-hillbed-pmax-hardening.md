# Change Record: Hillbed Purchase PMax Hardening

## Related Task

`hard-001` / `ai/tasks/2026-03-15-hillbed-pmax-hardening.yaml`

## Summary

這次改動穩定既有的 `hillbed-purchase-pmax` production lane，
補齊 production change control ADR、policy wording watchlist，
並把 regression baseline 從單一 canonical output 擴成 3 筆 approved references。

## Files Created

- `ai/tasks/2026-03-15-hillbed-pmax-hardening.yaml`
- `ai/decisions/ADR-003-hillbed-pmax-production-change-control.md`
- `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`
- `ai/outputs/lovefu-pmax-hillbed.approved-reference-03.output.json`
- `ai/outputs/lovefu-pmax-hillbed.approved-reference-03.output.md`
- `ai/validation/2026-03-15-hillbed-pmax-hardening.md`

## Files Updated

- `ai/validation/regression-baseline-hillbed-pmax.yaml`
- `ai/registry/supported-matrix.yaml`
- `ai/specs/lovefu-hillbed-pmax-writer-spec.md`
- `ai/playbooks/lovefu-hillbed-pmax-runbook.md`

## Files Removed

無

## Sync / Deployment Impact

- 不需 sync skill
- 不影響 schema / playbook runtime
- 會影響未來 production rerun 的 gate，reviewer 應改看新的 watchlist 與 multi-reference baseline

## Open Issues

- 三筆 approved references 目前仍都建立在同一份 brief version 1 上，尚未覆蓋 brief 更新情境
- Gemini / OpenClaw 尚未對這條 lane 做 smoke test
