# Facebook Chrome Scrape Playbook

## Purpose

用 Chrome MCP 以互動式方式收集 Facebook 貼文與留言，
並輸出可被其他 agent 或工作流消費的結構化 collection。

這不是 headless crawler playbook。
它是針對 Codex skill 的 small-batch collection playbook。

## Required Files

執行前應讀取：

1. `ai/memory/shared-context.yaml`
2. `ai/skill-src/facebook-chrome-scraper/SKILL.md`
3. `ai/schemas/facebook-post-collection.schema.json`
4. `ai/evals/facebook-post-collection-rubric.yaml`
5. `ai/skill-src/facebook-chrome-scraper/references/feature-mapping.md`
6. `ai/skill-src/facebook-chrome-scraper/references/mcp-operating-rules.md`

## Inputs

- `target_url` 或明確的 page/profile/group/post 目標
- `max_posts`
- 是否包含 `comments`
- 是否包含 `reactors`
- 是否包含 `media`
- 使用者是否已在 Chrome 中有對應 access

## Execution Flow

### Step 1: Preflight

先確認：

1. Codex 是否可用 Chrome MCP
2. target 是否打得開
3. target 是 public 還是 authenticated
4. scope 是否屬於 interactive / small-batch

若失敗，直接回報缺口，不進入收集階段。

### Step 2: Stabilize the Target

- direct post URL：直接進 permalink
- page/profile/group feed：先讓主 feed 穩定顯示，再決定是否進 permalink
- 若畫面仍在 loading、跳 modal、或 feed 尚未穩定，不要急著記錄欄位

### Step 3: Capture Posts

每篇貼文至少收集：

- `post_id`
- `post_url`
- `author_name`
- `published_text`
- `text`
- reaction/comment/share counts
- media URLs

若從 feed card 只能拿到部分資料，應在 `capture_notes` 記錄。

### Step 4: Expand Comments

只有在 `include_comments = true` 時進行：

- 依 `comment_limit_per_post` 控制展開深度
- 遇到需要登入、工具逾時、或 UI 不穩時停止
- 未成功展開的留言不能算收集完成

### Step 5: Expand Reactors Only If Stable

reactors 屬於 optional path：

- 只有 dialog 能打開、內容可見、切換不會造成整頁失穩時才抓
- 若不穩定，保留 reaction count，並把 reactor 名單標為未收集

### Step 6: Normalize Output

輸出 JSON 必須符合：

`ai/schemas/facebook-post-collection.schema.json`

另外輸出一段短摘要，建議依：

`ai/skill-src/facebook-chrome-scraper/templates/collection-report.md`

### Step 7: Self-Evaluate

依 rubric 檢查：

- 是否做過 preflight
- 是否沒有虛構 inaccessible data
- 是否把 limitation 寫清楚
- 是否保留 schema required fields

## Stop Conditions

出現以下任一情況就停止：

- 沒有 Chrome MCP
- page/group/post 無法存取
- Facebook 要求登入、checkpoint 或 CAPTCHA
- 單次任務 scope 已超出 interactive range
- 工具重試後仍無法穩定觀察內容
