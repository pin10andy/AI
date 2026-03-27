---
name: "ad-copy-builder"
description: "Google Ads 文案策略技能。根據現有廣告成效判斷哪些素材保留、哪些替換、哪些新測試角度，並依 RSA/PMax 規格產出。當使用者提到廣告文案、標題、RSA、PMax 素材、文案優化、Ad Strength、素材替換時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
  python-tools: ad_copy_validator.py
---

# Ad Copy Builder

> **Canonical source**: `ai/skill-src/google-ads/ad-copy-builder/SKILL.md`
> Do NOT edit copies in `.claude/skills/`. Always edit here and run `scripts/sync-skills.sh` to deploy.

這是「文案策略技能」，不是純文案生成工具。核心是：根據現有廣告表現，決定什麼留、什麼換、什麼新試，然後按格式產出。

Google 本身已在做 AI 文案生成（AI Max text customization），所以這個 skill 的重點是**策略判斷與品牌一致性**，而不是單純輸出文字。

## Required References

執行前必須讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`（voice.do、voice.do_not、品牌語氣）
2. **Google Ads Playbook**：`ai/playbooks/google-ads.md`（格式規格、Ad Strength 標準）
3. **RSA 規則**：`references/rsa-guidelines.md`（字元限制、多樣性要求）

## When to Use

- 使用者已經有既有廣告素材，需要做 RSA 或 PMax 的保留 / 替換 / 新測試判斷
- 使用者說「幫我優化文案」「哪些標題要換」「Ad Strength 太低怎麼辦」
- 季度素材審查：整包替換老舊文案

如果需求是「從固定 brief 直接產出全新 Search RSA 或 PMax」，優先改走 `ai/skill-src/google-ads-writer/SKILL.md`。

## Required Inputs

執行前詢問：

1. **廣告群組名稱與主題**：這組廣告在打什麼產品 / 痛點
2. **目標關鍵字**（3–5 個）：文案需包含的核心字
3. **現有廣告素材**（選填）：現有標題 + 說明 + Ad Strength 評分
4. **廣告類型**：RSA / PMax / 兩者都要
5. **主打訴求**（選填）：價格、體驗、信任、解決問題……

## Execution Steps

### Step 1：讀取品牌 Context + Playbook

```
Read ai/brand/master-brand.yaml
Read ai/playbooks/google-ads.md
重點：voice.tone、voice.do、voice.do_not、language.rules
```

### Step 2：現有素材審查（如有）

如果使用者提供現有廣告，先做素材評估：

**保留標準**（全部符合才保留）：
- CTR 高於廣告群組均值
- 包含關鍵字（提升 Ad Strength）
- 符合品牌語氣（無違反 voice.do_not）
- 非重複語意（與其他標題差異度足夠）

**替換標準**（任一觸發即替換）：
- CTR 持續低於均值超過 14 天
- Ad Strength 評為 Poor 且已超過 30 天
- 語意與其他標題過於相似（多樣性不足）
- 違反 voice.do_not 規則

**新測試標準**：
- 目前缺少某個訴求角度（如有問題型但缺解決方案型）
- 有新的 USP 或活動資訊需要帶入
- Ad Strength 在 Good 以下，需補充更多標題選項

### Step 3：執行格式驗證腳本

```bash
python3 scripts/ad_copy_validator.py --headlines "標題1|標題2|..." --descriptions "說明1|說明2"
```

腳本驗證：字元限制、關鍵字包含率、語意多樣性、禁用詞。

### Step 4：依策略產出新素材

**RSA 格式規格**（硬性限制）：
- 標題：最多 15 個，每個 ≤ 30 字元（中文），每個 ≤ 30 字元（英文）
- 說明：最多 4 個，每個 ≤ 90 字元
- 至少 3–4 個標題包含目標關鍵字
- 標題之間語意必須不同（不得重複概念）

**PMax 格式規格**：
- 短標題：≤ 30 字元，5 個
- 長標題：≤ 90 字元，5 個
- 說明：≤ 90 字元，5 個（至少 1 個 ≤ 60 字元）

**品牌語氣規則**（嚴格執行）：
- 使用 master-brand.yaml 的 voice.do 語言風格
- 禁止 voice.do_not 中的所有禁用語氣
- 主要語言：繁體中文（zh-TW）
- 禁止中英混用（除專有名詞外）

**訴求角度必須覆蓋**（至少各 1 個標題）：
- 產品特性角度（獨立筒、乳膠、記憶棉）
- 痛點解決角度（腰痛、睡不好、頸椎）
- 信任/社證角度（量脖子服務、試躺、認證）
- CTA 角度（立即了解、預約試躺、馬上看）

### Step 5：輸出素材組合表

按 `templates/asset-portfolio.md` 格式輸出三欄：
- **保留**：現有標題 + 保留原因
- **替換**：現有標題 → 新標題 + 替換原因
- **新增**：新測試標題 + 測試目的

## Output Format

1. **素材審查摘要**：現有幾個標題、幾個保留、幾個替換、補充幾個新的
2. **三欄素材表**：保留 / 替換 / 新增
3. **完整 RSA 素材包**：可直接貼入 Google Ads 的格式
4. **Ad Strength 預估**：根據標題數量、關鍵字覆蓋、多樣性評估

## Quality Gates

- [ ] 所有標題字元數已驗證符合限制
- [ ] 每個替換都有具體原因（不是「表現不好」這種廢話）
- [ ] 訴求角度已覆蓋：特性 / 痛點 / 信任 / CTA
- [ ] 無違反 master-brand.yaml voice.do_not 規則
- [ ] 標題間語意多樣性足夠（無重複概念）
- [ ] RSA 標題至少 12 個以達到 Good Ad Strength

---

## Artifact Governance

本技能產出為文案策略報告與素材包。

### 輸出路徑規則

- 正式輸出寫入 `ai/outputs/google-ads/{brand}/{product}/{lane}/` 對應子目錄
- 暫存/測試輸出寫入 `scratch/google-ads/`
- 驗證報告寫入 `ai/validation/`（命名 `YYYY-MM-DD-{slug}.md`）
- **禁止**將輸出寫入 repo 根目錄

### 寫入後必須

1. 正式 artifact 在 `ai/registry/artifacts.yaml` 登記
2. 執行 `python3 scripts/check_artifact_governance.py` 確認合規

### 政策參考

- `ai/registry/storage-map.yaml` / `ai/policies/artifact-naming-policy.md` / `ai/policies/artifact-write-policy.md`
