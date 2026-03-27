# Creative Performance 解讀報告 v1.2

**解讀 ID**：{interpretation_id}
**品牌**：{brand_name}
**產品**：{product_name}
**廣告類型**：{campaign_type}
**產出者**：{generated_by}
**產出日期**：{generated_at}

---

## 數據充分度

- 總曝光量：{total_impressions}
- 整體判定：{overall_verdict}
- click layer：{click_layer_verdict}
- conversion layer：{conversion_layer_verdict}
- placement layer：{placement_layer_verdict}
- duration layer：{duration_layer_verdict}
- 報表粒度：{asset_granularity}
- asset-level conversion：{includes_asset_level_conversion}
- placement breakout：{includes_placement_breakout}

## Asset-Type Percentiles

| Asset Type | Basis | P25 | P50 | P75 | Eligible Assets |
|-----------|-------|-----|-----|-----|-----------------|
{每個 asset_type_percentile 一列}

## 素材決策

| 素材 ID | 文案 | 類型 | Angle | 決策 | Basis | Confidence | Observe | 原因 |
|---------|------|------|-------|------|-------|------------|---------|------|
{每個 asset_decision 一列}

## Legacy Message State

### Protected Phrases

| Phrase | Required | Matched Assets | Status | Notes |
|--------|----------|----------------|--------|------|
{每個 protected_phrase 一列}

### Must-Include Tokens

| Token | Required | Matched Assets | Status | Notes |
|-------|----------|----------------|--------|------|
{每個 must_include_token 一列}

### Reusable Motifs

| Motif Key | Description | Source Assets | Confidence | Recommendation |
|-----------|-------------|---------------|------------|----------------|
{每個 reusable_motif 一列}

## 本輪建議下架

| 素材 ID | 文案 | 類型 | Confidence | Coverage Gap | Replacement |
|---------|------|------|------------|--------------|------------|
{每筆 retire_now_assets 一列}

## 本輪新增候選

| Candidate ID | 文案 | 類型 | Angle | 角色 | Rewrite | Risk | Related Gap |
|--------------|------|------|-------|------|---------|------|-------------|
{每筆 new_candidate_assets 一列}

## 下輪 Brief 建議

- Protected phrases：{constraints_protected_phrases}
- Must-include tokens：{constraints_must_include_tokens}
- Reusable motifs：{constraints_reusable_motifs}
- Proven angles：{proven_angles}
- Language to avoid：{language_to_avoid}
- Candidate triggers：{candidate_pipeline_triggers}

## 合規備註

- 數據注意事項：{data_caveats}
- 解讀信心：{interpretation_confidence}
- 人工審查：必須
