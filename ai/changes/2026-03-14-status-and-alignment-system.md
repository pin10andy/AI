# Change Record: 建立狀態追蹤與設計核對機制

## Related Task

`ai/tasks/2026-03-14-status-and-alignment-system.yaml` (rnd-002)

## Summary

新增 PM 設計基準（specs）和對照報告（reports）機制，
讓 agent 能回答「做到哪了」和「跟設計一致嗎」。

## Files Created

- `ai/specs/` — 設計基準目錄
- `ai/specs/product-spec-template.md` — milestone spec 模板
- `ai/specs/current-milestone-spec.md` — Phase 1 實際 spec
- `ai/reports/` — 對照報告目錄
- `ai/reports/spec-vs-implementation-template.md` — report 模板
- `ai/reports/2026-03-14-spec-vs-implementation.md` — 第一份實際報告
- `ai/tasks/2026-03-14-status-and-alignment-system.yaml` — 本任務
- `ai/changes/2026-03-14-status-and-alignment-system.md` — 本變更紀錄

## Files Updated

- `CLAUDE.md` — 新增 Role 擴展（PMO + auditor）、Design & Status SOT 索引、Status Tracking 和 Design Alignment 區塊

## Files Removed

無

## Sync / Deployment Impact

不影響 skill sync。AGENTS.md 和 GEMINI.md 建議同步更新 R&D + status/alignment 引用。

## Open Issues

- AGENTS.md 和 GEMINI.md 尚未同步更新
- DS-002 drift: CLAUDE.md 行數因 PMO 功能超過原預期，可考慮抽為共用 playbook
