# Multi-Agent AI Workspace

一個讓 Claude、Codex、Gemini、OpenClaw 共用知識、技能和工作流程的操作系統。

## Repo Layers

- `docs/ai/`：operating-pack docs，說明協作者應如何在這個 repo 內工作
- `ai/`：domain truth 與 runtime truth，承載共享規則、任務記錄、驗證證據與正式 artifact

## 架構概覽

```
docs/ai/                    ← Operating Pack / collaboration rules
  PRD-*.md                  ← repo-level execution brief
  SSD-*.md                  ← repo structure and boundary docs
  *_PROTOCOL.md             ← handoff / validation / governance operating rules
  templates/                ← template entrypoints

ai/                         ← Domain truth + runtime truth
  brand/                    ← 品牌規範
  knowledge/                ← 共用知識庫
  playbooks/                ← 執行流程手冊
  schemas/                  ← 輸出格式定義
  tasks/                    ← 任務記錄與模板
  evals/                    ← 品質評估標準
  skill-src/                ← Skill 原始碼（唯一編輯位置）
  memory/                   ← 跨 agent 共用記憶

CLAUDE.md                   ← Claude adapter（薄層包裝）
AGENTS.md                   ← Codex adapter
GEMINI.md                   ← Gemini adapter
openclaw/agents/            ← OpenClaw adapter

.claude/skills/             ← Claude skill 部署目標
.agents/skills/             ← Codex skill 部署目標
runtime/openclaw/           ← OpenClaw skill 部署目標

scripts/sync-skills.sh      ← Skill 同步腳本
```

## 核心原則

1. **分層但不重複**：`docs/ai/` 管 operating pack，`ai/` 管 domain truth 與 runtime truth
2. **薄 adapter**：工具設定檔只做引用，不複製規則
3. **一處修改，全面同步**：改 `ai/skill-src/` → 跑 sync → 所有工具更新

## Canonical Boundary

### `docs/ai/`

放 repo-level 的協作與執行規則，例如：

- operating PRD / SSD
- handoff protocol
- worktree policy
- validation levels
- memory governance
- template entrypoints

### `ai/`

放實際執行時會被消費與持續更新的 canonical artifacts，例如：

- shared context / brand / knowledge
- playbooks / schemas / evals
- tasks / decisions / changes / validation / reports
- policies / registries
- skill source
- governed outputs

原則上：
- 不把 domain governance 複製到 `docs/ai/`
- 不把 operating-pack docs 混進 task runtime records

## 快速開始

### 同步 skill 到所有工具
```bash
bash scripts/sync-skills.sh
```

### 新增 skill
1. 在 `ai/skill-src/your-skill-name/` 建立 `SKILL.md`
2. 執行 `bash scripts/sync-skills.sh`

### 新增共用知識
編輯 `ai/memory/shared-context.yaml` 或在 `ai/knowledge/` 新增檔案。

## 目前狀態

- [x] Repo 骨架
- [x] 品牌規範模板
- [x] Google Ads playbook
- [x] 輸出 schema
- [x] 評估 rubric
- [x] 第一個 skill: google-ads-writer
- [x] Skill sync 腳本
- [x] 四個 agent adapter
- [ ] 填入實際品牌資料
- [ ] 端到端驗證 Google Ads 生成流程
