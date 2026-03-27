# ADR-006: Google Ads Creative Auditor as a Sidecar Reviewer

## Status

accepted

## Background

外部 Claude Ads creative pipeline 的公開資料顯示，它的強項是：

1. creative quality / fatigue / sufficiency audit
2. weighted health score 與 severity-based findings
3. 可行動的修正建議與 preflight review

但目前 workspace 內的 Google Ads copy pipeline 主鏈是：

1. `creative-performance-interpreter`
2. `ad-copy-portfolio-builder`
3. `upload-packager`

這條主鏈的目標是把歷史成效與上游 brief 轉成可上稿的素材包，而不是做 creative-health 稽核。

若直接把 external creative pipeline 合進主鏈，會造成三個 contract 風險：

1. 把 audit score 誤當成 asset-level `decision_confidence`
2. 讓 audit finding 直接覆寫 retain / retire / safer rewrite 等 production decision
3. 在弱資料條件下，把 creative-health 推論包裝成高信心 upload decision

## Decision

採用 `creative-auditor` 作為 **Google Ads copy pipeline 的 sidecar reviewer**，不取代主鏈。

具體決策如下：

- 新增獨立 skill：`ai/skill-src/google-ads/creative-auditor/`
- 新增獨立 input schema、output schema、playbook、rubric、report template
- creative-auditor 只接受 `packager output`、`export snapshot`、`MCP snapshot` 經 adapter 正規化後的 audit input
- creative-auditor 輸出 `health_score`、`findings`、`upload_decision`、`integration_handoff`
- creative-auditor **不得**直接修改平台，不建立 write-mode capability
- creative-auditor **不得**覆寫 interpreter / builder / packager 的主決策
- creative-auditor 的結果只能透過：
  - `packager_blockers`
  - `upstream_constraints`
  - `challenger_notes`
  回灌現有 pipeline

## Rationale

這個決策保留了兩邊系統各自最有價值的能力：

- 主鏈繼續負責 production-oriented asset decision 與 upload packaging
- 新 sidecar 專注做 creative health、coverage、policy risk、platform fit 的 challenger review

這樣能避免 contract 汙染，同時讓外部 creative audit 的能力以最小風險接入目前框架。

## Impact

- 影響的檔案：
  - `ai/inputs/google-ads-creative-audit-input.schema.json`
  - `ai/schemas/google-ads-creative-audit-output.schema.json`
  - `ai/playbooks/google-ads-creative-audit.md`
  - `ai/evals/google-ads-creative-audit-rubric.yaml`
  - `ai/skill-src/google-ads/creative-auditor/`
  - `ai/skill-src/google-ads/SKILL.md`
- 影響的 agent：
  - claude
  - codex
  - gemini
  - openclaw
- 影響的流程：
  - final pack preflight review
  - challenger audit
  - 後續 read-only MCP / export adapter 接入

## Related

- Task: `ai/tasks/2026-03-21-google-ads-creative-auditor-mvp.yaml`
- Change: `ai/changes/2026-03-21-google-ads-creative-auditor-mvp.md`
- Validation: `ai/validation/2026-03-21-google-ads-creative-auditor-mvp.md`
- Analysis: `ai/reports/2026-03-21-claude-ads-creative-pipeline-analysis.md`
- Previous ADR: `ai/decisions/ADR-005-google-ads-copy-pipeline-v1-2-data-observe-taxonomy.md`
