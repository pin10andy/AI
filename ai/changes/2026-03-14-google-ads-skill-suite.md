# Change Record: Google Ads AI Skill Suite — Phase 1 建立與 CSV 驗收修正

> 任務：`ai/tasks/2026-03-14-google-ads-skill-suite.yaml`

## Related Task

`ai/tasks/2026-03-14-google-ads-skill-suite.yaml`（gads-001）

## Summary

建立 5 個 Google Ads 自動化技能，並以 LOVEFU 真實搜尋字詞報表（87,966 行）驗收
`search_terms_analyzer.py`，修正欄位名稱不符與小計行混入問題。

---

## Files Created

- `ai/skill-src/google-ads/SKILL.md` — 技能套件入口路由
- `ai/skill-src/google-ads/search-terms-cleaner/SKILL.md`
- `ai/skill-src/google-ads/search-terms-cleaner/scripts/search_terms_analyzer.py`
- `ai/skill-src/google-ads/search-terms-cleaner/references/classification-rules.md`
- `ai/skill-src/google-ads/search-terms-cleaner/templates/output-report.md`
- `ai/skill-src/google-ads/search-terms-cleaner/assets/sample-report.csv`
- `ai/skill-src/google-ads/performance-reviewer/SKILL.md`
- `ai/skill-src/google-ads/performance-reviewer/scripts/performance_analyzer.py`
- `ai/skill-src/google-ads/keyword-architect/SKILL.md`
- `ai/skill-src/google-ads/keyword-architect/references/grouping-guide.md`
- `ai/skill-src/google-ads/ad-copy-builder/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `ai/skill-src/google-ads/lp-alignment-auditor/SKILL.md`
- `ai/skill-src/google-ads/lp-alignment-auditor/references/alignment-criteria.md`

## Files Updated

- `ai/skill-src/google-ads/search-terms-cleaner/scripts/search_terms_analyzer.py`
  — 以下為 CSV 驗收後的修正項目：

  | 修正項目 | 原因 |
  |---------|------|
  | COLUMN_MAP 新增 `互動` → `clicks` | Google Ads 新版 / PMax 格式使用「互動」而非「點擊次數」 |
  | COLUMN_MAP 新增 `互動率` → `ctr_raw` | 同上，「互動率」取代「點閱率」 |
  | COLUMN_MAP 新增 `平均費用` → `avg_cpc` | PMax 使用「平均費用」而非「平均單次點擊出價」 |
  | COLUMN_MAP 新增 `曝光` → `impressions` | 新版格式省略「次數」兩字 |
  | COLUMN_MAP 新增 `轉換` → `conversions` | 同上 |
  | COLUMN_MAP 新增 `單次轉換費用` → `cost_per_conv` | 取代「費用/轉換次數」 |
  | COLUMN_MAP 新增 `廣告活動類型`、`貨幣代碼`、`平均千次曝光出價` | 新格式欄位，需辨識但部分僅作顯示用 |
  | 搜尋字詞空格正規化 | Google Ads 匯出的中文字詞會在字元間插入空格（如「乳膠 墊 如何 清洗」），統一以 `.replace(' ', '')` 移除 |
  | 保留 `term_raw` 欄位 | 正規化後保留原始格式供稽核 |
  | 增加 `campaign_type` 欄位 | 輸出報告中顯示廣告活動類型（最高成效 / 搜尋 / 購物） |
  | 小計行過濾修正 | 原本只過濾 `'總計'`，未處理 `'總計：需求開發'` 格式的子計行 |

## Files Removed

無

## Sync / Deployment Impact

如要讓 Claude Code 即時使用，需執行：
```
bash scripts/sync-skills.sh
```
本次尚未執行 sync，技能仍僅存在於 `ai/skill-src/`。

## Open Issues

- [ ] `keyword_analyzer.py`（keyword-architect 技能）尚未建立
- [ ] 無厘頭動畫、青寓品牌資料未填入 `ai/brand/master-brand.yaml`
- [ ] 搜尋字詞中的「轉換」數值異常偏高（含微轉換），分析閾值需依實際帳戶校準
- [ ] 轉換率 37.49% 疑似包含微轉換（頁面停留、按鈕點擊等），需確認 Google Ads 轉換設定
