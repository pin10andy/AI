---
name: "lp-alignment-auditor"
description: "稽核關鍵字→廣告文案→Landing Page 的訊息一致性，找出漏斗斷點並給出具體修改建議。當使用者提到 LP 轉換率低、廣告和頁面不一致、漏斗斷點、CTA 問題、landing page 優化時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
---

# LP Alignment Auditor

> **Canonical source**: `ai/skill-src/google-ads/lp-alignment-auditor/SKILL.md`
> Do NOT edit copies in `.claude/skills/`. Always edit here and run `scripts/sync-skills.sh` to deploy.

找出「廣告點了進來，但沒有轉換」的根本原因。Google 的 AI Max text customization 會根據 landing page 自動生成素材，這代表 LP 內容直接影響廣告品質——LP 爛，廣告再強也一起爛。

## Required References

執行前必須讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`（target_audience、voice、desired_outcomes）
2. **稽核標準**：`references/alignment-criteria.md`（一致性評分規則）

## When to Use

- 使用者說「點擊率不錯但轉換率很差」「LP 可能有問題」
- 準備新廣告群組，想先確認 LP 是否就緒
- Google Ads 警告「廣告與 landing page 相關性低」
- 季度性漏斗健康檢查

## Required Inputs

執行前詢問：

1. **關鍵字**（3–5 個）：這組廣告主打的關鍵字
2. **廣告文案**：目前使用的標題 + 說明（或讓我讀現有 RSA）
3. **Landing Page**：提供網址或直接貼入頁面主要內容（標題、副標、CTA、首屏）
4. **廣告類型**（選填）：Search / PMax / 再行銷（影響一致性標準）

## Execution Steps

### Step 1：讀取品牌 Context

```
Read ai/brand/master-brand.yaml
重點：target_audience.desired_outcomes → 頁面是否回應了這些期望？
      voice.do_not → 頁面有無違反品牌規範？
```

### Step 2：三層一致性評分

參考 `references/alignment-criteria.md`，對以下三個層面各給 1–5 分：

**層面 1：關鍵字 → 廣告文案**
- 搜尋意圖是否被廣告標題接住？
- 廣告承諾是否具體且可信？（避免過度承諾）
- CTA 是否與搜尋意圖相符？（搜尋「推薦」卻叫人「免費諮詢」→ 不符）

**層面 2：廣告文案 → LP 首屏**
- 廣告標題在 LP 第一屏是否有對應的主標題？
- 廣告承諾的 USP 在首屏是否可見？
- CTA 按鈕文字是否與廣告 CTA 一致或相關？

**層面 3：LP 首屏 → 轉換完整路徑**
- 信任要素是否在適當位置出現？（認證、評價、保證）
- 是否有清楚的次要行動（如試躺預約、LINE 諮詢）？
- 頁面是否回應了使用者可能的疑慮？（FAQ、差異化說明）

### Step 3：找出漏斗斷點

對每個評分 < 3 的層面，找出具體斷點：

**常見斷點類型**：
- **承諾落差**：廣告說「腰痛解決方案」，但 LP 只賣床墊規格
- **CTA 不一致**：廣告說「立即選購」，LP 首屏是品牌故事
- **首屏沒接住**：使用者搜尋「枕頭推薦」，進 LP 看到的是促銷活動
- **信任缺失**：廣告主打「睡眠顧問建議」，LP 無社證或顧問介紹
- **行動路徑不清**：頁面有多個 CTA，沒有明確的主要行動

### Step 4：依廣告類型給出修改優先級

**Search 廣告 LP**：
- 最高優先：首屏標題對齊關鍵字意圖
- 次優先：CTA 清晰且在首屏可見
- 加分項：包含關鍵字（提升 Quality Score → 降低 CPC）

**PMax 廣告 LP**：
- 最高優先：頁面主要訴求清楚（AI 會掃描頁面生成素材）
- 次優先：避免誤導性內容（Google 政策）
- 加分項：結構化資料標記（FAQ、Product schema）

**再行銷 LP**：
- 最高優先：針對已看過品牌的用戶給予推進理由（限時、獨家）
- 次優先：減少重複資訊，加強差異化訴求

### Step 5：輸出稽核報告

按 `templates/audit-report.md` 格式輸出。

## Output Format

1. **一致性評分表**：三個層面各 1–5 分 + 評分說明
2. **漏斗斷點清單**：按優先級排序，每個斷點有具體位置描述
3. **修改建議**：每個斷點的具體改法（不得只說「需要優化」）
4. **Quick Wins**：不需改程式碼、立即可執行的 2–3 個改動

## Quality Gates

- [ ] 三個層面都有評分且有說明
- [ ] 每個斷點都有「在頁面哪裡」的具體定位
- [ ] 每個修改建議都有「改成什麼」的具體內容
- [ ] Quick Wins 只包含真的容易實作的改動
- [ ] 無 「建議優化首屏體驗」 這類廢話建議

---

## Artifact Governance

本技能產出為 LP 一致性稽核報告。

### 輸出路徑規則

- 分析報告寫入 `ai/reports/`（命名 `YYYY-MM-DD-{slug}.md`）
- 暫存/測試輸出寫入 `scratch/google-ads/`
- **禁止**將輸出寫入 repo 根目錄

### 政策參考

- `ai/registry/storage-map.yaml` / `ai/policies/artifact-naming-policy.md` / `ai/policies/artifact-write-policy.md`
