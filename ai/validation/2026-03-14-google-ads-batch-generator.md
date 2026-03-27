# Validation Record: Google Ads 文案批次生成工具

> 任務：`ai/tasks/2026-03-14-google-ads-batch-generator.yaml`（gads-copy-003）

## Related Task

`gads-copy-003` / `ai/tasks/2026-03-14-google-ads-batch-generator.yaml`

## What Was Tested

1. 批次腳本是否可讀取 6 份 brief
2. 是否可依 `campaign_type` 產出 Search RSA / PMax JSON + Markdown
3. 生成的 Search JSON 是否皆通過 `--exact-search-output`
4. 生成的 PMax JSON 是否皆通過 `--exact-pmax-output`
5. `google-ads-writer` skill 是否已補上 batch usage
6. skill sync 是否完成

## Agents / Tools Involved

- codex
- Ruby
- Python 3

## Source of Truth Files

- `ai/skill-src/google-ads-writer/scripts/batch_generate_ads_copy.rb`
- `ai/skill-src/google-ads-writer/SKILL.md`
- `ai/inputs/google-ads-brief.schema.json`
- `ai/schemas/google-ads-search-output.schema.json`
- `ai/schemas/google-ads-pmax-output.schema.json`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `ai/testcases/google-ads/lovefu-mattress-search.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-search.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-search.yaml`
- `ai/testcases/google-ads/lovefu-mattress-pmax.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-pmax.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-pmax.yaml`
- `.tmp/google-ads-batch/`

## Result

通過

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| 批次腳本可讀取 6 份 brief | ✓ | Search 3 份 + PMax 3 份 |
| 批次腳本可輸出 JSON + Markdown | ✓ | 共產出 12 個檔案到 `.tmp/google-ads-batch/` |
| Search outputs 通過 exact validator | ✓ | 3 份 Search JSON 皆通過 `--exact-search-output` |
| PMax outputs 通過 exact validator | ✓ | 3 份 PMax JSON 皆通過 `--exact-pmax-output` |
| `google-ads-writer` 已補 batch usage | ✓ | Skill 文件可直接指引批次操作 |
| skill sync 完成 | ✓ | `.claude/.agents/runtime` 三處副本皆已確認包含 batch script |

## Commands Run

```bash
ruby ai/skill-src/google-ads-writer/scripts/batch_generate_ads_copy.rb \
  --output-dir .tmp/google-ads-batch \
  ai/testcases/google-ads/*search.yaml \
  ai/testcases/google-ads/*pmax.yaml
```

```bash
for file in .tmp/google-ads-batch/*search.output.json; do
  python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py \
    --file "$file" \
    --exact-search-output >/dev/null
done
```

```bash
for file in .tmp/google-ads-batch/*pmax.output.json; do
  python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py \
    --file "$file" \
    --exact-pmax-output >/dev/null
done
```

## Issues Found

1. 本機環境仍缺少 `jsonschema` 與 `pyyaml`
   - 影響：無法直接跑標準 schema validator
   - 處理方式：以 Ruby 讀 brief，並用既有 exact validator 驗證輸出結構

2. `/tmp/google-ads-batch` 在本機流程中未保留結果
   - 影響：批次驗證改寫到 workspace 內的 `.tmp/google-ads-batch`
   - 處理方式：改用 workspace 暫存路徑，便於後續複核與重跑

3. 批次工具目前屬 deterministic draft generator
   - 影響：可保證格式與基本結構，但不代表已達最終上稿品質
   - 建議：仍需搭配 human review checklist 進行商業與品牌複核

## Conclusion

`batch_generate_ads_copy.rb` 已可作為 Google Ads 文案 MVP 的批次入口，
把既有 Search RSA / PMax brief 一次轉成可 review 的 JSON + Markdown 草稿。
目前已確認可讀取 6 份 brief、產出 12 份檔案，且 6 份 JSON 皆通過現有 exact validator。

**建議下一步：**
1. 由 PM / 投手抽查 `.tmp/google-ads-batch/` 的 6 份草稿
2. 若要再往前一步，可把此腳本包成更固定的 `brief-to-output` CLI
3. 如果之後要進正式釋出，可再補 release artifact 或接到自動化 pipeline
