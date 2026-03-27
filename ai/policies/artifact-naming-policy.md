# Artifact Naming Policy — Google Ads

> **Scope**: Google Ads workflow outputs only.
> **Effective**: 2026-03-16
> **Related files**:
> - Storage map: `ai/registry/storage-map.yaml`
> - Artifact registry: `ai/registry/artifacts.yaml`
> - Write policy: `ai/policies/artifact-write-policy.md`

---

## 1. General rules

| Rule | Detail |
|------|--------|
| Character set | lowercase ASCII, digits, hyphens only |
| Separator | hyphen `-` (no underscores, no spaces, no CJK) |
| Extension | `.json`, `.md`, `.yaml`, `.xlsx`, `.csv` |
| Max length | 80 characters (excluding extension) |
| Encoding | UTF-8 throughout |

**Forbidden in filenames**: uppercase letters, spaces, underscores, CJK characters, special symbols.

---

## 2. ID formats

### brief_id

Format: `{brand}-{campaign_type}-{product}`

| Segment | Rule | Example |
|---------|------|---------|
| brand | brand slug from `master-brand.yaml` | `lovefu` |
| campaign_type | `pmax`, `search`, `display` | `pmax` |
| product | product slug, kebab-case | `hillbed` |

Example: `lovefu-pmax-hillbed`

### lane_id

Format: `{message_scope}-{goal}-{campaign_type}`

| Segment | Rule | Example |
|---------|------|---------|
| message_scope | `evergreen`, `seasonal`, `promo` | `evergreen` |
| goal | `purchase`, `lead`, `store-visit` | `purchase` |
| campaign_type | same as brief_id | `pmax` |

Example: `evergreen-purchase-pmax`

### task_id

Format: `YYYY-MM-DD-{slug}`

Matches the task filename in `ai/tasks/`. The slug should be descriptive and kebab-case.

Example: `2026-03-15-pipeline-v1-2-uat`

---

## 3. Filename patterns by artifact type

### Golden output

```
{brief_id}.output.{json|md}
```

- One per lane (JSON is authoritative, MD is companion)
- Example: `lovefu-pmax-hillbed.output.json`

### Approved reference

```
{brief_id}.ref-{nn}.output.{json|md}
```

- `{nn}` = zero-padded sequence number (01, 02, 03...)
- Example: `lovefu-pmax-hillbed.ref-03.output.json`

### Pipeline stage output

```
{stage}.{json|md}
```

- Files live inside a task directory: `pipeline/{task_id}/`
- Stage names: `input`, `builder`, `interpreter`, `interpretation`, `packager`, `portfolio`
- Example: `pipeline/2026-03-15-pipeline-v1-2-uat/builder.json`

### ~~Dry-run~~ (removed 2026-03-16)

Cross-agent validation outputs are now classified as **approved-reference**.
Use the approved reference naming pattern with the next available sequence number.
Scratch/test outputs go to `scratch/google-ads/` with no naming governance.

### Deliverable

```
{task_id}.deliverable.{ext}
```

- For final upload-ready files (xlsx, csv, etc.)
- Example: `2026-03-15-rsa-copy.deliverable.xlsx`

### Validation

```
YYYY-MM-DD-{slug}.md
```

- Stored in `ai/validation/`, not in `ai/outputs/`
- Example: `2026-03-15-google-ads-copy-pipeline-v1-2-rerun.md`

### Report

```
YYYY-MM-DD-{slug}.md
```

- Stored in `ai/reports/`, not in `ai/outputs/`
- Example: `2026-03-15-hillbed-pmax-wording-risk-watchlist.md`

---

## 4. Path composition

Full path = `ai/outputs/google-ads/{brand}/{product}/{lane}/{artifact_type}/{filename}`

Example:
```
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/golden/lovefu-pmax-hillbed.output.json
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/pipeline/2026-03-15-pipeline-v1-2-uat/builder.json
ai/outputs/google-ads/lovefu/hillbed/evergreen-purchase-pmax/deliverables/2026-03-15-rsa-copy.deliverable.xlsx
```

---

## 5. Scratch / temp files

Scratch files go to `scratch/google-ads/` and have **no naming governance**.
They are explicitly excluded from the artifact registry.

Agents may use any naming convention in scratch, but should avoid names that
could be confused with formal artifact patterns.

---

## 6. Anti-patterns (explicitly forbidden)

| Anti-pattern | Why |
|-------------|-----|
| `LoveFu_pipeline_v1-1_rerun_builder.json` | Underscores, CamelCase, repo root |
| `LoveFu_山丘樂眠床_RSA新文案.xlsx` | CJK in filename, repo root |
| Writing outputs to repo root | No governance, no discoverability |
| Flat dump in `ai/outputs/` | No brand/product/lane hierarchy |
| Pipeline files without task directory | Loses task traceability |

---

## 7. Multi-agent compliance

All agents (Claude, Codex, Gemini, OpenClaw) MUST follow this policy.
The policy is referenced from:

- `ai/registry/storage-map.yaml` (where to write)
- `ai/policies/artifact-write-policy.md` (how to write)
- Each agent's skill definitions (should reference this policy)

When an agent produces a formal output, it must:
1. Follow this naming convention
2. Write to the path defined in `storage-map.yaml`
3. Register the artifact in `artifacts.yaml`
