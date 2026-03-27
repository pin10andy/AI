# MCP Operating Rules

## 1. Fail Closed

若以下任一條件不成立，停止並回報：

- 沒有 Chrome MCP server
- target URL 無法打開
- Chrome session 沒有對應 access
- Facebook 顯示 login wall、checkpoint 或 CAPTCHA

## 2. Use the Browser Session as the Trust Boundary

- 只收集目前 Chrome session 真正可見的內容
- 不導出 cookies
- 不保存帳密
- 不模擬登入流程

## 3. Prefer Small, Explicit Runs

建議一次只做：

- 1–20 篇貼文
- 或少量 direct post URLs

若使用者要求大量 feed crawling，先明確標示風險與限制。

## 4. Keep the Output Honest

- 真的看不到的欄位填 `null`
- 沒展開成功的留言不能算已擷取
- 不能根據 summary count 腦補完整 reactor / comment 名單
- 所有缺口都寫進 `limitations` 或 `capture_notes`

## 5. Preserve Evidence

每篇貼文至少保留一段 `capture_notes`，用來說明：

- 資料是從 feed card 還是 permalink 觀察到
- engagement counts 是否清楚可見
- comments/reactors 是否有成功展開
- 有沒有 lazy load、截斷、登入牆或工具逾時

## 6. Suggested MCP Setup Note

依 OpenAI Codex MCP 文件，Codex 可以在 `~/.codex/config.toml` 或專案 `.codex/config.toml`
加入類似設定：

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled = true
```

實際 server 名稱可不同，但 skill 需要有等價的 Chrome/DevTools browser capability。
