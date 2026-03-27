# Change Record: Productization v1 — Hillbed Evergreen Purchase PMax

## Related Task

`prod-001` / `ai/tasks/2026-03-14-productization-v1.yaml`

## Summary

把已驗證的 hillbed purchase PMax lane 從實驗品升級為正式產品化能力。
建立了 registry 系統、writer spec、操作手冊、回歸基準線、漂移報告與完整的發布套件，
並由 Codex 以非原作者身份完成 dry run 與一致性校正，
使此 lane 成為可重跑、可稽核、可擴張的正式 supported capability。

## Files Created

- `ai/registry/supported-matrix.yaml` — 正式支援的 lane 登錄表
- `ai/registry/canonical-briefs.yaml` — 已核可的正式 brief 清單與版控政策
- `ai/specs/lovefu-hillbed-pmax-writer-spec.md` — hillbed purchase PMax writer spec
- `ai/playbooks/lovefu-hillbed-pmax-runbook.md` — 操作員導向的端到端執行手冊
- `ai/validation/regression-baseline-hillbed-pmax.yaml` — 品質回歸基準線
- `ai/reports/2026-03-14-hillbed-message-drift.md` — 官網 vs brief vs 文案一致性比對
- `ai/releases/2026-03-productization-v1.md` — 版本發布紀錄
- `ai/reports/2026-03-14-productization-v1-readiness.md` — PM checkpoint 就緒報告
- `ai/reports/2026-03-14-productization-v1-known-issues.md` — 已知限制
- `ai/reports/2026-03-14-productization-v1-spec-vs-implementation.md` — 規格對照報告
- `ai/tasks/2026-03-14-productization-v1.yaml` — 任務紀錄
- `ai/decisions/ADR-002-productization-v1-scope.md` — 產品化範圍決策
- `ai/changes/2026-03-14-productization-v1.md` — 本變更紀錄
- `ai/validation/2026-03-14-productization-v1.md` — 驗證紀錄
- `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json` — Codex 非作者 dry run 輸出
- `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.md` — Codex 非作者 dry run Markdown

## Files Updated

- `ai/tasks/2026-03-14-productization-v1.yaml` — status / owner / validation method 更新
- `ai/registry/supported-matrix.yaml` — validation record 改為 productization v1，註記 dry run 已完成
- `ai/specs/lovefu-hillbed-pmax-writer-spec.md` — open questions 改為目前仍未驗證的項目
- `ai/playbooks/lovefu-hillbed-pmax-runbook.md` — FAQ 補上 Claude / Codex 已驗證可重跑
- `ai/validation/regression-baseline-hillbed-pmax.yaml` — 對齊 canonical output 的字元統計與 baseline score
- `ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md` — 對齊目前 canonical output 的驗證結果
- `ai/releases/2026-03-productization-v1.md` — 移除 dry run pending，更新 next focus
- `ai/reports/2026-03-14-productization-v1-readiness.md` — Checkpoint 2 改為通過
- `ai/reports/2026-03-14-productization-v1-known-issues.md` — 移除 dry run issue，保留剩餘風險
- `ai/reports/2026-03-14-productization-v1-spec-vs-implementation.md` — 對齊 FR/WF 統計與 dry run 狀態
- `ai/validation/2026-03-14-productization-v1.md` — 補入 Codex dry run 證據與最終結論

## Files Removed

- 無

## Sync / Deployment Impact

- 不需跑 `scripts/sync-skills.sh`（本次未修改 skill 檔案）
- 新建的 `ai/registry/` 目錄為新的查詢入口，所有 agent 可直接讀取
- 無部署影響

## Open Issues

1. Regression baseline 累積 3+ 筆後需重新校準 threshold
2. Brief drift check 自動提醒機制尚未建立
3. Gemini / OpenClaw parity 仍待 smoke test
