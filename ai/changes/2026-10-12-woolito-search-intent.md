# Change — 2026-10-12-woolito-search-intent

Canonical state: [OS #47](https://github.com/pin10andy/personal-operating-dashboard/issues/47).
唯一 Builder Codex。現有 google-ads-writer / google-ads / search-terms-cleaner 已核對；重用 legacy COLUMN_MAP，
不使用有缺值歸零、遺失 IDs/date、高成本零轉換等風險的 parser/analyzer。

新增同一 skill 內離線入口、嚴格 CSV 契約、完全合成 fixtures、9 個 focused tests；SKILL.md 加優先路由。
task / change / validation / report 各留最小收據；沒有新平台、資料庫、服務或 Ads 寫入。
既有 Creative Workbench 是 review_ready 文案 contract，scope 明確排除 search terms cleaner；未覆蓋其未提交成果。

本機 AI main 2b83f4e 與遠端 main d40022d 不同，發布時基於遠端 main，避免夹帶本機 bootstrap 工作。
用工作區內隔離 clone/branch（可寫範圍）取代改動外部 worktree metadata，保留兩個既有 checkout。
本機 memory directory 空，未修改記憶；僅既有床墊 demo，無真實 Woolito CSV。

假設：Woolito B2B 保護語境依 Issue，不沿用 LOVEFU 品牌政策。
未知措辭降 REVIEW，文字清楚不等於 Ads match semantics 確認，無自動排除。
已跑 skill sync，部署複本屬 ignored、本機可再生，PR 僅 canonical source，不部署到正式環境。

風險與後續：缺真實帳戶匯出／完整性／lag 證據；報告 BLOCKED_ON_ACCOUNT_DATA，
產品決策 null。DOT / Andy 下一步協調既有合法私有五份匯出，再執行同一 CLI。


後續已授權實帳 read-only：從 existing Chrome DOM 核實來源、私有匯出與正規化，未碰正式 Ads 設定。
真實 11,887 日列處理發現重複 norm 導致效能問題；只調整歷史衝突核對先檢查 conversion>0、
且只追加 converting visible rows，邏輯等价、無分類政策變更；原9 focused tests通過。
私有 raw/normalized/results 全部在 repo 外，不進公開 PR。公開報告僅匿名摘要、比例、hash。
原始 search query match 與正向 match type 不同，私有 adapter 正確還原 keyword設定並合併1對 disjoint query-match outcomes。
Bounded result NEGATIVE_LIST_FIRST for manual review；完整歷史帳戶/qualified lead/lag仍有邊界。無merge/deploy/livewrite。
