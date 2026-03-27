# Hillbed Tryout Booking PMax — Candidate Lane Spec

## Status

draft candidate only

此 lane 尚未納入 `ai/registry/supported-matrix.yaml`，
也尚未被視為正式 supported capability。

## Goal

定義 `hillbed × tryout booking` 這條候選 lane 的初始範圍與驗證需求，
讓後續驗證時不會污染既有的 purchase production lane。

## Background

- 既有 production lane：`hillbed-purchase-pmax`
- 擴張策略依據：`ai/decisions/ADR-002-productization-v1-scope.md`
- 本 lane 是同產品、不同 goal 的第一條候選擴張線

## Proposed Scope

- 產品：山丘樂眠床
- Campaign type：PMax
- Goal：`store_visit`（用來承載 tryout booking 導向）
- 素材類型：文字素材
- 狀態：draft / validation pending

## Out of Scope

- 不加入 `supported-matrix`
- 不建立 canonical brief
- 不產出正式 golden output
- 不擴到其他產品
- 不移除 human review

## Input Contract

| 項目 | 路徑 |
|------|------|
| Draft brief | `ai/inputs/briefs/lovefu-pmax-hillbed-tryout-booking-draft.json` |
| Brief schema | `ai/inputs/google-ads-brief.schema.json` |
| Output schema | `ai/schemas/google-ads-pmax-output.schema.json` |
| Parent brief | `ai/inputs/briefs/lovefu-pmax-hillbed.json` |

## How This Lane Differs From Purchase PMax

| 面向 | 現行 production lane | Tryout booking candidate lane |
|------|----------------------|-------------------------------|
| Goal | `purchase` | `store_visit` |
| Primary CTA | `立即選購` | `預約門市試躺` |
| Conversion intent | 直接購買 | 先預約體驗，再決定是否購買 |
| Keyword intent | 床墊推薦 / 獨立筒床墊 / 支撐床墊 | 床墊試躺 / 門市試躺 / 預約試躺 |
| Message center | 支撐品質 + 購買信任 + 入門價值 | 試躺體驗 + 顧問陪伴 + 預約下一步 |
| Price signal | 可在 smart-start 角度保留 `14,900起` | 不是主角，原則上不作為主要轉換誘因 |
| Stable offers | 100天安心睡 / 10年保固 | 可保留為信任輔助，但不應壓過 booking CTA |
| Extra validation | 一般 drift / regression / human review | 另需 LP alignment、預約流程承接、地區/門市資訊核對 |

## Candidate Angle Direction

1. **實際試躺體驗**
   - 讓人先感受山丘樂眠床的支撐與包覆，而不是只看規格
2. **顧問陪伴與低壓決策**
   - 用睡眠顧問與陪伴式引導，降低進店焦慮
3. **預約行動與下一步清楚**
   - 把轉換目標收斂成清楚的 booking CTA

## Required Validation Before Support

1. Draft brief 通過 brief schema validation
2. 確認實際 landing page 是否存在且 CTA 可承接 `預約門市試躺`
3. 完成 LP alignment review，確認門市/預約訊息不是憑空新增
4. 至少產出 1 份 golden output + 1 份 non-author rerun output
5. output 通過 schema / `ad_copy_validator` / rubric / human review
6. 建立 message drift report 與 regression baseline
7. 完成 readiness report 後，才能考慮加入 `supported-matrix`

## Current Blocking Questions

- 最終 landing page 是商品頁、門市頁，還是新的 booking page？
- 是否允許使用地區名或門市資訊？目前 repo 沒有 hillbed 專屬門市承接事實
- `100天安心睡` 與 `10年保固` 在 booking lane 中的權重應保留到什麼程度？

## Recommendation

這條 lane 目前適合繼續做 validation，
但在確認 landing page 與門市承接前，不應提前視為 supported。
