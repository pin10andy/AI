# Claude Ads Creative Pipeline Analysis and Integration Design

- generated_by: codex
- generated_at: 2026-03-21
- scope: external creative-pipeline analysis and local integration design only

## 1. Executive Summary

外部 Claude Ads 的 creative pipeline，**本質上不是 copy production pipeline**，而是 **creative audit / creative intelligence pipeline**。  
它擅長做：

- creative quality evaluation
- asset sufficiency detection
- fatigue / risk / platform-fit checking
- weighted scoring
- action-oriented audit report

它不擅長取代我們目前的：

- `creative-performance-interpreter`
- `ad-copy-portfolio-builder`
- `upload-packager`

因此，最合理的整合方式不是「取代現有 pipeline」，而是把它放成：

1. **upstream audit gate**
2. **downstream challenger / preflight reviewer**

一句話結論：

> Claude Ads 的 creative pipeline 應整合成我們 copy pipeline 的前後側車層（sidecar），而不是核心主鏈。

## 2. Source Note

使用者提供的原始頁面 `https://tenten.co/learning/claude-ads-skill/` 在 **2026-03-21** 無法直接讀取。  
本分析使用以下可取得來源：

- [Google Ads MCP 設定指南：OpenClaw 整合](https://university.tenten.co/t/google-ads-mcp-openclaw/2176)
- [Claude Ads overview on SkillsLLM](https://skillsllm.com/skill/claude-ads)
- [Stormy: Scaling Agency Operations with Claude Code Ad Audits](https://stormy.ai/blog/scaling-agency-operations-claude-code-ad-audits)
- [WEEL: Claude Ads 仕組み解説](https://weel.co.jp/media/tech/claude-ads/)

其中對 creative pipeline stage 的部分拆解，**部分是根據 command structure、architecture 描述與 feature list 的合理推論**，不是作者官方 schema dump。

## 3. What the External Creative Pipeline Actually Is

從公開資料看，Claude Ads 提供：

- `/ads audit`
- `/ads google`
- `/ads plan ...`
- `/ads creative`
- `/ads budget`

其中 `/ads creative` 被描述為 **cross-platform creative quality audit**，在 WEEL 的整理中是 **21 項 creative checks**。  
此外，整體 skill 也明確包含：

- parallel subagent delegation
- weighted scoring (`Ads Health Score`)
- industry template loading
- RAG-style reference loading
- optional MCP-backed live data access

這表示它的 creative pipeline 比較接近：

### Stage A: Command intake and routing

- 使用者觸發 `/ads creative`
- orchestrator 判斷是 creative-only audit，而不是 full account audit
- 視平台 / business type 決定啟用哪些檢查

### Stage B: Context loading

- 讀取平台特定規則
- 讀取 industry templates / benchmarks
- 讀取 compliance / bidding / creative references

### Stage C: Data acquisition

- 從 CSV export 或 MCP 拉資料
- 如有 live connector，則可直接讀 account state
- 來源可以是 Google Ads、Meta、TikTok、LinkedIn 等

### Stage D: Creative check execution

這一層會檢查的不是單一 copy contract，而是整體 creative health。可合理拆成：

- asset coverage / asset sufficiency
- platform-fit / format-fit
- fatigue / staleness
- quality / clarity / offer fit
- policy / compliance sensitivity
- creative diversity / testing depth

可直接證據包括：

- WEEL 明確提到 `P-MAXアセット不足検出`
- SkillsLLM / README snippet 提到 `Cross-platform creative quality audit and fatigue detection`

### Stage E: Severity and scoring

- 每個 finding 會被標記嚴重度
- 匯總成 weighted score / grade
- 不只是 pass/fail，而是 health score

### Stage F: Actionable report generation

- 生成 findings report
- 給出優先修正清單
- 把 creative 問題連到 budget waste / platform mismatch / funnel loss

## 4. External Pipeline vs Our Current Pipeline

| Dimension | Claude Ads Creative Pipeline | Current Workspace Pipeline |
|---|---|---|
| Core purpose | Audit / score / diagnose creatives | Interpret performance → build portfolio → package upload-ready copy |
| Unit of analysis | Account / platform / campaign / creative set | Asset-level copy decisions and downstream handoff |
| Primary output | Audit findings + health score + action plan | Final asset pack + replacement_map + strategic_notes |
| Data stance | CSV or MCP live data; multi-platform | Governed input JSON / output artifacts; Google Ads-focused |
| Main question | 「現有素材和創意體系哪裡有問題？」 | 「哪些句子保留、替換、補位，最後要上什麼？」 |
| Best role | Auditor / challenger / gate | Production pipeline |

這兩者不是重複系統，而是互補系統。

## 5. Detailed Mapping to Current Skills

### 5.1 Orchestrator Layer

External:

- `/ads creative`
- `/ads audit`
- orchestrator routes to subskills

Current equivalent:

- [ai/skill-src/google-ads/SKILL.md](/Users/andychou/AI/ai/skill-src/google-ads/SKILL.md)

Gap:

- 我們現在的 router 比較像「工作類型路由」
- 外部 skill 則多了一層「command namespace + audit mode routing」

Integration implication:

- 如果要接 creative audit，不要塞進現有 `creative-performance-interpreter`
- 應新增一個獨立 audit orchestrator 或至少獨立 skill

### 5.2 Data Ingress Layer

External:

- CSV export
- optional MCP live read

Current equivalent:

- normalized input JSON
- real-UAT rerun script (`scripts/google_ads_copy_pipeline_v12_real_uat_rerun.py`)

Gap:

- 目前沒有 connector abstraction
- 沒有 `mcp_remote / mcp_local / export_csv` 的統一 ingress contract

Integration implication:

- 應先新增 creative-audit input schema
- 再做 adapter 將 MCP/export 映射進 normalized audit input

### 5.3 Creative Intelligence Layer

External:

- creative quality
- fatigue
- asset insufficiency
- platform-fit

Current equivalent:

- `creative-performance-interpreter` 處理 performance-derived interpretation
- `performance-reviewer` 處理 campaign / ad group 層 performance review
- `upload-packager` 處理 char audit、strategic notes、watchlist

Gap:

- 我們沒有一個專門做「creative health audit」的 skill
- 目前最接近的是 `performance-reviewer` + `upload-packager` 的部分輸出

Integration implication:

- 應新增 `google-ads-creative-auditor`
- 它的位置應在 interpreter 外側，而不是內部

### 5.4 Decision Layer

External:

- weighted severity
- health score
- prioritized fixes

Current equivalent:

- `decision_basis`
- `decision_confidence`
- `replacement_map`
- `coverage_check`

Gap:

- 我們的 decision 是 asset-level operational decision
- 外部 decision 是 audit-level health decision

Integration implication:

- **不能**把 health score 直接灌進 `decision_confidence`
- **不能**把 audit finding 直接覆蓋 asset-level retain / retire decision
- 應當把 creative audit 結果變成：
  - pre-brief constraints
  - quality warnings
  - packager preflight blockers

### 5.5 Final Output Layer

External:

- findings report
- recommendations
- scorecard

Current equivalent:

- `ai/reports/`
- `ai/validation/`
- packager markdown

Gap:

- packager markdown 是 delivery artifact，不是 audit artifact

Integration implication:

- creative audit 應優先寫入 `ai/reports/`
- 若作為 release gate，才在 `ai/validation/` 追加一份 pass/fail evidence

## 6. Best Integration Position

### Option A: Replace Existing Pipeline

不建議。

原因：

- external creative pipeline 不產生 governed final asset pack
- 沒有我們目前的 `replacement_map` / `coverage_check` / `handoff_validation` 主鏈
- 它比較像 reviewer，不像 builder-packager system

### Option B: Put It Upstream

可行，而且有價值。

建議位置：

`creative audit -> interpreter -> portfolio builder -> packager`

上游用途：

- 先檢出 asset sufficiency 問題
- 先檢出 generic / drift / fatigue / platform-fit 問題
- 把結果轉成 interpreter 的限制條件或 caveats

### Option C: Put It Downstream

也可行。

建議位置：

`interpreter -> builder -> packager -> creative audit preflight`

下游用途：

- 對 final pack 做 challenger review
- 檢查是否仍有 fatigue / low-diversity / platform mismatch / policy risk
- 若不過 gate，禁止標記 ready-for-upload

### Recommended Position

**最佳做法是雙位置，但先做下游。**

原因：

- 下游 creative audit 比較不會污染現有 pipeline contract
- 可以先當 `preflight reviewer`
- 等 schema 穩定後，再考慮把其中一部分前移成 upstream constraint layer

## 7. Proposed Local Integration Shape

### Phase 1: Downstream Creative Audit Sidecar

新增：

- `ai/skill-src/google-ads-creative-auditor/SKILL.md`
- `ai/playbooks/google-ads-creative-audit.md`
- `ai/schemas/google-ads-creative-audit-output.schema.json`
- `ai/evals/google-ads-creative-audit-rubric.yaml`

Input:

- packager output
- optional account / campaign summary
- optional export / MCP snapshot

Output:

- creative findings
- creative health score
- fatigue / insufficiency / diversity / risk findings
- upload blockers / warnings / recommendations

### Phase 2: Upstream Constraint Bridge

若 sidecar 穩定，再把部分 output 映射回：

- `next_round_brief_additions`
- `must_avoid`
- `coverage_check.gaps`
- `do_not_expand_angles`

這樣 creative audit 會變成下一輪產生器的真實限制條件，而不是孤立報告。

## 8. Output Mapping Proposal

| External Creative Audit Finding | Local Destination |
|---|---|
| Asset insufficiency | `coverage_check.gaps` or audit report |
| Platform format mismatch | packager warning / preflight blocker |
| Creative fatigue | `observe_stale` candidate input or audit report |
| Low diversity | `strategic_notes.test_angles` recommendation |
| Policy-sensitive creative | `safer_rewrite_watchlist` or policy-risk section |
| Generic brand drift | `do_not_expand_angles` + product-scope filter |
| Creative health score | report-level metric only, not asset-level confidence |

## 9. What Must Not Be Merged

以下幾點很重要：

1. 不要把 creative audit score 當作 `decision_confidence`
2. 不要讓 audit layer 直接重寫 interpreter 的 asset decisions
3. 不要讓 MCP write-mode 直接進 production pipeline
4. 不要把 multi-platform check 直接塞進 Google Ads-only registry / storage map

## 10. Recommended MVP

最小可行版本應該是：

1. 做一個 **Google Ads-only creative auditor**
2. 只支援 `read_only`
3. 先吃 packager output + export snapshot
4. 輸出到 `ai/reports/`
5. 若需要 gate，再額外寫 `ai/validation/`

這樣可以先驗證：

- creative audit 是否真的能補現有 pipeline 的盲點
- 它是否比純 packager notes 更有決策價值
- 它會不會和現有 `replacement_map` / `coverage_check` 產生語意衝突

## 11. Final Recommendation

**整合方向應該是：`creative-auditor sidecar`, not `creative-pipeline replacement`.**

若要一句話講完：

> 外部 Claude Ads creative pipeline 最適合整合成我們現有 copy pipeline 的審查層與前置情報層；它不是主生產鏈，而是讓主生產鏈更安全、更接近真實帳戶運作的 reviewer system。
