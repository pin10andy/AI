# Hillbed Brief Field Grading

> 目的：把 `lovefu-pmax-hillbed` 這次實作中用到的 brief 欄位分成 A / B 級，作為 Phase 2 brief builder 的欄位設計依據。  
> 分級定義：A = 必須人工拍板；B = 可由工具草擬，但仍需人工確認。

## A 級：必須人工

| 欄位 | 原因 | 本次觀察 |
|------|------|----------|
| `goal` | 直接影響 CTA 與輸出路徑，產品頁可下單不代表所有投放都要走 `purchase`。 | 本輪選 `purchase`，但若改打門市導流就必須另開 brief。 |
| `landing_page_summary.hero_message` | 同一商品頁可能有 H1、meta title、活動文案多種寫法，工具難判斷哪句該成為 brief 主敘事。 | 本輪採用「山丘樂眠床｜第2張床 擁有支撐腰背與放鬆的魔法」。 |
| `landing_page_summary.primary_cta` | 商品頁、活動頁、門市頁 CTA 常不同，會直接改變文案行動導向。 | 本輪用 `立即選購`，沒有沿用試躺導向。 |
| `keyword_cluster.primary_keywords` | 要對齊實際投放意圖、廣告群結構與商業優先序，不能只靠頁面抽詞。 | 本輪人工定為 `床墊推薦 / 獨立筒床墊 / 支撐床墊`。 |
| `offers` | 促案時效短、站內商品頁與活動頁常不一致，最容易出現誤寫。 | 本輪只保留穩定承諾 `100天安心睡全額退款 / 10年保固`，沒有直接把保潔墊贈品寫進 offer。 |
| `constraints.must_include` | 決定哪些訊息一定要進 copy，屬策略取捨，不是純抽取。 | 本輪人工指定 `山丘樂眠床 / 100天安心睡 / 立即選購`。 |
| `constraints.must_avoid` | 涉及法務、品牌與平台風險，不能全自動決定。 | 本輪明確排除 `最低價 / 保證治好腰痛 / 醫療級治療`。 |
| `forbidden_claims` | 需要結合法規、品牌風險與品類敏感詞，必須人工把關。 | 本輪把腰痛療效、最低價與醫療級效果列為禁用。 |
| `seed_angles` | 是這次輸出的策略骨架，牽動素材分布與評分。 | 本輪沿用已定的三角度，不重新發明方向。 |
| `notes` | 目前承載 schema 外的重要決策與不確定值，沒有人工整理就會遺失上下文。 | 本輪用來保留 `landing_page_url`、USP 分層與促案差異。 |

## B 級：可工具草擬，但需人工確認

| 欄位 | 可草擬來源 | 人工仍需確認的點 |
|------|------------|------------------|
| `brief_id` | 檔名規則 / batch 命名規則 | 是否符合團隊命名與後續追蹤需求 |
| `brand_name` | `ai/brand/master-brand.yaml` | 是否對應當前品牌正式寫法 |
| `product_name` | 商品頁標題 / 商品資料 | 是否要用正式商品名或投放友善別名 |
| `campaign_type` | 任務上下文 | 是否真的該走 `pmax` 而不是 `search_rsa` / `store_visit` |
| `landing_page_summary.supporting_points` | 商品頁 scrape | 是否要保留技術細節，或轉成更貼近轉換的語句 |
| `target_audience.segments` | 品牌 target audience + 商品頁 | 是否符合這次 campaign 的實際受眾切片 |
| `target_audience.pain_points` | 商品頁敘事 + 搜尋字詞 | 是否過度放大痛點，或和當前搜尋意圖不符 |
| `target_audience.desired_outcomes` | 品牌語氣 + 產品頁結果敘事 | 是否與 CTA、goal 一致 |
| `keyword_cluster.secondary_keywords` | 搜尋字詞分析 / 既有 keyword list | 哪些是保留觀察字，哪些該排除 |
| `keyword_cluster.negative_themes` | 搜尋字詞清洗工具 | 是否會誤傷品牌字、討論字或研究型字詞 |
| `usp` | 商品頁 facts 抽取 | 是否需要扁平化、哪些屬產品事實、哪些屬活動訊息 |
| `constraints.character_policy` | schema / playbook | 幾乎可全自動，但仍要確認 campaign type 路由沒錯 |
| `tone` | `ai/brand/master-brand.yaml` | 本商品是否要強化某個子語氣，如安心或入門感 |

## 結論

這次最值得 Phase 2 自動化的，不是直接生完整 brief，而是先做「B 級欄位草擬器」：

1. 從品牌檔與商品頁先產出 `brand_name / product_name / supporting_points / target_audience / usp / tone`
2. 從搜尋字詞工具草擬 `secondary_keywords / negative_themes`
3. 把 `goal / primary_keywords / offers / must_include / forbidden_claims / seed_angles / notes` 留給人工最後拍板

這樣最能維持策略控制，同時降低人工整理成本。
