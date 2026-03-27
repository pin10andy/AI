# Google Ads Human Review Checklist

> 用途：5 分鐘內判斷這組 Search RSA 文案能不能進下一步。
> 適用：`ai/schemas/google-ads-search-output.schema.json`

## Review Fields

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| 是否符合品牌語氣 | 是 / 否 | 是否有 LOVEFU 的溫柔、安心、陪伴感 |
| 是否有 3 種以上不同訴求 | 是 / 否 | angle 是否真的不同，不是換句話說 |
| 是否避免違規宣稱 | 是 / 否 | 是否出現治療、保證、誇大、最低價等 |
| 是否有商業意圖 | 是 / 否 | 是否能推動點擊、了解、預約、試躺、購買 |
| 是否可直接上稿 | 是 / 否 | 是否只需極小修改即可丟進 Google Ads |
| 是否重複感過高 | 是 / 否 | 這一欄若為「是」，通常不可直接上稿 |

## Fast Decision Rule

- `可直接上稿`：前五項至少 4 項為「是」，且「是否重複感過高」為「否」
- `可微調後上稿`：品牌語氣、商業意圖、違規宣稱三項都過，但仍有重複或角度不夠開
- `需重寫`：有違規宣稱、品牌語氣明顯跑掉，或 headline 幾乎都在說同一句話

## Reviewer Notes

- 哪 2-3 個 headlines 最能代表品牌？
- 哪 2-3 個 headlines 最像模板腔或重複？
- 哪個 description 最接近 LP 首屏？哪個最需要改？
- 若要上稿，優先 pin 哪個品牌字或 CTA？
