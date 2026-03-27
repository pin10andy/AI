# PRD: Multi-Agent Operating System

## Document Status

- Status: draft-for-implementation
- Owner: execution team
- Scope: repository operating model only

## Problem

The repository already contains a working multi-agent workspace, but the operating
rules are scattered across adapter files, task records, templates, and
domain-specific governance documents. Execution can proceed, but the operating
pack is not yet represented as a single, reviewable set of canonical documents
for implementation teams.

## Goal

Turn the existing multi-agent workspace into a repo-native operating system that:

1. exposes the canonical execution model in stable documents under `docs/ai/`
2. keeps `ai/` as the source of truth for domain rules, artifacts, and runtime records
3. keeps agent adapters thin
4. makes task -> change -> validation handoff executable through artifacts
5. supports isolated execution branches for non-trivial work

## Non-Goals

- redesign the product direction
- replace existing Google Ads governance
- introduce a new orchestration framework
- move domain knowledge out of `ai/`
- treat chat history as a formal source of truth

## Primary Users

- Human PM / reviewer
- Claude
- Codex
- Gemini
- OpenClaw

## Canonical Source Hierarchy

### Operating-pack docs

Repository-level operating docs live in `docs/ai/`.

### Domain and runtime truth

The following remain canonical in `ai/`:

- brand and shared context
- playbooks
- schemas and evals
- task / change / validation records
- artifact governance
- skill source

## Functional Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-001 | Thin adapters | Agent-specific files point to canonical docs instead of restating them | `AGENTS.md` and `CLAUDE.md` reference shared docs and remain thin |
| FR-002 | Artifact-only handoff | Work can be handed over through repo artifacts without chat dependency | Handoff protocol exists and maps to task/change/validation chain |
| FR-003 | Template entrypoints | Contributors can find the correct template from a stable location | `docs/ai/templates/` contains the requested template entry files |
| FR-004 | Worktree discipline | Non-trivial work is isolated from the primary branch | Worktree policy exists and is referenced by adapters |
| FR-005 | Validation discipline | Work is not marked done without evidence | Validation levels exist and at least one validation script can check artifact linkage |

## Process Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| WF-001 | Implementation-first workflow | Execution follows existing backlog and canonical docs rather than inventing new flows | New docs explicitly reference existing canonical files |
| WF-002 | Task chain | Meaningful changes follow task -> decision(optional) -> change -> validation | Handoff protocol and templates align to this chain |
| WF-003 | Minimal tooling | Only minimal scripts needed to validate workflow integrity are added | New validation script is stdlib-only and runnable from repo root |

## Design Constraints

- Do not duplicate domain governance already defined under `ai/`
- Do not create a second storage map, naming policy, or artifact registry
- Prefer references over copied rules
- Default to the smallest viable file or script that lets the workflow run

## Success Criteria

- `docs/ai/` contains operating-pack canonical docs
- `AGENTS.md` and `CLAUDE.md` are thin adapters
- template entrypoints exist for task, ADR, change, review, and validation
- at least one task / change / validation round can be linked and checked inside the repo

## Evidence Sources

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `ai/tasks/`
- `ai/changes/`
- `ai/validation/`
- `ai/policies/`
- `ai/registry/`
- `scripts/`
