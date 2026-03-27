---
name: "facebook-chrome-scraper"
description: "在 Codex 中透過 Chrome MCP 擷取 Facebook pages、profiles、groups 或指定 post URLs 的貼文與留言，輸出結構化 collection。當使用者提到 Facebook scraping、貼文擷取、留言擷取、社團貼文整理、指定貼文內容擷取時觸發。"
license: MIT
metadata:
  version: 0.1.0
  author: Andy Chou
  category: web-scraping
  updated: 2026-03-24
---

# Facebook Chrome Scraper

> **Canonical source**: `ai/skill-src/facebook-chrome-scraper/SKILL.md`
> Do NOT edit copies in `.claude/skills/`, `.agents/skills/`, or `runtime/`.
> Always edit here and run `scripts/sync-skills.sh` to deploy.

這個 skill 不是大規模 crawler，也不是 cookie scraper。
它是用來讓 Codex 在 **有 Chrome MCP 能力時**，
以互動式方式收集 Facebook 可見內容並輸出結構化資料。

## Required References

執行前必須讀取：

1. `ai/memory/shared-context.yaml`
2. `ai/playbooks/facebook-chrome-scrape.md`
3. `ai/schemas/facebook-post-collection.schema.json`
4. `ai/evals/facebook-post-collection-rubric.yaml`
5. `references/feature-mapping.md`
6. `references/mcp-operating-rules.md`

## When to Use

- 使用者要擷取 Facebook page / profile 的最新貼文
- 使用者要整理某個 group feed 中可見的貼文
- 使用者給定一或多個 Facebook post URLs，要抓全文與留言
- 使用者要把互動式 Facebook 觀察結果整理成可重用的 JSON collection

## Prerequisites

以下條件至少要成立：

1. Codex 已配置可用的 Chrome MCP server
2. 目標內容是 public，或使用者當前 Chrome session 已有權限查看
3. 使用者要求的是 small-batch / interactive collection，不是大規模爬取

若任一條件不成立，停止並回報缺口，不要假裝完成。

## Non-Goals

這個 skill 明確不做：

- 自動登入或保存帳密
- CAPTCHA / checkpoint / rate-limit bypass
- stealth / anti-detection tactics
- 大規模、長時間、無限捲動式爬取
- 透過非授權方式擷取 private content

## Execution Steps

### Step 1: Run preflight

- 確認 Chrome MCP 可用
- 確認目標是 `page` / `profile` / `group` / `post_url`
- 確認需要的欄位與限制：
  - `max_posts`
  - 是否抓 `comments`
  - 是否抓 `reactors`
  - 是否抓 `media`
- 若是 group 或 private post，先確認目前 Chrome session 已可見

### Step 2: Prefer the most stable target

穩定度優先順序：

1. direct post URL
2. page / profile feed
3. group feed

若使用者提供 post URL，優先逐篇擷取，不要先回到 feed。

### Step 3: Capture visible data only

對每篇貼文至少收集：

- `post_id`
- `post_url`
- `author_name`
- `published_text`
- `text`
- 可見的 engagement counts
- 可見的 media URLs

只記錄你真的看到或展開成功的資料。
抓不到的欄位填 `null` 或寫進 `limitations` / `capture_notes`。

### Step 4: Expand comments carefully

若 `include_comments = true`：

- 只展開到使用者要求的上限
- 可抓 replies，但不要無限展開
- 若頁面不穩、評論需要額外登入或 UI 無法穩定展開，停止並記錄限制

### Step 5: Treat reactors as optional

若 `include_reactors = true`：

- 只有在 reaction dialog 可穩定打開時才抓
- 若 reactor list 不可見、被登入牆擋住、或工具逾時，標記限制即可
- 不要從 reaction count 推測 reactor 名單

### Step 6: Emit structured output

最終輸出必須符合：

`ai/schemas/facebook-post-collection.schema.json`

並附上一段短的 markdown 摘要，格式可依：

`templates/collection-report.md`

### Step 7: Self-evaluate

依 `ai/evals/facebook-post-collection-rubric.yaml` 自查：

- preflight 是否確實做過
- 是否只輸出可追溯、可觀察到的資料
- 是否明確記錄 limitations
- schema 是否完整

## Quality Gates

- [ ] 沒有 Chrome MCP 時必須停止，不可虛構 browser run
- [ ] 沒有 access 時必須停止，不可猜測 private content
- [ ] 抓不到的 counts 用 `null`，不可亂補數字
- [ ] `reactors` 只在真的打開 dialog 且可觀察時收集
- [ ] collection 應維持 small-batch；預設不要超過 20 篇貼文
- [ ] 每篇貼文都要有 `capture_notes`

## Output Notes

- `generated_by` 固定填 `codex`
- `capture_environment.method` 固定填 `chrome_mcp`
- `limitations` 必填，即使是空陣列也要保留
