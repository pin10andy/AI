# Validation: Creative Performance Interpreter Baseline

**日期**：2026-03-15
**驗證項目**：Creative Performance Interpreter Skill v1.0 — Baseline Dry Run
**驗證者**：claude
**狀態**：validated

---

## 驗證範圍

使用 LOVEFU 山丘樂眠床 PMax 的 25 則實際產出文案（canonical output），搭配模擬成效數據，完整跑完 Skill 的 6 步工作流程，產出 JSON + Markdown report。

### 輸入輸出對照

| 項目 | 路徑 |
|------|------|
| 輸入（模擬成效數據） | `ai/inputs/lovefu-pmax-hillbed-performance.json` |
| 輸出 JSON | `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.json` |
| 輸出 Markdown | `ai/outputs/lovefu-pmax-hillbed-performance-interpretation.md` |

---

## Rubric 自評

### data_honesty (0.25) — **5 / 5**

- ✅ 整體判定 sufficient（183,850 >> threshold 5,000）
- ✅ sh-14 曝光 450 < threshold 1,000，歸類 observe
- ✅ 識別 3 項數據缺口（素材層級轉換、曝光不足素材、版位拆分）
- ✅ compliance_notes 列出 5 項 data_caveats，包含 legacy 佔比過高的結構性提醒
- ✅ 未在 insufficient data 下做 retire 判斷

### decision_consistency (0.20) — **5 / 5**

- ✅ 所有 25 個決策均符合 decision-rules.md 的觸發條件
- ✅ 每個 rationale 都有具體 CTR、impressions、percentile 數字
- ✅ Legacy 素材（含山丘樂眠床 / 100天安心睡 / 立即選購）全部 retain
- ✅ CTR < P25 且非 legacy 且 impressions ≥ threshold → retire（4 則）
- ✅ CTR 在 P25-P50 → observe（3 則 + 1 則 insufficient data）
- ✅ retire → retire_now_assets mapping 正確（4 筆）
- ✅ reinforce → new_candidate_assets 正確（2 筆 expansion）
- ✅ observe 素材未進入 retire_now_assets
- ✅ retain 素材未進入任何清單

### legacy_preservation (0.20) — **pass**

- ✅ 3 條 Validated Legacy Messaging 全部出現在 retain 決策
- ✅ 全部出現在 validated_legacy_preserved
- ✅ 全部出現在 must_retain_messages
- ✅ 含 legacy 文字的 13 則素材全部為 retain（含 CTR < P25 的 sh-15、lh-04）
- ✅ 無任何 legacy 素材出現在 retire_now_assets

### pattern_extraction (0.15) — **5 / 5**

- ✅ 萃取 5 個語言模式，每個都有具體素材 ID + CTR 數據
- ✅ 3 個 high confidence（跨 2+ 素材驗證）、1 個 medium、1 個 high
- ✅ 模式可直接被 writer 使用（如「先...再... 句式」「口語化降低門檻」）
- ✅ 中文模式使用全形逗號

### brief_actionability (0.10) — **5 / 5**

- ✅ must_include_language 4 項，具體可操作
- ✅ proven_angles 2 個，附完整 evidence
- ✅ language_to_avoid 3 項，有退場素材佐證
- ✅ suggested_seed_angles 2 個，來自 observe / insufficient data 素材
- ✅ tone_adjustments 3 項，有具體的效果梯度（100天 > 10年 > 14,900起）
- ✅ 新增候選文案 6 筆，全部有 source / intent / related_gap / suggested_role

### format_compliance (0.10) — **pass**

- ✅ JSON 語法合法
- ✅ 所有 required 欄位齊全
- ✅ additionalProperties 無違規
- ✅ enum 值正確（decision、source、suggested_role、asset_type）
- ✅ 中文使用全形逗號
- ✅ manual_review_required = true
- ✅ retire_now_assets 的 replaced_by_candidate_id 交叉引用正確

### Overall Score

| 維度 | 權重 | 分數 | 加權 |
|------|------|------|------|
| data_honesty | 0.25 | 5 | 1.25 |
| decision_consistency | 0.20 | 5 | 1.00 |
| legacy_preservation | 0.20 | pass | — |
| pattern_extraction | 0.15 | 5 | 0.75 |
| brief_actionability | 0.10 | 5 | 0.50 |
| format_compliance | 0.10 | pass | — |

**Overall = 5.0**（非 pass/fail 維度加總：1.25 + 1.00 + 0.75 + 0.50 = 3.50 / 0.70 = 5.0）
**Required pass：** legacy_preservation ✅ / format_compliance ✅

---

## Quality Gates 逐項確認

- [x] 每個決策都有具體數字支撐的原因（CTR、impressions、percentile）
- [x] 沒有任何 Validated Legacy Messaging 被標為 retire
- [x] 數據不足的素材全部標為 observe（sh-14）
- [x] 全域 sufficient，retire 判斷有效
- [x] must_retain_messages 包含所有 3 條 legacy messaging 文本
- [x] 中文文案分隔符使用全形逗號
- [x] manual_review_required = true
- [x] Rubric 總分 5.0 ≥ 3.5，legacy 和 format 均 pass
- [x] retire → retire_now_assets 正確 mapping（4 筆）
- [x] reinforce → new_candidate_assets 正確觸發（2 筆 expansion）
- [x] observe 不進 retire_now_assets
- [x] retain 不進任何清單
- [x] 新候選文案中文使用全形逗號
- [x] replace_retired_asset 的交叉引用完整（cand-01 ↔ sh-05、cand-02 ↔ sh-06、cand-03 ↔ sh-13）

---

## Dry Run 發現的結構性問題

### 1. Legacy 保護範圍過廣

**問題**：`validated_legacy_messaging` 中包含「山丘樂眠床」（產品名），導致 13/25 則素材（52%）被 legacy 保護，retain 比例偏高至 60%。

**影響**：即使某些含產品名的素材 CTR 低於 P25（如 sh-15 CTR 2.5%、lh-04 CTR 3.8%），仍無法被退場。

**建議**：PM 應區分「legacy messaging 保護」與「must-include 關鍵字」。產品名「山丘樂眠床」更適合作為 must-include（確保出現在至少 N 則素材中），而非逐則 legacy 保護。

### 2. Description 版位的 CTR 基準問題

**問題**：所有素材混在一起計算 percentile，但 description 版位可能天生 CTR 較低。desc-05 被判 retire（CTR 2.7%），可能部分是版位因素而非文案問題。

**建議**：未來可考慮按 asset_type 分組計算 percentile，避免版位差異造成不公平比較。

### 3. 缺少素材層級轉換數據

**問題**：僅以 CTR 做分類，CTR 高不代表購買轉換高。可能存在 CTR 高但轉換低的素材被 reinforce、CTR 低但轉換高的素材被 retire 的風險。

**建議**：下輪 PMax 報表匯出時，爭取取得 asset 層級的 conversion 和 conversion value 數據。

---

## 結論

Creative Performance Interpreter v1.0 的完整工作流程驗證通過。Skill 定義、Schema、Decision Rules、Template、Playbook 均在 dry run 中正確運作。上述 3 個結構性問題為已知限制，不影響 baseline 凍結。
