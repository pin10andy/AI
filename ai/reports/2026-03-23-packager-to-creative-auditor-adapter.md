# Packager to Creative Auditor Adapter Integration

- generated_by: codex
- generated_at: 2026-03-23
- scope: upload-packager v1.2 handoff into creative-auditor sidecar

## 1. Executive Summary

`creative-auditor` 已從獨立 contract 推進到 **可接現有 workflow 的 adapter**。

目前新增的 bridge 是：

- script: `scripts/google_ads_packager_to_creative_audit.py`
- upstream source: `upload-packager` v1.2 output
- downstream target: `google-ads-creative-audit-input.schema.json`

這代表 workflow 可以正式收斂成：

`packager -> adapter -> creative-auditor -> PM / media buyer sign-off`

而不是讓 PM / 投手自己手動重組 packager output 再做人腦審查。

## 2. Workflow Placement

### Before

1. `upload-packager` 產出 final pack
2. PM / 投手直接閱讀 packager markdown / json
3. creative health、產品聚焦、risk watch、coverage gap 仍靠人工抽讀

### After

1. `upload-packager` 產出 final pack
2. `scripts/google_ads_packager_to_creative_audit.py` 將 packager output 正規化成 audit input
3. `creative-auditor` 產生 preflight audit
4. PM / 投手根據 `upload_decision`、`findings`、`recommended_actions` 決定：
   - 可送審
   - 要退回
   - 哪些問題只是 watch

## 3. Field Mapping

| Packager Output Field | Audit Input Field | Mapping Rule |
|---|---|---|
| `package_id` | `audit_id` | 加上 `-creative-audit` suffix |
| `brand_name` | `brand_name` | direct |
| `product_name` | `product_name` | direct |
| `campaign_type` | `campaign_type` | direct，payload 為權威值 |
| `delivery_metadata.sign_off_status` | `delivery_context.sign_off_status` | direct |
| `compliance_notes.manual_review_required` | `delivery_context.manual_review_required` | direct |
| `upload_ready_assets.primary_pack` | `creative_inventory.primary_assets` | flatten + infer `asset_type` |
| `upload_ready_assets.test_pack` | `creative_inventory.test_assets` | flatten + infer `asset_type` |
| `character_audit.results[*].asset_type` | `creative_inventory.*[].asset_type` | 若 upload asset 未明示型別，回補 asset type |
| `coverage_tags.must_include_tokens` | `coverage_context.required_tokens` | aggregate + dedupe |
| `coverage_tags.protected_phrases` | `coverage_context.protected_phrases` | aggregate + dedupe |
| `angle_taxonomy.keys` + `strategic_notes.*` | `coverage_context.angle_status` | 依 main/test/do-not-expand 與實際 count 推導 status |
| `redundancy_warnings` | `history_signals.asset_reuse_clusters` | 轉成 reuse cluster evidence |
| `strategic_notes.safer_rewrite_watchlist` | `compliance_context.policy_watch_terms` / `must_avoid` | 轉成 policy watch evidence |
| artifact path | `lane_context` | 推導 `lane_id / message_scope / goal` |

## 4. Important Adapter Rules

### 4.1 Payload over path

adapter 把 **payload `campaign_type` 視為權威值**。  
原因是 sample source artifact 已經出現：

- storage lane: `evergreen-purchase-pmax`
- payload `campaign_type`: `search_rsa`

若不明訂這條規則，downstream review 很容易用錯平台標準。

### 4.2 No hidden audit conclusions

adapter 只做：

- flatten
- normalize
- weak-data labeling
- metadata carry-over

adapter 不做：

- 高信心 fatigue 結論
- health score
- blocking upload decision
- 覆寫 packager 主決策

### 4.3 Character audit as type recovery, not performance evidence

`character_audit.results` 的用途是回補：

- `asset_type`
- `char_count`

它不是 performance evidence，也不能被升格成 creative-quality proof。

## 5. Workflow Value

### PM

- 直接看到 `needs_manual_review / blocked_for_upload / clear_to_review`
- 不必自己從 packager JSON 裡猜 coverage gap 與 drift
- 可以明確分辨「可送審」和「應退回 builder / packager」

### Media Buyer

- 有一份明確的 preflight gate，而不是靠經驗看素材包
- 可直接接手 `recommended_actions`
- path / payload drift 這類 operational issue 會先被攔下，不會拖到上稿時才發現

### Development

- handoff contract 從「口頭流程」變成 script + schema
- 後續要接 MCP / export adapter 時，有一致的 audit ingress format
- 可以把 sidecar review 獨立演進，不污染 interpreter / builder / packager 主鏈

## 6. Sample Run Outcome

sample source artifact:

- `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-2-uat/packager.json`

sample report:

- `ai/reports/2026-03-23-lovefu-hillbed-packager-preflight-audit.md`

這次 sample preflight 的核心結論是：

- `upload_decision = needs_manual_review`
- final pack 已有可審核規模，但仍存在：
  - generic LOVEFU / 飄雲語言稀釋 hillbed focus
  - `entry_value` angle gap
  - medium-risk sleep outcome wording
  - artifact path / payload `campaign_type` drift

## 7. Risks and Limits

- 目前 source evidence 仍是 `pack_only`，fatigue 與 live serving 只能低信心判讀。
- adapter 目前只支援 `upload-packager` output，不支援 export snapshot / MCP snapshot。
- sample source artifact 本身有 path/payload drift，這次報告刻意保留並揭露，不做靜默修飾。

## 8. Recommended Next Step

最有槓桿的下一步是：

1. 把 `creative-auditor` sample run 納入正式驗證鏈。
2. 補 `export snapshot -> creative-audit input` adapter，讓 fatigue / platform-fit 不再停留在 `pack_only`。
3. 若 sidecar 連續幾輪都穩定，再決定要不要把 `creative-audit` 納入正式 pipeline stage 與 registry。
