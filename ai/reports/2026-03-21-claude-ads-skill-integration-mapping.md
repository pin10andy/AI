# Claude Ads Skill Integration Mapping

- generated_by: codex
- generated_at: 2026-03-21
- scope: framework-fit evaluation only; no MCP setup, no skill contract changes

## 1. Executive Summary

目前的開發框架 **可以整合 Claude Ads Skill 類型的 workflow**，但只能用 **adapter integration**，不能直接把外部 skill / MCP / write flow 原樣搬進來。

最適合的整合方式是：

1. 先整合 **read-only audit layer**
2. 保留目前 repo 的 **skill → playbook → schema → eval → report / validation → task/change** 鏈
3. 把外部 MCP 能力當成 **data ingress adapter**，不是新的 source of truth

**結論**：

- `Audit / analysis / reporting`：可整合，且相容度高
- `Live MCP read access`：可整合，但需要新的 connector / secret / permission layer
- `Live write actions to ad platforms`：目前不宜直接整合

## 2. Source Note

使用者提供的原始頁面 `https://tenten.co/learning/claude-ads-skill/` 在 **2026-03-21** 無法直接讀取。  
本評估改以以下可取得來源為基礎：

- [Google Ads MCP 設定指南：OpenClaw 整合](https://university.tenten.co/t/google-ads-mcp-openclaw/2176)
- [Claude Ads Skill overview](https://skillsllm.com/skill/claude-ads)
- [Stormy: Scaling Agency Operations with Claude Code Ad Audits](https://stormy.ai/blog/scaling-agency-operations-claude-code-ad-audits)

## 3. External Framework Pattern

從可讀來源抽出的外部框架核心元素如下：

| External Pattern | Meaning |
|---|---|
| `SKILL.md`-native execution | skill 本身定義流程、檢查項、輸出格式 |
| MCP-backed live data access | 透過 Google Ads / Meta / LinkedIn 等 MCP server 拉即時資料 |
| Parallel audit checks | 將大量檢查項並行執行，產出 PASS / WARNING / FAIL |
| Weighted scoring | 依類別權重算健康分數或 audit score |
| Actionable audit report | 不只摘要，還包含 action plan / budget / tracking / creative findings |
| Read / write mode split | 某些 MCP 只讀，某些可寫；成熟流程會區分兩者 |
| Multi-platform abstraction | skill 不只處理 Google Ads，而是 Google / Meta / TikTok / LinkedIn / Microsoft Ads 的共同 audit shell |

## 4. Current Workspace Mapping

| External Concept | Current Workspace Equivalent | Fit | Notes |
|---|---|---|---|
| Skill-native workflow | `ai/skill-src/google-ads/*/SKILL.md` | High | 現有 skill 架構與 external skill pattern 本質一致。 |
| Structured execution playbook | `ai/playbooks/google-ads.md`, `ai/playbooks/google-ads-creative-interpretation.md` | High | 我們比一般 skill marketplace 多一層 playbook 與明確 quality gates。 |
| Contracted input / output | `ai/inputs/*.schema.json`, `ai/schemas/*.schema.json` | High | 現有 pipeline 已是 schema-first。 |
| Weighted scoring / review | `ai/evals/*.yaml` | High | 已有 rubric 機制，可直接映射 audit scoring。 |
| Human-readable findings | `ai/reports/`, `ai/validation/` | High | 已有正式報告與驗證檔案位置。 |
| Reproducible artifact chain | `ai/tasks/`, `ai/changes/`, `ai/validation/` | High | 這是目前框架比外部 skill 更強的地方。 |
| Formal output governance | `ai/policies/artifact-write-policy.md`, `ai/registry/storage-map.yaml`, `ai/registry/artifacts.yaml` | High | 現有治理足以約束 audit output，但還是 Google Ads-only。 |
| MCP connector layer | 無正式 connector abstraction | Low | 目前 framework 沒有統一的 live connector policy。 |
| Secrets / token / OAuth governance | 無 formal secrets policy in repo | Low | 這是最大缺口之一。 |
| Multi-platform paid-ads abstraction | Google Ads-focused only | Low | 目前 scope 還沒抽象到 Meta / LinkedIn / TikTok。 |
| Read vs write execution modes | 部分存在於 task notes / human review gate | Medium | 有人工審核與 `pending_review`，但沒有統一的 connector permission model。 |

## 5. Where It Already Fits

以下幾件事已經和 Claude Ads Skill 類型模式天然對齊：

1. **Skill packaging**
   - 現有 `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md`
   - 現有 `ai/skill-src/google-ads/ad-copy-portfolio-builder/SKILL.md`
   - 現有 `ai/skill-src/google-ads/upload-packager/SKILL.md`
   - 這些都已是「技能 + references + templates + scripts」結構。

2. **Workflow decomposition**
   - 外部 skill 把 audit / scoring / report 拆清楚。
   - 我們目前也已把 interpreter / builder / packager 拆成明確責任邊界。

3. **Audit-style outputs**
   - `ai/reports/` 很適合接 audit findings
   - `ai/validation/` 很適合接 checkpoint / pass-fail / evidence
   - `ai/tasks` → `ai/changes` → `ai/validation` 很適合保存每次 audit run 的決策鏈

4. **Governed production posture**
   - 目前 Google Ads workflow 有 artifact write policy、storage map、artifact registry
   - 這代表外部 skill 若要被整合，不需要改變 repo 的治理主軸，只要適配它

## 6. What Does Not Fit Yet

以下是目前不能直接照搬的部分：

### 6.1 MCP live data layer is missing

目前 repo 沒有正式的：

- MCP server registry
- connector config convention
- OAuth / Developer Token / API key policy
- account-scoped permission boundary
- read-only vs write-mode enforcement

這使得外部文章那種「接上 Google Ads MCP 後直接 `/ads audit`」的體驗，
在本 repo 內還沒有標準接點。

### 6.2 Scope is Google Ads-only, not paid-ads-wide

目前 artifact governance 與 storage map 明確只管 Google Ads：

- `ai/policies/artifact-write-policy.md`
- `ai/registry/storage-map.yaml`
- `ai/registry/artifacts.yaml`

如果直接導入多平台 skill，會立刻碰到：

- path naming 不夠
- lane registry 不夠
- cross-platform schema 不存在
- validation / scoring 標準未抽象化

### 6.3 Live write actions are not ready

從可讀 Tenten MCP 文章可見，不同方案有 read/write 能力差異，甚至遠端服務可直接建 campaign。  
但目前我們的正式流程仍然是：

- human review required
- sign-off gating
- output artifact governed

還沒有到「允許 agent 直接改 account」的成熟度。

## 7. Recommended Integration Shape

### Phase 1: Add Read-Only Google Ads Audit Lane

先新增一個 **Google Ads account auditor**，只做讀取與報告，不做寫入。

建議新增：

- `ai/skill-src/google-ads-account-auditor/SKILL.md`
- `ai/playbooks/google-ads-account-audit.md`
- `ai/schemas/google-ads-account-audit-output.schema.json`
- `ai/evals/google-ads-account-audit-rubric.yaml`
- `ai/reports/YYYY-MM-DD-{slug}.md`
- `ai/validation/YYYY-MM-DD-{slug}.md`

這一層的任務是把 MCP / CSV / exported report 統一轉成：

- audit findings
- weighted score
- action checklist
- risk register
- next-step recommendation

### Phase 2: Add Connector Adapter Layer

不要讓 skill 直接綁特定第三方 MCP。

建議新增一個抽象層，例如：

- `data_source.type = export_csv | mcp_remote | mcp_local`
- `data_source.mode = read_only | write_enabled`
- `data_source.provider = google_official | adspirer | otto | custom`

這樣 skill 消費的是 normalized input，不是某一家 MCP 的專有格式。

### Phase 3: Add Live Connector Governance

若真的要接 live MCP，需要新增至少三份治理文件：

- `ai/policies/live-connector-policy.md`
- `ai/policies/credential-handling-policy.md`
- `ai/registry/connectors.yaml`

這層至少要定義：

- 哪些 connector 可用
- 哪些是 read-only
- 哪些需要 human confirmation
- 哪些 task 類型禁止 write mode

### Phase 4: Consider Paid-Ads Generalization

只有在 Google Ads audit lane 穩定後，才值得把 framework 抽象成 paid-ads-wide。

那時才應該新增：

- `ai/skill-src/paid-ads-*`
- `ai/registry/storage-map.yaml` 的 cross-platform extension
- Meta / LinkedIn / TikTok / Microsoft Ads 的 platform-specific schemas

## 8. Concrete File-Level Mapping

| If We Adopt Claude Ads Pattern | Best Local Home |
|---|---|
| `SKILL.md` audit orchestrator | `ai/skill-src/google-ads-account-auditor/SKILL.md` |
| Audit reference checks | `ai/skill-src/google-ads-account-auditor/references/*.md` |
| Scoring system | `ai/evals/google-ads-account-audit-rubric.yaml` |
| Account audit playbook | `ai/playbooks/google-ads-account-audit.md` |
| Output schema | `ai/schemas/google-ads-account-audit-output.schema.json` |
| Human-readable findings report | `ai/reports/YYYY-MM-DD-google-ads-account-audit.md` |
| Verification report | `ai/validation/YYYY-MM-DD-google-ads-account-audit.md` |
| Task record | `ai/tasks/YYYY-MM-DD-google-ads-account-audit.yaml` |
| Connector metadata | `ai/registry/connectors.yaml` |
| Live connector guardrails | `ai/policies/live-connector-policy.md` |

## 9. Go / No-Go Decision

| Area | Decision | Why |
|---|---|---|
| Integrate skill pattern | Go | 現有 skill-first + schema-first + governance 模式高度相容。 |
| Integrate Google Ads MCP read-only access | Go, with adapter | 需要 connector abstraction 與 credential policy。 |
| Integrate direct write-mode campaign actions | No-Go for now | 目前缺正式 permission / review / rollback policy。 |
| Generalize to multi-platform paid ads now | No-Go for now | 目前治理與 artifact 結構仍是 Google Ads-only。 |

## 10. Recommended Next Step

最小且高槓桿的下一步是：

1. 新開一個 task，定義 **read-only Google Ads account auditor** 的 MVP。
2. 先用 exported report + optional MCP-read adapter 做 input normalization，不碰 write mode。
3. 等第一版 audit lane 跑通後，再決定是否需要升級成 paid-ads-wide framework。

## 11. Final Answer

**能整合，但應該整合的是「framework pattern」，不是直接整包導入外部 implementation」。**

用一句話總結：

> 現有框架已足以承接 Claude Ads Skill 的 audit workflow 與 artifact discipline；真正需要新增的不是 skill 基礎，而是 connector adapter、credential governance、以及 read/write mode policy。
