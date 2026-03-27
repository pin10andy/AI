# Validation Record: Google Ads Copy Pipeline v1.1 E2E

## Related Task

`gads-pipeline-011` / `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-1.yaml`

## What Was Tested

1. interpreter / builder / packager 的 input/output schema 是否可解析
2. legacy 模型是否已拆成 `protected_phrase` / `must_include_token` / `reusable_motif`
3. 每個 decision 是否要求 `decision_basis` / `decision_confidence`
4. percentile 是否改為 `asset_type` cohort
5. builder / packager handoff 是否改為 field-level validation
6. LOVEFU / 山丘樂眠床 sample run 是否形成完整 rerun chain

## Agents / Tools Involved

- Codex
- `python3`
- `ruby`
- `rg`

## Source of Truth Files

- `ai/inputs/creative-performance-input.schema.json`
- `ai/schemas/creative-performance-output.schema.json`
- `ai/inputs/ad-copy-portfolio-input.schema.json`
- `ai/schemas/ad-copy-portfolio-output.schema.json`
- `ai/inputs/upload-packager-input.schema.json`
- `ai/schemas/upload-packager-output.schema.json`
- `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/SKILL.md`
- `ai/skill-src/google-ads/upload-packager/SKILL.md`
- `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/references/decision-rules.md`
- `ai/skill-src/google-ads/upload-packager/references/decision-rules.md`

## Result

通過

## E2E Validation Checklist

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| interpreter input schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| interpreter output schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| builder input schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| builder output schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| packager input schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| packager output schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| rubric / task YAML 語法合法 | ✓ | `ruby` 成功載入 4 個 YAML |
| legacy 三分模型出現在 interpreter input / output / sample run | ✓ | 三類欄位與 sample 一致 |
| `decision_basis` / `decision_confidence` 出現在 interpreter schema / rules / sample run | ✓ | schema、rules、skill doc 全數對齊 |
| percentile 改為 `asset_type` cohort | ✓ | playbook、rules、schema 已改 |
| builder handoff 改為 field-level validation | ✓ | rules / input schema 均要求逐欄 |
| packager handoff 改為 field-level validation | ✓ | rules / input schema / output `handoff_validation` 對齊 |
| builder final asset 保留 `decision_confidence` / `coverage_tags` | ✓ | output schema + sample run 已對齊 |
| packager 保留 `decision_confidence` / `coverage_tags` / `coverage_after_replacement` | ✓ | output schema + sample run 已對齊 |
| LOVEFU rerun：sh-15 不再因 legacy blanket retain | ✓ | 改為 must_include token carrier，可 retire + replacement |
| LOVEFU rerun：cand-07 補回 `山丘樂眠床` / `立即選購` coverage | ✓ | builder / packager sample run 均可追到 |

## LOVEFU Rerun Trace

### Interpreter

- `sh-15` 在 v1.1 rerun 中不再因產品名與 CTA 自動 retain
- 原因：`山丘樂眠床` / `立即選購` 被歸到 `must_include_token`
- 結果：`sh-15` 可依 short_headline cohort 基準退休，但要記錄 token coverage gap

### Builder

- `cand-07` 被定義為 replacement candidate
- `covers_tokens = ["山丘樂眠床", "立即選購"]`
- `inherits_motifs = ["lower-friction-cta"]`
- `replacement_map.coverage_after_replacement` 明確說明補回 coverage

### Packager

- `handoff_validation` 驗證 builder output 的 field-level completeness
- `action_checklist` 新增 token coverage 驗證步驟

## Issues Found

無阻塞問題。

## Conclusion

Google Ads copy pipeline v1.1 的三個核心修正已完成：

1. legacy 模型已三分化
2. decision basis / confidence 已成為 required contract
3. builder / packager handoff 已升級為 field-level validation

LOVEFU / 山丘樂眠床 rerun 已能展示新 contract 的完整傳遞。
