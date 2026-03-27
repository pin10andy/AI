# Validation Record: Search RSA 文案生成 MVP

> 任務：`ai/tasks/2026-03-14-google-ads-copy-mvp.yaml`（gads-copy-001）

## Related Task

`gads-copy-001` / `ai/tasks/2026-03-14-google-ads-copy-mvp.yaml`

## What Was Tested

1. 新增的 brief schema 與 Search RSA output schema 是否可被 JSON parser 讀取
2. 三份 Search RSA testcase 是否可被 YAML parser 讀取，且核心欄位完整
3. `ad_copy_validator.py` 是否可讀取新的 Search RSA JSON 結構
4. `ad_copy_validator.py` 是否能強制檢查 `15 headlines + 4 descriptions`
5. `google-ads-writer` 是否已改為 Search RSA only 流程
6. skill sync 是否成功更新 `.claude/skills/`、`.agents/skills/`、`runtime/openclaw/`
7. 三份 testcase 是否已成功產出第一批 Search RSA JSON + Markdown
8. 用 human review checklist 快速判斷第一批結果是否接近可上稿

## Agents / Tools Involved

- codex
- Python 3
- Ruby（YAML parser）
- `bash scripts/sync-skills.sh`

## Source of Truth Files

- `ai/inputs/google-ads-brief.schema.json`
- `ai/schemas/google-ads-search-output.schema.json`
- `ai/playbooks/google-ads-search-rsa.md`
- `ai/evals/ads-rubric.yaml`
- `ai/evals/google-ads-human-review.md`
- `ai/skill-src/google-ads-writer/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `ai/testcases/google-ads/lovefu-mattress-search.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-search.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-search.yaml`
- `ai/testcases/google-ads/outputs/lovefu-mattress-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-mattress-search.output.md`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-search.output.md`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-search.output.json`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-search.output.md`
- `.agents/skills/google-ads-writer/SKILL.md`
- `.claude/skills/google-ads-writer/SKILL.md`
- `runtime/openclaw/google-ads-writer/skills/SKILL.md`

## Result

通過

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| `ai/inputs/google-ads-brief.schema.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| `ai/schemas/google-ads-search-output.schema.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| 三份 testcase YAML 可讀取 | ✓ | Ruby `YAML.load_file` 通過，且必填欄位完整 |
| testcase `campaign_type` 鎖定為 `search_rsa` | ✓ | 3 份檔案皆符合 |
| testcase `character_policy` 為 `15 / 4` | ✓ | 3 份檔案皆符合 |
| validator 可讀取新 Search RSA JSON 結構 | ✓ | 成功讀取 `/tmp/search_rsa_sample_output.json` 中的 object arrays |
| validator 可強制檢查 `15 headlines + 4 descriptions` | ✓ | `--exact-search-output` 通過，無 issues |
| validator 字元限制檢查 | ✓ | sample output 全數合規 |
| `google-ads-writer` 已改為 Search RSA only | ✓ | SKILL 內明確拒絕非 `search_rsa` |
| skill sync 完成 | ✓ | `.claude/.agents/runtime` 三處皆已有更新後副本 |
| `lovefu-mattress` 第一批輸出產生 | ✓ | JSON + Markdown 已建立，validator 通過 |
| `lovefu-neck-pillow` 第一批輸出產生 | ✓ | JSON + Markdown 已建立，validator 通過 |
| `lovefu-store-visit` 第一批輸出產生 | ✓ | JSON + Markdown 已建立，validator 通過 |
| 快速 human review：`lovefu-mattress` | ✓ | 品牌語氣與商業意圖穩，接近可直接上稿 |
| 快速 human review：`lovefu-neck-pillow` | ✓ | 量脖子差異化清楚，適合人工微調後上稿 |
| 快速 human review：`lovefu-store-visit` | ✓ | 到店 CTA 清楚，適合人工微調後上稿 |

## Issues Found

1. 本機環境缺少 `jsonschema` 與 `pyyaml`
   - 影響：無法直接跑標準 schema validator
   - 處理方式：改用 `python3 -m json.tool` 驗證 JSON 語法、Ruby 驗證 YAML 可讀性、更新後的 `ad_copy_validator.py` 驗證 Search RSA 結構

2. 第一批 human review 仍是快速內部評估
   - 影響：目前可判斷流程可用，但尚未經 PM / 投放端最終確認
   - 建議：下一步直接用 `ai/evals/google-ads-human-review.md` 由 PM 或實際投手複核

## Conclusion

Search RSA 文案生成 MVP 已不只停在架構層。
目前已具備固定 brief、固定 output contract、可執行 skill 流程、3 份 testcase、第一批 JSON + Markdown 輸出、人工 review checklist，以及可讀取新 JSON 結構的 validator。

**建議下一步：**
1. 由 PM / 投放端用 `ai/evals/google-ads-human-review.md` 複核這 3 組輸出
2. 根據複核意見調整 angle 與 CTA 寫法，建立第二版樣本
3. 若 3 組中至少 2 組可直接微調後上稿，再開始 PMax 擴充
