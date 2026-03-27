# Hillbed Evergreen Purchase PMax — Writer Spec

> 此文件定義 hillbed purchase PMax 素材生成的正式可用契約。
> 所有 agent 核對設計時以此為準。

## Milestone Name

Productization v1 — Hillbed Evergreen Purchase PMax

## Goal

定義 hillbed purchase PMax 文字素材生成的正式範圍、輸入、輸出、驗收與失敗處理，
使其成為一條可重跑、可驗收、可交接、可稽核、可受控擴張的正式 lane。

## Background

Phase 1 已驗證此 lane 的可行性：
- Golden brief 得分 4.65/5（`ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md`）
- Human review 判定「可直接上稿」
- 欄位分級報告完成（`ai/reports/2026-03-14-hillbed-brief-field-grading.md`）
- Scope 決策見 `ai/decisions/ADR-002-productization-v1-scope.md`

需要把散落在 playbook / schema / rubric / validation 中的規則
整合成一份 PM 可核對的正式規格。

## Scope

本 spec 涵蓋：
- 品牌：LOVEFU大島樂眠
- 產品：山丘樂眠床
- Campaign type：PMax
- Goal：purchase
- 素材類型：文字（short headlines, long headlines, descriptions）
- 含 human review 步驟

## Out of Scope

- 其他 LOVEFU 產品（樂眠枕、主人床等）
- 其他 campaign type（search_rsa）
- 其他 goal（store_visit, lead, product_discovery）
- 圖片 / 影片 / feed 素材
- Brief 自動建立（A 級欄位仍需人工）
- 全自動化（移除 human review）

## Primary Deliverables

每次執行應產出：
1. **PMax copy pack (JSON)** — 符合 `ai/schemas/google-ads-pmax-output.schema.json`
2. **PMax copy pack (Markdown)** — 依 `ai/skill-src/google-ads-writer/templates/pmax-output.md`
3. **Compliance notes** — 包含 policy_risks 和 brand_risks
4. **Self-evaluation score** — 依 `ai/evals/ads-rubric.yaml`

## Input Contract

### Brief 來源

| 項目 | 值 |
|------|-----|
| Canonical brief | `ai/inputs/briefs/lovefu-pmax-hillbed.json` |
| Brief schema | `ai/inputs/google-ads-brief.schema.json` |
| Registry | `ai/registry/canonical-briefs.yaml` |

### Brief 必填欄位（13 個）

`brief_id`, `brand_name`, `product_name`, `campaign_type`, `goal`,
`landing_page_summary`, `target_audience`, `keyword_cluster`,
`usp`, `offers`, `constraints`, `tone`, `forbidden_claims`

### Character Policy（PMax）

| 資產類型 | 數量 | 字元上限 |
|---------|------|---------|
| Short headlines | 15 | 30 |
| Long headlines | 5 | 90 |
| Descriptions | 5 | 90 |

額外規則：至少 1 個 description ≤ 60 字元。

## Functional Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-001 | Brief 驗證 | 輸入 brief 必須通過 `google-ads-brief.schema.json` | jsonschema validation pass |
| FR-002 | 品牌規範遵循 | 輸出必須遵守 `master-brand.yaml` voice/tone/do/do_not | 無 voice 違規項 |
| FR-003 | 3 Angle 產出 | 恰好 3 個不同 angle，每個有 key/label/rationale | angle_coverage ≥ 4/5 |
| FR-004 | 資產數量正確 | 15 short + 5 long + 5 description | `ad_copy_validator --exact-pmax-output` pass |
| FR-005 | 字元限制合規 | short ≤30, long ≤90, desc ≤90, 至少 1 desc ≤60 | char_limit_compliance = pass |
| FR-006 | Keyword 覆蓋 | 至少 3 個 short headline 含 primary keyword | keyword_message_fit ≥ 3/1/1 |
| FR-007 | 禁用宣稱清除 | 無 forbidden_claims 出現在任何資產 | no_forbidden_claims check pass |
| FR-008 | 必含詞出現 | must_include 中的每個詞至少出現一次 | must_include_terms_present |
| FR-009 | 合規備註 | compliance_notes 完整，manual_review_required = true | schema validation pass |
| FR-010 | Rubric 通過 | overall score ≥ 3.5/5 | `ads-rubric.yaml` 評分通過 |

## Process / Workflow Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| WF-001 | Runbook 可執行 | 非作者可依 runbook 完成端到端流程 | 非作者實測通過 |
| WF-002 | Human Review | 輸出前必須經人工審查 | `google-ads-pmax-human-review.md` checklist 完成 |
| WF-003 | Regression 比對 | 新產出可與 baseline 比對 | baseline 存在且比對方法定義 |
| WF-004 | Drift Check | brief 更新前須跑 message drift report | drift report 格式已定義 |

## Design / Structure Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| DS-001 | Registry 登錄 | 此 lane 出現在 `supported-matrix.yaml` | lane entry 存在且 status=production |
| DS-002 | Canonical Brief | brief 登錄在 `canonical-briefs.yaml` | brief entry 存在且 status=canonical |
| DS-003 | 擴張隔離 | 新增 lane 不需修改此 spec 或既有檔案 | registry 為 append-only 設計 |
| DS-004 | 版本控制 | brief 有版本號與版控政策 | `brief_version_policy` 已定義 |

## Validation Requirements

每次產出需通過以下驗證：

1. **Schema validation**
   - Brief: `jsonschema` 對 `ai/inputs/google-ads-brief.schema.json`
   - Output: `jsonschema` 對 `ai/schemas/google-ads-pmax-output.schema.json`

2. **Format validation**
   - `ad_copy_validator.py --exact-pmax-output`

3. **Rubric self-evaluation**
   - `ai/evals/ads-rubric.yaml`，overall ≥ 3.5

4. **Human review**
   - `ai/evals/google-ads-pmax-human-review.md` checklist

5. **Regression comparison**（重跑時）
   - 對照 `ai/validation/regression-baseline-hillbed-pmax.yaml`
   - 整體分數需通過 baseline floor，且任一 rubric 維度不可低於 4.0

6. **Wording risk review**
   - 依 `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`
   - Tier 2 字句需 reviewer 明確判定可留，Tier 3 字句不得出現

## Failure Handling

| 失敗情境 | 處理方式 |
|---------|---------|
| Brief 無法通過 schema validation | 拒絕執行，回報缺失欄位清單 |
| 無法產出 3 個真正不同的 angle | 停止並報告，不得假裝完成 |
| 資產大量重複（語意相同僅換字序） | 停止並報告 |
| Brief 與品牌規範衝突 | 停止並報告衝突點 |
| 任何 forbidden_claim 出現 | 回到 Step 4 重新生成 |
| Rubric overall < 3.5 | 標記為未通過，不得上稿 |
| 官網事實與 brief 不一致 | 停止，先跑 drift check，更新 brief |

## Evidence Sources

本 spec 的核對依據：
- `ai/registry/supported-matrix.yaml`
- `ai/registry/canonical-briefs.yaml`
- `ai/inputs/briefs/lovefu-pmax-hillbed.json`
- `ai/outputs/lovefu-pmax-hillbed.output.json`
- `ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md`
- `ai/validation/regression-baseline-hillbed-pmax.yaml`
- `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`
- `ai/decisions/ADR-003-hillbed-pmax-production-change-control.md`
- `ai/reports/2026-03-14-hillbed-message-drift.md`
- `ai/tasks/2026-03-14-productization-v1.yaml`

## Risks

1. **官網價格或政策變更** — brief 中的 14,900 起、100 天退款、10 年保固需持續與官網一致
2. **平台政策風險** — 「托住腰背」「接住身體」等感受描述可能被重新定義為醫療宣稱
3. **Regression baseline 雖已擴成 3 筆，但仍集中在 brief version 1** — 尚未覆蓋 brief 更新情境
4. **活動促案干擾** — 時效性活動資訊不應進入 canonical brief，需另開 brief

## Open Questions

- brief 的 drift check 自動提醒機制尚未建立（目前為 calendar reminder）
- Claude 與 Codex 已驗證可重跑，Gemini / OpenClaw parity 尚未確認
- production change 需額外遵循 `ADR-003`，不得直接覆寫 canonical output

## Checkpoint Definition

| Checkpoint | 完成條件 | 驗證方式 |
|-----------|---------|---------|
| 1. 正式可用 | hillbed purchase PMax 在 supported-matrix，status=production | 查 registry |
| 2. 可重跑 | 非作者可依 runbook 完成端到端流程 | 非作者 dry run |
| 3. 可稽核 | PM 可查 canonical brief / validation / boundaries / readiness | 查 registry + reports |
| 4. 可擴張 | 新增 lane 不需修改既有檔案 | 模擬新增 entry |
