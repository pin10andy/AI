# ADR-003: Hillbed Purchase PMax Production Change Control

## Status

accepted

## Background

`hillbed-purchase-pmax` 已在 `ai/registry/supported-matrix.yaml` 中標記為 production。
這代表後續任何修改都不再只是「重跑一次文案」，而是可能影響：

- canonical brief 的事實正確性
- regression baseline 的可比性
- human review 的政策邊界
- supported lane 的可交接與可稽核性

目前 production lane 已有：
- canonical brief
- canonical output
- Codex non-author dry run

但還缺少一份明確的 production change gate，來區分：
1. 哪些變更可以直接重跑
2. 哪些變更必須先做 drift check / version bump
3. 哪些變更其實已經超出既有 production lane 的邊界

## Decision

為 `hillbed-purchase-pmax` 採用三層 change control：

### 1. Change Classes

| Class | 說明 | 範例 | 是否允許在既有 lane 內處理 |
|------|------|------|----------------------------|
| A | 文案表述微調，不改 brief 事實與 lane 邊界 | headline wording、角度排序、prompt wording | 可以 |
| B | 事實或 gate 變更，但仍在同 lane 邊界內 | 價格/保固更新、watchlist 更新、baseline 擴充 | 可以，但需額外 gate |
| C | 超出既有 lane 邊界 | 新 goal、新產品、新 campaign type | 不可以，需新 task / spec / validation |

### 2. Hard Gates for Production Changes

任何 Class A 或 Class B 的 production change，都必須先通過以下 gate：

1. 建立 task record
2. 若屬架構或控制邏輯調整，建立 ADR 或引用既有 ADR
3. 若 touched facts，先跑 drift report，再決定是否更新 brief
4. 任何 output 變更都必須：
   - 通過 brief schema / output schema validation
   - 通過 `ad_copy_validator.py --exact-pmax-output`
   - 通過 wording watchlist review
   - 通過 human review
   - 與 `ai/validation/regression-baseline-hillbed-pmax.yaml` 的 approved reference set 比對
5. 建立 change record 與 validation record 後，才可視為完成

### 3. Canonical Asset Rules

- 不得直接覆寫 canonical brief 而不更新 `canonical-briefs.yaml` 的 version
- 不得把時效性促案寫回 canonical brief
- `14,900起` 只能出現在 `smart-start` 角度，不得擴散成整包價格訊號
- 若要替換 canonical output，human review verdict 必須為 `可直接上稿`

## Recommended Gate

未來任何 production change，建議使用以下 release gate：

1. `task + change + validation` 三件套齊全
2. touched facts 時必跑 drift report
3. schema / validator / must_include / forbidden_claims 全數 pass
4. wording watchlist 中的高風險詞句全部有 reviewer 結論
5. regression compare 通過：
   - overall `>= 4.30`
   - 任一 rubric 維度不可低於 `4.0`
   - 每個 angle 至少 `4 short / 1 long / 1 description`
   - `14,900起` 只可出現在 `smart-start`
6. human review：
   - 替換 canonical output：`可直接上稿`
   - 非 canonical 實驗輸出：至少 `可微調後上稿`

## Rationale

- `hillbed-purchase-pmax` 已是正式 supported lane，不能再用「感覺差不多」來接納變更
- Class A / B / C 拆分後，可以避免把「新 lane 初始化」混成 production hardening
- 用 3 筆 approved references 建 baseline，能降低單一輸出偶然性的影響
- 用 wording watchlist 補齊 human review 最容易漏掉的政策敏感語意

## Impact

- 影響的檔案：
  - `ai/validation/regression-baseline-hillbed-pmax.yaml`
  - `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`
  - `ai/playbooks/lovefu-hillbed-pmax-runbook.md`
  - `ai/specs/lovefu-hillbed-pmax-writer-spec.md`
  - `ai/registry/supported-matrix.yaml`
- 不影響：
  - `ai/inputs/briefs/lovefu-pmax-hillbed.json`
  - 其他產品 lane

## Related

- Task: `hard-001` / `ai/tasks/2026-03-15-hillbed-pmax-hardening.yaml`
- Prior ADR: `ai/decisions/ADR-002-productization-v1-scope.md`
- Validation: `ai/validation/2026-03-15-hillbed-pmax-hardening.md`
