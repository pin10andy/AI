# Google Ads PMax Playbook

> PMax 文案 workflow。
> 目前只處理文字素材，不包含圖片、影片與 feed。

## Goal

把固定 brief 轉成可直接進人工 review 的 PMax 文案包：

- 15 個 short headlines
- 5 個 long headlines
- 5 個 descriptions
- 3 個 distinct angles
- compliance notes

## Required Inputs

執行前必須讀取：

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/google-ads-brief.schema.json`
3. `ai/schemas/google-ads-pmax-output.schema.json`
4. `ai/evals/ads-rubric.yaml`
5. `ai/evals/google-ads-pmax-human-review.md`

## Workflow

### Step 1: Validate the brief

- brief 必須符合 `ai/inputs/google-ads-brief.schema.json`
- `campaign_type` 必須是 `pmax`
- `constraints.character_policy` 必須對應 PMax counts

### Step 2: Read brand constraints

從 `ai/brand/master-brand.yaml` 抓出：

- `voice.tone`
- `voice.do`
- `voice.do_not`
- `languages.rules`
- `target_audience`

強制規則：

- 行銷素材使用繁體中文
- 不得做醫療治療承諾
- 不得低價促銷喊賣
- 不得中英混雜一句話

### Step 3: Derive exactly 3 angles

先產 angle，再產資產。

每個 angle 必須：

- 有清楚標籤
- 有 brief / 品牌脈絡支撐
- 能同時延伸到 short headlines、long headlines、descriptions

### Step 4: Generate the PMax asset pack

硬性規格：

- short headlines 恰好 15 個，≤ 30 字元
- long headlines 恰好 5 個，≤ 90 字元
- descriptions 恰好 5 個，≤ 90 字元
- 至少 1 個 description ≤ 60 字元
- 至少 3 個 short headlines 含 primary keywords

內容規格：

- short headlines 要可被不同版位重組，不要只是同一句換字序
- long headlines 要補足短標題沒講清楚的價值
- descriptions 要能承接 PMax 自動組合情境
- CTA 要能對應 landing page 的主要行動

### Step 5: Self-check before output

輸出前逐項確認：

- schema 欄位齊全
- 三種資產數量都正確
- 至少一個短版 description
- 3 個 angle 都有實際覆蓋
- 無 `forbidden_claims`
- 無 `voice.do_not` 違規

### Step 6: Produce two deliverables

1. JSON：符合 `ai/schemas/google-ads-pmax-output.schema.json`
2. Markdown：依 `ai/skill-src/google-ads-writer/templates/pmax-output.md`

## Failure Conditions

以下情況不得假裝完成：

- 無法湊出 3 個真正不同的 angle
- short / long headlines 大量重複
- 沒有任何 description 能壓到 60 字內
- brief 明確要求與品牌規範衝突
- 使用者其實要的是既有素材優化，而不是新建素材
