# Google Ads PMax Human Review Checklist

> 用途：快速判斷這組 PMax 文案能不能進下一步。
> 適用：`ai/schemas/google-ads-pmax-output.schema.json`

## Review Fields

| 檢查項目 | 結果 | 備註 |
|---------|------|------|
| 是否符合品牌語氣 | 是 / 否 | 是否有 LOVEFU 的溫柔、安心、陪伴感 |
| 是否有 3 種以上不同訴求 | 是 / 否 | angle 是否真的不同 |
| 是否避免違規宣稱 | 是 / 否 | 有無醫療、保證、最低價等 |
| Short headlines 是否夠分散 | 是 / 否 | 是否能支援 PMax 重組，而非一直講同一句 |
| Long headlines 是否有補充價值 | 是 / 否 | 是否不是短標題加長版 |
| Descriptions 是否可直接上稿 | 是 / 否 | 是否語意完整且可被重組 |
| 是否重複感過高 | 是 / 否 | 若為是，通常不可直接上稿 |

## Fast Decision Rule

- `可直接上稿`：前六項至少 5 項為「是」，且最後一項為「否」
- `可微調後上稿`：品牌語氣、違規宣稱、short headlines 分散度三項都過，但長標題或說明仍需微調
- `需重寫`：訴求角度不成立、素材過度重複，或有明顯違規風險
