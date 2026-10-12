# Woolito 搜尋意圖診斷 v0.1 — CSV 契約與安全邊界

Canonical work-state：[OS #47](https://github.com/pin10andy/personal-operating-dashboard/issues/47)。
本工具只讀本機 CSV、輸出本機 JSON/CSV，無網路、Ads 寫入、排程或資料庫。
帳戶原始 CSV、輸出（含查詢）及憑證只能存於既有核准私有位置，不得提交公開 repo、Issue 或第三方。
repo 的 `assets/woolito-synthetic/` 完全合成；不能據此聲稱 Woolito 花費、轉換、節省金額或產品決策。

## 最小匯出包

UTF-8（可含 BOM），一列 header，無報表前置列、總計列、重疊匯出。
日期以帳戶時區計算，90 個完整日 **2026-07-14 至 2026-10-11**（含首尾）。
只收 Search，固定相同 campaign 範圍、幣別、轉換定義、歸因口徑及匯出時間；不混 PMax/互動報表。
若 UI 不能一次提供欄位，於私有環境按穩定 IDs 合併；不能猜 trigger keyword 或 IDs。
指標不可空白／`--`／NaN／負值；真實零才填 `0`。轉換可為小數。

| 檔名 | 必填欄位與粒度 |
|---|---|
| `search_terms.csv` | date, query, campaign_id, ad_group_id, trigger_keyword, positive_match_type, impressions, clicks, cost, conversions；一列＝日×campaign×group×原始查詢×觸發 keyword×正向比對類型。conversion_value 選填。query 不移除原始空格。 |
| `positives.csv` | campaign_id, ad_group_id, keyword, match_type, status；只含目前 ENABLED；同範圍完整快照。 |
| `negatives.csv` | scope, campaign_id, ad_group_id, list_id, keyword, match_type；scope＝ACCOUNT/SHARED/CAMPAIGN/AD_GROUP。ACCOUNT IDs 可空；SHARED 每個實際套用 campaign 一列，list_id 必填；AD_GROUP group 必填。無否定字也需 header-only 檔＋完整宣告。 |
| `campaign_totals.csv` | date, campaign_id, clicks, cost, conversions；每個範圍內 campaign 每日一列，含真實零花費日，共 90 天；無 keyword/query filter。 |
| `historical_conversions.csv` | query, conversions；同 scope 已知有效轉換查詢（可含較長歷史），避免誤排曾轉換字。缺歷史不是「沒有轉換」。 |

正向與否定 match_type 都用 EXACT/PHRASE/BROAD，含義不同。
搜尋 CSV 重用 legacy 英文／繁中 aliases，如搜尋字詞、日期、Campaign ID、Ad group ID、Keyword、Keyword match type。
其餘檔案使用上表 canonical header。其他 UI 欄名需明確人工轉換，不能靜默猜測。

`manifest.json` 必含 source_kind (`synthetic`/`account`)、start、end、currency、account_timezone（IANA）、
exported_at（含時區）、conversion_lag_days（非負整數）、campaign_ids；
complete 內五份檔案名稱各為布林，只有核對完整且無不明 filter 才填 true。
protected_phrases 為選填品牌確認完整服務詞組。複製合成 manifest 前需逐欄核對，不能沿用 true。
無法取得的檔案可省略，或 complete=false；候選因此降 REVIEW，coverage 不完整則不能做 90 天結論。
近期最後 conversion_lag_days 天的零轉換需等待成熟重跑；此值由帳戶歸因與轉換延遲證據確認，fixture 的 14 天不是 Woolito 事實。

## 可重跑指令

從 repo root 執行（示例僅合成）：

```sh
python3 ai/skill-src/google-ads/search-terms-cleaner/scripts/woolito_intent_diagnostic.py \
  ai/skill-src/google-ads/search-terms-cleaner/assets/woolito-synthetic \
  --output-dir scratch/google-ads/woolito-synthetic
python3 -m unittest discover -s ai/skill-src/google-ads/search-terms-cleaner/tests -v
```

真實資料用既有核准私有 input/output 路徑。stdout 只印 source/status，JSON 與 candidates.csv 含查詢不得公開。
每列輸出 query/date/campaign/group/trigger/match/cost/conversions/decision/reason_code/confidence/evidence/
proposed_negative_match/conflict_check/review_status；候選層級只建議原 ad group，無上稿格式或執行器。

## 規則與衝突檢查

- 用 Unicode NFKC、大小寫及中文相鄰空格正規化供比較，原始 query 保留。沒有英文 N-gram 或單字否定。
- 優先保護完整服務語境：企業形象動畫、產品介紹、品牌製作、商業報價、企業教育訓練、互動賀卡、企業節慶、商業角色設計、動畫製作免費估價。完整保護詞命中即 KEEP_B2B；這不是商業成效證明。
- 僅完整查詢符合已知娛樂觀看／下載／招聘／學生作業規則才為 NEGATIVE_EXACT_CANDIDATE。新片名及未涵蓋措辭一律 REVIEW；不自動泛化片名詞庫。
- 動畫角色設計、動畫教學、3D 動畫、免費動畫製作報價等語意邊界不明均 REVIEW。成本不改 decision，只排序。
- 每個候選對同包所有可見轉換列＋歷史有效轉換查詢（保守全範圍保護）、原 ad group enabled positive 文字做核對；命中轉 REVIEW。
- 對適用 account/shared binding/campaign/ad group 現有 negative 核對 exact 文字；已有 exact 轉 REVIEW，避免重複提案。適用的 phrase/broad negative 無法可靠模擬中文切詞，轉 REVIEW。
- 任一必要衝突檢查表缺失／complete!=true，轉 REVIEW；禁止把 UNKNOWN 當 clear。
- 正向 keyword 意圖擴張／close variants 與中文否定切詞無法完整模擬。TEXT_CHECK_CLEAR_SEMANTICS_UNCONFIRMED 只代表有限文字核對，**不是平台衝突已確認或批准排除**。所有列 MANUAL_REVIEW_REQUIRED。

Google 官方說明：否定字與正向字比對規則不同；否定完全比對不攔含額外字詞的查詢，且不自動涵蓋近似變體。
[否定關鍵字](https://support.google.com/google-ads/answer/2453972)（2026-10-12 核對）。
[搜尋字詞報表](https://support.google.com/google-ads/answer/2472708) 是 Issue 的參考；本次頁面 fetch 失敗，隱藏長尾限制依 Issue 明確要求記錄。

## Coverage 與策略審核

工具核對 daily/campaign totals 無重複、日期完整、可見指標不超過總計。輸出各 campaign 的 visible cost/total cost、visible clicks/total clicks；分母零為 null。
CONFIRMED 只指已宣告範圍的 CSV 完整性，不代表可見查詢等於全部查詢，也不證明 manifest 宣告正確。
`top_visible_sources` 按 campaign/trigger keyword/positive match/decision/reason 排序，可查高意圖、候選與 REVIEW 的可見成本。
不能把零轉換算浪費、候選成本當可回收 savings，或把可見比例套全帳戶。真實來源沒有完整性時 BLOCKED_ON_ACCOUNT_DATA。

人工拿到真實資料後比較三種槓桿：

| 方案 | 檢視證據與 trade-off |
|---|---|
| STRUCTURE_FIRST | 若 broad/phrase「動畫」在少數來源集中大量明確非商業可見成本，先試服務長尾／分群／匹配結構；保留未知優質流量的風險需另案審核。 |
| NEGATIVE_LIST_FIRST | 若污染是有限、穩定且通過衝突核對的完整查詢，精確提案較低成本；不能阻擋新變體，仍有維護工時。 |
| AUTOMATION_WARRANTED | 需真實新候選頻率、每次審核分鐘、每月人工時與可觀測成本證據，才評估自動化；本輪不部署。 |
| NO_OP | 可見候選成本／維護價值小或風險高，停止；仍記 coverage 與不確定性。 |

v0.1 不自動選產品策略，product_decision=null。缺資料不能虛選上述方案；live_write_go 固定 NO_GO。
