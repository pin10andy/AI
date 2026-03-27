# Validation Plan: Hillbed Tryout Booking PMax

## Purpose

定義 `hillbed × tryout booking` 這條候選 lane 在成為 supported capability 前，
必須完成哪些驗證。

## Phase 0: Input Readiness

| Gate | Pass Criteria |
|------|---------------|
| Landing page defined | 有明確的試躺預約承接頁面 |
| CTA alignment | 頁面首屏或主要區塊能承接 `預約門市試躺` |
| Store facts available | 若文案要寫門市/地區/流程，需有可核對事實 |

## Phase 1: Draft Brief Validation

| Gate | Pass Criteria |
|------|---------------|
| Brief schema validation | `lovefu-pmax-hillbed-tryout-booking-draft.json` 通過 `google-ads-brief.schema.json` |
| Purchase lane isolation | 不覆寫 `lovefu-pmax-hillbed.json` |
| Goal mapping clarity | 文件中清楚標示 `tryout booking -> store_visit` |
| Price signal control | draft brief 不把 `14,900起` 當主要 CTA |

## Phase 2: Output Validation

| Gate | Pass Criteria |
|------|---------------|
| Output schema validation | 通過 `google-ads-pmax-output.schema.json` |
| Format validation | `ad_copy_validator --exact-pmax-output` pass |
| Keyword-message fit | 至少 `3 short / 1 long / 1 desc` 命中 primary keywords |
| Angle coverage | 每個 angle 至少 `4 short / 1 long / 1 desc` |
| Human review | 至少 `可微調後上稿`，若要轉 supported 建議 `可直接上稿` |

## Phase 3: Lane-Specific Checks

| Gate | Pass Criteria |
|------|---------------|
| Booking CTA consistency | `預約門市試躺` 或同義 CTA 在 LP 與 copy 中一致 |
| No unsupported location claims | 未經證實前不得寫台北/門市地址等具體地區資訊 |
| Trust-vs-booking balance | 100天安心睡 / 10年保固 僅作信任輔助，不壓過主要 booking intent |
| Policy wording review | 試躺、放鬆、支撐類語句完成人工政策邊界檢查 |

## Phase 4: Support Readiness

| Gate | Pass Criteria |
|------|---------------|
| Golden brief approved | draft brief 升級為 canonical brief |
| Regression baseline established | 至少 2 筆 approved reference outputs |
| Runbook exists | 非作者可依文件重跑 |
| Registry update approved | 完成後才可新增到 `supported-matrix.yaml` |

## Exit Criteria

只有在以上 4 個 phase 全數通過後，
這條 lane 才能從 `draft candidate` 升級為 `supported capability`。
