---
name: "search-terms-cleaner"
description: "分析 Google Ads 搜尋字詞報表 CSV，產出否定關鍵字建議、新廣告群組建議、浪費預算分析。當使用者提到搜尋字詞清洗、否定關鍵字、negative keyword、字詞報表、低效字詞、浪費預算時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
  python-tools: search_terms_analyzer.py
---

# Search Terms Cleaner

> **Canonical source**: `ai/skill-src/google-ads/search-terms-cleaner/SKILL.md`
> Do NOT edit copies in `.claude/skills/`. Always edit here and run `scripts/sync-skills.sh` to deploy.

分析 Google Ads 搜尋字詞報表，找出該排除的字、該獨立成群組的字、正在燒錢的字。輸出人工審核後可直接執行的建議清單。

## Required References

執行前必須讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`（品牌語氣、產品線、受眾）
2. **分類規則**：`references/classification-rules.md`（意圖分類與否定字判斷邏輯）

## When to Use

- 使用者提供搜尋字詞 CSV，要求清洗或分析
- 使用者說「幫我看搜尋字詞」「哪些字要加否定」「有哪些字在燒錢」
- 定期帳戶維護（建議每 2 週執行一次）

## Required Inputs

執行前詢問使用者：

1. **CSV 路徑**：從 Google Ads 後台匯出的搜尋字詞報表
2. **花費閾值**（選填，預設 NT$300）：超過此金額且零轉換才列入否定候選
3. **分析週期**（選填，如「過去 30 天」）：寫入報告標題

如果使用者沒提供閾值，使用預設值並在報告中標注。

## Execution Steps

### Step 1：讀取品牌 Context

```
Read ai/brand/master-brand.yaml
注意：brand.name、target_audience.segments、voice.do_not
這些會影響「相關 vs 不相關」的判斷
```

### Step 2：執行量化預篩腳本

```bash
python3 scripts/search_terms_analyzer.py {csv_path} \
  --cost-threshold {threshold} \
  --format json
```

腳本輸出 JSON，包含：
- `summary`：總覽數據
- `negative_candidates`：高花費零轉換
- `new_group_candidates`：高點擊高轉換率
- `wasted`：明確不相關且有花費
- `monitor`：數據不足需觀察

### Step 3：意圖分類與策略判斷

根據 `references/classification-rules.md` 的規則，逐一對 `negative_candidates` 和 `wasted` 清單做意圖判斷：

**對每個字詞判斷：**
- 搜尋意圖是否符合品牌受眾？（參考 `master-brand.yaml > target_audience`）
- 是否為競品字？（查 `master-brand.yaml > voice.do_not` 有無提示）
- 是否為資訊型低商業意圖字？
- 建議加入哪個層級的否定清單？（帳戶 / 廣告活動 / 廣告群組）

**判斷標準（嚴格執行，不得只說「建議優化」）：**
- 排除：花費超閾值 + 轉換 = 0 + 明確不相關
- 排除：與品牌受眾完全不符（如 DIY 教學字、職缺字、非目標受眾字）
- 保留觀察：有點擊無轉換但意圖模糊（放入 monitor）
- 新 ad group：轉換率高於均值且字詞還沒獨立成群組

### Step 4：產出結構化報告

按 `templates/output-report.md` 格式輸出。

**強制要求：**
- 每一列否定字建議必須有「原因」欄，不得空白
- 每一列新 ad group 建議必須有「建議群組名」
- 浪費預算摘要必須列出總金額與佔比
- 不得輸出「建議持續優化」這類空話

## Output Format

輸出為 Markdown 表格報告，包含：

1. **執行摘要**（5 行以內）：分析字詞數、總花費、浪費金額、建議否定字數、建議新 ad group 數
2. **建議新增否定關鍵字**：字詞 / 廣告活動 / 花費 / 點擊 / 轉換 / 建議層級 / 原因
3. **建議建立新廣告群組**：字詞 / 目前歸屬 / 點擊 / 轉換率 / 建議群組名 / 原因
4. **持續監控**：字詞 / 花費 / 點擊 / 轉換 / 監控原因
5. **浪費預算分析**：字詞 / 花費 / CTR / 原因 + 分類小計

## Quality Gates

輸出前自我檢查：

- [ ] 每一筆否定字建議都有具體原因（不是「花費高」這種廢話）
- [ ] 建議層級（帳戶/活動/群組）已標注
- [ ] 浪費金額已計算並標注佔比
- [ ] 沒有模糊字詞被錯誤標記為排除（應放 monitor）
- [ ] 報告格式符合 templates/output-report.md

---

## Artifact Governance

本技能產出為搜尋字詞清洗報告。

### 輸出路徑規則

- 分析報告寫入 `ai/reports/`（命名 `YYYY-MM-DD-{slug}.md`）
- 暫存/測試輸出寫入 `scratch/google-ads/`
- **禁止**將輸出寫入 repo 根目錄

### 政策參考

- `ai/registry/storage-map.yaml` / `ai/policies/artifact-naming-policy.md` / `ai/policies/artifact-write-policy.md`
