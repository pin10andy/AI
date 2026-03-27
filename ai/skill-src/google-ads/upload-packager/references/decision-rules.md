# 上稿素材包打包規則 v1.2

Upload Packager 在 v1.2 仍不是決策者，但要多做兩件事：

1. 驗證 builder output 的 angle-taxonomy field-level contract
2. 直接把 taxonomy 轉成 PM / 投手可執行的 strategic notes

---

## 1. 不可改寫文案

Packager 不可：

- 改字
- 重寫句子
- 重新選角度

它只能：

- 驗欄位
- 重算字數
- 重組視圖
- 生成 strategic notes 與操作 checklist

---

## 2. field-level handoff validation

搬運前必須逐欄驗證 `portfolio_output`。

必驗欄位：

- `angle_taxonomy.version / keys`
- `final_asset_pack.primary[*].angle_key`
- `final_asset_pack.primary[*].decision_confidence`
- `final_asset_pack.primary[*].decision_basis_metric`
- `final_asset_pack.primary[*].coverage_tags`
- `final_asset_pack.test[*].angle_key`
- `final_asset_pack.test[*].rewrite_mode`
- `final_asset_pack.test[*].risk_level`
- `replacement_map[*].replacement_gap_unfilled`
- `replacement_map[*].replacement_decision_confidence`
- `replacement_map[*].coverage_after_replacement`
- `coverage_check.taxonomy_version`
- `coverage_check.angle_coverage[*].status`
- `coverage_check.angle_coverage[*].redundancy_status`
- `portfolio_summary.observe_breakdown`
- `portfolio_summary.replacement_gap_unfilled_count`
- `compliance_notes.field_level_contract_passed`
- `compliance_notes.angle_taxonomy_aligned`

若任一缺失：

- `handoff_validation.portfolio_field_validation_passed = false`
- `delivery_metadata.sign_off_status` 不得高於 `pending_review`

---

## 3. strategic_notes v1.2

Packager 必須根據 `coverage_check.angle_coverage` 產出四塊 notes。

### main_angles

放進：

- `status = core`
- 或主力數量明顯高且 `redundancy_status = balanced`

### test_angles

放進：

- `status = test_only`
- 或值得擴寫但仍在驗證的 supporting angle

### do_not_expand_angles

放進：

- `redundancy_status = overbuilt`
- 或只承擔 legacy coverage、不是本輪要繼續擴寫的角度
- 或仍帶有高風險原句傾向的角度

### safer_rewrite_watchlist

從以下來源整理：

- `replacement_map[*].rewrite_mode = safer-rewrite`
- 或 final test assets 中 `source = safer_rewrite`

---

## 4. upload_ready_assets

將 `final_asset_pack` 依 role / asset_type 拆成：

- `primary_pack`
- `test_pack`

每則素材除原文外，至少保留：

- `angle_key`
- `decision_confidence`
- `observe_subtype`
- `risk_level`
- `rewrite_mode`
- `coverage_tags`

---

## 5. 字數審核

沿用既有字數審核邏輯：

- Packager 重新計算 `char_count`
- 輸出 `char_pass`

若字數未過：

- `packager_warnings` 必須明示
- `sign_off_status` 不得是 `ready_to_upload`

---

## 6. retirement_changelog

`replacement_map` 原封搬運到 `retirement_changelog`，不可遺漏：

- `replacement_gap_unfilled`
- `replacement_decision_confidence`
- `rewrite_mode`
- `coverage_after_replacement`

---

## 7. action checklist v1.2

Checklist 除了原有 QA 步驟，還要新增：

- 確認 protected phrase coverage 在線上素材中存在
- 確認 must_include token coverage 在線上素材中存在
- 若有 `observe_new`，安排回看時間點
- 若有 `replacement_gap_unfilled = true`，要求 PM 決定是否接受空缺
- 若有 safer rewrite watchlist，人工確認新句是否真的降風險且仍保留 intent

---

## 8. quality gates

- 不可只檢查 object 存在
- 不可遺失 `angle_key`
- 不可遺失 `rewrite_mode` / `risk_level`
- 不可遺失 `replacement_gap_unfilled`
- 不可省略 taxonomy strategic notes
- 不可把過度重複角度包裝成正常 coverage
