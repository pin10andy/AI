# Current Milestone Spec

## Milestone Name
Phase 1: Multi-Agent Repo Skeleton + Recording Framework

## Goal
建立一個可運作的 multi-agent 共用 repo，讓 Claude、Codex、Gemini、OpenClaw 能共用知識、技能和工作流程，並且所有研發工作都有可追溯的 repo 原生紀錄。

## Background
目前使用多個 AI 工具但各自獨立，沒有共用的品牌規範、技能庫或記錄機制。當工作橫跨多個 agent 和多次會話時，變更歷史和決策脈絡容易遺失。

## Scope
本階段包含：
- 建立 repo 骨架結構
- 建立共用核心檔案（brand, playbooks, schemas, evals, skills）
- 建立各工具的 adapter 層
- 建立 skill sync 機制
- 建立研發記錄機制（task, ADR, change, validation, release, retro）
- 建立狀態追蹤與設計核對機制
- 完成第一個 skill（google-ads-writer）和第一個品牌提取（brand-extractor）
- 填入實際品牌資料（LOVEFU）

## Out of Scope
本階段不包含：
- Google Ads 素材的正式量產
- 自動化驗證腳本（CI/CD）
- 多語系支援（超出中英雙語範圍）
- 付費 API 串接

## Primary Deliverables
- repo 骨架目錄結構
- 四份 agent adapter（CLAUDE.md, AGENTS.md, GEMINI.md, openclaw/agents/）
- 品牌規範 master-brand.yaml（含 LOVEFU 實際資料）
- Google Ads playbook + schema + rubric
- 兩個共用 skill（google-ads-writer, brand-extractor）
- skill sync script
- 六份 R&D 記錄模板
- milestone spec + alignment report 模板

## Functional Requirements
| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-001 | 共用品牌規範 | 所有 agent 可讀取同一份 master-brand.yaml | 品牌檔案存在且必填欄位 ≥ 90% |
| FR-002 | 共用 skill | skill 從 ai/skill-src/ 同步到各工具部署目錄 | sync script 可執行且三個目標都有檔案 |
| FR-003 | Codex 可用性 | Codex 能讀取 AGENTS.md 和 .agents/skills/ | Codex smoke test 通過 |
| FR-004 | 品牌提取 | brand-extractor skill 能從網站提取品牌資料 | Claude 和 Codex 獨立提取結果一致性 > 70% |
| FR-005 | 研發記錄 | task → change → validation 流程可走通 | 存在至少一筆完整的三環記錄 |
| FR-006 | 狀態查詢 | 能從 repo 檔案回答「做到哪了」 | task 有 status 欄位，可列出各狀態清單 |
| FR-007 | 設計核對 | 能從 spec 和實作比對產出 alignment report | spec 存在且 report 模板可用 |

## Process / Workflow Requirements
| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| WF-001 | Skill 管理流程 | 修改 skill-src → 跑 sync → 部署到各工具 | sync-skills.sh 可正常執行 |
| WF-002 | R&D 記錄流程 | task → decision(optional) → change → validation → status | 有完整範例且模板可用 |
| WF-003 | 設計核對流程 | spec → inspect → compare → report | 有模板且可產出報告 |

## Design / Structure Requirements
| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| DS-001 | 單一來源 | 所有規則在 ai/ 維護，adapter 只做引用 | 無重複規則在多處 |
| DS-002 | 薄 adapter | 工具設定檔 < 50 行，只引用不複製 | 各 adapter 行數符合 |
| DS-003 | 可預測命名 | 檔案命名遵循 YYYY-MM-DD-short-name 慣例 | 所有記錄檔案符合命名規則 |
| DS-004 | 目錄完整 | 所有規格要求的目錄都存在 | ai/ 下 12 個子目錄全部存在 |

## Validation Requirements
- Codex smoke test：能讀取 AGENTS.md 和 .agents/skills/
- Claude-Codex 品牌提取對照：一致性 > 70%
- sync-skills.sh 執行成功
- task → change → validation 記錄鏈完整

## Evidence Sources
- `ai/tasks/`
- `ai/validation/`
- `ai/changes/`
- `.agents/skills/`
- `.claude/skills/`
- `runtime/openclaw/`
- `scripts/sync-skills.sh`

## Risks
- Codex 的工作目錄需要手動確認在 repo root（已解決）
- Gemini 和 OpenClaw 尚未進行 smoke test
- 品牌視覺欄位中 font_family 仍未填入

## Open Questions
- Gemini 是否支援讀取 .gemini/config.yaml？需實測
- OpenClaw 的 agent 載入機制是否支援 YAML config？需實測

## Checkpoint Definition
本階段 checkpoint 完成條件：
1. repo 骨架完整（12 個 ai/ 子目錄 + adapter 層）
2. 至少一個 skill 可跨 agent 使用
3. 品牌資料已填入且完成度 > 90%
4. R&D 記錄機制有模板且有至少一筆實際記錄
5. 能從 spec 產出 alignment report
