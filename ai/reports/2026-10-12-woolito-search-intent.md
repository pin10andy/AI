# Woolito 診斷 v0.1 — fallback 與後續真實唯讀收據

**初次 fallback 收據（下方後續真實唯讀收據更新此狀態）**：BLOCKED_ON_ACCOUNT_DATA。GO：離線契約、分類器與合成回測可交審。
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


## 後續真實帳戶唯讀收據（2026-10-12）

Andy 明確批准 Ads／入口 business.google.com 唯讀。沒有 Google Ads MCP，使用既有 Chrome 的獨立 DOM 分頁，未操作其他 X/Fantasy tabs 或前景輸入，未新增 OAuth。
帳戶 picker/header 與品牌廣告網站交叉核實成功；CID／名稱與完整查詢僅保留私有收據。
來源 scope 是原 UI 的 **目前 ENABLED campaign＋ENABLED group**，不是整個歷史帳戶。

下載時間（檔案 mtime UTC）：2026-10-12T08:22:50Z～08:33:55Z。
主期間 2026-07-14～2026-10-11；4 campaign / 5 group。
11,888 search 日明細 → 11,887 normalized（1 個 disjoint query-match pair 合併到 positive-keyword grain）；
44 enabled positive；273 直接 negatives＋8 list bindings；2 shared lists 共667詞；
360 campaign daily totals；168 歷史 tracked-converting query rows。
歷史範圍 2015-11-01～2026-10-12，仍僅 current enabled scope；不是已核實 qualified leads。

coverage：daily visible cost / scoped campaign total = **45.94%**，clicks = **49.89%**。
UI period aggregate 與 daily export 有小差額，原因未確認；不補零或改數字，不外推隱藏 queries。
帳戶 conversion lag 未量測，14 日僅敏感度提示；須成熟後 review。

主要發現：實際關注来源是語義較寬的 **PHRASE 來源 B**，非預設的單字 BROAD。
該來源有 tracked conversions，不能整組判浪費。保守全查詢觀看語境26個、5個有花費；
其可見成本下限佔 daily visible 1.89% / scoped campaign total 0.87%，全部集中來源 B。
1 個 highest-cost query 已在現有 exact negative，不重複提案；歷史花費不能證明 current negative 失效。
其餘4個 paid 完整 query 交人工 exact review，成本只佔 scoped total 0.565%。
21個 zero-cost觀看 queries 不優先新增；未知片名、工具、學習、角色設計仍 REVIEW。
engine 232 KEEP / 11655 REVIEW / 0 可確認自動排除；高 REVIEW 是保守規則與未模擬 semantics，非低品質流量比例。

**產品建議 NEGATIVE_LIST_FIRST（人工審四個 paid 完整 query）**。
GO：bounded diagnosis 與小清單人工審核。NO_GO：live mutation、整組結構改動、自動化／排程。
無實測 maintenance hours／新候選頻率證據，不選 AUTOMATION_WARRANTED。
如果四個提案已被其他 existing negatives 排除或缺實質價值，採 NO_OP。
現有 phase/broad negative 中文 matching 仍需人工/平台核對，4列全部 REVIEW，非已批准排除。
缺 qualified lead / lag / disabled-removed historical scope / hidden-tail，限制 full-account 結論，不再稱「完全沒有真實帳戶資料」。
下一 owner Andy / DOT：review 4個 exact提案、核實 lead quality/lag；任何正式修改另案授權。

匿名 evidence SHA-256（原始資料未提交）：

| 類別 | hash |
|---|---|
| search daily | e1192491909a25b1a638188fc5aa688abd061efc298fbbb823c222554a7b53a6 |
| positives | 60f347d0acd28eb57c3f2f7aa03ee2c100224c3241c0bb7b1891c6a56451d56c |
| direct negatives / bindings | 2c3c67fcd2087a52d9e0bd25a76babbfbaa7bb21e0d8d825ca80f206287cf1da |
| campaign daily | 6754933920e4b0cd612bc8e53b81d9f356593f98cee71d292599ded17b8c8a33 |
| group ID mapping | a64a1da09a30ebe01deaed60b48e8d5c9322a872da33c8b646fc45c7cf720659 |
| shared list A | c54a143409344df0bf0ca84a7ae349439587cc872668beb71e0cd46061ce6206 |
| shared list B | 8add3d055ffb4c4da5a6910c442767ede402a68745fa6b73cf841546efbee8b2 |
| historical conversions | cd342ec814b3ba4417f12a198bc84dcbf065bcbae38c50cfe77e9017b8e9a672 |
| private diagnosis report | 9728d86d357937d7a4758bc205a0fa1070e2dd7b9612585271a1535c36e49786 |
