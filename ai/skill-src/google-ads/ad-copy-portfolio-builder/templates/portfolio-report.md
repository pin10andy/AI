# Ad Copy Portfolio 組建報告 v1.2

**Portfolio ID**：{portfolio_id}
**來源解讀 ID**：{source_interpretation_id}
**品牌**：{brand_name}
**產品**：{product_name}
**廣告類型**：{campaign_type}
**產出者**：{generated_by}
**產出日期**：{generated_at}

---

## Portfolio 摘要

- 主力：{total_primary}
- 測試：{total_test}
- 最終總數：{total_final}
- 退場：{retired_count}
- 新增：{newly_added}
- 被拒候選：{rejected_candidates_count}
- observe：{observe_count}
- replacement gap unfilled：{replacement_gap_unfilled_count}
- field-level contract：{field_level_contract_passed}

## 退場替換地圖

| Retired Asset | Replacement | Rewrite | Gap Unfilled | Coverage After Replacement |
|---------------|-------------|---------|--------------|----------------------------|
{每筆 replacement_map 一列}

## Final Asset Pack

| 資產 ID | 文案 | Role | Angle | Source | Confidence | Rewrite | 備註 |
|---------|------|------|-------|--------|------------|---------|------|
{每筆 final_asset_pack 一列}

## Coverage Check

### Protected Phrases

| Term | Required | Found | Assets | Status |
|------|----------|-------|--------|--------|
{每筆 protected_phrase_check 一列}

### Must-Include Tokens

| Term | Required | Found | Assets | Status |
|------|----------|-------|--------|--------|
{每筆 token_coverage_check 一列}

### Motifs

| Motif | Assets | Status | Notes |
|-------|--------|--------|------|
{每筆 motif_coverage_check 一列}

### Angle Coverage

| Angle | Primary | Test | Status | Redundancy | Recommendation |
|-------|---------|------|--------|------------|----------------|
{每筆 angle_coverage 一列}

### Gaps

{gaps}

## 冗餘警告

| 素材 A | 素材 B | 原因 | 建議 |
|--------|--------|------|------|
{每筆 redundancy_alert 一列}

## 被拒候選

| Candidate | 文案 | 原因 |
|-----------|------|------|
{每筆 rejected_candidate 一列}

## 合規備註

- 上游信心：{upstream_confidence}
- 數據 caveats：{data_caveats}
- 字數警告：{character_limit_violations}
- 人工審查：必須
