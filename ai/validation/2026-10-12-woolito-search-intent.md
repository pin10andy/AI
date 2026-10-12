# Validation — 2026-10-12-woolito-search-intent

Canonical：[OS #47](https://github.com/pin10andy/personal-operating-dashboard/issues/47)。
Level 3（bounded synthetic domain validation）；真實帳戶結論 BLOCKED_ON_ACCOUNT_DATA。

- `python3 -m unittest discover -s ai/skill-src/google-ads/search-terms-cleaner/tests -v` — 9 tests PASS。
  指定 KEEP/REVIEW、僅全查詢 exact 候選、歷史＋跨列可見轉換、positive 衝突、缺檢查資料、negative scopes、coverage、重複 grain/date/metric 拒收。
- `python3 ai/skill-src/google-ads/search-terms-cleaner/scripts/woolito_intent_diagnostic.py ai/skill-src/google-ads/search-terms-cleaner/assets/woolito-synthetic --output-dir scratch/google-ads/woolito-synthetic` — PASS。
  source=synthetic、account_conclusion=BLOCKED_ON_ACCOUNT_DATA、coverage_status=CONFIRMED、live_write_go=NO_GO；21 列 11 KEEP / 6 REVIEW / 4 exact candidates。
- `bash scripts/sync-skills.sh` — PASS，本隔離 checkout ignored 複本可再生；沒有正式部署。
- `python3 scripts/check_artifact_governance.py` — PASS：92 passed / 0 failed / 14 existing legacy warnings。
  clone 初始無 ignored scratch directory，首次為 2 FAIL；建立 scratch/google-ads 後通過，不改政策。
- `python3 scripts/validate_task_artifacts.py --repo-root . --task ai/tasks/2026-10-12-woolito-search-intent.yaml --change ai/changes/2026-10-12-woolito-search-intent.md --validation ai/validation/2026-10-12-woolito-search-intent.md` — PASS。
- `git diff --check` — PASS。

無 UI/E2E、無多輪審稿、無 Ads API 呼叫或 live mutation。
有限核對 AI 及 Creative Workbench 本機未提交成果；無同範圍 active Builder；GitHub AI issues/PR 再查為空。
Google 官方 negative keyword 文件已核對；search terms 文件 fetch 失敗，hidden-tail 限制按 Issue 記錄。
Known limits：有限規則字庫、未知中文詞降 REVIEW、未模擬正向近似／語意扩張、negative tokenization，
manual review mandatory。synthetic coverage 不能代表真實帳戶資料完整性；manifest 的宣告需 owner 核實。


## 真實資料 bounded rerun

同一CLI在私有 normalized input 跑通：source=account、account_conclusion=MANUAL_DIAGNOSIS_REQUIRED、
coverage_status=CONFIRMED（僅已宣告 enabled範圍）、live_write_go=NO_GO。
原始11,888 rows → 11,887正規化日列；4×90 campaign totals；44 enabled positives；2941 negative checks；168 historical conversion rows。
日期齊全、原始 grain無重複／缺指標、group ID joins完整；未補造0；daily/period總計差額保留。
Engine232 KEEP /11655 REVIEW/0 confirmed candidates；另有私有人工核對4 paid exact proposals，全部REVIEW。
首次大資料CLI因重複 norm 耗時，已中止該進程；2行等價conversion-first與非零history追加修正後實帳CLI完成。
對實际變更重跑原9 focused tests PASS；沒有新UI/E2E或重複審稿。
公開資料僅匿名摘要與hash，完整report/候選與raw只有本機private目錄。No Ads mutations/OAuth/merge/deploy。
