# Change Record: Google Ads Copy Pipeline v1.2 Input / Observe / Candidate / Taxonomy Upgrade

## Related Task

`gads-pipeline-012` / `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-2.yaml`

## Summary

將 Google Ads copy pipeline 的三個 skill 升級到 v1.2，集中修正 richer input layers、observe 子類別、candidate pipeline automation、與 angle taxonomy 標準化。並以 LOVEFU / 山丘樂眠床案例重寫 sample input、sample run 與 rerun checklist。

## Files Created

- `ai/tasks/2026-03-15-google-ads-copy-pipeline-v1-2.yaml`
- `ai/decisions/ADR-005-google-ads-copy-pipeline-v1-2-data-observe-taxonomy.md`
- `ai/validation/2026-03-15-google-ads-copy-pipeline-v1-2-rerun.md`
- `ai/changes/2026-03-15-google-ads-copy-pipeline-v1-2.md`

## Files Updated

- `ai/inputs/creative-performance-input.schema.json`
- `ai/schemas/creative-performance-output.schema.json`
- `ai/inputs/ad-copy-portfolio-input.schema.json`
- `ai/schemas/ad-copy-portfolio-output.schema.json`
- `ai/inputs/upload-packager-input.schema.json`
- `ai/schemas/upload-packager-output.schema.json`
- `ai/inputs/lovefu-pmax-hillbed-performance.json`
- `ai/skill-src/google-ads/creative-performance-interpreter/SKILL.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/SKILL.md`
- `ai/skill-src/google-ads/upload-packager/SKILL.md`
- `ai/skill-src/google-ads/creative-performance-interpreter/references/decision-rules.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/references/decision-rules.md`
- `ai/skill-src/google-ads/upload-packager/references/decision-rules.md`
- `ai/skill-src/google-ads/creative-performance-interpreter/templates/interpretation-report.md`
- `ai/skill-src/google-ads/ad-copy-portfolio-builder/templates/portfolio-report.md`
- `ai/skill-src/google-ads/upload-packager/templates/upload-package-report.md`
- `ai/playbooks/google-ads-creative-interpretation.md`
- `ai/evals/creative-performance-rubric.yaml`
- `ai/evals/ad-copy-portfolio-rubric.yaml`
- `ai/evals/upload-packager-rubric.yaml`

## Files Removed

- 無

## Sync / Deployment Impact

- 需重新同步 skills 到 `.agents/skills/` / 其他 agent runtime 才會生效
- schema contract 已變更為 v1.2，舊 sample / 舊 payload 不再視為完整 input

## Open Issues

- 目前仍是 sample rerun 與 static validation，尚未接上真實 brief generator runtime
- `association_proxy_only` fallback 仍保留，表示 pipeline 仍需兼容較差的歷史報表
- final pack 的實際成效仍需等真實上稿回饋，不能只靠 sample run 判定
