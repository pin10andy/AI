---
name: "google-ads"
description: "Google Ads 帳戶管理技能套件。涵蓋搜尋字詞清洗、成效診斷、關鍵字研究、文案策略、素材成效解讀、素材池組建、上稿打包、LP 一致性檢查。當使用者提到 Google Ads、廣告帳戶、搜尋字詞、否定關鍵字、廣告文案、成效報表、ROAS、CPA、歷史成效分析、語言模式、legacy messaging、素材池、上稿素材包、打包上傳、交付素材等相關工作時觸發。"
license: MIT
metadata:
  version: 1.0.0
  author: Andy Chou
  category: google-ads
  updated: 2026-03-13
---

# Google Ads 帳戶管理技能套件

> **Canonical source**: `ai/skill-src/google-ads/SKILL.md`
> Do NOT edit copies in `.claude/skills/`, `.agents/skills/`, or `runtime/`.
> Always edit here and run `scripts/sync-skills.sh` to deploy.

## Required References

執行任何子技能前，先讀取：

1. **品牌設定**：`ai/brand/master-brand.yaml`
2. **共用 context**：`ai/memory/shared-context.yaml`

## 可用技能

| 技能 | 目錄 | 用途 |
|------|------|------|
| Search / PMax 文案生成 | `ai/skill-src/google-ads-writer/` | 從固定 brief 產出 Search RSA 或 PMax 文案包 |
| 搜尋字詞清洗 | `search-terms-cleaner/` | 分析搜尋字詞報表，產出否定字建議、新 ad group 建議、浪費預算分析 |
| 成效診斷 | `performance-reviewer/` | 週報摘要，保留/停用/擴量/測試四欄判斷，強制附具體原因 |
| 關鍵字研究 | `keyword-architect/` | 關鍵字分群、意圖分類、比對類型建議、landing page 配對 |
| 文案策略 | `ad-copy-builder/` | RSA/PMax 文案策略生成，含素材保留/替換/新測試三欄判斷 |
| 素材成效解讀 | `creative-performance-interpreter/` | 歷史素材成效分析，萃取高價值語言模式，保護 Legacy Messaging，產出下輪 brief 的繼承限制 |
| 素材池組建 | `ad-copy-portfolio-builder/` | 消費 interpreter 輸出，整合 retain/retire/new_candidate 為可直接上稿的素材池，分離主力與測試 |
| 上稿打包 | `upload-packager/` | 消費 portfolio builder 輸出，整理成可交付 PM / 投手 / 客戶的最終素材包，含操作清單與字數審核 |
| Creative 稽核 | `creative-auditor/` | 稽核既有素材池或 final pack 的 asset sufficiency、creative diversity、product drift、policy risk 與 platform fit，作為 preflight gate 或 challenger review |
| LP 一致性檢查 | `lp-alignment-auditor/` | 關鍵字—廣告文案—頁面三層一致性稽核，找出漏斗斷點 |

## 路由規則

根據使用者需求路由到對應子技能，執行其 SKILL.md 中的步驟：

- 提到「從 brief 直接產生 Search RSA」「15 個標題」「4 個說明」「3 個 angle」→ 執行 `ai/skill-src/google-ads-writer/SKILL.md`
- 提到「從 brief 直接產生 PMax」「短標題」「長標題」「asset group 文案」→ 執行 `ai/skill-src/google-ads-writer/SKILL.md`
- 提到「搜尋字詞」「否定關鍵字」「negative keyword」「字詞清洗」→ 執行 `search-terms-cleaner/SKILL.md`
- 提到「成效」「週報」「報表分析」「KPI」→ 執行 `performance-reviewer/SKILL.md`
- 提到「關鍵字研究」「分群」「keyword research」→ 執行 `keyword-architect/SKILL.md`
- 提到「哪些標題要換」「Ad Strength 太低」「PMax 素材」→ 執行 `ad-copy-builder/SKILL.md`
- 提到「歷史成效分析」「哪些文案有效」「語言模式」「legacy messaging」「素材決策」「文案承接」「高價值語言」→ 執行 `creative-performance-interpreter/SKILL.md`
- 提到「組建素材池」「下一輪上稿」「退場替換」「素材包整合」「portfolio」「可上稿素材」→ 執行 `ad-copy-portfolio-builder/SKILL.md`
- 提到「上稿素材包」「打包上傳」「交付素材」「上稿格式」「操作清單」「upload package」→ 執行 `upload-packager/SKILL.md`
- 提到「creative audit」「素材疲乏」「asset 不足」「final pack 審查」「上稿前再檢查」「creative preflight」→ 執行 `creative-auditor/SKILL.md`
- 提到「LP」「landing page」「一致性」「漏斗斷點」→ 執行 `lp-alignment-auditor/SKILL.md`

---

## Artifact Governance

所有子技能產出的正式 artifact 必須遵循以下治理政策：

| 政策 | 檔案 |
|------|------|
| 存儲映射 | `ai/registry/storage-map.yaml` |
| 命名規範 | `ai/policies/artifact-naming-policy.md` |
| 寫入規範 | `ai/policies/artifact-write-policy.md` |
| Artifact 登記 | `ai/registry/artifacts.yaml` |

### 核心規則

1. **正式輸出**寫入 `ai/outputs/google-ads/{brand}/{product}/{lane}/` 對應子目錄
2. **暫存/測試輸出**寫入 `scratch/google-ads/`，禁止放在 `ai/outputs/`
3. **驗證報告**寫入 `ai/validation/`，命名 `YYYY-MM-DD-{slug}.md`
4. **分析報告**寫入 `ai/reports/`，命名 `YYYY-MM-DD-{slug}.md`
5. **禁止**將任何輸出寫入 repo 根目錄
6. 所有正式 artifact 必須在 `ai/registry/artifacts.yaml` 登記
7. 完成後執行 `python3 scripts/check_artifact_governance.py` 確認合規
