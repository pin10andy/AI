# Change Record: Creative Performance Interpreter v1.0 Frozen

**日期**：2026-03-15
**狀態**：shipped
**變更者**：claude

---

## 變更摘要

建立 Creative Performance Interpreter skill v1.0 並完成 baseline dry run 驗證後凍結。

## 涵蓋的變更

### Phase 1：Skill 建立（8 檔案）

| 檔案 | 動作 | 說明 |
|------|------|------|
| `ai/inputs/creative-performance-input.schema.json` | 新增 | 輸入合約 |
| `ai/schemas/creative-performance-output.schema.json` | 新增 | 輸出合約（含 retire_now_assets + new_candidate_assets） |
| `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md` | 新增 | 核心 skill 定義 |
| `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md` | 新增 | 四欄決策規則 + 可執行清單 mapping |
| `ai/skill-src/google-ads/creative-performance-interpreter/templates/interpretation-report.md` | 新增 | Markdown 輸出模板 |
| `ai/evals/creative-performance-rubric.yaml` | 新增 | 6 維度評估標準 |
| `ai/playbooks/google-ads-creative-interpretation.md` | 新增 | 10 步工作流程 |
| `ai/skill-src/google-ads/SKILL.md` | 修改 | 路由表新增 creative-performance-interpreter |

### Phase 2：Baseline Dry Run（4 檔案）

| 檔案 | 動作 | 說明 |
|------|------|------|
| `ai/inputs/lovefu-pmax-hillbed-performance.json` | 新增 | 25 則實際文案 + 模擬成效數據 |
| `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.json` | 新增 | 完整 JSON 輸出 |
| `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.md` | 新增 | 完整 Markdown 報告 |
| `ai/validation/2026-03-15-creative-performance-interpreter-baseline.md` | 新增 | Dry run 驗證報告（score 5.0） |

### Phase 3：Baseline 凍結（1 檔案）

| 檔案 | 動作 | 說明 |
|------|------|------|
| `ai/validation/baseline-creative-performance-interpreter.yaml` | 新增 | Skill baseline，含回歸規則與已知限制 |

## 已知限制

1. Legacy 保護範圍過廣（52% 素材被自動 retain）
2. 缺少素材層級轉換數據
3. 未按版位分組計算 percentile

## 下一步

- [ ] Ad Copy Portfolio Builder（消費 interpreter output）
- [ ] 上稿素材包輸出器（產出可直接上稿的格式）
