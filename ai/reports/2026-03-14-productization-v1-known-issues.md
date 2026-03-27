# Known Issues: Productization v1

## Report Date

2026-03-14

## Active Issues

### 1. Regression Baseline 僅一筆資料點

- **影響**：回歸規則的 threshold（如 overall 下降 > 0.65 需調查）統計意義有限
- **嚴重度**：低
- **建議**：累積 3+ 次正式產出後，重新校準 `regression-baseline-hillbed-pmax.yaml` 中的 threshold
- **追蹤**：每次重跑記錄分數，達 3 筆後重新評估

### 2. 「托住腰背」等表述的平台政策風險

- **影響**：Google Ads 政策更新可能影響 copy 上稿
- **嚴重度**：低（目前為感受描述，非醫療承諾）
- **建議**：每月 drift check 時同步確認 Google Ads 政策對「身體感受」類描述的最新規範
- **追蹤**：記錄於 drift report

### 3. Brief Drift Check 無自動提醒

- **影響**：依賴人工記得每月執行 drift check
- **嚴重度**：低
- **建議**：以 calendar reminder 或 Notion task 處理，本 milestone 不建自動化
- **追蹤**：`canonical-briefs.yaml` → `drift_check.next_check_due`

### 4. 跨 Agent 品質一致性未驗證

- **影響**：Claude 與 Codex 已驗證可重跑，但 Gemini 和 OpenClaw 的產出品質尚未確認
- **嚴重度**：低（目前 Checkpoint 2 已通過，不影響此 milestone 結案）
- **建議**：在後續 milestone 安排 cross-agent smoke test
- **追蹤**：列為下階段待辦

### 5. 活動促案與常態 Offer 的區分

- **影響**：brief 目前不含時效性活動，若投放活動期間廣告需另建 brief
- **嚴重度**：低
- **建議**：在 runbook FAQ 中已說明處理方式。PM 投放活動廣告前需另建 campaign-specific brief
- **追蹤**：無需額外追蹤

## Resolved Issues

無（本輪為首次產品化，Phase 1 issues 已記錄在各自的 validation record 中）
