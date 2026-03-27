# Validation Record: Hillbed Purchase PMax Hardening

## Related Task

`hard-001` / `ai/tasks/2026-03-15-hillbed-pmax-hardening.yaml`

## What Was Tested

1. 第三筆 approved reference output 是否建立完成
2. 三筆 approved references 是否都可納入 regression baseline
3. 三筆 approved references 是否都通過正式 output schema validation
4. 新 reference output 是否通過 `ad_copy_validator`、rubric 與 human review
5. wording risk watchlist 與 production change control ADR 是否落檔
6. production lane 的核心操作文件是否已引用新的 gate

## Agents / Tools Involved

- Codex
- `.tmp/jsonschema-venv/bin/python` + `jsonschema`
- `python3`
- `ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py`

## Source of Truth Files

- `ai/inputs/briefs/lovefu-pmax-hillbed.json`
- `ai/outputs/lovefu-pmax-hillbed.output.json`
- `ai/outputs/lovefu-pmax-hillbed.codex-dry-run.output.json`
- `ai/outputs/lovefu-pmax-hillbed.approved-reference-03.output.json`
- `ai/validation/regression-baseline-hillbed-pmax.yaml`
- `ai/decisions/ADR-003-hillbed-pmax-production-change-control.md`
- `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`

## Result

通過

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| approved reference outputs 數量 | ✓ | canonical + codex dry run + reference 03，共 3 筆 |
| canonical output schema validation | ✓ | 通過 |
| codex dry run output schema validation | ✓ | 通過 |
| reference 03 output schema validation | ✓ | 通過 |
| canonical output `ad_copy_validator --exact-pmax-output` | ✓ | 通過 |
| codex dry run output `ad_copy_validator --exact-pmax-output` | ✓ | 通過 |
| reference 03 `ad_copy_validator --exact-pmax-output` | ✓ | 15 short / 5 long / 5 desc 全 pass |
| reference 03 must_include terms | ✓ | `山丘樂眠床 / 100天安心睡 / 立即選購` 皆出現 |
| reference 03 keyword-message fit | ✓ | `short=4 / long=2 / desc=1`，高於 `3 / 1 / 1` |
| reference 03 angle coverage | ✓ | `body-first-comfort=6/2/2`、`worry-free-choice=5/1/2`、`smart-start=4/2/1` |
| reference 03 price signal scope | ✓ | `14,900起` 僅出現在 `smart-start` |
| reference 03 rubric self-eval | ✓ | `brand=4.5 / cta=4.0 / diversity=4.5 / angle=5.0 / policy=4.0 / language=5.0 / overall=4.50` |
| reference 03 human review verdict | ✓ | `可直接上稿` |
| change control ADR 落檔 | ✓ | ADR-003 已定義 Class A/B/C 與 future gate |
| wording risk watchlist 落檔 | ✓ | Tier 1 / 2 / 3 與 reviewer checklist 完整 |
| supported lane docs 已更新引用 | ✓ | supported-matrix / spec / runbook 已對齊新 gate |

## Issues Found

無阻塞問題。

## Conclusion

既有 `hillbed-purchase-pmax` production lane 已完成 hardening。
未來 production change 可依 ADR-003 的 gate 執行，
且 regression baseline 不再依賴單一輸出。
