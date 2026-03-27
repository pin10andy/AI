# Google Ads 成效週報

**品牌**：{brand_name}
**分析層級**：{level}（廣告活動 / 廣告群組 / 廣告素材）
**分析週期**：{date_range}
**目標 ROAS**：{target_roas}x | **目標 CPA**：NT${target_cpa}
**產出日期**：{today}

---

## 整體摘要

| 指標 | 本期 | 上期 | 變化 |
|------|------|------|------|
| 總花費 | NT${total_cost} | NT${prev_cost} | {cost_change}% |
| 總轉換 | {total_conv} | {prev_conv} | {conv_change}% |
| 整體 ROAS | {overall_roas}x | {prev_roas}x | {roas_change}% |
| 整體 CPA | NT${overall_cpa} | NT${prev_cpa} | {cpa_change}% |
| 整體轉換率 | {conv_rate}% | {prev_conv_rate}% | {conv_rate_change}% |

> {overall_assessment}（一句話整體判斷，如「本期整體 ROAS 達標，但競品活動明顯拖低效率」）

---

## 四欄判斷表

| 名稱 | 花費 | ROAS | CPA | 轉換 | 判斷 | 原因 |
|------|------|------|-----|------|------|------|
| {name} | NT${cost} | {roas}x | NT${cpa} | {conv} | 🚀 擴量 | {reason} |
| {name} | NT${cost} | {roas}x | NT${cpa} | {conv} | ✅ 保留 | {reason} |
| {name} | NT${cost} | {roas}x | NT${cpa} | {conv} | 🔬 測試 | {reason} |
| {name} | NT${cost} | {roas}x | NT${cpa} | {conv} | ⏸ 停用 | {reason} |

**統計**：擴量 {scale_count} / 保留 {keep_count} / 測試 {test_count} / 停用 {pause_count}

---

## 異常項目原因假設

> 針對本期 ROAS 變動 > 20% 或 CTR 變動 > 15% 的項目

### {item_name}（{change_type}：{change_pct}%）

**可能原因**：
1. {hypothesis_1}
2. {hypothesis_2}

**建議確認步驟**：
- [ ] {verification_step}

---

## 下週優先事項

1. 【{action_type}】{specific_action}（{reason}）
2. 【{action_type}】{specific_action}（{reason}）
3. 【{action_type}】{specific_action}（{reason}）

> ⚠️ 超過 5 點請刪除優先級最低的，保持清單可執行。

---

*此報告由 Claude performance-reviewer skill 產出，執行前請人工審核。*
