# LOVEFU 山丘樂眠床 PMax Runbook

> **目的**：讓非原作者能端到端執行 hillbed purchase PMax 素材生成。
> **前提**：熟悉基本 CLI 操作與 AI agent 指令，但不需了解 playbook 或 schema 設計細節。
> **對應 spec**：`ai/specs/lovefu-hillbed-pmax-writer-spec.md`

---

## 前置準備

在開始之前，確認以下環境：

- [ ] Repo 已 pull 到最新版本
- [ ] Python 3 可用（`python3 --version`）
- [ ] jsonschema 套件可用（`pip3 install jsonschema` 或使用 `.tmp/jsonschema-venv/`）
- [ ] `ad_copy_validator.py` 可執行（位於 `ai/skill-src/google-ads/ad-copy-builder/scripts/`）
- [ ] 至少一個 AI agent 可用（Claude / Codex / Gemini / OpenClaw）
- [ ] Git hooks 已安裝（`bash scripts/install-hooks.sh`）
- [ ] Artifact governance check 可執行（`python3 scripts/check_artifact_governance.py`）

---

## Step 1: 確認 Brief 狀態

1. 開啟 `ai/registry/canonical-briefs.yaml`
2. 找到 `brief_id: lovefu-pmax-hillbed`
3. 確認以下欄位：

| 檢查項目 | 期望值 |
|---------|--------|
| `status` | `canonical` |
| `version` | 記下目前版號 |
| `drift_check.next_check_due` | 未過期 |

4. **如果 drift check 已過期** → 先執行 [Step 1a: Drift Check](#step-1a-drift-check)
5. **如果正常** → 繼續 Step 2

### Step 1a: Drift Check

當 drift check 過期時，需要比對官網與 brief 的事實一致性。

1. 開啟 https://www.lovefu.tw/products/hillbed
2. 逐項比對以下事實宣稱：

| 事實項目 | Brief 中的值 | 官網當前值 | 一致？ |
|---------|-------------|-----------|--------|
| 產品名稱 | 山丘樂眠床 | | |
| 入門價格 | 14,900 起 | | |
| 退款政策 | 100天安心睡全額退款 | | |
| 保固期間 | 10年保固 | | |
| 泡棉材質 | MDI高密度慢回彈泡棉 | | |
| 彈簧規格 | 2.4mm高碳鋼獨立筒 | | |
| 安全認證 | CertiPUR + OEKO-TEX | | |
| 主要 CTA | 立即選購 | | |

3. **如果全部一致**：
   - 更新 `canonical-briefs.yaml` 中的 `drift_check.last_checked` 為今天日期
   - 設定 `drift_check.next_check_due` 為一個月後
   - 繼續 Step 2

4. **如果有差異**：
   - 停止流程
   - 更新 `ai/inputs/briefs/lovefu-pmax-hillbed.json` 中的對應欄位
   - 遞增 `canonical-briefs.yaml` 中的 `version`
   - 建立新的 drift report（格式見 `ai/reports/2026-03-14-hillbed-message-drift.md`）
   - 確認 regression baseline 是否需要重建
   - 完成後回到 Step 2

---

## Step 2: 啟動生成

向 AI agent 提供以下指令（可複製貼上）：

```
請使用 Google Ads Writer skill 為山丘樂眠床生成 PMax 文案。

Brief 檔案：ai/inputs/briefs/lovefu-pmax-hillbed.json
Skill 檔案：ai/skill-src/google-ads-writer/SKILL.md
Playbook：ai/playbooks/google-ads-pmax.md

請依照 SKILL.md 的 7 步驟工作流執行：
1. 驗證 brief
2. 讀取品牌規範
3. 推導 3 個 angle
4. 生成 PMax 資產包
5. 自檢
6. 輸出 JSON + Markdown
7. Rubric 自評

輸出 JSON 須符合：ai/schemas/google-ads-pmax-output.schema.json
輸出 Markdown 須依照：ai/skill-src/google-ads-writer/templates/pmax-output.md
```

等待 agent 完成，取得 JSON 和 Markdown 兩份輸出。

---

## Step 3: 格式驗證

### 3a. JSON Schema Validation

```bash
# 如果有 venv
.tmp/jsonschema-venv/bin/python -c "
import json, jsonschema
with open('輸出的JSON路徑') as f: data = json.load(f)
with open('ai/schemas/google-ads-pmax-output.schema.json') as f: schema = json.load(f)
jsonschema.Draft7Validator(schema).validate(data)
print('Schema validation: PASS')
"
```

### 3b. 資產數量與字元驗證

```bash
python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py \
  --file 輸出的JSON路徑 \
  --exact-pmax-output
```

期望結果：所有 check 顯示 PASS。

**如果失敗** → 回到 Step 2 重新生成，並在指令中加註具體失敗項目。

---

## Step 4: Rubric 自評確認

檢查 agent 輸出中的 rubric self-score：

| 維度 | Reference Gate | 本次分數 | 通過？ |
|------|----------------|---------|--------|
| brand_consistency | ≥ 4.0 | | |
| char_limit_compliance | pass | | |
| cta_clarity | ≥ 4.0 | | |
| headline_diversity | ≥ 4.0 | | |
| angle_coverage | ≥ 4.0 | | |
| policy_safety | ≥ 4.0 | | |
| language_quality | ≥ 4.0 | | |
| **overall** | **≥ 4.30** | | |

通過標準：
- overall ≥ 4.30（production change gate）
- 任一 rubric 維度不可低於 4.0
- 任一維度較 approved reference 慣性水位下降 > 1.0 分需調查

**如果未通過** → 記錄具體弱項，回到 Step 2 在指令中加強該面向。

---

## Step 5: Human Review

依照 `ai/evals/google-ads-pmax-human-review.md` 逐項檢查：

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| 是否符合品牌語氣 | | |
| 是否有 3 種以上不同訴求 | | |
| 是否避免違規宣稱 | | |
| Short headlines 是否夠分散 | | |
| Long headlines 是否有補充價值 | | |
| Descriptions 是否可直接上稿 | | |
| 是否重複感過高 | | |
| Tier 2 詞句是否已過 watchlist 檢查 | | |
| Tier 3 詞句是否完全未出現 | | |

**判定**（三選一）：
- 可直接上稿 → 繼續 Step 6
- 可微調後上稿 → 記錄需微調項目，手動修改後繼續 Step 6
- 需重寫 → 回到 Step 2，附上具體問題說明

---

## Step 6: Regression 比對

開啟 `ai/validation/regression-baseline-hillbed-pmax.yaml`，對照 `aggregated_baseline` 與 `reference_outputs`：

| 比對項目 | Gate / Reference | 本次 | 差異 | 通過？ |
|---------|------------------|------|------|--------|
| short_headlines count | 15 | | | |
| long_headlines count | 5 | | | |
| descriptions count | 5 | | | |
| angles count | 3 | | | |
| overall score | ≥ 4.30 | | | |
| single rubric floor | ≥ 4.0 | | | |
| forbidden_claims found | 0 | | | |
| must_include all present | true | | | |
| human_review verdict | 至少可微調後上稿 | | | |
| 14,900起 所在 angle | smart-start only | | | |

回歸規則：
- overall < 4.30 → 不得直接上稿
- 任一 rubric 維度 < 4.0 → 需調查
- forbidden_claims > 0 → 不得上稿
- must_include 缺失 → 不得上稿
- `14,900起` 若出現在非 `smart-start` angle → 不得上稿

---

## Step 7: Artifact Governance Check

> **此步驟為必要 gate**。任務不得在未通過治理檢查前標記為 validated。

執行 artifact governance 檢查腳本：

```bash
python3 scripts/check_artifact_governance.py
```

### 檢查項目

| 檢查項目 | 期望結果 | 實際結果 |
|---------|---------|---------|
| Repo root 無新增 Google Ads 散落檔 | PASS | |
| 正式輸出在 canonical 路徑下 | PASS | |
| 檔案命名符合政策 | PASS | |
| Scratch 未混入 ai/outputs/ | PASS | |
| Registry 欄位完整 | PASS | |
| Validation 命名合規 | PASS | |

### 通過條件

- 所有 FAIL 必須為 0（legacy 警告不計）
- 新產出的 artifact 已在 `ai/registry/artifacts.yaml` 登記

**如果未通過** → 修正違規後重新執行檢查。常見修正：
- 輸出寫錯位置 → 移至 `ai/outputs/google-ads/{brand}/{product}/{lane}/` 對應子目錄
- 命名違規 → 依 `ai/policies/artifact-naming-policy.md` 重新命名
- 未登記 → 在 `ai/registry/artifacts.yaml` 補登

---

## Step 8: 記錄

完成以上所有步驟後，建立紀錄：

### 8a. 儲存輸出

> **重要**：所有正式輸出必須遵循 artifact governance 政策。
> - 命名規範：`ai/policies/artifact-naming-policy.md`
> - 寫入規範：`ai/policies/artifact-write-policy.md`
> - 存儲映射：`ai/registry/storage-map.yaml`

正式輸出路徑：
```
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.json
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.md
```

Pipeline 階段輸出路徑：
```
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/{task_id}/
├── builder.json
├── interpreter.json
├── packager.json
└── packager.md
```

### 8b. 登記 Artifact

在 `ai/registry/artifacts.yaml` 新增條目，包含所有必填欄位：
`artifact_id`, `task_id`, `artifact_type`, `brand`, `product`, `lane`,
`status`, `canonical_path`, `source_brief`, `generated_by`, `owner`, `created_at`。

### 8c. 建立 Validation Record

在 `ai/validation/` 建立 `YYYY-MM-DD-hillbed-pmax-rerun.md`，格式參考：
`ai/validation/2026-03-14-lovefu-hillbed-golden-brief.md`

### 8d. 更新 Registry

- 更新 `ai/registry/canonical-briefs.yaml` → `drift_check.last_checked`
- 如有 brief 變更 → 遞增 `version`

---

## 常見問題 FAQ

**Q: Agent 回報 brief validation 失敗怎麼辦？**
A: 檢查 brief JSON 是否符合 `ai/inputs/google-ads-brief.schema.json`。
常見原因：缺少必填欄位、`campaign_type` 不是 `pmax`、`character_policy` 數值錯誤。

**Q: 分數低於 baseline 怎麼辦？**
A: 先確認是不是低於 production gate（overall < 4.30 或任一 rubric < 4.0）。
如果是 policy_safety，先看 `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md`；
如果是 headline_diversity，可能 angle 太接近。在 Step 2 指令中加強該面向後重跑。

**Q: 官網改了價格怎麼辦？**
A: 執行 Step 1a Drift Check。更新 brief 後重跑全流程。
注意：價格變更可能影響「入門」角度的文案，需特別注意 regression 比對。

**Q: 想加入活動促案怎麼辦？**
A: 不要修改 canonical brief。另建一份 campaign-specific brief（如 `lovefu-pmax-hillbed-spring2026.json`），
在 `canonical-briefs.yaml` 中以 `draft` status 登錄。

**Q: 不同 agent 跑出來的結果品質差很多怎麼辦？**
A: 目前 Claude 與 Codex 都已驗證可完成這條 lane 的重跑。
Gemini 和 OpenClaw 的品質一致性仍待後續 smoke test。

---

## 快速參考

| 資源 | 路徑 |
|------|------|
| Canonical brief | `ai/inputs/briefs/lovefu-pmax-hillbed.json` |
| Brief schema | `ai/inputs/google-ads-brief.schema.json` |
| Output schema | `ai/schemas/google-ads-pmax-output.schema.json` |
| Skill | `ai/skill-src/google-ads-writer/SKILL.md` |
| Playbook | `ai/playbooks/google-ads-pmax.md` |
| Rubric | `ai/evals/ads-rubric.yaml` |
| Human review checklist | `ai/evals/google-ads-pmax-human-review.md` |
| Regression baseline | `ai/validation/regression-baseline-hillbed-pmax.yaml` |
| Wording risk watchlist | `ai/reports/2026-03-15-hillbed-pmax-wording-risk-watchlist.md` |
| Production change control | `ai/decisions/ADR-003-hillbed-pmax-production-change-control.md` |
| Supported matrix | `ai/registry/supported-matrix.yaml` |
| Canonical briefs registry | `ai/registry/canonical-briefs.yaml` |
| Writer spec | `ai/specs/lovefu-hillbed-pmax-writer-spec.md` |
| Golden output (JSON) | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.json` |
| Golden output (MD) | `ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.md` |
| Artifact naming policy | `ai/policies/artifact-naming-policy.md` |
| Artifact write policy | `ai/policies/artifact-write-policy.md` |
| Storage map | `ai/registry/storage-map.yaml` |
| Artifact registry | `ai/registry/artifacts.yaml` |
| Migration plan | `ai/migration/2026-03-16-artifact-migration-plan.md` |
