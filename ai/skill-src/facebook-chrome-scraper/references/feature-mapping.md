# Feature Mapping

本檔把 `kevinzg/facebook-scraper` 的常見能力，映射到 `facebook-chrome-scraper` skill 的工作流。

## Source Capability -> Skill Mapping

| 原 repo 能力 | Chrome MCP skill 對應做法 | 備註 |
|---|---|---|
| `get_posts(page_or_profile)` | 開啟 page/profile feed，收集可見貼文卡片，再視需要進入 permalink | 適合 public page/profile |
| `group=<id>` | 開啟 group feed，僅在目前 Chrome session 已授權可見時收集 | 不做 access bypass |
| `post_urls=[...]` | 逐篇開啟 direct post URL 擷取全文、留言、媒體 | 這是最穩定的 MVP 路徑 |
| `options={"comments": n}` | 展開留言與 replies 到指定上限 | 只收集已展開、可見的內容 |
| `options={"reactors": n}` | 視 UI 是否穩定，打開 reaction dialog 後再收集 | reactor 名單永遠是 optional |
| `cookies` / `from_browser` | 不匯出 cookies；直接使用現有 Chrome session | 避免 cookie file handoff |
| `credentials=(user, pass)` | 不支援 | skill 不處理登入流程 |

## Why This Is Not a Direct Port

原 repo 的強項是：

1. 用 Python 在 HTTP 層面拿 Facebook 頁面資料
2. 在需要時用 cookie bridge 連到瀏覽器 session
3. 用 parser 萃取貼文欄位

Codex skill 的強項則是：

1. 直接使用瀏覽器工具觀察「當前可見狀態」
2. 把流程、限制與輸出契約包成可重用 skill
3. 在不確定時回報限制，而不是靜默降級

所以這個 skill 採取的是 **功能映射**，不是 **程式碼移植**。

## MVP Scope

MVP 保留的能力：

- public page/profile collection
- authorized group/post collection
- direct post URL extraction
- limited comments extraction
- optional reactor extraction
- structured JSON output

MVP 刻意不做的能力：

- login automation
- browser cookie export/import
- large-page-count crawling
- stealth / ban-avoidance logic
- video downloader integration

## Feasibility Verdict

可行，但前提是：

1. 有可用的 Chrome MCP
2. 以 interactive / small-batch 任務為主
3. 接受 Facebook UI 與 access state 會影響可抓範圍
