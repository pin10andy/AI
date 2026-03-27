# Validation Record: PMax 文案生成 MVP

> 任務：`ai/tasks/2026-03-14-google-ads-pmax-mvp.yaml`（gads-copy-002）

## Related Task

`gads-copy-002` / `ai/tasks/2026-03-14-google-ads-pmax-mvp.yaml`

## What Was Tested

1. 共用 brief schema 是否可同時接受 Search 與 PMax brief
2. PMax output schema 是否可被 JSON parser 讀取
3. `google-ads-writer` 是否已升級為依 `campaign_type` 路由
4. `ad_copy_validator.py` 是否可讀取新的 PMax JSON 結構
5. `ad_copy_validator.py` 是否能強制檢查 `15 short / 5 long / 5 descriptions`
6. 三份 PMax testcase 是否可被 YAML parser 讀取，且 counts 正確
7. 三份 PMax 輸出樣本是否皆通過 validator
8. PMax human review 快照是否已建立
9. skill sync 是否已完成

## Agents / Tools Involved

- codex
- Python 3
- Ruby（YAML parser）

## Source of Truth Files

- `ai/inputs/google-ads-brief.schema.json`
- `ai/schemas/google-ads-pmax-output.schema.json`
- `ai/playbooks/google-ads-pmax.md`
- `ai/evals/ads-rubric.yaml`
- `ai/evals/google-ads-pmax-human-review.md`
- `ai/skill-src/google-ads-writer/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`
- `ai/testcases/google-ads/lovefu-mattress-pmax.yaml`
- `ai/testcases/google-ads/lovefu-neck-pillow-pmax.yaml`
- `ai/testcases/google-ads/lovefu-store-visit-pmax.yaml`
- `ai/testcases/google-ads/outputs/lovefu-mattress-pmax.output.json`
- `ai/testcases/google-ads/outputs/lovefu-neck-pillow-pmax.output.json`
- `ai/testcases/google-ads/outputs/lovefu-store-visit-pmax.output.json`
- `ai/reports/2026-03-14-pmax-human-review.md`
- `.agents/skills/google-ads-writer/SKILL.md`
- `.claude/skills/google-ads-writer/SKILL.md`
- `runtime/openclaw/google-ads-writer/skills/SKILL.md`

## Result

通過

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| `ai/inputs/google-ads-brief.schema.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| `ai/schemas/google-ads-pmax-output.schema.json` JSON 語法 | ✓ | `python3 -m json.tool` 通過 |
| 共用 brief 保留 Search 相容性 | ✓ | Ruby 驗證 3 份 search briefs 仍有效 |
| 共用 brief 接受 PMax | ✓ | Ruby 驗證 3 份 pmax briefs 皆有效 |
| `google-ads-writer` 已升級為雙路徑 | ✓ | SKILL 明確依 `campaign_type` 切換流程 |
| validator 可讀取 PMax JSON 結構 | ✓ | 可直接讀取 `short_headlines` / `long_headlines` / `descriptions` |
| validator 可強制檢查 PMax exact counts | ✓ | `--exact-pmax-output` 通過，無 issues |
| `lovefu-mattress-pmax` 通過 validator | ✓ | counts、字元數、短說明條件皆通過 |
| `lovefu-neck-pillow-pmax` 通過 validator | ✓ | counts、字元數、短說明條件皆通過 |
| `lovefu-store-visit-pmax` 通過 validator | ✓ | counts、字元數、短說明條件皆通過 |
| PMax human review 快照存在 | ✓ | 已建立報告檔，可作為複核起點 |
| skill sync 完成 | ✓ | `.claude/.agents/runtime` 三處皆已更新副本 |

## Issues Found

1. 本機環境仍缺少 `jsonschema` 與 `pyyaml`
   - 影響：無法直接跑標準 schema validator
   - 處理方式：使用 JSON parser、Ruby YAML parser 與更新後 validator 完成驗證

2. PMax 目前只驗證文字欄位
   - 影響：尚未涵蓋圖片、影片、feed、asset group 結構等完整 PMax 需求
   - 建議：下一階段若要更接近投放，需補 asset group metadata 與非文字素材欄位

3. PMax human review 仍是快速內部評估
   - 影響：目前可確認流程成立，但尚未經 PM / 投放端最終確認
   - 建議：下一步請 PM / 投手依 `ai/evals/google-ads-pmax-human-review.md` 複核

## Conclusion

PMax 文案生成 MVP 已建立完成，並與既有 Search RSA 流程共用同一份 brief contract。
目前已具備 PMax output schema、專用 playbook、雙路徑 skill、3 份 testcase、3 份輸出樣本，
以及可做 exact PMax 結構檢查的 validator。

**建議下一步：**
1. 由 PM / 投手依 `ai/evals/google-ads-pmax-human-review.md` 複核這 3 組輸出
2. 若 3 組中至少 2 組可微調後上稿，再考慮補圖片 / 影片 / asset group metadata
3. 若要進一步自動化，再補 batch generation 與 brief-to-output script
