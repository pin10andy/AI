# Google Ads Writer Skill

> **Canonical source**: `ai/skill-src/google-ads-writer/SKILL.md`
> Do NOT edit copies in `.claude/skills/`, `.agents/skills/`, or `runtime/`.
> Always edit here and run `scripts/sync-skills.sh` to deploy.

## Purpose

Build a working **Google Ads copy generation workflow** from a fixed brief.

Supported outputs:

- `search_rsa`
- `pmax`

## When to Use

- User wants a brand-new Search RSA bundle from a brief
- User wants a brand-new PMax copy pack from a brief
- User provides a testcase or brief file and wants the same workflow reused
- User wants a repeatable copywriting contract across Claude / Codex / Gemini

If the user wants to optimize existing ads, replace weak headlines, or work on PMax assets, use `ai/skill-src/google-ads/ad-copy-builder/SKILL.md` instead.

## Required References

Before generating any output, load these files:

1. **Brand rules**: `ai/brand/master-brand.yaml`
2. **Brief schema**: `ai/inputs/google-ads-brief.schema.json`
3. **Pick one playbook based on `campaign_type`**:
   - `search_rsa` → `ai/playbooks/google-ads-search-rsa.md`
   - `pmax` → `ai/playbooks/google-ads-pmax.md`
4. **Pick one output schema based on `campaign_type`**:
   - `search_rsa` → `ai/schemas/google-ads-search-output.schema.json`
   - `pmax` → `ai/schemas/google-ads-pmax-output.schema.json`
5. **Self-check rubric**: `ai/evals/ads-rubric.yaml`
6. **Human review checklist**:
   - `search_rsa` → `ai/evals/google-ads-human-review.md`
   - `pmax` → `ai/evals/google-ads-pmax-human-review.md`
7. **Markdown template**:
   - `search_rsa` → `ai/skill-src/google-ads-writer/templates/search-rsa-output.md`
   - `pmax` → `ai/skill-src/google-ads-writer/templates/pmax-output.md`

## Required Input Format

Preferred input is a JSON or YAML brief that conforms to `ai/inputs/google-ads-brief.schema.json`.

If the user gives freeform requirements, first normalize them into the same brief contract before generating copy.

## Execution Steps

### Step 1: Validate the brief

Read the brief and confirm it contains:

- `brand_name`
- `product_name`
- `campaign_type`
- `goal`
- `landing_page_summary`
- `target_audience`
- `keyword_cluster`
- `usp`
- `offers`
- `constraints`
- `tone`
- `forbidden_claims`

Do not skip missing fields silently. If a field is absent, map what the user gave into the contract first.
Then read `campaign_type` and route the rest of the workflow.

### Step 2: Load brand constraints

```
Read ai/brand/master-brand.yaml
Apply voice.tone, voice.do, voice.do_not rules
Apply language rules
```

Priority order when brief and brand context overlap:

1. `master-brand.yaml` safety / voice constraints
2. brief-specific product and landing page facts
3. testcase notes

### Step 3: Derive exactly 3 distinct angles

Generate the angles **before** writing copy.

Each angle must include:

- `key`
- `label`
- `rationale`

Angle requirements:

- exactly 3 angles
- each angle must be meaningfully different
- each angle must map back to the brief or brand evidence
- avoid producing 3 CTA-only angles

### Step 4: Generate assets by campaign type

If `campaign_type = search_rsa`:

- generate 15 headlines
- generate 4 descriptions
- headline <= 30 chars
- description <= 90 chars

If `campaign_type = pmax`:

- generate 15 short headlines
- generate 5 long headlines
- generate 5 descriptions
- short headline <= 30 chars
- long headline <= 90 chars
- description <= 90 chars
- at least 1 description <= 60 chars

Shared rules:

- at least 3 primary-keyword assets
- all marketing copy must be in Traditional Chinese
- no forbidden claims
- no low-price / bargain language
- every angle must be used by multiple assets

### Step 5: Format JSON output

Output must conform to the schema that matches `campaign_type`.

Required metadata:

- `task_id`
- `brief_id`
- `generated_by`
- `generated_at`

### Step 6: Render a human-readable version

Render the same result as Markdown using the matching template.

This Markdown is for PM / human review only. JSON remains the source-of-truth output.

### Step 7: Self-check before finalizing

Evaluate against:

- `ai/evals/ads-rubric.yaml`
- the human review checklist that matches `campaign_type`

If possible, run the format validator:

```bash
python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py \
  --file {output_json_path} \
  --exact-search-output
```

or

```bash
python3 ai/skill-src/google-ads/ad-copy-builder/scripts/ad_copy_validator.py \
  --file {output_json_path} \
  --exact-pmax-output
```

If any check fails, revise before returning output.

## Output Format

Return two artifacts:

1. JSON conforming to the schema that matches `campaign_type`
2. Markdown following the template that matches `campaign_type`

## Batch Use

If you want to turn multiple briefs into first-draft output files, use:

```bash
ruby ai/skill-src/google-ads-writer/scripts/batch_generate_ads_copy.rb \
  --output-dir /tmp/google-ads-batch \
  ai/testcases/google-ads/*search.yaml \
  ai/testcases/google-ads/*pmax.yaml
```

This script is a **draft generator**, not a replacement for human review.

## Quality Gates

- Exactly 3 angles
- `search_rsa`: exactly 15 headlines + 4 descriptions
- `pmax`: exactly 15 short headlines + 5 long headlines + 5 descriptions
- All character limits must be met
- `manual_review_required` must be `true`
- Overall rubric score >= 3.5
- Language must match `master-brand.yaml > languages` rules
- No brand voice violations
- No policy-risk copy disguised as a benefit

---

## Artifact Governance

本技能產出的 JSON 與 Markdown 是正式 artifact，必須遵循治理政策。

### 輸出路徑

| 類型 | 路徑 |
|------|------|
| Golden output | `ai/outputs/google-ads/{brand}/{product}/{lane}/golden/{brief_id}.output.{json\|md}` |
| Approved reference | `ai/outputs/google-ads/{brand}/{product}/{lane}/approved-references/{brief_id}.ref-{nn}.output.{json\|md}` |
| Scratch/test | `scratch/google-ads/`（非正式，不登記） |

**禁止**將輸出寫入 repo 根目錄或 `ai/outputs/` 根層。

### 命名規則

- 全小寫、kebab-case、ASCII only
- Golden: `{brief_id}.output.{json|md}`
- Reference: `{brief_id}.ref-{nn}.output.{json|md}`
- 詳見 `ai/policies/artifact-naming-policy.md`

### 寫入後必須

1. 在 `ai/registry/artifacts.yaml` 登記（含所有必填欄位）
2. 執行 `python3 scripts/check_artifact_governance.py` 確認合規

### 政策參考

- `ai/registry/storage-map.yaml`
- `ai/policies/artifact-naming-policy.md`
- `ai/policies/artifact-write-policy.md`
