# 素材成效決策規則 v1.2

Creative Performance Interpreter 在 v1.2 只處理四件事：

1. 輸入資料層升級
2. observe 決策細化
3. candidate pipeline 自動化
4. angle taxonomy 標準化

---

## 0. legacy 三分模型維持不變，但 angle_key 變成硬欄位

### protected_phrase

- 保護的是 phrase coverage，不是保護任何單一 asset
- 例：`100天安心睡`

### must_include_token

- 保護的是 token 在線上素材池的可見性，不是保護某一則舊句
- 例：`山丘樂眠床`、`立即選購`

### reusable_motif

- 只作為 pattern reuse 與 candidate generation 依據
- 不可當 retain hard gate

### angle_key

- input `assets[*].angle_key` 必填
- 不可在 builder 端才用 heuristic 補欄位
- taxonomy 固定為：
  - `product_feel`
  - `risk_reversal`
  - `brand_trust`
  - `entry_value`
  - `life_scene`
  - `concrete_number`
  - `pain_point`
  - `social_proof`
  - `legacy_phrase`
  - `cta_lower_friction`

---

## 1. 先判資料層，不可直接跳到四欄決策

### 1.1 click layer

判讀 click-layer 的最低需求：

- `impressions`
- `clicks`
- `ctr`
- `active_duration_days`

若任一缺失：

- `decision_basis.primary_metric = association_proxy_only`
- `decision_confidence` 不得高於 `directional`
- `data_sufficiency.click_layer_verdict != ready`

### 1.2 conversion layer

判讀 conversion-layer 的最低需求：

- click-layer 全欄位
- `asset_level_conversions`

若缺 `asset_level_conversions`：

- 可繼續做 click-layer 判讀
- `decision_confidence` 不得高於 `medium`
- `decision_basis.primary_metric` 不得使用純 conversion basis

若有 `conversion_value`：

- 可作為 supporting metric
- 可提高 `hybrid_asset_type_percentile` 的可用性

### 1.3 placement layer

若 `placement_breakout` 可用：

- 允許 Search / Display 分開看
- `decision_basis.placement_scope` 必須顯示 `search` / `display` / `mixed` / `overall`
- 若 Search 與 Display 方向明顯衝突，`decision_confidence` 至少降一級

若 `placement_breakout` 不可用：

- `placement_scope = overall`
- 不可假裝知道 placement 差異

### 1.4 duration layer

`active_duration_days` 是 v1.2 observe 細化的必要欄位。

若缺此欄：

- 不得輸出 `observe_new` / `observe_stale`
- `decision_confidence` 不得高於 `low`

---

## 2. percentile 仍只在 asset_type cohort 內算

cohort 只能依下列類型分開計算：

- `short_headline`
- `long_headline`
- `headline`
- `description`

若 placement breakout 足夠且要做 split interpretation：

- 仍然先依 `asset_type` 分 cohort
- 再在同 asset_type 內參考 placement 差異
- 不可把不同 asset_type 混算

若 cohort eligible assets < 5：

- 可做方向性判斷
- `decision_confidence` 不得高於 `low`

---

## 3. decision_basis 與 decision_confidence

### 3.1 decision_basis.primary_metric

只能是：

- `association_proxy_only`
- `ctr_asset_type_percentile`
- `conversion_rate_asset_type_percentile`
- `hybrid_asset_type_percentile`

### 3.2 high confidence

全部成立才可標 `high`：

- click layer = ready
- conversion layer = ready
- `asset_level_conversions >= minimum_conversion_threshold`
- `impressions >= minimum_impressions_threshold`
- `clicks >= minimum_clicks_threshold`
- cohort eligible assets >= 5
- placement breakout 沒有明顯相反訊號

### 3.3 medium confidence

適用情況：

- click layer = ready
- conversion layer = ready or partial
- 指標方向一致，但 conversion 數仍不夠厚
- 或 placement 可用但有輕微信號落差

### 3.4 low confidence

適用情況：

- click layer 雖可用，但 cohort 偏小
- 或 placement split 顯示波動較大
- 或 `active_duration_days` 顯示素材仍處於很早期的觀察期

### 3.5 directional

適用情況：

- 只能靠 `association_proxy_only`
- 或 impression / click / ctr 缺欄
- 或素材明顯未達最小資料門檻

---

## 4. v1.2 決策桶

### retain

保留條件：

- 站在同 asset_type cohort 至少 >= P50
- 或是穩定的 protected phrase carrier
- 且沒有明顯 compliance 風險需要改寫

### retire

退場條件：

- 同 asset_type cohort < P25
- 有足夠資料量
- 不會打破 protected phrase coverage

若 asset 含 must-include token：

- 仍可 retire
- 但 `coverage_gap_created` 必須寫出 token gap
- candidate pipeline 必須補一個 replacement candidate

### retire_candidate

這不是正式停用，而是優先淘汰候補。

觸發條件：

- 原本應屬 `observe_insufficient_data`
- 但 `active_duration_days >= retire_candidate_days`
- 且 impression / click / conversion 仍不足以形成有效訊號

### reinforce

強化條件：

- 同 asset_type cohort >= P75
- 有明確 click / conversion 證據

reinforce 除了保留素材外，還要輸出：

- `high_value_language.patterns`
- 可重用 motif
- 至少一個 expansion 或 safer-rewrite candidate

### observe_new

適用於：

- 新上線
- `active_duration_days` 很短
- 指標尚未成熟但不弱

### observe_insufficient_data

適用於：

- 資料量不足
- 但尚未 stale
- 仍值得給一段觀察期

### observe_stale

適用於：

- impression / click / conversion 都偏薄
- `active_duration_days >= observe_stale_days`
- 再繼續佔 primary slot 的價值偏低

### observe_borderline

適用於：

- 指標接近 P25-P50 邊界
- 有部分訊號，但還不能直接 retire / reinforce

---

## 5. active_duration downgrade logic

### observe_insufficient_data -> retire_candidate

若同時成立：

- `active_duration_days >= retire_candidate_days`
- `impressions < minimum_impressions_threshold` 或 `clicks < minimum_clicks_threshold`
- `asset_level_conversions < minimum_conversion_threshold` 或缺 conversion

則：

- 不再維持 `observe_insufficient_data`
- 改輸出 `retire_candidate`

### observe_stale 的核心用途

- 告訴 builder 這些素材不該再預設留在主力池
- 進入 watchlist 或 demotion queue

---

## 6. candidate pipeline automation

### 6.1 retire gap 必補 replacement candidate

每個 `retire_now_assets[*]` 至少要嘗試補：

- 1 個 `replace_retired_asset` candidate

若該 retire gap 無法補滿：

- gap 必須仍寫進 `coverage_gap_created`
- 下游 builder 必須能把它標成 `replacement_gap_unfilled`

### 6.2 reinforce 必補 test candidate

若某個 angle 被判定為 `reinforce`：

- 至少補 1 個 test candidate
- `source = reinforce_expansion` 或 `brief_generator_auto`

### 6.3 高效但高風險語言

若歷史 winner 效果好，但語言風險高：

- 不可只因表現好就原句繼續擴寫
- 必須產出 `rewrite_mode = safer-rewrite` 的 candidate
- `safer_rewrite_of` 要指向風險來源素材

### 6.4 candidate 必填欄位

每筆 `new_candidate_assets` 必須有：

- `angle_key`
- `intent`
- `related_gap`
- `covers_tokens`
- `inherits_motifs`
- `risk_level`
- `rewrite_mode`

---

## 7. handoff contract

下游 builder 一定要吃到：

- `asset_decisions[*].angle_key`
- `asset_decisions[*].decision`
- `asset_decisions[*].observe_reason`
- `asset_decisions[*].active_duration_days`
- `retire_now_assets[*].coverage_gap_created`
- `new_candidate_assets[*].risk_level`
- `new_candidate_assets[*].rewrite_mode`
- `new_candidate_assets[*].safer_rewrite_of`
- `next_round_brief_additions.candidate_pipeline_triggers`

若這些欄位任一缺失：

- 視為 handoff 不完整

---

## 8. quality gates

- 不可在缺 impression / click / ctr 時假裝做 click-layer interpretation
- 缺 asset-level conversion 時，不可給 `high` confidence
- observe 不可再只輸出單一 `observe`
- `angle_key` 不可由下游 heuristic 補欄位
- 每個 retire gap 至少要嘗試補 replacement candidate
- 高效但高風險語言必須有 safer rewrite 路徑
