# 搜尋字詞清洗報告

**品牌**：{brand_name}
**分析週期**：{date_range}
**資料來源**：Google Ads 搜尋字詞報表
**產出日期**：{today}
**閾值設定**：花費 NT${cost_threshold} 以上且零轉換 → 否定候選

---

## 執行摘要

| 項目 | 數值 |
|------|------|
| 分析字詞總數 | {total_terms} |
| 分析期間總花費 | NT${total_cost} |
| 浪費花費（建議排除字詞） | NT${wasted_cost}（佔 {wasted_pct}%） |
| 建議新增否定關鍵字 | {neg_count} 個 |
| 建議建立新廣告群組 | {new_group_count} 個 |
| 持續監控字詞 | {monitor_count} 個 |

> ⚠️ 執行前請逐列審核，確認每個建議符合當前帳戶策略。

---

## 1. 建議新增否定關鍵字

> 標準：花費 ≥ NT${cost_threshold} 且轉換 = 0，且符合不相關判斷。

| 搜尋字詞 | 廣告活動 | 花費 | 點擊 | 轉換 | 建議層級 | 原因 |
|----------|----------|------|------|------|----------|------|
| {term} | {campaign} | NT${cost} | {clicks} | 0 | {level} | {reason} |

**各層級小計**
- 帳戶層級：{account_level_count} 個
- 廣告活動層級：{campaign_level_count} 個
- 廣告群組層級：{adgroup_level_count} 個

---

## 2. 建議建立新廣告群組

> 標準：點擊 ≥ 10 且轉換率高於帳戶均值 1.2 倍，目前在混合群組中稀釋預算。

| 搜尋字詞 | 目前廣告群組 | 點擊 | 轉換率 | 建議群組名 | 優先原因 |
|----------|-------------|------|--------|-----------|---------|
| {term} | {current_group} | {clicks} | {conv_rate}% | {suggested_name} | {reason} |

---

## 3. 持續監控

> 這些字詞目前數據不足以判斷，不建議立即排除。下次審查時重新評估。

| 搜尋字詞 | 廣告活動 | 花費 | 點擊 | 曝光 | 監控原因 |
|----------|----------|------|------|------|----------|
| {term} | {campaign} | NT${cost} | {clicks} | {impressions} | {reason} |

---

## 4. 浪費預算分析

> 有花費、低 CTR（< 2%）、零轉換，但花費低於閾值暫未列入否定候選。

| 搜尋字詞 | 廣告活動 | 花費 | CTR | 點擊 | 判定原因 |
|----------|----------|------|-----|------|----------|
| {term} | {campaign} | NT${cost} | {ctr}% | {clicks} | {reason} |

### 浪費預算分類小計

| 類型 | 金額 | 佔浪費比例 |
|------|------|-----------|
| 明確不相關字詞 | NT${irrelevant_cost} | {irrelevant_pct}% |
| 低意圖資訊字詞 | NT${info_cost} | {info_pct}% |
| 競品字詞 | NT${competitor_cost} | {competitor_pct}% |
| 其他低效字詞 | NT${other_cost} | {other_pct}% |
| **合計** | **NT${total_wasted}** | **100%** |

---

## 5. 下一步行動清單

- [ ] 將「建議新增否定關鍵字」清單匯入 Google Ads 否定關鍵字工具
- [ ] 為「建議建立新廣告群組」的字詞建立新群組並撰寫對應文案
- [ ] 將「持續監控」清單記錄，{next_review_date} 再次審查
- [ ] 確認浪費預算的根本原因（比對類型設定是否過於廣泛？）

---

*此報告由 Claude search-terms-cleaner skill 產出，請人工審核後執行。*
