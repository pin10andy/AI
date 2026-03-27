# 素材池組建決策規則 v1.2

Ad Copy Portfolio Builder 在 v1.2 只做四件事：

1. 嚴格吃 interpreter 的 richer handoff contract
2. observe 不再整桶留主力
3. candidate pipeline 真的用來補 retire gap 與 safer rewrite
4. coverage / redundancy 改用統一 angle taxonomy

---

## 1. field-level handoff validation

開始組建前，必須逐欄驗證 `interpretation_output`。

必驗欄位：

- `angle_taxonomy.version / keys`
- `data_sufficiency.click_layer_verdict`
- `data_sufficiency.conversion_layer_verdict`
- `asset_decisions[*].angle_key`
- `asset_decisions[*].decision`
- `asset_decisions[*].observe_reason`
- `asset_decisions[*].active_duration_days`
- `asset_decisions[*].decision_basis.primary_metric`
- `retire_now_assets[*].coverage_gap_created`
- `new_candidate_assets[*].angle_key`
- `new_candidate_assets[*].intent`
- `new_candidate_assets[*].related_gap`
- `new_candidate_assets[*].risk_level`
- `new_candidate_assets[*].rewrite_mode`
- `next_round_brief_additions.candidate_pipeline_triggers`

若任一缺失：

- 直接 fail
- 不得用 object presence 假裝通過

---

## 2. 基底池建立

### retain / reinforce

- `retain` -> primary
- `reinforce` -> primary

### observe_new

- 可暫留 primary
- 但只能佔少量 slot
- `status_note` 必須保留觀察條件與回看日期

### observe_borderline

- 預設先進 test 或 primary 尾端
- 若容量不足，先移除 observe_borderline，不先移除高信心 retain

### observe_stale

- 不得預設留在主力池
- 先進 `observe_assets_status`
- `disposition = retire_candidate_watchlist` 或 `demoted_pending_review`

### observe_insufficient_data

- 若 `active_duration_days` 尚短，可暫留 test
- 若已接近 stale / retire_candidate 邏輯，不可再佔主力池

### retire_candidate

- 預設不進 final primary
- 若沒有 replacement，仍需在 `observe_assets_status` 或 `replacement_map` 中留下明確紀錄

---

## 3. retire 與 replacement

每筆 `retire_now_assets` 都必須進 `replacement_map`。

### 3.1 有候選時

- `action = replaced`
- `replacement_gap_unfilled = false`
- 保留：
  - `replacement_decision_confidence`
  - `rewrite_mode`
  - `coverage_after_replacement`

### 3.2 無候選時

- `action = removed_no_replacement`
- `replacement_gap_unfilled = true`
- 將 gap 寫進：
  - `replacement_map.notes`
  - `coverage_check.gaps`
  - `compliance_notes.data_caveats`

### 3.3 must_include / protected coverage

優先順序：

1. 補 `protected_phrase`
2. 補 `must_include_token`
3. 補關鍵 angle gap
4. 才是 motif expansion

---

## 4. candidate selection

候選納入順序：

1. field completeness
2. gap fit
3. rewrite safety
4. capacity
5. redundancy
6. test ratio

### 4.1 field completeness

缺任何一欄直接拒絕：

- `angle_key`
- `intent`
- `related_gap`
- `covers_tokens`
- `inherits_motifs`
- `risk_level`
- `rewrite_mode`

### 4.2 gap fit

若 retire 造成 coverage gap：

- 先收能補 exact gap 的 candidate
- 再收 reinforce expansion

### 4.3 safer rewrite

若來源素材是高效但高風險語言：

- 優先收 `rewrite_mode = safer-rewrite`
- 不可只保留風險原句，卻不提供降風險候選

### 4.4 candidate fill ratio

- `new_candidate_assets` 數量不應低於 retire 數量的 20%
- 若低於此門檻，`compliance_notes.candidate_pipeline_complete = false`

---

## 5. 以 taxonomy 為核心做 coverage_check

`coverage_check` 必須以 taxonomy 為核心，而不是只算 must_include 是否出現。

### angle_coverage

每個 taxonomy key 都要有：

- `primary_count`
- `test_count`
- `total`
- `status`
- `redundancy_status`

`status` 定義：

- `core`: 主力角度
- `supporting`: 有承接但不是主軸
- `test_only`: 只在測試池
- `thin`: 有但太少
- `gap`: 幾乎沒承接

`redundancy_status` 定義：

- `balanced`
- `watch`
- `overbuilt`

### protected_phrase / token / motif

v1.2 仍需完整輸出：

- `protected_phrase_check`
- `token_coverage_check`
- `motif_coverage_check`

---

## 6. final pack 收斂規則

Builder 不可再把所有 retained / observe 通通塞進 final pack。

收斂原則：

- 以 `character_policy` target 為硬上限
- 先保高信心 retain / reinforce
- 再放 gap-fill replacement
- 最後才考慮 observe_new / observe_borderline

若容量衝突：

1. 先刪 `observe_stale`
2. 再刪 `observe_borderline`
3. 再刪低價值 expansion
4. 最後才動高信心主力

---

## 7. confidence carry-forward

最終素材必須攜帶：

- `decision_confidence`
- `decision_basis_metric`
- `observe_subtype`
- `risk_level`
- `rewrite_mode`
- `coverage_tags`

舊素材：

- 直接繼承 interpreter 的 confidence / basis / observe subtype

新候選：

- replacement：通常 `medium`
- safer rewrite：通常 `medium`
- reinforce expansion：通常 `low` 或 `medium`
- brief_new：通常 `low`

---

## 8. observe_assets_status

Builder 必須額外輸出 `observe_assets_status`，不能把 observe 資訊吞掉。

每筆至少要有：

- `observe_subtype`
- `active_duration_days`
- `disposition`
- `rationale`

目的：

- 讓 packager 能生成真正可執行的 follow-up checklist

---

## 9. quality gates

- 不可把所有 observe 預設留 primary
- 不可遺失 `angle_key`
- 不可遺失 `risk_level` / `rewrite_mode`
- retire 無候選時，必須標記 `replacement_gap_unfilled`
- `coverage_check` 必須能回答哪個角度過度保留、哪個角度不足
- final pack 必須接近真實上稿規模，而不是單純把舊池打包
