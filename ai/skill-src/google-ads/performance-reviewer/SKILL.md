---
name: "performance-reviewer"
description: "分析 Google Ads 成效報表，對每個廣告活動／廣告群組／素材做「保留 / 停用 / 擴量 / 測試」四欄判斷，強制附上原因。當使用者提到成效分析、週報、報表、哪些廣告要停、ROAS 下滑、KPI 檢查時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
  python-tools: performance_analyzer.py
---

# Performance Reviewer

> **Canonical source**: `ai/skill-src/google-ads/performance-reviewer/SKILL.md`
> Do NOT edit copies in `.claude/skills/`. Always edit here and run `scripts/sync-skills.sh` to deploy.

分析 Google Ads 帳戶成效數據，產出可直接執行的判斷清單。每一筆必須給出「保留 / 停用 / 擴量 / 測試」其中一個結論，並強制附上具體原因，不得輸出「建議持續觀察」這類無效結論。

## Required References

執行前必須讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`（目標受眾、產品線、轉換目標）
2. **決策規則**：`references/decision-rules.md`（四欄判斷標準）

## When to Use

- 使用者上傳 Google Ads 成效 CSV（廣告活動 / 廣告群組 / 廣告層級）
- 使用者說「幫我看這週成效」「哪些廣告要停」「報表分析」
- 建議週期：每 7 天執行一次

## Required Inputs

執行前詢問：

1. **CSV 路徑**：廣告活動或廣告群組成效報表（7 / 14 / 30 天皆可）
2. **目標 ROAS 或目標 CPA**（選填）：沒有則從 master-brand.yaml 推估
3. **分析層級**（選填）：廣告活動 / 廣告群組 / 廣告素材，預設廣告群組

## Execution Steps

### Step 1：讀取品牌 Context

```
Read ai/brand/master-brand.yaml
注意 target_audience.desired_outcomes → 這些是轉換品質的判斷依據
```

### Step 2：執行量化腳本

```bash
python3 scripts/performance_analyzer.py {csv_path} \
  --level {campaign|adgroup|ad} \
  --format json
```

腳本輸出 JSON，包含每個項目的核心指標與初步分類。

### Step 3：套用決策規則做四欄分類

參考 `references/decision-rules.md`，對每個廣告活動 / 群組做判斷：

**保留**：成效穩定、接近或達到目標 ROAS/CPA，不需調整
**停用**：連續 14 天以上 ROAS/CTR 不達標，且無改善跡象
**擴量**：ROAS 高於目標 1.5 倍以上，且預算受限制（曝光率低）
**測試**：數據量不足（< 30 次點擊），或新推出尚在學習期

每個判斷**必須附上具體原因**，例如：
- ✅ 停用原因：「過去 21 天 ROAS 0.8x，低於目標 2x，且已連續 3 週下滑」
- ❌ 禁止：「成效不佳，建議優化」

### Step 4：找出變動原因假設

對「停用」和「ROAS 明顯下滑」的項目，提出可能的原因假設：
- 素材疲乏？（點擊率下滑但曝光穩定）
- 競爭加劇？（CPC 上升但 CTR 下滑）
- 季節性？（對比同期數據）
- LP 問題？（CTR 正常但轉換率驟降）

### Step 5：輸出週報

按 `templates/weekly-report.md` 格式輸出，最後附上下週優先事項（最多 5 點）。

## Output Format

1. **週報標題**：品牌 / 日期範圍 / 分析層級
2. **整體摘要**：總花費、總轉換、整體 ROAS / CPA、與上週比較
3. **四欄判斷表**：每個項目一列，強制有原因欄
4. **變動原因假設**：針對異常項目
5. **下週優先事項**：最多 5 點，具體可執行

## Quality Gates

- [ ] 每一筆判斷都有具體數字支撐的原因
- [ ] 沒有任何一筆原因欄寫「建議持續觀察」或「成效一般」
- [ ] 「擴量」的項目已確認是預算受限，而非自然飽和
- [ ] 「停用」的項目已排除是季節因素或追蹤異常
- [ ] 下週優先事項最多 5 點且全部具體可執行

---

## Artifact Governance

本技能產出為成效分析報告。

### 輸出路徑規則

- 分析報告寫入 `ai/reports/`（命名 `YYYY-MM-DD-{slug}.md`）
- 暫存/測試輸出寫入 `scratch/google-ads/`
- **禁止**將輸出寫入 repo 根目錄

### 政策參考

- `ai/registry/storage-map.yaml` / `ai/policies/artifact-naming-policy.md` / `ai/policies/artifact-write-policy.md`
