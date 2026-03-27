# Google Ads Creative Audit Report

- audit_id: lovefu-hillbed-search-rsa-real-uat-upload-v1-2-creative-audit
- generated_by: codex
- generated_at: 2026-03-24T00:05:41+08:00

## Executive Summary

- Evidence level: `pack_only`
- Health score: **76 / 100 (B)**
- Upload decision: **needs_manual_review**
- Verdict: RSA 素材量已達可審核水位，但 evidence 仍是 pack_only，且產品聚焦、angle gap、政策語氣與 path/payload drift 仍需人工確認。

## Source Data Assessment

- Fatigue confidence: `low`
- Platform-fit confidence: `low`
- Notes:
  - Input is derived from upload-packager output only; no export-backed click, impression, placement, or duration layers are attached.
  - Fatigue and platform-fit remain directional because evidence_level is pack_only.
  - This audit uses text assets only; serving behavior still needs live or export-backed evidence.
  - Artifact path suggests `evergreen-purchase-pmax` while payload declares `search_rsa`; payload is treated as the authoritative contract.
  - 這次是真實 LOVEFU 素材資源關聯報表 rerun，但 source export 不足以支撐 richer click / conversion / placement / duration layers。
  - 所有舊素材 decision_confidence 都只能是 directional，不能誤用成 high / medium / low 的表現結論。

## Dimension Scores

| Dimension | Score | Verdict | Rationale |
|---|---:|---|---|
| Asset Sufficiency | 5 | pass | headline / description 數量達到 RSA 常用水位，且 primary / test 兩個 bucket 都存在。 |
| Creative Diversity | 4 | warn | 目前覆蓋 9/10 個 angle，只有 2 組近義重複警示，整體多樣性可用但仍需控制相近變體。 |
| Product Specificity | 3 | warn | 共有 9/19 則素材明確提到山丘，仍有一批 generic LOVEFU / 飄雲語言稀釋 hillbed 焦點。 |
| Policy Risk | 3 | warn | 高風險醫療式語句已被 safer rewrite 移除，但目前仍有 4 則素材保留睡眠結果或舒壓效果語氣。 |
| Platform Fit | 4 | warn | RSA headline / description 已通過 char audit，且數量可上稿；但目前 artifact path 與 payload campaign_type 不一致，需先清掉流程漂移。 |

## Findings

| Severity | Category | Title | Evidence | Affected Assets | Blocking |
|---|---|---|---|---|---|
| high | product_drift | Generic LOVEFU / 飄雲 language still dilutes hillbed focus | 只有 9/19 則素材明確提到山丘或山丘樂眠床。<br>packager strategic notes 已將 brand_trust 列為 do_not_expand，代表 generic trust copy 已接近過量。 | hl-01, hl-02, hl-06, hl-07, hl-09, hl-11, cand-h05, desc-02 | no |
| medium | coverage_gap | Angle coverage still has an unfilled gap | gap angles: entry_value<br>packager warnings 已明示本輪 final pack 未承接 entry_value angle。 | - | no |
| medium | policy_risk | Policy-sensitive outcome language still needs manual QA | current medium-risk assets: hl-06, desc-02, cand-d02, cand-d01<br>safer rewrite watchlist 已證明此 lane 對結果承諾敏感，不能只因 schema pass 就放行。 | hl-06, desc-02, cand-d02, cand-d01 | no |
| medium | platform_fit | Artifact path and payload campaign_type are inconsistent | lane_context.lane_id=evergreen-purchase-pmax<br>payload campaign_type=search_rsa | - | no |

## Recommended Actions

- `P1` `copy_runner`: Replace 1-2 generic LOVEFU / 飄雲 lines with hillbed-specific support or pain-relief framing that stays policy-safe. Reason: 目前 generic 語言仍佔顯著比例，會稀釋 hillbed product focus。
- `P1` `human_reviewer`: Manually QA `hl-06` and `desc-02` for sleep-outcome wording before changing sign_off_status. Reason: 目前仍保留中度敏感的結果語氣，不能只依賴 safer rewrite watchlist 就放行。
- `P1` `pm`: Decide whether `entry_value` should be intentionally absent or explicitly reintroduced as a low-risk test angle. Reason: 目前 taxonomy gap 還在，會影響後續 builder / packager 的 coverage discipline。
- `P2` `copy_runner`: Resolve the path / payload campaign_type drift before promoting this audit handoff into a formal gate. Reason: 目前 artifact 被放在 pmax lane，但 payload 是 search_rsa，會讓 downstream review 誤判格式要求。

## Integration Handoff

### Packager Blockers

- none

### Upstream Constraints

- Introduce a hillbed-specificity floor or generic-brand ratio cap before final pack assembly.
- Carry accepted angle gaps as explicit metadata instead of leaving them as silent omissions.
- Promote policy watch terms from safer rewrite watchlist into a structured packager handoff field.

### Challenger Notes

- Packager already improved safer rewrite discipline; the remaining issue is product focus, not raw policy triage.
- Because this run is pack-only, fatigue conclusions should not be upgraded beyond directional.
- Use this audit as a preflight gate before PM / media buyer sign-off, not as a replacement for packager output.

## Limitations

- No live or export-backed delivery data was available for fatigue analysis.
- This sample still does not validate live serving behavior or real post-upload delivery splits.
- Artifact path uses lane `evergreen-purchase-pmax` while payload campaign_type is `search_rsa`.
- This sample audit is derived from the 2026-03-15 v1.2 UAT packager artifact only.
