# Google Ads Search RSA Playbook

> Search RSA 文案 MVP 的單一路徑。
> V1 只處理 Search RSA，不處理 PMax。

## Goal

把固定 brief 轉成可直接進人工 review 的 Search RSA 素材包：

- 15 個 headlines
- 4 個 descriptions
- 3 個 distinct angles
- compliance notes

## Required Inputs

執行前必須讀取：

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/google-ads-brief.schema.json`
3. `ai/schemas/google-ads-search-output.schema.json`
4. `ai/evals/ads-rubric.yaml`
5. `ai/evals/google-ads-human-review.md`

## Workflow

### Step 1: Validate the brief

- brief 必須符合 `ai/inputs/google-ads-brief.schema.json`
- `campaign_type` 必須是 `search_rsa`
- 若 brief 缺欄位，不可自行腦補品牌規則；先以 brief + `master-brand.yaml` 能支持的範圍生成

### Step 2: Read brand constraints

從 `ai/brand/master-brand.yaml` 抓出：

- `voice.tone`
- `voice.do`
- `voice.do_not`
- `languages.rules`
- `target_audience`

強制規則：

- 行銷素材使用繁體中文
- 不得使用廉價促銷語氣
- 不得做醫療治療承諾
- 不得中英混用一句話

### Step 3: Derive exactly 3 angles

先產 angle，再產 copy。

每個 angle 必須：

- 有清楚標籤
- 有 brief / 品牌脈絡支撐理由
- 與另外兩個 angle 有明顯區隔

建議優先從以下方向擇三：

- product truth
- pain-to-relief
- trust / service proof
- CTA / next step

### Step 4: Generate the RSA bundle

硬性規格：

- headlines 恰好 15 個
- descriptions 恰好 4 個
- headline ≤ 30 字元
- description ≤ 90 字元
- 至少 3 個 headlines 含 primary keywords
- 每個 angle 至少對應 4 個 headlines

內容規格：

- headlines 不能只是同一句換字序
- descriptions 要補充 headlines 沒說清楚的價值
- CTA 要跟 `landing_page_summary.primary_cta` 一致或相近
- 如有風險，放進 `compliance_notes`

### Step 5: Self-check before output

輸出前逐項確認：

- schema 欄位齊全
- 字元數全部合規
- 3 個 angle 都有被實際使用
- 無 `forbidden_claims`
- 無 `voice.do_not` 違規

### Step 6: Produce two deliverables

1. JSON：符合 `ai/schemas/google-ads-search-output.schema.json`
2. Markdown：依 `ai/skill-src/google-ads-writer/templates/search-rsa-output.md` 呈現，供人工 review

## Failure Conditions

以下情況不得假裝完成：

- 無法湊出 3 個真正不同的 angle
- headline 或 description 超字數
- 素材大量重複
- brief 明確要求與品牌規範衝突
- 使用者要的是 PMax
