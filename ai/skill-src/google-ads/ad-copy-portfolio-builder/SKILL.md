---
name: "ad-copy-portfolio-builder"
description: "消費 Creative Performance Interpreter 的輸出，將 retain / retire / observe / candidate / brief 建議整合成下一輪可直接上稿的素材池。v1.2 聚焦 observe 分流、candidate automation、angle taxonomy coverage，並維持 field-level handoff validation。"
license: MIT
metadata:
  version: 1.2.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-15
---

# Ad Copy Portfolio Builder v1.2

這是組裝器，不是生成器。

v1.2 只修四件事：

1. 接住 richer data / observe / candidate handoff
2. 不再把 observe 整桶留在主力池
3. 真的用 candidate pipeline 補 retire gap 與 safer rewrite
4. 以 taxonomy 為核心收斂 coverage

## Required References

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/ad-copy-portfolio-input.schema.json`
3. `ai/schemas/ad-copy-portfolio-output.schema.json`
4. `references/decision-rules.md`
5. `ai/evals/ad-copy-portfolio-rubric.yaml`
6. `ai/schemas/creative-performance-output.schema.json`

## Execution Steps

### Step 1: Validate interpretation_output field by field

不能只驗 `interpretation_output` object 存在。

必查：

- `angle_taxonomy`
- `asset_decisions[*].angle_key`
- `asset_decisions[*].decision`
- `asset_decisions[*].observe_reason`
- `asset_decisions[*].active_duration_days`
- `retire_now_assets[*].coverage_gap_created`
- `new_candidate_assets[*].risk_level / rewrite_mode / safer_rewrite_of`
- `candidate_pipeline_triggers`

### Step 2: Build base pack

- retain / reinforce -> primary
- observe_new -> 可暫留
- observe_borderline -> 優先進 test
- observe_stale / retire_candidate -> 不預設留主力

### Step 3: Process retirements

- retire 一定進 `replacement_map`
- 若 retire 造成 token / phrase gap，replacement 邏輯必須明示
- 若沒有候選，必須標 `replacement_gap_unfilled`

### Step 4: Select candidates

候選不只看容量與冗餘，也要看：

- 是否補回 protected phrase / must_include token
- 是否承接 reinforce angle
- 是否屬 safer rewrite
- 是否真的讓素材池更接近上稿規模

### Step 5: Emit taxonomy coverage

`coverage_check` 必須輸出：

- `angle_coverage`
- `protected_phrase_check`
- `token_coverage_check`
- `motif_coverage_check`

### Step 6: Mark contract ready

`compliance_notes.field_level_contract_passed = true` 的前提：

- 所有必欄存在
- final pack 每則素材都有 `angle_key`
- final pack 每則素材都有 `decision_confidence`
- final pack 每則素材都有 `coverage_tags`

## Quality Gates

- 不可把所有 observe 留在 primary
- 不可遺失 `angle_key`
- 不可遺失 `risk_level` / `rewrite_mode`
- `replacement_map` 必須保留 `replacement_gap_unfilled`
- `coverage_check` 必須能指出過度保留與補位不足的角度
- final pack 要接近真實上稿規模

## Sample Run: LOVEFU / 山丘樂眠床 v1.2 Rerun

### Sample Input Excerpt

```json
{
  "portfolio_id": "hillbed-pmax-2026q1-portfolio-v1-2",
  "product_name": "山丘樂眠床",
  "campaign_type": "pmax",
  "interpretation_output": {
    "interpretation_id": "hillbed-pmax-2026q1-rerun-v1-2",
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
    "retire_now_assets": [
      {
        "asset_id": "sh-15",
        "asset_text": "山丘樂眠床 立即選購",
        "asset_type": "short_headline",
        "angle_key": "legacy_phrase",
        "decision_confidence": "high",
        "coverage_gap_created": [
          "must_include_token:山丘樂眠床",
          "must_include_token:立即選購",
          "angle:legacy_phrase"
        ],
        "replaced_by_candidate_id": "cand-07"
      }
    ],
    "new_candidate_assets": [
      {
        "candidate_id": "cand-07",
        "asset_text": "山丘樂眠床 立即選購前先安心試睡",
        "asset_type": "short_headline",
        "source": "replace_retired_asset",
        "angle_key": "cta_lower_friction",
        "intent": "補回 token coverage 並降低 CTA 壓力",
        "related_gap": "sh-15 retire gap",
        "suggested_role": "測試",
        "covers_tokens": ["山丘樂眠床", "立即選購"],
        "inherits_motifs": ["lower-friction-cta"],
        "risk_level": "low",
        "rewrite_mode": "retain-intent"
      },
      {
        "candidate_id": "cand-12",
        "asset_text": "睡姿壓力少一點，也想被山丘穩穩接住一整晚",
        "asset_type": "long_headline",
        "source": "safer_rewrite",
        "angle_key": "pain_point",
        "intent": "保留痛點吸引力，但降風險",
        "related_gap": "safer rewrite for pain-point winners",
        "suggested_role": "測試",
        "covers_tokens": ["山丘樂眠床"],
        "inherits_motifs": ["steady-support"],
        "risk_level": "medium",
        "rewrite_mode": "safer-rewrite",
        "safer_rewrite_of": "lh-05"
      }
    ]
  },
  "brief_constraints": {
    "character_policy": {
      "short_headline_count": 5,
      "short_headline_max": 30,
      "long_headline_count": 5,
      "long_headline_max": 90,
      "description_count": 5,
      "description_max": 90
    },
    "protected_phrases": ["100天安心睡"],
    "must_include_tokens": ["山丘樂眠床", "立即選購"],
    "must_avoid": ["最低價", "保證治好腰痛"],
    "forbidden_claims": ["保證治好腰痛", "醫療級治療效果"]
  }
}
```

### Sample Output Excerpt

```json
{
  "final_asset_pack": {
    "primary": [
      {
        "asset_id": "sh-01",
        "text": "床墊推薦 先接住身體再放鬆",
        "asset_type": "short_headline",
        "role": "主力",
        "source": "retained",
        "angle_key": "product_feel",
        "performance_tier": "top",
        "decision_confidence": "high",
        "decision_basis_metric": "hybrid_asset_type_percentile",
        "observe_subtype": null,
        "risk_level": null,
        "rewrite_mode": null,
        "is_protected_phrase_carrier": false,
        "char_count": 13,
        "coverage_tags": {
          "protected_phrases": [],
          "must_include_tokens": [],
          "reusable_motifs": ["steady-support"]
        }
      },
      {
        "asset_id": "sh-07",
        "text": "100天安心睡 不怕選錯",
        "asset_type": "short_headline",
        "role": "主力",
        "source": "retained_protected_phrase",
        "angle_key": "risk_reversal",
        "performance_tier": "top",
        "decision_confidence": "high",
        "decision_basis_metric": "hybrid_asset_type_percentile",
        "observe_subtype": null,
        "risk_level": null,
        "rewrite_mode": null,
        "is_protected_phrase_carrier": true,
        "char_count": 12,
        "coverage_tags": {
          "protected_phrases": ["100天安心睡"],
          "must_include_tokens": [],
          "reusable_motifs": []
        }
      }
    ],
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
        "is_protected_phrase_carrier": false,
        "char_count": 16,
        "coverage_tags": {
          "protected_phrases": [],
          "must_include_tokens": ["山丘樂眠床", "立即選購"],
          "reusable_motifs": ["lower-friction-cta"]
        },
        "status_note": "補回 sh-15 retire 後的 token coverage"
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
        "is_protected_phrase_carrier": false,
        "char_count": 24,
        "coverage_tags": {
          "protected_phrases": [],
          "must_include_tokens": ["山丘樂眠床"],
          "reusable_motifs": ["steady-support"]
        },
        "status_note": "safer rewrite for lh-05 high-performing risky copy"
      }
    ]
  },
  "replacement_map": [
    {
      "retired_asset_id": "sh-15",
      "retired_text": "山丘樂眠床 立即選購",
      "retired_asset_type": "short_headline",
      "retirement_reason": "hybrid basis 顯示 CTR 與 asset-level conversions 都在 short_headline cohort 底部",
      "action": "replaced",
      "replacement_gap_unfilled": false,
      "replacement_asset_id": "cand-07",
      "replacement_text": "山丘樂眠床 立即選購前先安心試睡",
      "replacement_rationale": "保留產品名與 CTA coverage，但以低壓 CTA 句型替換硬推進站語言",
      "replacement_decision_confidence": "medium",
      "rewrite_mode": "retain-intent",
      "coverage_after_replacement": [
        "must_include_token:山丘樂眠床",
        "must_include_token:立即選購",
        "angle:cta_lower_friction"
      ]
    }
  ],
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
        "angle_key": "risk_reversal",
        "label": "安心試睡與保固",
        "primary_count": 4,
        "test_count": 0,
        "total": 4,
        "status": "core",
        "redundancy_status": "balanced"
      },
      {
        "angle_key": "cta_lower_friction",
        "label": "低壓 CTA",
        "primary_count": 1,
        "test_count": 1,
        "total": 2,
        "status": "supporting",
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
      }
    ]
  },
  "observe_assets_status": [
    {
      "asset_id": "sh-14",
      "text": "第2張床 從山丘開始",
      "observe_subtype": "observe_new",
      "active_duration_days": 7,
      "disposition": "keep_observing",
      "rationale": "新上線且前期訊號不差，保留回看窗口，但不擴大主力比例"
    }
  ],
  "portfolio_summary": {
    "total_primary": 12,
    "total_test": 4,
    "total_final": 16,
    "retained_from_previous": 11,
    "newly_added": 5,
    "retired_count": 3,
    "rejected_candidates_count": 1,
    "test_ratio": 0.25,
    "observe_count": 2,
    "observe_breakdown": {
      "observe_new": 1,
      "observe_insufficient_data": 0,
      "observe_stale": 0,
      "observe_borderline": 1
    },
    "replacement_gap_unfilled_count": 0
  },
  "compliance_notes": {
    "data_caveats": [],
    "manual_review_required": true,
    "upstream_confidence": "high",
    "field_level_contract_passed": true,
    "angle_taxonomy_aligned": true,
    "candidate_pipeline_complete": true
  }
}
```

---

## Artifact Governance

本技能是 pipeline 階段技能，產出為正式 pipeline artifact。

### 輸出路徑

```
ai/outputs/google-ads/{brand}/{product}/{lane}/pipeline/{task_id}/
├── builder.json       (前一階段輸入)
├── interpreter.json   (前一階段輸入)
├── packager.json      (下一階段輸出，非本技能)
└── portfolio.json     (本技能輸出)
```

**禁止**將輸出寫入 repo 根目錄或 `ai/outputs/` 根層。
暫存/測試輸出寫入 `scratch/google-ads/`。

### 寫入後必須

1. 在 `ai/registry/artifacts.yaml` 登記 pipeline artifact（含所有必填欄位）
2. 執行 `python3 scripts/check_artifact_governance.py` 確認合規

### 政策參考

- `ai/registry/storage-map.yaml`
- `ai/policies/artifact-naming-policy.md`
- `ai/policies/artifact-write-policy.md`
