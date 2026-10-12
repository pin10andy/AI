# Woolito 診斷 v0.1 — 匿名 fallback 完成

**BLOCKED_ON_ACCOUNT_DATA**。GO：離線契約、分類器與合成回測可交審。
NO_GO：真實花費結論、正式排除／帳戶改動、automation／production schedule。
產品策略留空，未選 STRUCTURE_FIRST／NEGATIVE_LIST_FIRST／AUTOMATION_WARRANTED／NO_OP。

Canonical：[OS #47](https://github.com/pin10andy/personal-operating-dashboard/issues/47)。
落點既有 AI search-terms-cleaner；唯一 Builder Codex，本輪完成即釋放 owner，下一 owner DOT / Andy。

## 主要發現

1. Legacy analyzer 無 date/IDs/trigger keyword/coverage，缺值變零，高成本零轉換列 negative，免費／教學子字串推高層級；不能據此得出 Woolito 浪費或排除結論。
2. 本機限定來源只有床墊 demo，未取得 Woolito 五份 export；不新增 connector，不索取新權限。
3. 合成 21 列：KEEP_B2B 11、REVIEW 6、NEGATIVE_EXACT_CANDIDATE 4，所有列人工審核。
   候選只為完整鬼滅之刃動畫／動漫線上看／動畫免費下載／動畫工作招聘；無「動畫」單字否定。
4. 跨列可見轉換、歷史轉換、原 group enabled positive 衝突均阻擋候選；缺資料降 REVIEW。
   正向意圖擴張、近似變體、中文否定切詞未模擬，clear 僅有限文字核對。

## 匿名執行證據（完全合成，不是 Woolito）

合成範圍 2026-07-14～2026-10-11，synthetic-c1 有 90 日 totals（含零日）。
可見 cost 2310 / total 4000 = 57.75%；可見 clicks 105 / total 200 = 52.5%。
這些數字只驗證計算與分母口徑，**沒有真實浪費／節省／ROAS 結論**。
工具輸出 top_visible_sources 按 campaign/trigger keyword/match/decision/reason 分組；
候選成本不稱作 recoverable savings，零轉換不等於浪費。
fixture conversion lag 為 14 天示例，真實 lag 待確認；近期查詢等成熟後重跑。
搜尋報表隱藏長尾不可歸類、不可將可見比例外推全帳戶。

執行方式與欄位詳見
[CSV 契約](../skill-src/google-ads/search-terms-cleaner/references/woolito-diagnostic-contract.md)。
匿名候選證據可由版本內 fixture 重跑；scratch 不作永久 evidence link。

## 決策比較與最小下一步

- 先看 broad/phrase「動畫」是否在少數來源集中明確非商業可見成本。若是，結構調整可能比長期追逐新片名有效；需評估優質流量流失。
- 若是有限穩定完整查詢，先審低風險 exact 提案；新變體需維護，不能保證覆蓋所有污染。
- 自動化必須先有新候選頻率、每次審核分鐘、每月工時與真實成本收益證據；不足不建。
- 若影響微小或風險高可 NO_OP；本輪無真實資料，不能任選。

下一 owner DOT / Andy：在**既有核准私有位置**備齊 search terms、enabled positives、
分層 negatives＋shared bindings、90 日 campaign totals、已知有效轉換查詢／保護詞，核對 manifest 完整性與 lag。
不公開原始資料，無需增加權限。下一次 Codex 只重跑此 CLI、審 coverage/候選及成本來源，
再選產品策略。任何 live write 需另案授權。本輪不 merge、不 deploy。
