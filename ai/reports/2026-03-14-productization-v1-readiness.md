# Readiness Report: Productization v1 — Hillbed Evergreen Purchase PMax

## Report Date

2026-03-14

## Milestone

Productization v1

## Spec Reference

- `ai/specs/lovefu-hillbed-pmax-writer-spec.md`

---

## PM's 4 Checkpoints

### Checkpoint 1: 正式可用

hillbed purchase PMax 是否正式納入 supported capability？

| 檢查項目 | 結果 | 證據 |
|---------|------|------|
| hillbed purchase PMax 在 supported-matrix | ✓ | `ai/registry/supported-matrix.yaml` → lane_id: hillbed-purchase-pmax |
| Lane status = production | ✓ | `supported-matrix.yaml` → status: production |
| Canonical brief 登錄 | ✓ | `ai/registry/canonical-briefs.yaml` → brief_id: lovefu-pmax-hillbed |
| Brief status = canonical | ✓ | `canonical-briefs.yaml` → status: canonical |
| Writer spec 定稿 | ✓ | `ai/specs/lovefu-hillbed-pmax-writer-spec.md` |
| FR/WF/DS 表格完整 | ✓ | FR-001~010, WF-001~004, DS-001~004 |

**Checkpoint 1 結論：通過**

---

### Checkpoint 2: 可重跑

非原作者是否能依 runbook 重跑成功？

| 檢查項目 | 結果 | 證據 |
|---------|------|------|
| Runbook 存在 | ✓ | `ai/playbooks/lovefu-hillbed-pmax-runbook.md` |
| Runbook 包含完整 7 步驟 | ✓ | Step 1~7 + Drift Check + FAQ |
| 前置準備清單明確 | ✓ | 環境、工具、套件皆列出 |
| 常見問題 FAQ | ✓ | 4 個常見情境已涵蓋 |
| 非作者實測通過 | ✓ | Codex 依 runbook 重跑，產出 `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json` 並完成 schema/validator/human review/baseline 比對 |

**Checkpoint 2 結論：通過**

---

### Checkpoint 3: 可稽核

PM 是否可隨時查看 canonical brief、最近 validation、使用邊界、readiness 狀態？

| 檢查項目 | 結果 | 證據 |
|---------|------|------|
| Canonical brief 可查 | ✓ | `canonical-briefs.yaml` → 指向 `ai/inputs/briefs/lovefu-pmax-hillbed.json` |
| Brief 版本與版控政策 | ✓ | `canonical-briefs.yaml` → version: 1 + `brief_version_policy` |
| Validation record 完整 | ✓ | `ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md` |
| Regression baseline 建立 | ✓ | `ai/validation/regression-baseline-hillbed-pmax.yaml` |
| Message drift report | ✓ | `ai/reports/2026-03-14-hillbed-message-drift.md` |
| 使用邊界明確 | ✓ | `supported-matrix.yaml` → boundaries 列表 |
| Readiness report 本身 | ✓ | 本文件 |
| Known issues 列出 | ✓ | `ai/reports/2026-03-14-productization-v1-known-issues.md`（目前 5 項） |

**Checkpoint 3 結論：通過**

---

### Checkpoint 4: 可擴張

是否已具備擴到下一條 lane 的條件，而不污染目前 canonical brief？

| 檢查項目 | 結果 | 證據 |
|---------|------|------|
| Registry 為 append-only 設計 | ✓ | 新 lane 只需新增 entry，不需修改既有 lane |
| Spec 範圍明確限縮 | ✓ | Out of Scope 已排除其他產品/goal |
| 新 lane 不需修改既有檔案 | ✓ | ADR-002 決策確認 |
| 擴張策略已定義 | ✓ | ADR-002: 先同產品擴 goal，再跨產品 |
| Brief version policy 支援多版本 | ✓ | `canonical-briefs.yaml` → version_history + versioning_rule |

**Checkpoint 4 結論：通過**

---

## Overall Readiness

| Checkpoint | 狀態 | 備註 |
|-----------|------|------|
| 1. 正式可用 | ✓ 通過 | |
| 2. 可重跑 | ✓ 通過 | Codex dry run 已完成 |
| 3. 可稽核 | ✓ 通過 | |
| 4. 可擴張 | ✓ 通過 | |

**總體就緒度：4/4 fully met**

## Recommendation

1. 本 milestone 可標記為 **validated**，Checkpoint 1–4 已全數具備證據
2. 開始規劃第二條 lane：hillbed × 試躺預約（store_visit）
3. 後續再安排 Gemini / OpenClaw smoke test，補齊 parity 邊界
