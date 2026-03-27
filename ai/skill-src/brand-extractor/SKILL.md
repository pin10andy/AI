# Brand Extractor Skill

> **Canonical source**: `ai/skill-src/brand-extractor/SKILL.md`
> Do NOT edit copies in `.claude/skills/`, `.agents/skills/`, or `runtime/`.
> Always edit here and run `scripts/sync-skills.sh` to deploy.

## Purpose

從多種來源（網站、文件、使用者問答）提取品牌資料，並填入 `ai/brand/master-brand.yaml`。
確保所有 AI agent 共用一致的品牌規範。

## When to Use

- 使用者要求建立或更新品牌資料
- `ai/brand/master-brand.yaml` 的欄位尚未填入
- 使用者提供了品牌相關的網站、文件或素材
- 使用者提到「品牌」「brand」「品牌設定」「brand setup」

## Output Target

填入的結果寫入：`ai/brand/master-brand.yaml`
輸出格式必須符合：`ai/schemas/brand-extract.schema.json`

---

## Execution Steps

### Step 1: 確認目前品牌資料狀態

讀取 `ai/brand/master-brand.yaml`，列出哪些欄位已填、哪些仍為空。
將空欄位整理成一份「待填清單」。

### Step 2: 判斷可用輸入來源

詢問使用者有哪些來源可以提取品牌資料：

```
可用來源：
A. 品牌網站 URL（我會從網站內容提取）
B. 已有文件（品牌手冊、簡報、PDF 等）
C. 直接問答（我會用結構化問題引導你）
D. 以上皆有（我會先從網站和文件提取，不足的再問你）
```

### Step 3: 依來源提取資料

#### 3a. 從網站提取（如有 URL）

瀏覽品牌網站，重點提取：
- 首頁的品牌標語、價值主張
- 關於我們頁面的品牌描述
- 產品/服務頁面的目標受眾線索
- 網站的語氣風格（正式/活潑/專業等）
- 視覺元素：主色、輔色、字型（從 CSS 或設計觀察）

提取時記錄每筆資料的來源 URL。

#### 3b. 從文件提取（如有文件）

讀取使用者提供的文件，重點尋找：
- 品牌名稱、標語、使命宣言
- 品牌個性描述
- 目標客群描述
- 品牌語氣規範
- 視覺識別規範（色彩、字型）
- 競爭差異化描述

#### 3c. 問答補充（填補剩餘空欄位）

針對仍為空的欄位，用以下結構化問題逐項詢問：

**基本資訊：**
- 你的品牌名稱是什麼？
- 用一句話形容你的品牌？（標語）
- 你的產業類別是什麼？

**品牌語氣：**
- 如果你的品牌是一個人，它的性格是什麼？（例：專業但親切、大膽創新、溫暖可靠）
- 在文案中絕對不能出現的用詞或語氣？

**目標受眾：**
- 你的主要客群是誰？（年齡、職業、特徵）
- 他們最大的痛點是什麼？
- 他們期望從你的產品/服務中得到什麼結果？

**視覺識別：**
- 品牌主色的 HEX 色碼？
- 輔色的 HEX 色碼？
- 品牌使用的字型名稱？

### Step 4: 整合與確認

將所有提取的資料整合成 `master-brand.yaml` 格式，向使用者展示：

```
以下是我從 [來源] 提取的品牌資料：

品牌名稱：___
標語：___
產業：___
語氣：___
...

請確認是否正確，或告訴我需要修改的地方。
```

### Step 5: 寫入檔案

使用者確認後，更新 `ai/brand/master-brand.yaml`。
只更新有新資料的欄位，保留使用者先前已填入的內容。

### Step 6: 驗證

重新讀取 `ai/brand/master-brand.yaml`，確認：
- 所有必填欄位已有值
- YAML 格式正確
- 語言規則符合（中文內容用繁體中文、英文欄位用英文）

回報填入完成度百分比。

---

## Required Fields（必填）

以下欄位必須在流程結束時有值：

| 欄位 | YAML 路徑 | 說明 |
|------|-----------|------|
| 品牌名稱 | `brand.name` | 品牌正式名稱 |
| 產業類別 | `brand.industry` | 所屬產業 |
| 語氣 | `brand.voice.tone` | 至少 2 項 |
| 可做 | `brand.voice.do` | 至少 2 項 |
| 不可做 | `brand.voice.do_not` | 至少 2 項 |
| 目標客群 | `brand.target_audience.segments` | 至少 1 組 |
| 客戶痛點 | `brand.target_audience.pain_points` | 至少 1 項 |

## Optional Fields（選填）

| 欄位 | YAML 路徑 |
|------|-----------|
| 品牌標語 | `brand.tagline` |
| 品牌個性 | `brand.voice.personality` |
| 主色 | `brand.visual.primary_color` |
| 輔色 | `brand.visual.secondary_color` |
| 字型 | `brand.visual.font_family` |
| 期望結果 | `brand.target_audience.desired_outcomes` |

---

## Extraction Principles

1. **優先使用已有來源**：能從網站或文件提取的，不要問使用者
2. **標注來源**：每筆提取的資料標注出處（URL 或文件名）
3. **不要編造**：提取不到的欄位直接留空，交由問答補充
4. **保持一致性**：提取結果要與 `master-brand.yaml` 現有欄位風格一致
5. **使用者確認**：所有提取結果都必須經使用者確認才寫入

## Error Handling

- 如果網站無法存取：跳過網站提取，改用問答
- 如果文件格式無法解析：通知使用者，改用問答
- 如果使用者跳過某個問題：將該欄位標記為「待補充」，不強迫填入
- 如果 YAML 寫入失敗：輸出 YAML 純文字，讓使用者手動貼入
