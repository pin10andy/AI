# Validation Record: search_terms_analyzer.py — 真實 CSV 驗收測試

> 任務：`ai/tasks/2026-03-14-google-ads-skill-suite.yaml`（gads-001）

## Related Task

`gads-001` / `ai/tasks/2026-03-14-google-ads-skill-suite.yaml`

## What Was Tested

以 LOVEFU 真實 Google Ads 搜尋字詞報表驗證 `search_terms_analyzer.py` 的解析能力：

1. CSV 欄位自動識別（新版欄位名稱）
2. 數值解析（NT$ 前綴、百分比、`--` 空值）
3. 小計行過濾（`總計：xxx` 格式）
4. 搜尋字詞空格正規化
5. 四類分析輸出（否定字候選 / 建議廣告群組 / 浪費字詞 / 監控）

## Agents / Tools Involved

- claude（腳本撰寫與修正）
- Python 3（腳本執行環境）

## Source of Truth Files

- `ai/skill-src/google-ads/search-terms-cleaner/scripts/search_terms_analyzer.py`
- `ai/brand/master-brand.yaml`（品牌脈絡，供否定字層級判斷）

## Test Input

| 檔案 | 說明 |
|------|------|
| `~/Downloads/搜尋字詞報表.csv` | ❌ 排除：含 22 種轉換動作分段（12,188 行），幾乎全為零花費，不適合分析 |
| `~/Downloads/搜尋字詞報表 (1).csv` | ✅ 採用：無轉換動作分段（87,966 行），有實際花費資料 |

執行指令：
```bash
python3 ai/skill-src/google-ads/search-terms-cleaner/scripts/search_terms_analyzer.py \
  "/Users/andychou/Downloads/搜尋字詞報表 (1).csv" \
  --cost-threshold 100 --min-clicks 3 --format text
```

## Result

**通過（修正後）**

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| CSV 標題列自動偵測 | ✓ | 正確跳過前 2 行（報表標題 + 日期範圍） |
| 欄位識別：`互動` → clicks | ✓ | 修正後正確映射 |
| 欄位識別：`互動率` → ctr_raw | ✓ | 修正後正確映射 |
| 欄位識別：`平均費用` → avg_cpc | ✓ | 修正後正確映射 |
| 欄位識別：`曝光` → impressions | ✓ | 修正後正確映射 |
| 欄位識別：`轉換` → conversions | ✓ | 修正後正確映射 |
| 欄位識別：`單次轉換費用` → cost_per_conv | ✓ | 修正後正確映射 |
| 廣告活動類型欄位顯示 | ✓ | 輸出中可分辨最高成效 / 搜尋 / 購物 |
| 搜尋字詞空格正規化 | ✓ | "乳膠 墊 如何 清洗" → "乳膠墊如何清洗" |
| 小計行過濾（`總計：需求開發`）| ✓ | 修正後正確排除 |
| NT$ 數值解析 | ✓ | NT$0.99 到 NT$2,906 均正確解析 |
| `--` 空值處理 | ✓ | 解析為 0.0 |
| 總資料行數 | ✓ | 87,954 筆（扣除標題、空行、小計行後） |

## Output Summary

```
分析字詞數：87,954
總花費：    NT$1,855,331
總轉換：    42,596
平均 CPC：  NT$16.3
平均轉換率：37.49%
⚠ 浪費花費：NT$93,509（佔 5.0%）

否定字候選：324 個
建議廣告群組：大量（轉換率高於均值 1.2 倍）
浪費字詞：  460 個（小計 NT$12,314）
持續監控：  3,893 個
```

## Issues Found

1. **轉換率異常偏高（37.49%）**
   - 推測原因：Google Ads 帳戶設定了微轉換事件（如頁面捲動、按鈕點擊）
   - 影響：`new_group_candidate` 分類可能過度觸發
   - 建議：確認帳戶「轉換動作」設定，或改用「主要轉換」欄位

2. **`--` 廣告群組名稱**
   - PMax 廣告活動的字詞，廣告群組欄位顯示為 `--`
   - 對分析結果無影響，但視覺上較難識別來源
   - 建議：可改以廣告活動名稱作為 PMax 字詞的群組標識

3. **否定字候選中仍含品牌字詞**（如 `lovefu評價ptt`）
   - 這些字詞有花費但零轉換，屬合理候選，需人工審查
   - 建議：品牌字詞應在報告中特別標記，避免誤加否定

## Conclusion

`search_terms_analyzer.py` 已能正確解析 LOVEFU 真實搜尋字詞報表。
Phase 1 核心技能（search-terms-cleaner）驗收通過。

**建議下一步：**
1. 人工審查 324 筆否定字候選，篩出真正應排除的字詞
2. 確認 Google Ads 轉換設定，校準轉換率基準值
3. 執行 `bash scripts/sync-skills.sh` 部署技能到 `.claude/skills/`
