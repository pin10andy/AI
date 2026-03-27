# Google Ads Creative Performance Interpretation Playbook v1.2

> 素材成效解讀 workflow。
> v1.2 對齊 richer input layers、observe 子類別、candidate automation、angle taxonomy。

## Goal

把歷史素材成效數據轉成可直接驅動下輪文案決策的解讀報告：

- 每個素材的 v1.2 decision bucket
- 每個決策的 `decision_basis` 與 `decision_confidence`
- `protected_phrase` / `must_include_token` / `reusable_motif` 狀態
- 可供 Builder 直接消費的 `retire_now_assets` / `new_candidate_assets`
- 同步輸出可跨 skill 傳遞的 `angle_key`

## Required Inputs

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/creative-performance-input.schema.json`
3. `ai/schemas/creative-performance-output.schema.json`
4. `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md`
5. `ai/evals/creative-performance-rubric.yaml`

## Workflow

### Step 1: Validate reporting context

- `performance_data.reporting_context` 必填
- `interpretation_layers` 必須存在
- 先判 click / conversion / placement / duration layer 是否 ready

### Step 2: Validate legacy + taxonomy

- `protected_phrases`
- `must_include_tokens`
- `reusable_motifs`
- `assets[*].angle_key`

### Step 3: Compute asset-type cohorts

- 依 `asset_type` 分 cohort
- 各自算 P25 / P50 / P75
- placement 可用時，保留 split interpretation 註記

### Step 4: Choose decision_basis

- impression / click / ctr 不足 -> `association_proxy_only`
- conversion ready -> conversion 或 hybrid
- 否則 -> `ctr_asset_type_percentile`

### Step 5: Decide and score confidence

每筆素材都必須輸出：

- `decision`
- `decision_basis`
- `decision_confidence`
- `observe_reason`
- `active_duration_days`
- `legacy_tags`

### Step 6: Emit downstream handoff fields

`retire_now_assets` 必須有：

- `angle_key`
- `decision_confidence`
- `decision_basis_ref`
- `coverage_gap_created`

`new_candidate_assets` 必須有：

- `angle_key`
- `intent`
- `related_gap`
- `covers_tokens`
- `inherits_motifs`
- `risk_level`
- `rewrite_mode`

## Quality Gates

- 不可再用混合 asset-type percentile
- 不可在 click / conversion layer 缺失時假裝高信心
- observe 不可再只有單一桶
- `angle_key` 不可由下游 heuristic 補欄位
- Builder handoff 所需欄位不可缺失
