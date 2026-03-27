# Validation Record: LOVEFU 山丘樂眠床 Golden Brief

> 任務：`ai/tasks/2026-03-14-lovefu-hillbed-golden-brief.yaml`（gads-copy-004）

## Related Task

`gads-copy-004` / `ai/tasks/2026-03-14-lovefu-hillbed-golden-brief.yaml`

## What Was Tested

1. 指定 repo 檔案是否存在，且 brief / PMax workflow 契約與規劃一致
2. `lovefu-pmax-hillbed` brief 是否正式通過 `ai/inputs/google-ads-brief.schema.json`
3. PMax output 是否正式通過 `ai/schemas/google-ads-pmax-output.schema.json`
4. PMax output 是否通過 `ad_copy_validator.py --exact-pmax-output`
5. forbidden claims 是否完全未出現在輸出文案
6. angle coverage 是否達到每個 angle `4+ short / 1+ long / 1+ description`
7. keyword-message fit 是否達到 `3+ short / 1+ long / 1+ description`
8. rubric 自評是否達到 `overall >= 3.5`
9. 依 `ai/evals/google-ads-pmax-human-review.md` 的人工審查結果

## Agents / Tools Involved

- codex
- Python 3
- `.tmp/jsonschema-venv/bin/python` + `jsonschema`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`

## Source of Truth Files

- `ai/inputs/google-ads-brief.schema.json`
- `ai/brand/master-brand.yaml`
- `ai/playbooks/google-ads-pmax.md`
- `ai/schemas/google-ads-pmax-output.schema.json`
- `ai/skill-src/google-ads-writer/templates/pmax-output.md`
- `ai/evals/ads-rubric.yaml`
- `ai/evals/google-ads-pmax-human-review.md`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `ai/testcases/google-ads/outputs/lovefu-mattress-pmax.output.json`
- `ai/inputs/briefs/lovefu-pmax-hillbed.json`
- `ai/outputs/lovefu-pmax-hillbed.output.json`
- `ai/outputs/lovefu-pmax-hillbed.output.md`
- `https://www.lovefu.tw/products/hillbed`

## Result

通過

## Repo Fact Check

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| brief schema `additionalProperties: false` | ✓ | root object 明確禁止額外欄位 |
| `campaign_type = pmax` 的 brief `character_policy` | ✓ | required 為 `short_headline_count / short_headline_max / long_headline_count / long_headline_max / description_count / description_max` |
| PMax one-short-description rule 是否寫在 brief schema | ✗ | 不在 brief schema；存在於 playbook 與 validator |
| brief required 欄位 | ✓ | 與規劃一致：`brief_id / brand_name / product_name / campaign_type / goal / landing_page_summary / target_audience / keyword_cluster / usp / offers / constraints / tone / forbidden_claims` |
| 可重用 output format / testcase | ✓ | 已存在 `lovefu-mattress-pmax` testcase 與對應 output，可直接比照 |

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| `ai/inputs/briefs/lovefu-pmax-hillbed.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| `ai/outputs/lovefu-pmax-hillbed.output.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| brief formal schema validation | ✓ | 使用 `.tmp/jsonschema-venv/bin/python` + `jsonschema.Draft7Validator` 對 `ai/inputs/google-ads-brief.schema.json` 驗證，PASS |
| output formal schema validation | ✓ | 使用 `.tmp/jsonschema-venv/bin/python` + `jsonschema.Draft7Validator` 對 `ai/schemas/google-ads-pmax-output.schema.json` 驗證，PASS |
| brief / output structural check | ✓ | 以 repo-aware script 檢查 required keys、額外欄位與 PMax `character_policy`，結果 `structural_check_passed` |
| `ad_copy_validator.py --exact-pmax-output` | ✓ | 15 short / 5 long / 5 descriptions 與字元限制全通過 |
| `forbidden_claims` 清除檢查 | ✓ | 沒有任何輸出命中 forbidden claims |
| must_include terms | ✓ | `山丘樂眠床 / 100天安心睡 / 立即選購` 皆至少出現一次 |
| angle coverage | ✓ | `body-first-comfort=6/2/2`、`worry-free-choice=5/1/2`、`smart-start=4/2/1` |
| keyword-message fit | ✓ | 命中 `short=4`、`long=2`、`description=1`，皆高於最低要求 |
| description 短版條件 | ✓ | 最短 description 為 `100天安心睡 選床少一點壓力`，15 字 |
| markdown deliverable | ✓ | 與 JSON 一致，已建立 `ai/outputs/lovefu-pmax-hillbed.output.md` |

## Rubric Self-Score

| 維度 | 分數 | 理由 |
|------|------|------|
| brand_consistency | 4.5 / 5 | 情緒語氣與品牌陪伴感更完整，但仍有少數句子偏直接，需保留人工把關 |
| char_limit_compliance | pass | validator 全通過 |
| cta_clarity | 4.0 / 5 | `立即選購` 與商品頁導向一致，但 CTA 集中在部分資產，仍有微調空間 |
| headline_diversity | 5.0 / 5 | 3 條 angle 清楚，短標題之間有明顯分工，非單純換字序 |
| angle_coverage | 5.0 / 5 | 3 個 angle 都有 short / long / description 實際覆蓋 |
| policy_safety | 4.0 / 5 | 避開醫療與最低價宣稱，但腰背放鬆語意仍需人工守邊界 |
| language_quality | 5.0 / 5 | 全繁體中文、語意自然，品牌化表達與產品事實結合穩定 |

**Overall score**: `4.65 / 5.00`  
**Passing threshold**: `3.5 / 5.0`  
**Result**: 通過

## Human Review

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| 是否符合品牌語氣 | 是 | 有 LOVEFU 的安心、陪伴與放鬆感，沒有硬促銷口吻 |
| 是否有 3 種以上不同訴求 | 是 | 支撐安全 / 安心試睡 / 入門不將就三線清楚 |
| 是否避免違規宣稱 | 是 | 未出現醫療治療、最低價或保證效果 |
| Short headlines 是否夠分散 | 是 | 15 則可重組，沒有一直重講同一句 |
| Long headlines 是否有補充價值 | 是 | 有補材質、信任與入門定位，不是單純加長版 |
| Descriptions 是否可直接上稿 | 是 | 5 則都能獨立成立，且有 1 則短版 |
| 是否重複感過高 | 否 | 角度分布與語意差異足夠 |

**初步判斷**: 可直接上稿

## Issues Found

1. 商品頁與活動頁的促案訊息不同
   - 商品頁可驗的是 `100天安心睡`、`10年保固` 與站內方案資訊
   - 規劃草稿中的 `購床贈竹眠防水保潔墊` 較接近活動頁訊息
   - 本輪處理：不把該贈品寫成商品頁常態 offer，僅保留在 brief `notes`

## Conclusion

`lovefu-pmax-hillbed` 已完成 golden brief、正式 PMax output、Markdown、欄位分級與 R&D 記錄，
而且在不修改 schema 的前提下通過正式 JSON Schema validation、格式驗證、rubric 自評、
human review、angle coverage 與 keyword-message fit 檢查。

這份 brief 可以作為 hillbed 的第一份正式 golden brief，也可作為 Phase 2 brief builder 的欄位切分基準。
