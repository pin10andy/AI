# Validation Levels

## Purpose

Provide a shared vocabulary for how complete a validation pass is.

## Levels

### Level 0 — Artifact Exists

Confirms files exist at the expected canonical paths.

Typical checks:

- file existence
- directory existence
- template presence

### Level 1 — Structural Integrity

Confirms files are parseable and linked correctly.

Typical checks:

- YAML / JSON parse
- task -> change -> validation linkage
- adapter references resolve to canonical docs

### Level 2 — Workflow Smoke Test

Confirms the intended repo workflow runs at least once.

Typical checks:

- `bash scripts/sync-skills.sh`
- `python3 scripts/check_artifact_governance.py`
- `python3 scripts/validate_task_artifacts.py ...`

### Level 3 — Domain Validation

Confirms the task-specific workflow produces acceptable outputs under its own
playbook, schema, rubric, or human review standard.

Typical checks:

- schema validation
- report review
- governed artifact check
- domain-specific rerun

## Completion Rule

The required level depends on task scope:

- docs-only structure work: usually Level 1 or 2
- workflow implementation: at least Level 2
- production-facing domain changes: Level 3

## Reporting Rule

Every validation record should state:

- the highest level reached
- commands run
- evidence used
- remaining risks
