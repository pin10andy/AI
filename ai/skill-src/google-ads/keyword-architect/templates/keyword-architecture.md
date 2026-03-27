# 關鍵字架構規劃表

**品牌**：{brand_name}
**廣告活動**：{campaign_name}
**目的**：{campaign_goal}（品牌曝光 / 產品轉換 / 競品搶量）
**產出日期**：{today}

---

## 分群總覽

| 廣告群組名稱 | 關鍵字數 | 主要意圖 | 比對類型 | 建議 Landing Page |
|------------|---------|---------|---------|-----------------|
| {group_name} | {count} | 商業型 | Exact/Phrase | {lp_url_or_type} |

**共 {total_groups} 個廣告群組 / {total_keywords} 個關鍵字**

---

## 各群組詳細分配

### 廣告群組：{group_name_1}

**主題**：{theme}
**目標 Landing Page**：{lp}
**建議文案方向**：{copy_direction}

| 關鍵字 | 意圖 | 比對類型 | 備註 |
|--------|------|---------|------|
| {keyword} | 商業型 | Exact | |
| {keyword} | 商業型 | Phrase | |
| {keyword} | 問題型 | Phrase | 搭配否定字「DIY」|

---

### 廣告群組：{group_name_2}

（同上格式）

---

## 不建議投放的關鍵字

| 關鍵字 | 原因 | 建議處理 |
|--------|------|---------|
| {keyword} | 資訊型，無商業意圖 | 加入廣告活動層級否定字 |
| {keyword} | 明確不相關 | 加入帳戶層級否定字 |
| {keyword} | 搜尋量過低 | 暫不投放，未來觀察 |

---

## 否定字初始建議

### 帳戶層級否定字（所有活動共用）
```
免費, 贈品, 二手, 中古, 招募, 工作, 維修, 修理, DIY
```

### {campaign_name} 廣告活動層級否定字
```
{negative_keyword_1}, {negative_keyword_2}
```

### 各廣告群組交叉否定字建議
> 避免不同群組的字互相觸發

| 廣告群組 A | 需要在 A 排除的字（屬於群組 B）|
|-----------|------------------------------|
| {group_a} | {keyword_from_b} |

---

## 下一步行動

- [ ] 建立廣告活動與廣告群組結構
- [ ] 匯入各群組關鍵字（依建議比對類型）
- [ ] 加入帳戶層級否定字
- [ ] 加入廣告活動層級否定字
- [ ] 為每個群組建立至少 1 組 RSA 文案（觸發 ad-copy-builder）
- [ ] 確認各群組的 Landing Page 已就緒（觸發 lp-alignment-auditor）

---

*此報告由 Claude keyword-architect skill 產出，執行前請人工審核。*
