---
name: "upload-packager"
description: "消費 Ad Copy Portfolio Builder 的輸出，整理成可直接上稿、可交付 PM / 投手 / 客戶的素材包。v1.2 新增 taxonomy strategic notes、safer-rewrite watchlist，並擴充 field-level handoff validation。"
license: MIT
metadata:
  version: 1.2.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-15
---

# Upload Packager v1.2

這不是分析器，也不是生成器，更不是決策者。它仍然負責打包，但 v1.2 要多做兩件事：

- 驗證 builder output 的 angle-taxonomy contract
- 直接把 taxonomy coverage 轉成可執行的 strategic notes

## Required References

1. `ai/inputs/upload-packager-input.schema.json`
2. `ai/schemas/upload-packager-output.schema.json`
3. `references/decision-rules.md`
4. `ai/evals/upload-packager-rubric.yaml`

## Execution Steps

### Step 1: Validate portfolio_output field by field

不能只看 `portfolio_output` object 存在。

必查：

- `angle_taxonomy`
- `final_asset_pack[*].angle_key`
- `final_asset_pack[*].decision_confidence`
- `final_asset_pack[*].rewrite_mode`
- `replacement_map[*].replacement_gap_unfilled`
- `coverage_check.angle_coverage[*].status / redundancy_status`
- `portfolio_summary.observe_breakdown`
- `compliance_notes.field_level_contract_passed`

### Step 2: Move assets without changing text

將 primary / test 分到 upload packs，逐字搬運。

### Step 3: Recalculate char_count

重新計算字數，不信任上游 char_count。

### Step 4: Emit strategic_notes

根據 taxonomy 輸出：

- `main_angles`
- `test_angles`
- `do_not_expand_angles`
- `safer_rewrite_watchlist`

### Step 5: Emit handoff_validation

若欄位全數完整：

- `handoff_validation.portfolio_field_validation_passed = true`

### Step 6: Build action checklist

除原有步驟外，新增：

- 回看 `observe_new`
- 檢查 safer rewrite 候選
- 檢查 token / protected phrase coverage

### Step 7: Optional creative-auditor handoff

若使用者要求 preflight review / challenger audit：

- 先完成 packager output
- 再用 `python3 scripts/google_ads_packager_to_creative_audit.py {packager.json} --mode audit-input`
- 將正規化結果交給 `creative-auditor`

這一步是 downstream sidecar，不可反向覆寫 packager 的主決策。

## Quality Gates

- 不可只做 object-level validation
- 不可遺失 `angle_key`
- 不可遺失 `rewrite_mode` / `risk_level`
- 不可遺失 `replacement_gap_unfilled`
- 不可省略 taxonomy strategic notes
- `sign_off_status` 必須受 handoff validation 與 char audit 約束

## Sample Run: LOVEFU / 山丘樂眠床 v1.2 Rerun

### Sample Input Excerpt

```json
{
  "package_id": "hillbed-pmax-2026q1-upload-v1-2",
  "product_name": "山丘樂眠床",
  "campaign_type": "pmax",
  "portfolio_output": {
    "portfolio_id": "hillbed-pmax-2026q1-portfolio-v1-2",
    "source_interpretation_id": "hillbed-pmax-2026q1-rerun-v1-2",
    "angle_taxonomy": {
      "version": "v1.2",
      "keys": [
        "product_feel",
        "risk_reversal",
        "brand_trust",
        "entry_value",
        "life_scene",
        "concrete_number",
        "pain_point",
        "social_proof",
        "legacy_phrase",
        "cta_lower_friction"
      ]
    },
    "final_asset_pack": {
      "test": [
        {
          "asset_id": "cand-07",
          "text": "山丘樂眠床 立即選購前先安心試睡",
          "asset_type": "short_headline",
          "role": "測試",
          "source": "replacement",
          "angle_key": "cta_lower_friction",
          "performance_tier": "new",
          "decision_confidence": "medium",
          "decision_basis_metric": null,
          "observe_subtype": null,
          "risk_level": "low",
          "rewrite_mode": "retain-intent",
          "char_count": 16,
          "coverage_tags": {
            "protected_phrases": [],
            "must_include_tokens": ["山丘樂眠床", "立即選購"],
            "reusable_motifs": ["lower-friction-cta"]
          }
        },
        {
          "asset_id": "cand-12",
          "text": "睡姿壓力少一點，也想被山丘穩穩接住一整晚",
          "asset_type": "long_headline",
          "role": "測試",
          "source": "safer_rewrite",
          "angle_key": "pain_point",
          "performance_tier": "new",
          "decision_confidence": "medium",
          "decision_basis_metric": null,
          "observe_subtype": null,
          "risk_level": "medium",
          "rewrite_mode": "safer-rewrite",
          "char_count": 24,
          "coverage_tags": {
            "protected_phrases": [],
            "must_include_tokens": ["山丘樂眠床"],
            "reusable_motifs": ["steady-support"]
          }
        }
      ]
    },
    "coverage_check": {
      "taxonomy_version": "v1.2",
      "angle_coverage": [
        {
          "angle_key": "product_feel",
          "label": "支撐與放鬆感",
          "primary_count": 4,
          "test_count": 0,
          "total": 4,
          "status": "core",
          "redundancy_status": "balanced"
        },
        {
          "angle_key": "pain_point",
          "label": "痛點切入",
          "primary_count": 0,
          "test_count": 1,
          "total": 1,
          "status": "test_only",
          "redundancy_status": "watch"
        },
        {
          "angle_key": "legacy_phrase",
          "label": "legacy coverage only",
          "primary_count": 1,
          "test_count": 0,
          "total": 1,
          "status": "thin",
          "redundancy_status": "watch"
        }
      ]
    },
    "portfolio_summary": {
      "total_primary": 12,
      "total_test": 4,
      "total_final": 16,
      "observe_breakdown": {
        "observe_new": 1,
        "observe_insufficient_data": 0,
        "observe_stale": 0,
        "observe_borderline": 1
      },
      "replacement_gap_unfilled_count": 0
    },
    "compliance_notes": {
      "upstream_confidence": "high",
      "field_level_contract_passed": true,
      "angle_taxonomy_aligned": true
    }
  },
  "character_policy": {
    "short_headline_count": 5,
    "short_headline_max": 30,
    "long_headline_count": 5,
    "long_headline_max": 90,
    "description_count": 5,
    "description_max": 90
  },
  "delivery_config": {
    "delivery_target": "media_buyer",
    "version_label": "Q1-2026-refresh-v1-2"
  }
}
```

### Sample Output Excerpt

```json
{
  "delivery_metadata": {
    "delivery_target": "media_buyer",
    "version_label": "Q1-2026-refresh-v1-2",
    "source_interpretation_id": "hillbed-pmax-2026q1-rerun-v1-2",
    "upstream_confidence": "high",
    "angle_taxonomy_version": "v1.2",
    "sign_off_status": "pending_review"
  },
  "handoff_validation": {
    "portfolio_field_validation_passed": true,
    "validated_sections": [
      "angle_taxonomy",
      "final_asset_pack",
      "replacement_map",
      "coverage_check",
      "portfolio_summary",
      "compliance_notes"
    ]
  },
  "strategic_notes": {
    "main_angles": [
      {
        "angle_key": "product_feel",
        "label": "支撐與放鬆感",
        "evidence": "主力池內多個 short headline / description 同時穩定高信心"
      },
      {
        "angle_key": "risk_reversal",
        "label": "安心試睡與保固",
        "evidence": "100天安心睡相關素材維持 protected phrase coverage 且轉換穩定"
      }
    ],
    "test_angles": [
      {
        "angle_key": "cta_lower_friction",
        "label": "低壓 CTA",
        "evidence": "本輪用來補回 sh-15 retire 後的 CTA token gap"
      },
      {
        "angle_key": "pain_point",
        "label": "痛點切入",
        "evidence": "僅保留 safer rewrite 版本作測試，不直接擴寫舊高風險句"
      }
    ],
    "do_not_expand_angles": [
      {
        "angle_key": "legacy_phrase",
        "label": "Legacy coverage only",
        "evidence": "此角度目前僅作 token / phrase coverage，不是擴量主軸",
        "recommendation": "維持最低 coverage 即可，不再新增同型硬 CTA 句"
      }
    ],
    "safer_rewrite_watchlist": [
      {
        "source_asset_id": "lh-05",
        "source_text": "腰痠背痛的夜晚，也能被山丘穩穩接住一整晚",
        "reason": "歷史成效好，但含過強醫療暗示",
        "recommended_candidate_id": "cand-12",
        "recommended_text": "睡姿壓力少一點，也想被山丘穩穩接住一整晚"
      }
    ]
  },
  "upload_ready_assets": {
    "test_pack": {
      "short_headlines": [
        {
          "asset_id": "cand-07",
          "text": "山丘樂眠床 立即選購前先安心試睡",
          "char_count": 16,
          "char_pass": true,
          "source": "replacement",
          "angle_key": "cta_lower_friction",
          "performance_tier": "new",
          "decision_confidence": "medium",
          "observe_subtype": null,
          "risk_level": "low",
          "rewrite_mode": "retain-intent",
          "coverage_tags": {
            "protected_phrases": [],
            "must_include_tokens": ["山丘樂眠床", "立即選購"],
            "reusable_motifs": ["lower-friction-cta"]
          }
        }
      ],
      "long_headlines": [
        {
          "asset_id": "cand-12",
          "text": "睡姿壓力少一點，也想被山丘穩穩接住一整晚",
          "char_count": 24,
          "char_pass": true,
          "source": "safer_rewrite",
          "angle_key": "pain_point",
          "performance_tier": "new",
          "decision_confidence": "medium",
          "observe_subtype": null,
          "risk_level": "medium",
          "rewrite_mode": "safer-rewrite",
          "coverage_tags": {
            "protected_phrases": [],
            "must_include_tokens": ["山丘樂眠床"],
            "reusable_motifs": ["steady-support"]
          }
        }
      ]
    }
  },
  "action_checklist": [
    {
      "step": 1,
      "action": "確認 CTA 補位",
      "detail": "確認 cand-07 作為 sh-15 replacement 時，產品名與立即選購 token coverage 都成立",
      "done": false
    },
    {
      "step": 2,
      "action": "審高風險改寫",
      "detail": "人工確認 cand-12 是否已降風險，同時保留 pain-point intent",
      "done": false
    },
    {
      "step": 3,
      "action": "安排 observe 回看",
      "detail": "對 sh-14 設定 7-10 天後回看，避免 observe_new 長期佔位",
      "done": false
    }
  ],
  "compliance_notes": {
    "inherited_caveats": [],
    "packager_warnings": [],
    "manual_review_required": true
  }
}
```

---

## Artifact Governance

本技能是 pipeline 最終階段，產出為正式 pipeline artifact 與交付物。

### 輸出路徑

| 類型 | 路徑 |
|------|------|
| Pipeline stage | `ai/outputs/google-ads/{brand}/{product}/{lane}/pipeline/{task_id}/packager.json` |
| Pipeline report | `ai/outputs/google-ads/{brand}/{product}/{lane}/pipeline/{task_id}/packager.md` |
| Deliverable | `ai/outputs/google-ads/{brand}/{product}/{lane}/deliverables/{task_id}.deliverable.{xlsx\|csv}` |

**禁止**將輸出寫入 repo 根目錄或 `ai/outputs/` 根層。
暫存/測試輸出寫入 `scratch/google-ads/`。

### 寫入後必須

1. 在 `ai/registry/artifacts.yaml` 登記（含所有必填欄位）
2. 執行 `python3 scripts/check_artifact_governance.py` 確認合規

### 政策參考

- `ai/registry/storage-map.yaml`
- `ai/policies/artifact-naming-policy.md`
- `ai/policies/artifact-write-policy.md`
