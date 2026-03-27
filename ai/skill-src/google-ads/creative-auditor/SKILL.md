---
name: "creative-auditor"
description: "稽核 Google Ads 既有素材池或 final pack 的 creative health，檢查 asset sufficiency、creative diversity、product drift、policy risk 與 platform fit，輸出可作為 preflight gate 的報告。當使用者提到 creative audit、素材疲乏、asset 不足、final pack 審查、上稿前再檢查時觸發。"
license: MIT
metadata:
  version: 0.1.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-21
---

# Creative Auditor

> **Canonical source**: `ai/skill-src/google-ads/creative-auditor/SKILL.md`
> Do NOT edit copies in `.claude/skills/`, `.agents/skills/`, or `runtime/`.
> Always edit here and run `scripts/sync-skills.sh` to deploy.

這是 creative audit sidecar，不是生成器，也不是 packager。  
它的工作是審查既有素材或 final pack 是否已接近可上稿狀態。

## Required References

執行前必須讀取：

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/google-ads-creative-audit-input.schema.json`
3. `ai/schemas/google-ads-creative-audit-output.schema.json`
4. `references/audit-criteria.md`
5. `ai/evals/google-ads-creative-audit-rubric.yaml`

## When to Use

- 使用者說「幫我做 creative audit」
- 使用者說「final pack 上稿前再檢查一次」
- 使用者說「素材是否疲乏」「素材池是否太像」「PMax asset 不足」
- 已有 packager output，但想做 challenger review

## Required Inputs

至少要有以下其一：

1. `packager output` 經 adapter 正規化後的 audit input
2. 廣告素材匯出資料（CSV / snapshot）經 adapter 正規化後的 audit input
3. final pack 的 normalized JSON

若來源是現有 `upload-packager` 輸出，優先用：

`python3 scripts/google_ads_packager_to_creative_audit.py {packager.json} --mode audit-input`

建議補充：

1. `campaign_type`
2. `product_scope`
3. `required_tokens` / `protected_phrases`
4. 若要判 fatigue，需提供 `export_backed` 或 `live_snapshot` 的歷史訊號

## Execution Steps

### Step 1: Validate input and evidence level

- schema pass
- 先看 `data_source.evidence_level`
- `pack_only` 只能做低至中信心的 fatigue / platform-fit 判讀
- `write_enabled` source 不可被本技能用來直接修改平台
- `packager output` 不可直接拿來當 audit input；必須先經 adapter 正規化

### Step 2: Audit five dimensions

依 `references/audit-criteria.md` 對以下五個面向各給 1–5 分：

- `asset_sufficiency`
- `creative_diversity`
- `product_specificity`
- `policy_risk`
- `platform_fit`

### Step 3: Emit findings

每個 finding 必須輸出：

- `severity`
- `category`
- `title`
- `summary`
- `evidence`
- `affected_assets`
- `blocking`

### Step 4: Decide upload status

- blocker 存在 -> `blocked_for_upload`
- 無 blocker，但仍需人工確認 -> `needs_manual_review`
- 沒 blocker 且整體健康 -> `clear_to_review`

### Step 5: Emit integration handoff

必須輸出：

- `packager_blockers`
- `upstream_constraints`
- `challenger_notes`

這些欄位是給現有 interpreter / builder / packager 主鏈消費的，不可省略。

### Step 6: Recommend actions

每個 action 必須有：

- `priority`
- `owner`
- `action`
- `reason`

## Output Format

1. source data assessment
2. health score
3. dimension scores
4. findings list
5. upload decision
6. recommended actions
7. integration handoff
8. limitations

## Quality Gates

- [ ] 不可把 audit score 當作 `decision_confidence`
- [ ] 不可直接覆寫 interpreter / builder / packager 的主決策
- [ ] `pack_only` 不可高信心宣稱 fatigue
- [ ] blocker 存在時不可給 `clear_to_review`
- [ ] findings 必須附具體 evidence
- [ ] integration handoff 必須可回灌現有 pipeline

---

## Artifact Governance

本技能產出為 creative audit report / validation evidence。

### 輸出路徑規則

- 分析報告寫入 `ai/reports/`（命名 `YYYY-MM-DD-{slug}.md`）
- 若作為 gate evidence，驗證報告寫入 `ai/validation/`
- 暫存/測試輸出寫入 `scratch/google-ads/`
- **禁止**將輸出寫入 repo 根目錄

### 政策參考

- `ai/registry/storage-map.yaml`
- `ai/policies/artifact-naming-policy.md`
- `ai/policies/artifact-write-policy.md`
