# Change Record: Google Ads Copy Pipeline v1.1 Contract Upgrade

## Related Task

`gads-pipeline-011` / `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-1.yaml`

## Summary

將 Google Ads copy pipeline 的三個 skill 升級到 v1.1，集中修正 legacy 建模、decision basis / confidence、以及 builder / packager 的 field-level handoff contract。並以 LOVEFU / 山丘樂眠床案例重寫 sample run 與 E2E validation。

## Files Created

- `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-1.yaml`
- `ai/decisions/ADR-004-google-ads-copy-pipeline-v1-1-contracts.md`
- `ai/validation/2026-03-15-google-ads-copy-pipeline-v1-1-e2e.md`
- `ai/changes/2026-03-15-google-ads-copy-pipeline-v1-1.md`

## Files Updated

- `ai/inputs/creative-performance-input.schema.json`
- `ai/schemas/creative-performance-output.schema.json`
- `ai/inputs/ad-copy-portfolio-input.schema.json`
- `ai/schemas/ad-copy-portfolio-output.schema.json`
- `ai/inputs/upload-packager-input.schema.json`
- `ai/schemas/upload-packager-output.schema.json`
- `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/SKILL.md`
- `ai/skill-src/google-ads/upload-packager/SKILL.md`
- `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/references/decision-rules.md`
- `ai/skill-src/google-ads/upload-packager/references/decision-rules.md`
- `ai/playbooks/google-ads-creative-interpretation.md`
- `ai/evals/creative-performance-rubric.yaml`
- `ai/evals/ad-copy-portfolio-rubric.yaml`
- `ai/evals/upload-packager-rubric.yaml`

## Files Removed

- 無

## Sync / Deployment Impact

- 需重新同步 skills 到 `.agents/skills/` / 其他 agent runtime 才會生效
- schema contract 已變更為 v1.1，舊 sample / 舊 handoff payload 不再視為完整 input

## Open Issues

- 尚未把 v1.1 sample run 落成獨立的 JSON output artifact
- 尚未把其他 Google Ads 子技能一起升級到相同 legacy / contract 語意
