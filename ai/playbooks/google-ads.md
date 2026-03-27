# Google Ads 素材生成 Playbook

> 此 playbook 是所有 AI agent 產出 Google Ads 素材的共用流程。
> Search RSA 文案 MVP 請優先使用：`ai/playbooks/google-ads-search-rsa.md`
> PMax 文案 workflow 請優先使用：`ai/playbooks/google-ads-pmax.md`
> 品牌規範請引用：`ai/brand/master-brand.yaml`
> 輸出 schema 請遵循：`ai/schemas/ads-asset.schema.json`
> 評估標準請參照：`ai/evals/ads-rubric.yaml`

---

## 1. 輸入需求

執行此 playbook 前，需要確認以下資訊：

- **產品/服務名稱**
- **廣告類型**：搜尋廣告 / 回應式搜尋廣告 (RSA) / 多媒體廣告 / Performance Max
- **目標受眾**：參考 `master-brand.yaml > target_audience`
- **推廣重點**：主要賣點或優惠
- **CTA（行動呼籲）**：期望使用者採取的行動
- **關鍵字清單**（選填）

---

## 2. 執行步驟

### Step 1：讀取品牌規範
```
載入 ai/brand/master-brand.yaml
確認 voice、tone、language 設定
```

### Step 2：生成素材草稿
根據廣告類型產出對應欄位：

**RSA（回應式搜尋廣告）：**
- 標題 (headlines)：最多 15 組，每組 ≤ 30 字元
- 描述 (descriptions)：最多 4 組，每組 ≤ 90 字元

**多媒體廣告：**
- 短標題：≤ 25 字元
- 長標題：≤ 90 字元
- 描述：≤ 90 字元

### Step 3：自我檢查
依據 `ai/evals/ads-rubric.yaml` 的維度自行評估：
- 品牌一致性
- 字數限制
- CTA 明確度
- 語言正確性

### Step 4：輸出
輸出必須符合 `ai/schemas/ads-asset.schema.json` 格式。

---

## 3. 品質要求

- 每組標題之間要有足夠差異性，避免重複表達
- 至少包含 1 組含有關鍵字的標題
- 至少包含 1 組含有 CTA 的標題
- 描述要補充標題未涵蓋的賣點
- 所有文案遵循品牌 voice 規範

---

## 4. 常見錯誤

- 標題超過字元限制
- 使用品牌規範禁止的語氣或用詞
- 所有標題過於相似
- 缺少明確的行動呼籲
- 中英文混雜不當
