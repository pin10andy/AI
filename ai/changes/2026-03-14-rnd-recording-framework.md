# Change Record: 建立研發記錄機制

## Related Task

`ai/tasks/2026-03-14-rnd-recording-framework.yaml` (rnd-001)

## Summary

新增研發／改版記錄框架，讓所有 AI agent 的工作都能透過 repo 原生檔案追溯。
包含任務記錄、決策記錄、變更記錄、驗證記錄、發布紀錄和回顧紀錄六類。

## Files Created

- `ai/decisions/` — 決策記錄資料夾
- `ai/changes/` — 變更記錄資料夾
- `ai/validation/` — 驗證記錄資料夾
- `ai/releases/` — 發布紀錄資料夾
- `ai/retros/` — 回顧紀錄資料夾
- `ai/decisions/ADR-template.md`
- `ai/changes/change-template.md`
- `ai/validation/validation-template.md`
- `ai/releases/release-template.md`
- `ai/retros/retro-template.md`
- `ai/tasks/2026-03-14-rnd-recording-framework.yaml` — 第一筆正式 task

## Files Updated

- `ai/tasks/task-template.yaml` — 新增 status、owner、goal、background、related_adr 等欄位
- `CLAUDE.md` — 新增 R&D Records 區塊和 Recording Rules

## Files Removed

無

## Sync / Deployment Impact

不影響 skill sync。記錄機制是 repo 層級的，所有 agent 透過各自的 adapter 都可直接讀取 `ai/` 下的記錄檔案。

## Open Issues

- AGENTS.md、GEMINI.md 尚未同步更新 R&D recording rules（建議下一個 task 處理）
- 尚未定義自動化驗證流程（目前為手動驗證）
