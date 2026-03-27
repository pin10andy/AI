# LOVEFU 山丘樂眠床 Google Ads Copy Pipeline v1.2 真實 UAT Rerun

- generated_by: codex
- generated_at: 2026-03-16T00:28:26+08:00
- source_csv: /Users/andychou/Downloads/素材資源關聯報表 (1).csv

## Artifact Files
- normalized input: /Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.input.json
- interpreter JSON: /Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.interpreter.json
- builder JSON: /Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json
- packager JSON: /Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.json
- packager Markdown: /Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.md

## 1. Input sufficiency summary

| field | present_in_source | verdict | note |
| --- | --- | --- | --- |
| impressions | yes (column exists) | unusable | 全數為 0 |
| clicks | yes (column exists) | unusable | 全數為 0 |
| ctr | yes (column exists) | unusable | 全數為 --，因 impressions=0 |
| asset_level_conversions | no | missing | 只有跨 conversion action 的 association proxy，不是嚴格 asset-level conversion |
| active_duration_days | no | missing | 以 runtime placeholder 0 通過 schema，不能拿來做 observe_new / observe_stale |
| placement_breakout | no | missing | 原始報表沒有 placement split |

- data sufficiency verdict: `partial`
- 高信心可下的結論：只有『source export 缺 rich layers』這件事本身，還有 protected phrase / token presence 的 existence check。
- 只能 directional 的結論：所有 performance ranking、retain / retire / reinforce、observe routing、candidate 補位優先序。

## 2. Interpreter UAT output

- 完整 JSON：/Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.interpreter.json
- asset_decisions count：140
- retire_now_assets count：7
- new_candidate_assets count：12
- warnings / data caveats：["這次是真實 LOVEFU 素材資源關聯報表 rerun，但 source export 不足以支撐 richer click / conversion / placement / duration layers。", "所有舊素材 decision_confidence 都只能是 directional，不能誤用成 high / medium / low 的表現結論。", "active_duration_days 為 runtime placeholder 0，只用於 schema 通過與明確標記缺失。", "真實素材池混有泛 LOVEFU / 飄雲與山丘樂眠床語言，final pack 已刻意拉高 hillbed-specific 比例。"]
- protected_phrase 是否正確保留：`100天安心睡` 由 ["hl-06", "cand-h05", "desc-02"] 承接。
- must_include_token 是否不再誤保弱句：是。`hl-68`、`hl-61`、`hl-86` 都含 LOVEFU / 山丘樂眠床 / 飄雲專利，但仍被 retire，由 replacement 補位。
- observe 子類別分布：{"observe_borderline": 24, "observe_insufficient_data": 47}
- decision_basis 分布：{"association_proxy_only": 140}
- decision_confidence 分布：{"directional": 140}
- safer_rewrite_of 示例：`hl-03 -> cand-h01`、`desc-01 -> cand-d01`、`desc-03 -> cand-d02`、`desc-22 -> cand-d03`。
- asset_decisions / retire_now_assets / new_candidate_assets / next_round_brief_additions 已完整寫入 JSON artifact。

## 3. Builder UAT output

- 完整 JSON：/Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json
- final_asset_pack total：19（primary=14，test=5）
- replacement_map count：7
- rejected_candidates count：3
- observe_assets_status count：71
- retire gap 是否都有補位：`yes`
- primary / test 比例：`0.263`
- coverage_check gaps：["angle:entry_value 仍是 gap，真實報表缺乏足夠安全且產品對焦的價值句。", "angle:legacy_phrase 只有單一 headline 承接，屬 thin coverage。", "rich_layer_gap: source CSV 依舊缺 click / placement / duration layers。"]
- coverage 狀態：entry_value=`gap`，legacy_phrase=`thin`，pain_point=`test_only`，其餘 angle 依 final pack 進 primary / test。
- safer rewrite 是否進 final pack：是，`cand-h01`、`cand-d01`、`cand-d02`、`cand-d03` 都有進 final。

## 4. Packager UAT JSON output

- 完整 JSON：/Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.json
- upload_summary：delivery_target=media_buyer，version_label=real-uat-v1-2-20260315，sign_off_status=pending_review
- upload_asset_pack：primary headlines=11，test headlines=4，primary descriptions=3，test descriptions=1
- retirement_sheet count：7
- uploader_checklist count：6
- strategic_notes main_angles：["product_feel", "risk_reversal", "brand_trust", "social_proof"]
- warnings：["source report 缺 click / impression / duration / placement rich layers，所有舊素材 performance 只可視為 directional。", "本輪 final pack 有 9 則新 candidate，雖然更接近可上稿，但仍必須人工審核。", "entry_value angle 仍是 gap，本輪沒有進 final pack。"]

## 5. Packager UAT Markdown output

- 完整人類可讀版：/Users/andychou/AI/ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.md
- 內容已包含本輪上稿摘要、主力素材、測試素材、本輪下架素材、替換對照表、上稿前檢查清單、策略備註。

## 6. UAT validation summary

- 三層串接是否成功：`yes`，interpreter -> builder -> packager 三份 JSON 都已生成。
- 是否有 contract fail：`source_data_contract_fail`，因原始 CSV 缺 rich layers；`handoff_contract_fail=no`。
- 是否有 schema mismatch：`artifact_schema_mismatch=no`，validation={"input_schema": "pass", "interpreter_schema": "pass", "builder_schema": "pass", "packager_schema": "pass"}。
- 成功 handoff 的欄位：angle_taxonomy、asset_decisions.angle_key、decision_confidence、observe_reason、retire_now_assets.coverage_gap_created、new_candidate_assets.risk_level / rewrite_mode / safer_rewrite_of、coverage_check、replacement_map。
- 仍有流失的欄位：真實 source 沒有 asset_level_conversions、active_duration_days、placement_breakout；這些是 runtime 明示缺失，不是靜默補齊。
- 最值得注意的 warnings：1. rich layers 沒被真實資料支撐。2. active_duration_days 只能用 placeholder。3. 真實素材池混有泛 LOVEFU / 飄雲語言，會稀釋 hillbed specificity。

## 7. v1.2 UAT verdict

- v1.2 是否比 v1.1 更接近可上稿 workflow：`部分是`
- 最關鍵改善的 3 點：
  1. angle_key 真的成為三層共用語言，從 interpreter 到 packager 都沒有掉欄。
  2. safer_rewrite_of 真正作用在高風險歷史贏家，並且進 final pack 與 watchlist。
  3. builder / packager 已收斂到真實 RSA 規模，剛好 15 headlines + 4 descriptions，而不是把舊池整桶保留。
- 仍存在的 3 個問題：
  1. 真實 CSV 沒有 richer click / conversion / placement / duration layers，所以 v1.2 的核心升級無法被 live export 真正吃滿。
  2. observe_new / observe_stale / retire_candidate 無法被可靠驗證，這次只驗到 observe_insufficient_data / observe_borderline。
  3. 真實素材池混入泛 LOVEFU / 飄雲語言，產品對焦還需要前置過濾。
- 是否建議進 v1.3：`yes`
- v1.3 最有槓桿的 3 個修正點：
  1. 做一層 Google Ads export normalizer，優先吃到真實 impressions / clicks / asset-level conversions / active_duration_days / placement。
  2. 在 interpreter 前加 product-scope filter / drift detector，先把泛 LOVEFU 與 hillbed-specific 素材分池。
  3. 把 packager 升級成可直接輸出 RSA-ready upload sheet，並加上 policy-risk hard gate。

