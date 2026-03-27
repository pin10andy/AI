# ADR-002: Productization v1 範圍與策略

## Status

accepted

## Background

Phase 1 完成後，有多條已驗證的 lane 可選擇產品化：

| Lane | Campaign | Goal | Golden Brief | Score | Human Review |
|------|----------|------|-------------|-------|-------------|
| mattress | search_rsa | purchase | 無 | — | 可微調後上稿 |
| mattress | pmax | purchase | 無 | — | 可直接上稿 |
| neck-pillow | pmax | purchase | 無 | — | 可微調後上稿 |
| store-visit | pmax | store_visit | 無 | — | 可微調後上稿 |
| **hillbed** | **pmax** | **purchase** | **有** | **4.65/5** | **可直接上稿** |

需要決定三件事：
1. 先產品化哪條 lane
2. Human review 是否移除
3. 擴張順序策略

## Decision

1. **先產品化 hillbed purchase PMax**
   - 唯一同時具備 golden brief、formal validation、human review「可直接上稿」判定的 lane
   - 4.65/5 是目前最高分，且欄位分級報告已完成

2. **保留 human review 作為必要閘門**
   - policy_safety 仍需人工守邊界（如「托住腰背」等表述）
   - brief 的 A 級欄位（goal, hero_message, primary_cta 等）仍需人工拍板
   - 其他 3 份 PMax 輸出中有 2 份為「可微調後上稿」，品質尚未穩定到可免審

3. **擴張策略：先同產品擴 goal，再跨產品**
   - 下一條建議：hillbed × 試躺預約（store_visit goal）
   - 與目前 lane 僅差 goal，brief 的 B 級欄位可大量複用
   - 風險最低的擴張路徑，能驗證「同產品、不同 goal」的可行性

## Rationale

**替代方案 1：先跨產品（如 mattress purchase PMax）**
- 需要全新 golden brief，A 級欄位全部重寫
- 無法驗證 registry 的擴張隔離性是否足夠
- 風險較高

**替代方案 2：移除 human review 做全自動化**
- policy_safety 分數 4.0，尚有邊界模糊區
- 品牌風險語意（如醫療暗示）需持續人工監控
- 過早移除會增加上稿風險

**替代方案 3：多條 lane 同時產品化**
- 範圍過大，無法在兩週內完成
- 每條 lane 的 brief 品質不一，不宜混在同一 milestone

## Impact

- 影響的檔案：
  - 新建 `ai/registry/supported-matrix.yaml`
  - 新建 `ai/registry/canonical-briefs.yaml`
  - 新建 `ai/specs/lovefu-hillbed-pmax-writer-spec.md`
  - 新建 `ai/playbooks/lovefu-hillbed-pmax-runbook.md`
  - 新建 `ai/validation/regression-baseline-hillbed-pmax.yaml`
  - 不修改既有 schema / playbook / skill
- 影響的 agent：所有 agent 可查 registry 確認正式支援範圍
- 影響的流程：新增 registry 查詢步驟，runbook 取代口頭流程

## Related

- Task: `prod-001` / `ai/tasks/2026-03-14-productization-v1.yaml`
- Change: `ai/changes/2026-03-14-productization-v1.md`
