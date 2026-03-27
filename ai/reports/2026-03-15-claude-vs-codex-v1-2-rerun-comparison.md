# Claude vs Codex Google Ads Copy Pipeline v1.2 Rerun Comparison

- generated_by: codex
- generated_at: 2026-03-16
- scope: artifact-level comparison only; no pipeline rerun

## 1. Executive Summary

Claude 的 archived initial-run 產物有完整 schema 外觀，但關鍵 handoff 多停在「有欄位、少落地」；Codex 的 real-UAT rerun 則把弱資料限制、risk rewrite、replacement handoff 與 upload decision 真正串成可執行 artifact chain。

目前較適合當默認 runner 的是 **Codex**。  
**不建議雙 runner 並行當默認流程**；但建議保留 Claude，定位為 **challenger / auditor / backup runner**，專門做對照審查與補充視角。

## 2. Artifact Completeness Check

| Artifact Class | Claude rerun | Codex rerun | Notes |
|---|---|---|---|
| Input artifact | Partial | Yes | Claude 只有 `LoveFu_pipeline_v1-2_input_sufficiency.md`；Codex 有可重現的 `lovefu-hillbed-copy-pipeline-v1-2-real-uat.input.json`。 |
| Interpreter JSON | Yes | Yes | 兩邊都有完整 interpreter artifact。 |
| Builder JSON | Yes | Yes | 兩邊都有完整 builder artifact。 |
| Packager JSON | Yes | Yes | 兩邊都有完整 packager artifact。 |
| Human-readable packager Markdown | Yes | Yes | 兩邊都有 packager Markdown。 |
| Validation summary | Yes | Yes | Claude 是 archived draft `LoveFu_pipeline_v1-2_UAT_validation.md`；Codex 有 governed validation `2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md`。 |
| Task record | No | Yes | Codex 有 `2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.yaml`。 |
| Change record | No | Yes | Codex 有 `ai/changes/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md`。 |
| Executable rerun trace | Partial | Yes | `google_ads_copy_pipeline_v12_real_uat_rerun.py` 存在，但它被 Codex task/change 明確綁定；Claude archived run 沒有自己的 frozen input JSON 與 run-bound trace。 |
| Registry / provenance clarity | Partial | Yes | `ai/registry/artifacts.yaml` 明確標示 Claude 組是 archived initial-run snapshot，且與 governed UAT run 為不同 md5。 |

## 3. Side-by-Side Comparison

| Dimension | Claude Score (1-5) | Codex Score (1-5) | Evidence | Winner | Notes |
|---|---:|---:|---|---|---|
| Contract fidelity | 2 | 4 | Claude 的 `LoveFu_pipeline_v1-2_interpreter.json` / `builder.json` / `packager.json` top-level keys 齊全，但 handoff 沒真正落地：`builder.json` 的 `replacement_map` 為空、`coverage_check.protected_phrase_check[0].status=\"gap\"`、`hl-66` 在 interpreter 是 `observe_new`，到了 builder primary pack 變成 `source=\"retained\"` 且 `observe_subtype=null`。Codex 的 `lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json` 有 7 筆 `replacement_map`，`hl-39` 仍保留 `source=\"retained_observe\"` 與 `observe_subtype=\"observe_borderline\"`，`safer_rewrite_of` 也被寫進 replacement notes。 | Codex | Claude 比較像 schema pass；Codex 比較像 contract 真正被執行。 |
| Business realism | 2 | 4 | Claude final pack 規模雖然是 19 則，但主力 pack 仍保留 `hl-03`、`desc-01`、`desc-03` 這類高風險舊句，且 `replacement_map=[]`、`retirement_changelog=[]`。其 `coverage_check` 仍有 `100天安心睡` gap、`立即選購` gap，`life_scene` / `cta_lower_friction` 也未承接。Codex final pack 同樣收斂到 19 則，但真正 retire 7 則並用 `cand-h01`、`cand-d01`、`cand-d02`、`cand-d03` 等替換，主力 / 測試角度也更接近 media buyer 可執行結構。 | Codex | Codex 仍有 generic LOVEFU / 飄雲殘留與 `entry_value` gap，所以不是滿分。 |
| Honesty under weak data | 2 | 5 | Claude 的 `LoveFu_pipeline_v1-2_input_sufficiency.md` 其實已誠實寫出 `decision_confidence` 上限只能是 directional，但 `LoveFu_pipeline_v1-2_UAT_validation.md` 仍把 6 個 checkpoint 全部寫成 PASS，沒有把 source-data fail 與 handoff success 明確拆開。Codex 的 `2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md` 明確寫 `source_data_contract_fail`、`handoff_contract_fail=no`、`artifact_schema_mismatch=no`，並反覆標示 `active_duration_days` 是 runtime placeholder 0、`sign_off_status=pending_review`。 | Codex | Codex 在弱資料下更接近「誠實且可被審核」的 runner。 |
| Reproducibility | 2 | 5 | Claude 組缺 normalized input JSON，也沒有 task/change trace 綁定 archived run；`ai/registry/artifacts.yaml` 還明寫這組是 archived initial-run snapshot，不是 governed UAT run。Codex 組有 `input.json`、script、task、change、validation、packager md/json，且 validation 明列 schema pass 與 source CSV path。 | Codex | 這一維差距最大。 |
| Review usefulness | 2 | 5 | Claude 的 packager md 排版完整，但 PM / 投手看完仍不知道哪些高風險舊句要真的下架，因為 watchlist 與 upload list 斷開，`test_angles=[]`、`retirement_changelog=[]`。Codex 的 packager md 直接列出主力素材、測試素材、下架素材、替換對照表、上稿前檢查清單與策略備註，也在 validation 裡延伸到 v1.3 product decision。 | Codex | Claude 比較像漂亮摘要；Codex 比較像可交接工作包。 |

## 4. Key Differences

1. Claude 把 `hl-03`、`desc-01`、`desc-03` 留在主力 pack；Codex 則在 interpreter 直接 retire 這些高風險句，並在 builder `replacement_map` 用 `cand-h01`、`cand-d01`、`cand-d02` 補位。
2. Claude `LoveFu_pipeline_v1-2_builder.json` 的 `replacement_map` 是空陣列；Codex `lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json` 有 7 筆具體替換，包含 `hl-61 -> cand-h03`、`hl-86 -> cand-h04` 這類 generic token carrier 的實際改寫。
3. Claude final pack 沒有解掉自己 coverage check 的核心缺口：`100天安心睡` found_count=0、`立即選購` found_count=0、`cta_lower_friction` gap；Codex final pack 則讓 `100天安心睡` 由 `hl-06`、`cand-h05`、`desc-02` 承接，並補齊 `LOVEFU` / `山丘樂眠床` / `飄雲專利` token visibility。
4. Claude interpreter 對 `hl-66` 的 decision 是 `observe_new`，但 builder primary pack 把它變成一般 `retained`，`observe_subtype` 消失；Codex builder 對 `hl-39` 仍保留 `source=\"retained_observe\"`、`observe_subtype=\"observe_borderline\"` 與 `status_note`，handoff 語意沒有掉。
5. Claude `LoveFu_pipeline_v1-2_UAT_validation.md` 把所有 checkpoint 寫成 PASS，卻沒有對應 retire / replacement 事實；Codex validation 明確拆分 `source_data_contract_fail` 與 `handoff_contract_fail=no`，避免把 directional conclusion 包裝成真正 pass。
6. Claude final pack 的 `test_angles` 是空的；Codex `packager.json` / `packager.md` 則明確把 `pain_point`、`life_scene`、`cta_lower_friction` 列為測試角度，讓 PM 知道什麼是主力、什麼是實驗。
7. Claude 組缺 task/change provenance；Codex 組有 `2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.yaml`、change record、validation record 與 script，對開發端更容易追 source、trace、責任鏈。

## 5. Risks and Limitations

1. 兩邊都受同一個 source data 問題限制：缺 click layer、placement layer、可信 duration layer，也沒有真正 asset-level purchase conversion。
2. Codex 雖然更誠實，但仍使用 `active_duration_days=0` placeholder；Claude 則使用 proxy duration。兩邊都不能宣稱已在可信 duration data 上驗證 `observe_new / observe_stale`。
3. safer rewrite 是否真的比原句更能上線、更能過政策、或更能帶來轉換，這次都尚未經 live upload / live spend 驗證。
4. 這份比較是 artifact-level review，不是重跑或盲測；它比較的是「目前 workspace 裡實際存在的兩組成果」。
5. Claude 組在 registry 中被標示為 archived initial-run snapshot，而 Codex 組是 governed real-UAT rerun；因此本次比較部分反映 runner 能力，部分也反映 run maturity 與治理完整度。

## 6. Final Verdict

**Codex 較適合當目前默認 runner。**

原因不是檔案比較多，而是它在五個核心面向都更接近「可交接、可複查、可做產品決策」：

- 它沒有只停在 schema pass，而是真的把 `safer_rewrite_of`、`replacement_map`、`observe_subtype`、angle coverage 與 upload decision 串起來。
- 它把弱資料限制講清楚，沒有把 directional 結論包裝成高信心 PASS。
- 它提供了 input / script / task / change / validation 的完整證據鏈，讓 PM 與開發都能回溯。

如果要指定默認 runner，另一個 runner 建議保留為：

- **Claude = challenger / auditor / backup runner**

適合用來做：

- 對 Codex final pack 做第二意見審查
- 挑戰 Codex 是否過度收斂或過度保守
- 在需要 alternative candidate ideas 時提供補充視角

但不建議讓 Claude 在目前階段擔任默認 execution runner。

## 7. Recommended Next Step

1. 正式指定 Codex 為目前 Google Ads copy pipeline v1.2 / v1.3 的默認 runner，並把最低交付 bundle 固定為：`input.json`、script / trace、interpreter / builder / packager、validation summary。
2. 把這次比較萃成 v1.3 hard gates：若 `source_data_contract_fail` 沒有顯式寫出、若高風險 retire 沒有對應 `replacement_map`、或 final pack 仍留有未解 protected phrase / token gap，就不能標成 PASS。
3. 保留 Claude，但改成 frozen-input challenger flow：只在 Codex 出完 governed artifact 後做 artifact review / alternative proposal，不再與主流程並行爭奪默認 runner。
