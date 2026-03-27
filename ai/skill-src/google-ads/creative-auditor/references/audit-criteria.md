# Creative Audit Criteria

Creative Auditor 的評分規則與 blocker 判斷依據。

---

## 1. Evidence Levels

### `pack_only`

只拿到 final pack 或 packager output，沒有歷史表現或 live snapshot。

可以高信心判斷：

- asset sufficiency
- creative diversity
- product specificity
- policy risk

只能低至中信心判斷：

- fatigue
- platform fit

### `export_backed`

有匯出報表、歷史使用資訊或 asset snapshot，可做中信心 creative audit。

### `live_snapshot`

有 read-only live MCP snapshot 或等價的 account state。  
這是 fatigue / platform-fit 最可信的 evidence layer。

---

## 2. Audit Dimensions

### A. Asset Sufficiency

檢查素材數量與型別是否足以支撐該 campaign type。

#### Search RSA

- headline 目標：15
- description 目標：4

判斷：

- `5`: headline / description 都達標，且 primary / test 都存在
- `3`: 總數接近達標，但某一類明顯偏少
- `1`: headline 或 description 明顯不足，會直接限制投放學習

#### PMax

若只拿到文字素材：

- 先審文字 sufficiency
- 圖像 / 影片只能標 `not verified by current evidence`

若 input 包含 image / video / logo：

- 可一起審 asset completeness

### B. Creative Diversity

看素材是否語意過度重複、角度是否太集中。

判斷：

- `5`: main/test angles 有區分，重複資產少
- `3`: 有少量重複或 angle 偏斜，但仍可運作
- `1`: 大量近義重複，測試位與主力幾乎同句改寫

### C. Product Specificity

看素材是否真的對焦當前產品，而不是被泛品牌或泛系列語言稀釋。

判斷：

- `5`: 核心資產明確承接產品名與產品賣點
- `3`: 有產品對焦，但仍混入較多 generic brand copy
- `1`: 大部分素材只停在品牌層，產品焦點弱

### D. Policy Risk

看是否仍保留高風險結果承諾、醫療暗示、或過度絕對化主張。

blocker 例子：

- 明確醫療/療效承諾
- 高風險舊句仍位於 primary pack
- safer rewrite 被建議但未真正替換

### E. Platform Fit

看素材是否符合對應平台 / 格式 /投放模式。

Search RSA 常見問題：

- CTA / token / protected phrase coverage 不足
- headline / description 分工不清

PMax 常見問題：

- asset type 不全
- 文字與 LP / product feed 指向衝突
- final pack 無法支撐多樣化 asset serving

---

## 3. Severity Rules

### `blocker`

會直接阻斷上稿或必須退回修改。

觸發條件（任一）：

- 高風險政策句仍留在 primary
- asset sufficiency 嚴重不足
- 關鍵 token / protected phrase coverage 缺口未被補回
- creative output 與當前產品嚴重漂移

### `high`

不一定阻斷，但若忽略，極可能造成低效或高風險。

### `medium`

建議本輪處理，但可在人工確認後先保留。

### `low`

屬優化項，無阻斷性。

---

## 4. Upload Decision Rules

### `blocked_for_upload`

當以下任一成立：

- 任一 finding `blocking=true`
- policy risk 維度為 `fail`
- product specificity 嚴重漂移且無補救資產

### `needs_manual_review`

當以下成立：

- 無 blocker
- 但 evidence level 偏弱，或仍有 `high` finding 未處理

### `clear_to_review`

當以下全部成立：

- 無 blocker
- 整體 creative health 可接受
- 所有高風險問題已降為可審核狀態

---

## 5. Integration Rules

Creative Auditor 的輸出只可作為：

- preflight gate
- challenger review
- upstream constraints

不可：

- 直接改寫現有 `decision_confidence`
- 直接覆寫 `replacement_map`
- 直接跳過 human review
