# Validation Record: Facebook Chrome Scraper MVP

## Related Task

`fb-chrome-skill-001` / `ai/tasks/2026-03-24-facebook-chrome-scraper-mvp.yaml`

## Related Decision

`ai/decisions/ADR-007-facebook-scraper-chrome-mcp-skill.md`

## What Was Validated

1. `facebook-chrome-scraper` skill、references、template 是否存在
2. playbook、schema、rubric、task、openai metadata 是否可解析
3. `scripts/sync-skills.sh` 是否成功部署 skill
4. `.agents` 與 `runtime/openclaw` 是否有對應部署結果
5. skill contract 是否清楚規定：
   - Chrome MCP-first
   - no access / no MCP 時 fail closed
   - 不處理登入、cookie export、CAPTCHA bypass
6. `chrome-devtools` MCP server 是否已加到 Codex 設定
7. `chrome-devtools-mcp` package 是否能在本機啟動
8. 是否能對真實 Facebook 公開頁面做最小 live run
9. `--autoConnect --channel stable` 是否能接上既有 Chrome session

## Result

PASS (artifact / contract / sync / launcher / live-single-post scope)

## Evidence

- skill path: `ai/skill-src/facebook-chrome-scraper/SKILL.md`
- playbook: `ai/playbooks/facebook-chrome-scrape.md`
- schema: `ai/schemas/facebook-post-collection.schema.json`
- rubric: `ai/evals/facebook-post-collection-rubric.yaml`
- metadata: `ai/skill-src/facebook-chrome-scraper/agents/openai.yaml`
- deployed Codex skill: `.agents/skills/facebook-chrome-scraper/SKILL.md`
- deployed OpenClaw skill: `runtime/openclaw/facebook-chrome-scraper/skills/SKILL.md`
- global Codex config: `~/.codex/config.toml`

### Command Results

1. JSON parse
   - command: `python3 - <<'PY' ...`
   - result: `json_ok`

2. YAML parse
   - command: `ruby -e 'require "yaml"; ...'`
   - result: `yaml_ok`

3. Skill sync
   - command: `bash scripts/sync-skills.sh`
   - result: `Sync Complete`

4. Deployed path check
   - `.agents/skills/facebook-chrome-scraper/` exists
   - `runtime/openclaw/facebook-chrome-scraper/skills/` exists

5. Global MCP add
   - command: `codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest`
   - result: `Added global MCP server 'chrome-devtools'.`

6. Global MCP config check
   - config entry:
     `[mcp_servers.chrome-devtools]`
     `command = "npx"`
     `args = ["-y", "chrome-devtools-mcp@latest"]`

7. MCP launcher verification
   - command: `npx -y chrome-devtools-mcp@latest --help`
   - result: help output returned successfully
   - interpretation: package 可下載並啟動，launcher path 正常

8. Local runtime prerequisites
   - command: `node -v`
   - result: `v22.22.0`
   - command: `ls -d /Applications/Google\ Chrome.app`
   - result: `/Applications/Google Chrome.app`

9. Live public page check
   - target: `https://www.facebook.com/backtrue`
   - result: public profile/page 可見；關閉登入 modal 後可看到 feed、followers、pinned post 與其他貼文
   - interpretation: 至少 public page/profile 路徑可行，不需先登入

10. Live single-post capture
   - target: `https://www.facebook.com/backtrue/posts/pfbid02A9qsXGjGhmRWUrePs2gbpv17dReKvbCe75SmYbBRfvpzp9WtUTUpWY51CfL8po3El`
   - observed fields:
     - author: `邱煜庭`
     - published_text: `4小時`
     - reaction_count: `234`
     - comment_count: `4則留言`
     - share_count: `61次分享`
     - visible comments: `4`
   - interpretation: permalink 模式可穩定收集至少一篇公開貼文與其可見留言

11. Existing-session attach check
   - command: `npx -y chrome-devtools-mcp@latest --autoConnect --channel stable --logFile /tmp/chrome-devtools-mcp.log`
   - log evidence:
     - `Starting Chrome DevTools MCP Server v0.20.3`
     - `Chrome DevTools MCP Server connected`
   - interpretation: `autoConnect` 可接上既有 `Google Chrome stable` session

## Details

| 驗證項目 | 結果 | 備註 |
|---------|------|------|
| Skill artifact exists | ✓ | `ai/skill-src/facebook-chrome-scraper/` 完整存在 |
| Schema parse | ✓ | `facebook-post-collection.schema.json` 可由 Python `json` 解析 |
| YAML parse | ✓ | rubric / metadata / task 可由 Ruby `YAML` 解析 |
| Skill sync | ✓ | 新 skill 已同步到 `.claude`、`.agents`、`runtime/openclaw` |
| Fail-closed contract | ✓ | `SKILL.md` 與 `mcp-operating-rules.md` 已明確定義 |
| Global MCP registration | ✓ | `chrome-devtools` 已註冊到 `~/.codex/config.toml` |
| MCP launcher test | ✓ | `npx -y chrome-devtools-mcp@latest --help` 成功 |
| Live public page open | ✓ | `https://www.facebook.com/backtrue` 可在未登入狀態下觀察公開內容 |
| Live Facebook capture | ✓ | 已對一個公開 post permalink 完成最小收集 |
| Existing-session attach | ✓ | `--autoConnect --channel stable` log 顯示已 connected |

## Issues Found

- 專案層級仍未配置 Chrome MCP server；目前依賴全域設定
- 目前只驗證到單一公開頁與單一公開貼文；尚未驗證 5-post batch、reactors、或 private/group access
- 目前是以全域 Codex MCP config 驗證 attach；若要專案自含，仍需把相同設定下放到專案 `.codex/config.toml`

## Conclusion

在 artifact、workflow contract、schema、deployment、MCP launcher、單一公開貼文 live run，以及既有 stable Chrome session attach 這個範圍內，MVP 已成立。
下一步應擴展到 3–5 篇貼文 batch、reactor optional path，並確認 private/group 情境需要登入時的行為。
