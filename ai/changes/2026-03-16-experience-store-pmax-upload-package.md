# Change Record: Experience Store PMax Upload Package

## Related Task

`2026-03-16-experience-store-pmax-upload-package` / `ai/tasks/2026-03-16-experience-store-pmax-upload-package.yaml`

## Summary

這次改動把三店合併 booking PMax 的 builder 結果，整理成投手可直接用的 upload-view package。
重點不是再生成新文案，而是把現有 15/5/5 拆成 `主力先上 / 測試保留 / 先不要上`，
並把推薦 LP 與不要誤導到的 product LP 一起寫進 handoff。

## Files Created

- `ai/tasks/2026-03-16-experience-store-pmax-upload-package.yaml`
- `ai/changes/2026-03-16-experience-store-pmax-upload-package.md`
- `ai/validation/2026-03-16-experience-store-pmax-upload-package.md`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-upload-package/input.json`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/pipeline/2026-03-16-experience-store-pmax-upload-package/packager.md`
- `ai/outputs/google-ads/lovefu/experience-store/evergreen-store-visit-pmax/deliverables/2026-03-16-experience-store-pmax-upload-package.deliverable.md`

## Files Updated

- `ai/registry/artifacts.yaml`

## Files Removed

無

## Sync / Deployment Impact

- 無 deployment 影響
- 只是新增 booking lane 的 upload-view package 與 deliverable registry entry

## Open Issues

- 目前 deliverable 仍是 markdown handoff，不是 xlsx / csv upload sheet
- 若投手要做地區拆版，仍需再從 generic package 分出 store-specific 版本
