# Validation Record: Google Ads Copy Pipeline v1.2 Rerun

## Related Task

`gads-pipeline-012` / `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-2.yaml`

## What Was Tested

1. interpreter / builder / packager 的 input/output schema 是否可解析
2. richer input layers 是否進入 interpreter contract
3. observe 是否拆成可執行子類別
4. candidate pipeline 是否有 `risk_level / rewrite_mode / safer_rewrite_of`
5. angle taxonomy 是否成為顯式上游欄位並一路傳到底
6. LOVEFU / 山丘樂眠床 sample rerun 是否形成完整 v1.2 chain

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
- `ai/inputs/lovefu-pmax-hillbed-performance.json`
- `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/SKILL.md`
- `ai/skill-src/google-ads/upload-packager/SKILL.md`
- `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/references/decision-rules.md`
- `ai/skill-src/google-ads/upload-packager/references/decision-rules.md`

## Result

通過

## Static Validation

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| 6 個 schema JSON 語法合法 | ✓ | `python3` 成功載入 |
| LoveFu sample input JSON 語法合法 | ✓ | `python3` 成功載入 |
| 3 份 rubric + v1.2 task YAML 語法合法 | ✓ | `ruby` 成功載入 |
| skill docs / decision rules 已切到 v1.2 | ✓ | `rg` 掃描通過 |

## v1.2 Rerun Checklist

| 檢查項目 | 結果 | 證據 |
|---------|------|------|
| input data basis 不再只靠 association proxy | ✓ | LoveFu sample input 已提供 `impressions / clicks / ctr / asset_level_conversions / placement_breakout / active_duration_days` |
| decision_confidence 不再全面 low | ✓ | sample run 中 `sh-15 / sh-01 / sh-07` 可達 `high`，candidate / new assets 為 `medium` |
| observe 已拆成可執行子類別 | ✓ | schema / rules / sample run 全數使用 `observe_new / observe_insufficient_data / observe_stale / observe_borderline` |
| active_duration downgrade 已納入 contract | ✓ | input config 有 `observe_stale_days / retire_candidate_days`，rules 有 downgrade logic |
| `new_candidate_assets` 已支援補位與 safer rewrite | ✓ | `cand-07` 為 replacement；`cand-12` 為 `safer-rewrite` |
| candidate 數量與 retire gap 更匹配 | ✓ | sample rerun 中 retire gap 有 replacement，且另有 reinforce / safer rewrite test candidate |
| `angle_key` 已成為上游顯式欄位 | ✓ | input `assets[*].angle_key` 必填，interpreter / builder / packager 全數保留 |
| coverage / redundancy / notes 使用同一 taxonomy | ✓ | builder `coverage_check.angle_coverage` 與 packager `strategic_notes` 對齊同一 10-key taxonomy |
| final pack 已收斂到較合理規模 | ✓ | sample builder summary 為 `12 primary / 4 test / 16 total`，不再是無上限保留 |
| 高效高風險語言已有 safer rewrite 路徑 | ✓ | `lh-05` -> `cand-12` 出現在 interpreter candidates 與 packager watchlist |

## LOVEFU Rerun Trace

### Interpreter

- `sh-15` 不再因產品名與 CTA token 自動保留
- 在完整 click / conversion / placement 資料下，`decision_basis` 可用 `hybrid_asset_type_percentile`
- `sh-14` 由單一 observe 改成 `observe_new`
- `lh-05` / `sh-16` 的高效痛點語言不再只被視為 winner，而是觸發 safer rewrite candidate

### Builder

- `cand-07` 補回 `山丘樂眠床` / `立即選購` token coverage
- `cand-12` 讓 pain-point angle 改走 safer rewrite 測試，不直接擴寫風險原句
- `observe_new` 不再等同自動進主力
- final pack 依 character policy 收斂到可上稿規模

### Packager

- `strategic_notes` 直接輸出主力角度 / 測試角度 / 不再擴寫角度
- `safer_rewrite_watchlist` 能追到 `lh-05 -> cand-12`
- checklist 新增 observe 回看與 safer rewrite QA

## Updated Known Limitations

1. 目前仍是 sample rerun，不代表真實上稿後就一定提升轉換。
2. `association_proxy_only` fallback 仍存在，表示舊報表品質差時仍會回退到低信心模式。
3. builder / packager 雖更像 execution system，但真正的 candidate 量產仍需未來串接 brief generator runtime。

## Conclusion

Google Ads copy pipeline v1.2 的四個核心修正已完成：

1. richer input layers 已進入正式 contract
2. observe 已拆成可執行子類
3. candidate pipeline 已支援 replacement 與 safer rewrite
4. angle taxonomy 已成為跨 skill 的明確 handoff 語言
