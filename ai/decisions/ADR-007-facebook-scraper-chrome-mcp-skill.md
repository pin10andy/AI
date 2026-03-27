# ADR-007: Adapt facebook-scraper as a Chrome MCP-first Codex Skill

## Status

accepted

## Background

`kevinzg/facebook-scraper` 提供了實用的 Facebook 擷取面：

1. pages / profiles / IDs
2. groups
3. direct post URLs
4. comments / replies
5. optional reactors / media extraction

但它的核心做法是 requests/HTML parsing 與 cookies/browser-cookie bridge。
這種模式適合 Python library，不適合直接搬進 Codex skill。

Codex skill 的最佳做法是：

1. 把瀏覽器狀態、登入狀態與互動交給 Chrome MCP
2. 把 skill 本身設計成可重用的 workflow、限制規則與輸出契約
3. 在缺少 MCP 或缺少授權存取時 fail closed，而不是退回脆弱的 cookie scraping

## Decision

採用 `facebook-chrome-scraper` 作為新的 top-level skill，
以 **Chrome MCP-first** 的方式實作 Facebook 擷取工作流，而不是直接移植 Python scraper。

具體決策如下：

- 新增 skill：`ai/skill-src/facebook-chrome-scraper/`
- 新增 `agents/openai.yaml`，宣告 Chrome DevTools MCP 依賴
- 新增獨立 output schema、rubric、playbook、references 與 template
- 擷取來源限定為：
  - public pages / profiles
  - 使用者已在 Chrome 中授權存取的 groups / posts
  - direct post URLs
- cookies export / `from_browser` 模式改由「現有 Chrome session」取代
- skill 不負責登入、帳密儲存、CAPTCHA 處理、反封鎖策略或大規模爬取
- skill 必須在沒有 MCP、沒有 access、或頁面無法穩定展開時停止並回報限制

## Rationale

這個方案比直接移植 repo 更符合 Codex 的運作方式：

- 瀏覽與登入留在瀏覽器環境，避免複製 cookies 或繞過 session 保護
- skill 可以直接利用使用者當前 Chrome profile 的實際可見內容
- output schema 與 rubric 讓結果能被多 agent 重複消費與驗證
- 降低對 Facebook 前端私有 API 與 HTML 結構的直接耦合

## Impact

- 影響的檔案：
  - `ai/skill-src/facebook-chrome-scraper/`
  - `ai/playbooks/facebook-chrome-scrape.md`
  - `ai/schemas/facebook-post-collection.schema.json`
  - `ai/evals/facebook-post-collection-rubric.yaml`
- 影響的 agent：
  - codex
  - claude
  - gemini
  - openclaw
- 影響的流程：
  - Facebook public/authenticated content collection
  - Chrome MCP preflight and live capture
  - structured post collection output

## Related

- Task: `ai/tasks/2026-03-24-facebook-chrome-scraper-mvp.yaml`
- Change: `ai/changes/2026-03-24-facebook-chrome-scraper-mvp.md`
- Validation: `ai/validation/2026-03-24-facebook-chrome-scraper-mvp.md`
