# Change Record: Facebook Chrome Scraper MVP

## Related Task

`fb-chrome-skill-001` / `ai/tasks/2026-03-24-facebook-chrome-scraper-mvp.yaml`

## Related Decision

`ai/decisions/ADR-007-facebook-scraper-chrome-mcp-skill.md`

## Summary

新增 `facebook-chrome-scraper` top-level skill，
把 `kevinzg/facebook-scraper` 的核心收集面改寫成適合 Codex 的 Chrome MCP-first workflow，
並補齊 playbook、schema、rubric、references、UI metadata 與 R&D 記錄。

## Files Created

- `ai/tasks/2026-03-24-facebook-chrome-scraper-mvp.yaml`
- `ai/decisions/ADR-007-facebook-scraper-chrome-mcp-skill.md`
- `ai/skill-src/facebook-chrome-scraper/SKILL.md`
- `ai/skill-src/facebook-chrome-scraper/agents/openai.yaml`
- `ai/skill-src/facebook-chrome-scraper/references/feature-mapping.md`
- `ai/skill-src/facebook-chrome-scraper/references/mcp-operating-rules.md`
- `ai/skill-src/facebook-chrome-scraper/templates/collection-report.md`
- `ai/playbooks/facebook-chrome-scrape.md`
- `ai/schemas/facebook-post-collection.schema.json`
- `ai/evals/facebook-post-collection-rubric.yaml`
- `ai/changes/2026-03-24-facebook-chrome-scraper-mvp.md`
- `ai/validation/2026-03-24-facebook-chrome-scraper-mvp.md`

## Files Updated

- 無

## Sync / Deployment Impact

- 已執行 `bash scripts/sync-skills.sh`
- 新 skill 已同步到：
  - `.claude/skills/facebook-chrome-scraper/`
  - `.agents/skills/facebook-chrome-scraper/`
  - `runtime/openclaw/facebook-chrome-scraper/skills/`
- 已執行 `codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect --channel stable`
- 全域 Codex 設定已新增 `chrome-devtools` MCP server：`~/.codex/config.toml`
- attach mode 以 `stable` Chrome session 為目標

## Open Issues

- 專案 `.codex/config.toml` 目前仍沒有任何 `mcp_servers` 設定；現階段依賴全域 `~/.codex/config.toml`
- 雖已驗證 `autoConnect` 可接上 stable Chrome session，但這個 thread 內建的 devtools tool 未必會熱切換到新 session
