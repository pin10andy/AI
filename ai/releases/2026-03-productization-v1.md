# Release: Productization v1 — Hillbed Evergreen Purchase PMax

## Version / Milestone

Productization v1

## Date

2026-03-14

## Additions

- **Registry 系統**
  - `ai/registry/supported-matrix.yaml` — 正式支援的 lane 登錄表
  - `ai/registry/canonical-briefs.yaml` — 已核可的正式 brief 清單與版本控制政策

- **產品化規格**
  - `ai/specs/lovefu-hillbed-pmax-writer-spec.md` — hillbed purchase PMax 的正式 writer spec（含 FR/WF/DS 與 acceptance criteria）

- **操作手冊**
  - `ai/playbooks/lovefu-hillbed-pmax-runbook.md` — 操作員導向的端到端執行手冊

- **回歸驗證機制**
  - `ai/validation/regression-baseline-hillbed-pmax.yaml` — 品質回歸基準線（含回歸規則）

- **漂移檢查**
  - `ai/reports/2026-03-14-hillbed-message-drift.md` — 官網 vs brief vs 文案一致性比對

- **R&D 記錄**
  - `ai/tasks/2026-03-14-productization-v1.yaml` — 任務紀錄
  - `ai/decisions/ADR-002-productization-v1-scope.md` — 產品化範圍決策
  - `ai/changes/2026-03-14-productization-v1.md` — 變更紀錄
  - `ai/validation/2026-03-14-productization-v1.md` — 驗證紀錄
  - `ai/reports/2026-03-14-productization-v1-readiness.md` — PM checkpoint 就緒報告
  - `ai/reports/2026-03-14-productization-v1-known-issues.md` — 已知限制
  - `ai/reports/2026-03-14-productization-v1-spec-vs-implementation.md` — 規格對照報告

## Fixes

- 無（本輪為產品化新增，非修復）

## Known Limitations

- Regression baseline 僅一筆資料點，統計意義有限
- 「托住腰背」等表述的平台政策風險需持續監控
- Brief drift check 自動提醒機制尚未建立（目前為手動）
- Gemini / OpenClaw parity 尚未驗證

詳見：`ai/reports/2026-03-14-productization-v1-known-issues.md`

## Next Focus

1. **第二條 lane** — 山丘樂眠床 × 試躺預約（store_visit goal）
2. **Brief builder prototype** — B 級欄位半自動草擬工具
3. **Regression 累積** — 收集 3+ 次產出後重新校準 baseline threshold
