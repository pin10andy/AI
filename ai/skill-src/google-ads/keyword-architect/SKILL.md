---
name: "keyword-architect"
description: "將原始關鍵字清單分群、分類意圖、建議廣告群組結構與對應 landing page。當使用者提到關鍵字研究、關鍵字分群、keyword research、如何分廣告群組、哪些字要一起跑時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
  python-tools: keyword_analyzer.py
---

# Keyword Architect

> **Canonical source**: `ai/skill-src/google-ads/keyword-architect/SKILL.md`
> Do NOT edit copies in `.claude/skills/`. Always edit here and run `scripts/sync-skills.sh` to deploy.

將一包原始關鍵字轉化為「可直接建帳戶用」的廣告群組架構。輸出包含：分群結果、意圖分類、建議比對類型、推薦 landing page。

## Required References

執行前必須讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`（產品線、USP、受眾）
2. **分群指南**：`references/grouping-guide.md`（分群原則與比對類型選擇）

## When to Use

- 使用者提供一份關鍵字清單（CSV 或貼上文字）要求整理
- 使用者說「幫我分廣告群組」「這些字怎麼分」「哪些字要一起跑」
- 建立新廣告活動前的關鍵字架構規劃

## Required Inputs

執行前詢問：

1. **關鍵字清單**：CSV 或直接貼上（每行一個字）
2. **廣告活動目的**（選填）：品牌曝光 / 產品轉換 / 競品搶量 / 再行銷
3. **是否附帶搜尋量或 CPC 數據**（選填）：有的話影響優先級排序

## Execution Steps

### Step 1：讀取品牌 Context

```
Read ai/brand/master-brand.yaml
重點：brand.name、target_audience.segments、所有產品線名稱
這些決定「哪些字屬於哪個產品線」
```

### Step 2：執行量化腳本（如有 CSV）

```bash
python3 scripts/keyword_analyzer.py {keywords_csv} --format json
```

腳本輸出初步分群建議（依字詞相似度與主題聚類）。

如果使用者只是貼上文字，直接進入 Step 3。

### Step 3：意圖分類

對每個關鍵字標記意圖：

| 意圖 | 說明 | 建議比對類型 |
|------|------|------------|
| **商業型** | 有明確購買信號（推薦、比較、多少錢） | Exact / Phrase |
| **品牌型** | 包含品牌名或產品系列名 | Exact（高優先） |
| **問題型** | 描述痛點（腰痛、睡不好、頸椎不舒服） | Phrase / Broad（搭配否定字） |
| **競品型** | 包含競品品牌名 | Exact（策略性） |
| **資訊型** | 學習搜尋（什麼是、如何選、原理） | 視策略決定是否投放 |
| **產品型** | 直接搜尋產品名（獨立筒床墊、乳膠枕） | Exact / Phrase |

### Step 4：分群建議

依以下原則將關鍵字分配到廣告群組：

**分群原則**（詳見 `references/grouping-guide.md`）：
- 同一群組的字必須能共用同一套文案
- 同一群組的字應對應同一個 landing page
- 同一群組字數以 10–20 個為宜，超過考慮再拆
- 品牌字、競品字、產品字各自獨立群組

**命名規則**（依 master-brand.yaml 中的命名慣例）：
- 格式：`{廣告活動}_{群組主題}`
- 範例：`品牌_床墊_獨立筒`、`品牌_枕頭_頸椎痛`

### Step 5：Landing Page 建議

對每個廣告群組，建議最合適的 landing page 類型：

- 商業型 → 對應產品頁（需有價格、CTA、社證）
- 問題型 → 問題解決頁或測試/評測頁（需有量脖子/試躺流程）
- 品牌型 → 首頁或品牌故事頁
- 競品型 → 比較頁（如有）

### Step 6：輸出架構表

按 `templates/keyword-architecture.md` 格式輸出。

## Output Format

1. **分群總覽**：幾個廣告群組、總關鍵字數、建議廣告活動結構
2. **各群組詳細表**：群組名 / 關鍵字 / 意圖 / 比對類型 / 建議 LP
3. **不建議投放的字**：資訊型 / 低商業意圖字的處理建議
4. **否定字初始建議**：根據分群結果，各活動應先加的否定字

## Quality Gates

- [ ] 每個群組內的字都能共用同一套文案
- [ ] 品牌字與非品牌字已分開
- [ ] 每個群組都有對應的 landing page 建議
- [ ] 比對類型建議有說明理由
- [ ] 資訊型字有明確的處理建議（排除 or 單獨群組）

---

## Artifact Governance

本技能產出為關鍵字架構報告。

### 輸出路徑規則

- 分析報告寫入 `ai/reports/`（命名 `YYYY-MM-DD-{slug}.md`）
- 暫存/測試輸出寫入 `scratch/google-ads/`
- **禁止**將輸出寫入 repo 根目錄

### 政策參考

- `ai/registry/storage-map.yaml` / `ai/policies/artifact-naming-policy.md` / `ai/policies/artifact-write-policy.md`
