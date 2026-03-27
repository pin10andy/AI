# LP 一致性稽核報告

**品牌**：LOVEFU大島樂眠  
**廣告群組**：Experience Store Booking PMax（三店合併）  
**廣告類型**：PMax  
**稽核 URL**：推薦 `https://www.lovefu.tw/pages/lovefuhome`；避免 `https://www.lovefu.tw/products/hillbed`  
**產出日期**：2026-03-16

---

## 稽核範圍

- 關鍵字：`預約體驗 / 門市試躺 / 睡眠體驗店 / 量脖子 / 睡眠顧問`
- 廣告文案來源：`ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-booking-refresh/builder.json`
- 官方頁面來源：
  - `https://www.lovefu.tw/pages/lovefuhome`
  - `https://www.lovefu.tw/products/hillbed`

## 一致性評分

| 層面 | 分數（1–5） | 狀態 | 說明 |
|------|-----------|------|------|
| 關鍵字 → 廣告文案 | 4/5 | 穩定 | 文案已明確接住 `預約體驗 / 門市試躺 / 睡眠體驗店`，也把 `量脖子 / 睡眠顧問` 放進服務型角度。 |
| 廣告文案 → LP 首屏 | 4/5 | 可上 | 若落到 `lovefuhome`，頁面本身就有量脖子、30 分鐘沈浸式體驗、專屬空間與三店預約入口，與廣告承諾高度一致。 |
| LP 首屏 → 轉換路徑 | 4/5 | 可上 | 體驗店頁可直接選店預約，門市地址與時間也完整；但對三店合併流量而言，使用者仍要先做一次選店決策。 |
| **整體評分** | **12/15** | **優** | 前提是 campaign URL 真的落在 `lovefuhome`。若落到 `hillbed` 商品頁，整體會掉到「需要修正」。 |

> 評分說明：12–15 = 優（建議維持）/ 8–11 = 可優化 / < 8 = 需要修正

---

## 官方頁面觀察摘要

### 推薦 LP：`lovefuhome`

官方體驗店頁清楚寫出：

- 依身型與需求量脖子，適配合適寢具
- 提供專屬睡眠空間與 30 分鐘完全放鬆體驗
- 明確列出板橋、桃園、台中三店資訊與各自預約入口

這些內容能直接承接本次廣告的三個主軸：沉浸式試躺、顧問陪伴、低壓預約。

### 高風險 LP：`products/hillbed`

官方 hillbed 商品頁首屏主軸是：

- 山丘樂眠床的支撐、腰背放鬆與產品特性
- 100 天安心睡、配送與商品描述

這頁適合 purchase / product-discovery，不適合當三店合併 booking PMax 的主 LP。即使頁面整站 footer 有體驗店資訊，首屏仍然沒有先接住「預約體驗」。

---

## 漏斗斷點清單

### 斷點 1：CTA 不一致風險（影響：高）

**位置**：Google Ads campaign URL 設定

**現狀描述**：
> booking PMax 文案已經收斂成「預約體驗 / 門市試躺」，但如果後台 URL 被設到 `products/hillbed`，使用者進站先看到的是產品與購買資訊，不是體驗預約。

**影響說明**：
> 廣告承諾的是低壓預約，LP 首屏卻變成商品購買流程，會直接造成訊息斷裂，也會讓 PMax 自動學到較偏 purchase 的頁面語意。

---

### 斷點 2：Generic booking CTA 仍多一步選店（影響：中）

**位置**：`lovefuhome` 體驗店頁中段到店家列表區

**現狀描述**：
> 廣告寫的是 generic 的「預約體驗 / 就近預約」，頁面則要使用者再往下選板橋、桃園或台中。

**影響說明**：
> 這不是錯，但會增加一步決策成本。對已經知道自己在哪一區的人問題不大；對廣泛 PMax 流量，可能讓一部分人停在選店前。

---

### 斷點 3：若後續把產品名放回文案，首屏可能接不住（影響：中）

**位置**：廣告 headline / `lovefuhome` 首屏

**現狀描述**：
> 目前廣告刻意走 generic 體驗店語言，所以和 `lovefuhome` 一致性高。但如果下一版重新加重 `山丘樂眠床` 與支撐訴求，體驗店頁首屏未必會第一時間接住。

**影響說明**：
> 一旦廣告更像產品頁導流，但 LP 仍是 general experience page，就會回到「廣告講產品、頁面講體驗流程」的半斷裂狀態。

---

## 修改建議

### 高優先（本週處理）

| 斷點 | 目前狀態 | 建議修改 | 預期影響 |
|------|---------|---------|---------|
| Campaign URL 可能設錯 | `hillbed` 與 `lovefuhome` 都可能被拿來當 LP | 在 Google Ads 後台把這組三店合併 booking PMax 的最終網址固定為 `https://www.lovefu.tw/pages/lovefuhome` | 先把最大的一致性風險拿掉，避免 booking intent 被 purchase flow 稀釋 |
| 選店多一步 | generic CTA 對到多店選擇頁 | 廣告補強「就近預約」語意，並優先保留 `就近預約體驗 更方便` 與 `預約門市試躺 更安心` | 降低使用者看到多店列表時的認知落差 |

### 中優先（本月處理）

| 斷點 | 目前狀態 | 建議修改 | 預期影響 |
|------|---------|---------|---------|
| 首屏 CTA 還不夠一步到位 | 頁面要先選店再點預約 | 若站內可調內容，於首屏或首屏下方加一句「選擇最近門市，立即完成預約」 | 讓 generic ad copy 與頁內動線更連續 |
| 後續可能回加產品語言 | product token 目前不在第一版 copy | 若下一輪要測 `山丘樂眠床` 產品詞，建議拆一條 product-intent ad set，避免和 generic 體驗店 ad set 混用 LP | 保持 message clarity，不讓同一組文案同時打 booking 與 purchase |

---

## Quick Wins（今天就能做）

1. **確認 campaign URL 固定導向體驗店頁**（10 分鐘）
   - 做什麼：到 Google Ads 後台檢查這組 PMax 最終網址，確認是 `https://www.lovefu.tw/pages/lovefuhome`
   - 預期效果：立刻避免最大訊息斷裂

2. **保留「就近預約」型 headline**（10 分鐘）
   - 做什麼：上稿時不要把 `就近預約體驗 更方便`、`預約門市試躺 更安心` 這類 headline 移掉
   - 預期效果：讓廣告先替頁內的選店行為做好心理預期

3. **不要把 hillbed 商品詞硬塞回這組 ad set**（15 分鐘）
   - 做什麼：本組維持體驗店 / 預約語言；若要測 `山丘樂眠床`，另開更 product-led 的資產組
   - 預期效果：避免一組資產同時扛 booking 與 purchase 兩種 intent

---

## 廣告 vs. LP 對照表

| 廣告元素 | 廣告內容 | LP 是否對應 | 對應位置 |
|---------|---------|-----------|---------|
| 標題 1 | 預約門市試躺 更安心 | ✅ | `lovefuhome` 店家列表與預約入口 |
| 標題 2 | 量脖子試枕一起安排 | ✅ | `lovefuhome` 量脖子流程與體驗說明 |
| 說明 1 | 先預約體驗，再決定下一步。 | ✅ | `lovefuhome` 的預約店鋪 CTA 與體驗導向內容 |
| 說明 2 | 就近預約體驗店，先感受沉浸式試躺與放鬆流程，再慢慢決定下一步帶什麼回家。 | ✅ | `lovefuhome` 三店入口 + 30 分鐘沈浸式體驗描述 |
| 主要 CTA | 預約體驗 | ✅ / ❌ | 導 `lovefuhome` 時為 ✅；導 `hillbed` 時為 ❌ |

---

## 結論

這組三店合併 booking PMax 的推薦 LP 已經很明確：

- **應導向**：`https://www.lovefu.tw/pages/lovefuhome`
- **不應導向**：`https://www.lovefu.tw/products/hillbed`

文案本身現在沒有大問題，真正的高風險點是後台 URL 是否設對。

