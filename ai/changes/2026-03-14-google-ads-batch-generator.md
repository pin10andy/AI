# Change Record: Google Ads 文案批次生成工具

## Related Task

`ai/tasks/2026-03-14-google-ads-batch-generator.yaml` (`gads-copy-003`)

## Summary

新增 `google-ads-writer` 的批次生成腳本，讓團隊可直接讀取多份 Search RSA / PMax brief，
一次產出對應的 JSON + Markdown 草稿。這次也同步把 batch usage 寫回 skill 文件，
讓同一套流程可由 Codex、Claude 與其他 agent 重複使用。

## Files Created

- `ai/tasks/2026-03-14-google-ads-batch-generator.yaml`
- `ai/skill-src/google-ads-writer/scripts/batch_generate_ads_copy.rb`

## Files Updated

- `ai/skill-src/google-ads-writer/SKILL.md`
  - 新增 `Batch Use` 段落
  - 補上批次生成指令範例與工具定位說明

## Files Removed

無

## Sync / Deployment Impact

已執行：

```bash
bash scripts/sync-skills.sh
```

已同步更新：

- `.claude/skills/`
- `.agents/skills/`
- `runtime/openclaw/`

## Open Issues

- 目前批次工具是規則式 draft generator，不是 LLM 品質最佳化器
- 輸出仍需經 `ai/evals/google-ads-human-review.md` 或 `ai/evals/google-ads-pmax-human-review.md` 人工複核
- 目前輸出寫入指定資料夾，不會自動回填到正式 release artifact 或 dashboard
