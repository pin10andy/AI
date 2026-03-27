# Google Ads Creative Audit Playbook

> 用於 creative-auditor sidecar。
> 這不是文案生成流程，而是對既有素材池或 final pack 的 creative health review。

## Goal

把現有素材包、packager output、或帳戶匯出資料轉成可執行的 creative audit：

- asset sufficiency / diversity / product specificity / policy risk / platform fit 評估
- weighted health score
- upload blockers / warnings
- 可回灌現有 pipeline 的整合欄位

## Required Inputs

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/google-ads-creative-audit-input.schema.json`
3. `ai/schemas/google-ads-creative-audit-output.schema.json`
4. `ai/skill-src/google-ads/creative-auditor/references/audit-criteria.md`
5. `ai/evals/google-ads-creative-audit-rubric.yaml`

若上游來源是 `upload-packager` v1.2 output，優先使用：

`python3 scripts/google_ads_packager_to_creative_audit.py {packager.json} --mode audit-input`

## Workflow

### Step 0: Normalize source into audit input

- 若來源是 `packager.json`，先用 `scripts/google_ads_packager_to_creative_audit.py`
- adapter 只負責欄位正規化與弱資料標註，不可在這一步偷做高信心 creative 結論

### Step 1: Validate evidence level first

- 先判 input 來自 `pack_only` / `export_backed` / `live_snapshot`
- `pack_only` 不可高信心斷言 fatigue
- `write_enabled` source 只可作參考，不可在本 playbook 直接寫入平台

### Step 2: Audit five dimensions

- asset sufficiency
- creative diversity
- product specificity
- policy risk
- platform fit

### Step 3: Emit severity-based findings

每個 finding 必須有：

- `severity`
- `category`
- `evidence`
- `affected_assets`
- `blocking`

### Step 4: Decide upload status

- 有 blocker -> `blocked_for_upload`
- 無 blocker 但證據弱或 high severity 尚未處理 -> `needs_manual_review`
- 無 blocker 且整體健康 -> `clear_to_review`

### Step 5: Create integration handoff

至少輸出：

- `packager_blockers`
- `upstream_constraints`
- `challenger_notes`

## Quality Gates

- 不可把 audit score 當成 asset-level `decision_confidence`
- 不可直接覆寫 interpreter / builder / packager 的主決策
- 不可在 `pack_only` 證據下高信心宣稱 fatigue
- 有 blocker 時不可給 `clear_to_review`
- 必須提供可回灌現有 pipeline 的 handoff 欄位
