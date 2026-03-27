---
name: "creative-performance-interpreter"
description: "解讀 Google Ads 歷史素材成效，萃取高價值語言模式，使用 protected_phrase / must_include_token / reusable_motif 三分模型處理 legacy，並在 v1.2 新增 richer data-layer 判讀、observe 子類別、candidate pipeline automation、以及顯式 angle taxonomy handoff。不生成最終文案包。"
license: MIT
metadata:
  version: 1.2.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-15
---

# Creative Performance Interpreter v1.2

這是素材成效分析器，不是文案生成器。

v1.2 只修四件事：

1. 輸入資料層升級
2. observe 決策細化
3. candidate pipeline 自動化
4. angle taxonomy 標準化

## Required References

1. `ai/brand/master-brand.yaml`
2. `ai/inputs/creative-performance-input.schema.json`
3. `ai/schemas/creative-performance-output.schema.json`
4. `references/decision-rules.md`
5. `ai/evals/creative-performance-rubric.yaml`

## Required Input Highlights

- `performance_data.reporting_context.interpretation_layers` 必填
- `assets[*].angle_key` 必填
- `assets[*].active_duration_days` 必填
- `metrics` 支援 `impressions / clicks / ctr / asset_level_conversions / conversion_value / placement_breakout`
- `legacy_message_policy` 維持三分模型

## Execution Steps

### Step 1: Validate input

- schema pass
- `interpretation_layers` 完整
- `angle_key` 與 `active_duration_days` 不可缺
- `legacy_message_policy` 三類欄位結構正確

### Step 2: Grade data layers

- click layer 是否 ready
- conversion layer 是否 ready
- placement layer 是否 ready
- duration layer 是否 ready

### Step 3: Build asset-type cohorts

- 依 `asset_type` 分群
- 各 cohort 各算自己的 P25 / P50 / P75
- placement 可用時，保留 Search / Display 判讀備註

### Step 4: Select decision_basis

- impression / click / ctr 缺失 -> `association_proxy_only`
- conversion ready -> `conversion_rate_asset_type_percentile` 或 `hybrid_asset_type_percentile`
- 只有 click ready -> `ctr_asset_type_percentile`

### Step 5: Apply legacy + angle model

- `protected_phrase` 保 coverage
- `must_include_token` 保 token visibility，不保單一 asset
- `reusable_motif` 做 candidate guidance
- `angle_key` 原樣往下游傳遞

### Step 6: Decide v1.2 decision buckets

允許的 decision：

- `retain`
- `retire`
- `retire_candidate`
- `reinforce`
- `observe_new`
- `observe_insufficient_data`
- `observe_stale`
- `observe_borderline`

### Step 7: Emit downstream-ready output

必須完整輸出：

- `asset_type_percentiles`
- `data_sufficiency`
- `asset_decisions[*].angle_key / active_duration_days / observe_reason`
- `retire_now_assets[*].coverage_gap_created`
- `new_candidate_assets[*].risk_level / rewrite_mode / safer_rewrite_of`
- `next_round_brief_additions.candidate_pipeline_triggers`

## Quality Gates

- 不可在缺 click layer 資料時假裝高信心
- 缺 asset-level conversion 時，不可給 `high` confidence
- observe 不可再只輸出單一 `observe`
- `angle_key` 不可丟給下游 heuristic 補
- 每個 retire gap 至少要嘗試補 replacement candidate
- 高效但高風險語言必須有 safer-rewrite candidate

## Sample Run: LOVEFU / 山丘樂眠床 v1.2 Rerun

Source sample: `ai/inputs/lovefu-pmax-hillbed-performance.json`

### Sample Input Excerpt

```json
{
  "interpretation_id": "hillbed-pmax-2026q1-rerun-v1-2",
  "product_name": "山丘樂眠床",
  "campaign_type": "pmax",
  "performance_data": {
    "reporting_context": {
      "asset_granularity": "asset_level",
      "includes_asset_level_conversion": true,
      "includes_asset_level_conversion_value": true,
      "includes_placement_breakout": true,
      "interpretation_layers": {
        "click_layer": { "status": "ready" },
        "conversion_layer": { "status": "ready" },
        "placement_layer": { "status": "ready" },
        "duration_layer": { "status": "ready" }
      }
    }
  }
}
```

### Sample Decision Excerpt

```json
[
  {
    "asset_id": "sh-15",
    "text": "山丘樂眠床 立即選購",
    "asset_type": "short_headline",
    "angle_key": "legacy_phrase",
    "decision": "retire",
    "decision_rationale": "在 short_headline cohort 中，CTR 2.5% 與 4 筆 asset-level conversions 都落在 cohort 底部，且此句只承擔 must_include token，不是 protected phrase carrier，可退場並由 replacement candidate 補位。",
    "decision_basis": {
      "primary_metric": "hybrid_asset_type_percentile",
      "asset_type_cohort": "short_headline",
      "placement_scope": "overall",
      "eligible_asset_count": 8,
      "cohort_percentiles": { "p25": 0.041, "p50": 0.067, "p75": 0.073 },
      "data_layers_used": [
        "click_layer",
        "conversion_layer",
        "placement_layer",
        "duration_layer"
      ],
      "supporting_metrics_available": [
        "impressions",
        "clicks",
        "ctr",
        "asset_level_conversions",
        "conversion_value"
      ],
      "placement_breakout_available": true
    },
    "decision_confidence": "high",
    "performance_tier": "low",
    "active_duration_days": 49,
    "observe_reason": null,
    "staleness_flag": false
  },
  {
    "asset_id": "sh-14",
    "text": "第2張床 從山丘開始",
    "asset_type": "short_headline",
    "angle_key": "life_scene",
    "decision": "observe_new",
    "decision_rationale": "素材上線僅 7 天，雖然 CTR 4.5% 不差，但資料仍偏薄，先保留觀察，不直接進退。",
    "decision_basis": {
      "primary_metric": "ctr_asset_type_percentile",
      "asset_type_cohort": "short_headline",
      "placement_scope": "overall",
      "eligible_asset_count": 8,
      "cohort_percentiles": { "p25": 0.041, "p50": 0.067, "p75": 0.073 },
      "data_layers_used": ["click_layer", "conversion_layer", "duration_layer"],
      "supporting_metrics_available": [
        "impressions",
        "clicks",
        "ctr",
        "asset_level_conversions"
      ],
      "placement_breakout_available": true
    },
    "decision_confidence": "low",
    "performance_tier": "borderline",
    "active_duration_days": 7,
    "observe_reason": "newly_active_under_observation_window",
    "staleness_flag": false
  }
]
```

### Sample Output Excerpt

```json
{
  "data_sufficiency": {
    "overall_verdict": "sufficient",
    "click_layer_verdict": "ready",
    "conversion_layer_verdict": "ready",
    "placement_layer_verdict": "ready",
    "duration_layer_verdict": "ready",
    "total_impressions": 117300,
    "total_clicks": 6524,
    "total_asset_level_conversions": 352
  },
  "retire_now_assets": [
    {
      "asset_id": "sh-15",
      "asset_text": "山丘樂眠床 立即選購",
      "asset_type": "short_headline",
      "angle_key": "legacy_phrase",
      "reason": "hybrid basis 顯示此句在 short_headline cohort 低於 P25，且 token coverage 可由 replacement 補回",
      "decision_confidence": "high",
      "decision_basis_ref": "sh-15",
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
      "intent": "補回產品名與 CTA token，同時把直接催促改成低壓 CTA",
      "related_gap": "sh-15 retire 後的 must_include token gap",
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
      "intent": "保留 pain-point angle 的吸引力，但移除過度醫療化暗示",
      "related_gap": "高效痛點語言需要 safer rewrite",
      "suggested_role": "測試",
      "covers_tokens": ["山丘樂眠床"],
      "inherits_motifs": ["steady-support"],
      "risk_level": "medium",
      "rewrite_mode": "safer-rewrite",
      "safer_rewrite_of": "lh-05",
      "source_asset_ids": ["lh-05", "sh-16"]
    }
  ],
  "next_round_brief_additions": {
    "proven_angles": [
      {
        "key": "product_feel",
        "label": "支撐與放鬆感",
        "evidence": "short_headline / description 在 click 與 conversion 都穩定高於 cohort 中位數"
      },
      {
        "key": "risk_reversal",
        "label": "安心試睡與保固",
        "evidence": "100天安心睡相關資產在多 placement 都有穩定轉換"
      }
    ],
    "candidate_pipeline_triggers": [
      {
        "gap_id": "replace-sh-15-legacy-phrase",
        "angle_key": "cta_lower_friction",
        "rewrite_mode": "retain-intent",
        "priority": "high"
      },
      {
        "gap_id": "safer-rewrite-pain-point",
        "angle_key": "pain_point",
        "rewrite_mode": "safer-rewrite",
        "priority": "high"
      }
    ]
  }
}
```

---

## Artifact Governance

本技能是 pipeline 階段技能，產出為正式 pipeline artifact。

### 輸出路徑

```
ai/outputs/google-ads/{brand}/{product}/{lane}/pipeline/{task_id}/interpreter.json
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
