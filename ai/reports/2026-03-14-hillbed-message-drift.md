# Message Drift Report: 山丘樂眠床

## Report Date

2026-03-14

## Purpose

比對三個資訊來源之間的訊息一致性：
1. 官方商品頁 (`https://www.lovefu.tw/products/hillbed`)
2. Golden brief (`ai/inputs/briefs/lovefu-pmax-hillbed.json`)
3. Generated copy (`ai/outputs/lovefu-pmax-hillbed.output.json`)

## Source of Truth

| 來源 | 檔案 / 位置 | 確認日期 |
|------|------------|---------|
| 官網商品頁 | https://www.lovefu.tw/products/hillbed | 2026-03-14 |
| Golden brief | ai/inputs/briefs/lovefu-pmax-hillbed.json | 2026-03-14 |
| Generated copy | ai/outputs/lovefu-pmax-hillbed.output.json | 2026-03-14 |
| Validation record | ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md | 2026-03-14 |

## Fact Drift Check

| 事實宣稱 | 官網商品頁 | Brief | Generated Copy | 一致性 |
|----------|-----------|-------|---------------|--------|
| 產品名稱 | 山丘樂眠床 | 山丘樂眠床 | 山丘樂眠床 | match |
| 入門價格 | 14,900 起 | 14,900 起 | 14,900 起 | match |
| 退款政策 | 100天安心睡全額退款 | 100天安心睡全額退款 | 100天安心睡 | match |
| 保固期間 | 10年保固 | 10年保固 | 10年保固 | match |
| 泡棉材質 | MDI高密度慢回彈泡棉 | MDI高密度慢回彈泡棉 | 慢回彈泡棉 / 高密度慢回彈泡棉 | match |
| 彈簧規格 | 2.4mm高碳鋼獨立筒 | 2.4mm高碳鋼獨立筒 | 高碳鋼獨立筒 | match |
| 安全認證 | CertiPUR + OEKO-TEX | CertiPUR + OEKO-TEX | 歐盟CertiPUR與OEKO-TEX | match |
| 主要 CTA | 立即選購 | 立即選購 | 立即選購 | match |
| Hero message | 第2張床 擁有支撐腰背與放鬆的魔法 | 同上 | 語意覆蓋（多則 headline 傳達同義） | match |

## Activity / Promotion Check

| 項目 | 官網狀態 | Brief 處理 | Copy 處理 | 一致性 |
|------|---------|-----------|----------|--------|
| 活動促案（新家樂眠方案等） | 商品頁可見 | 僅記錄在 notes，未納入 offers | 未出現 | match（正確排除） |
| 贈品 | 視活動頁而異 | 未納入 | 未出現 | match（正確排除） |
| 任選 5 件 85 折 | 商品頁可見 | 未納入 | 未出現 | match（正確排除） |

> 設計決策：活動促案為時效性資訊，不應進入 canonical brief。
> 若需投放活動期間廣告，建議另開 campaign-specific brief。

## Forbidden Claims Check

| 禁用宣稱 | Brief 中列出 | Copy 中出現 | 結果 |
|----------|-------------|-------------|------|
| 保證治好腰痛 | ✓ 已列為 forbidden | 未出現 | pass |
| 睡一晚立刻不痠痛 | ✓ 已列為 forbidden | 未出現 | pass |
| 全台最低價 | ✓ 已列為 forbidden | 未出現 | pass |
| 醫療級治療效果 | ✓ 已列為 forbidden | 未出現 | pass |

## Policy Risk Areas

| 風險表述 | 出現位置 | 風險等級 | 說明 |
|---------|---------|---------|------|
| 「托住腰背」 | short headline | 低 | 感受描述而非醫療承諾，但需持續監控平台政策 |
| 「接住身體」 | short headline, long headline | 低 | 同上，為品牌慣用擬人語法 |
| 「支撐力提升20%」 | brief USP（未進入 copy） | — | 正確未進入文案，避免數據宣稱風險 |

## Must-Include Terms Check

| 必含詞 | Brief 指定 | Copy 中出現 | 結果 |
|--------|-----------|-------------|------|
| 山丘樂眠床 | ✓ | ✓（出現於 4 則 headline） | pass |
| 100天安心睡 | ✓ | ✓（出現於 3 則 headline + 2 則 description） | pass |
| 立即選購 | ✓ | ✓（出現於 1 則 headline） | pass |

## Drift Summary

- **三方資訊完全一致，無 drift 發現**
- 活動促案與贈品正確地被排除在 canonical brief 之外
- Copy 中的事實宣稱均可在官網商品頁驗證
- Forbidden claims 全數清除
- Must-include terms 全數出現

## Next Drift Check

- 建議日期：2026-04-14
- 重點確認：價格是否調整、退款/保固政策是否變更、是否有新增 forbidden claim 情境
- 記錄於：`ai/registry/canonical-briefs.yaml` → `drift_check.next_check_due`

## Conclusion

本份 golden brief 與 generated copy 均與官網商品頁事實一致，
且正確地將時效性活動資訊排除在 canonical brief 之外。
可安心做為 production baseline。
