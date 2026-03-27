# Validation Record: Productization v1

> 任務：`ai/tasks/2026-03-14-productization-v1.yaml`（prod-001）

## Related Task

`prod-001` / `ai/tasks/2026-03-14-productization-v1.yaml`

## What Was Tested

依 PM 定義的 4 個 checkpoint 驗證產品化交付物的完整性與正確性，並以 Codex 做非作者 dry run：

1. Checkpoint 1（正式可用）— Registry 登錄、spec 完整性
2. Checkpoint 2（可重跑）— Runbook 結構完整性 + Codex 非作者 dry run
3. Checkpoint 3（可稽核）— 所有稽核路徑可追蹤
4. Checkpoint 4（可擴張）— Registry 設計為 append-only

## Agents / Tools Involved

- Claude（建立 Productization v1 初版交付物）
- Codex（非作者 dry run、文件一致性校正）
- Python 3
- `.tmp/jsonschema-venv/bin/python` + `jsonschema`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`

## Source of Truth Files

- `ai/specs/lovefu-hillbed-pmax-writer-spec.md`
- `ai/registry/supported-matrix.yaml`
- `ai/registry/canonical-briefs.yaml`
- `ai/playbooks/lovefu-hillbed-pmax-runbook.md`
- `ai/validation/regression-baseline-hillbed-pmax.yaml`
- `ai/reports/2026-03-14-hillbed-message-drift.md`
- `ai/decisions/ADR-002-productization-v1-scope.md`
- `ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md`
- `ai/outputs/lovefu-pmax-hillbed.output.json`
- `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json`
- `ai/inputs/briefs/lovefu-pmax-hillbed.json`

## Result

通過

## Details

### Checkpoint 1: 正式可用

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| hillbed-purchase-pmax 在 supported-matrix | ✓ | lane_id 正確，status=production |
| lovefu-pmax-hillbed 在 canonical-briefs | ✓ | status=canonical, version=1 |
| Writer spec FR 表格完整 | ✓ | FR-001~010 共 10 項，均有 acceptance criteria |
| Writer spec WF 表格完整 | ✓ | WF-001~004 共 4 項 |
| Writer spec DS 表格完整 | ✓ | DS-001~004 共 4 項 |
| 使用邊界明確定義 | ✓ | supported-matrix → boundaries 列表，5 項限制 |
| Failure handling 定義 | ✓ | spec 中 7 種失敗情境均有處理方式 |

### Checkpoint 2: 可重跑

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| Runbook 存在 | ✓ | `ai/playbooks/lovefu-hillbed-pmax-runbook.md` |
| 包含 7 個主要步驟 | ✓ | Step 1~7 + Step 1a (Drift Check) |
| 前置準備清單 | ✓ | 環境、Python、jsonschema、validator |
| Agent 指令可複製貼上 | ✓ | Step 2 提供完整指令模板 |
| 格式驗證步驟 | ✓ | Step 3a (schema) + Step 3b (validator) |
| Regression 比對步驟 | ✓ | Step 6 附比對表格 |
| FAQ 涵蓋常見問題 | ✓ | 4 個常見情境 |
| 快速參考表 | ✓ | 所有關聯檔案路徑列表 |
| 非作者實測 | ✓ | Codex 依 runbook 重跑並完成完整驗證鏈 |

### Checkpoint 2 Dry Run Evidence

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| Dry run 輸出建立 | ✓ | `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json` / `.md` |
| Output schema validation | ✓ | 使用 `.tmp/jsonschema-venv/bin/python` + `jsonschema` 對 output schema 驗證通過 |
| `ad_copy_validator --exact-pmax-output` | ✓ | 15 short / 5 long / 5 desc 全數通過 |
| Keyword-message fit | ✓ | `short=4 / long=2 / desc=1`，高於 `3 / 1 / 1` |
| Must-include terms | ✓ | `山丘樂眠床 / 100天安心睡 / 立即選購` 皆出現 |
| Angle coverage | ✓ | `body-first-comfort=6/2/2`、`worry-free-choice=5/1/2`、`smart-start=4/2/1` |
| Rubric self-score | ✓ | overall `4.55 / 5.00`，高於 baseline threshold `4.00` |
| Human review verdict | ✓ | `可直接上稿` |
| Regression compare vs baseline | ✓ | counts、policy、must_include、verdict 皆一致，overall 未低於門檻 |

### Checkpoint 3: 可稽核

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| Canonical brief 可從 registry 查到 | ✓ | canonical-briefs.yaml → file 欄位指向 brief JSON |
| Brief 版本與版控政策 | ✓ | version=1, brief_version_policy 區塊完整 |
| Drift check 排程 | ✓ | next_check_due: 2026-04-14 |
| Validation record 可查 | ✓ | 指向 golden brief validation |
| Regression baseline 可查 | ✓ | 含分數、覆蓋率、回歸規則 |
| Message drift report 可查 | ✓ | 三方比對全部 match |
| Readiness report 可查 | ✓ | 4 checkpoint 狀態清楚 |
| Known issues 可查 | ✓ | 5 項已知限制已記錄 |

### Checkpoint 4: 可擴張

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| Registry 為 append-only | ✓ | 新 lane 只需新增 entry |
| Spec 範圍明確限縮 | ✓ | Out of Scope 排除其他產品/goal |
| ADR 確認擴張策略 | ✓ | ADR-002: 先同產品擴 goal，再跨產品 |
| 新 lane 不需修改既有檔案 | ✓ | 所有檔案為新建，未動既有 Phase 1 產出 |
| Brief version policy 支援多版本 | ✓ | versioning_rule 已定義 |

### 交叉驗證：Regression Baseline 與 Golden Output 一致性

| 比對項目 | Baseline 值 | Golden Output 實際值 | 一致？ |
|---------|------------|-------------------|--------|
| short_headlines count | 15 | 15 | ✓ |
| long_headlines count | 5 | 5 | ✓ |
| descriptions count | 5 | 5 | ✓ |
| angles count | 3 | 3 | ✓ |
| overall rubric score | 4.65 | 4.65 | ✓ |
| forbidden_claims_found | 0 | 0 | ✓ |
| human_review_verdict | 可直接上稿 | 可直接上稿 | ✓ |

## Issues Found

1. **Gemini / OpenClaw parity 尚未驗證**
   - 目前 Claude 與 Codex 都已完成可重跑驗證
   - 不影響本 milestone 的 4 個 checkpoint，但仍屬後續擴張風險

## Conclusion

Productization v1 的 4 個 PM checkpoint 已全部通過。

所有交付物均已建立且相互引用一致。Regression baseline 與 canonical output 數據吻合，
且 Codex 已依 runbook 完成 non-author dry run。
Registry 設計為 append-only，可安全擴張到下一條 lane。

建議下一步：
1. 開始規劃第二條 lane（hillbed × store_visit）
2. 後續安排 Gemini / OpenClaw smoke test
