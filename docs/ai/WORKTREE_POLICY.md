# Worktree Policy

## Purpose

Keep non-trivial execution isolated from the primary branch while preserving a
single canonical repository.

## Policy

### Non-trivial changes

Use an isolated git worktree when the work includes any of the following:

- multiple file edits
- governance or template changes
- new scripts
- adapter updates
- any change that should leave change / validation artifacts

### Trivial changes

Single-file typo or formatting fixes may stay on the primary checkout, unless a
task explicitly requires branch isolation.

## One Active Execution Branch

Do not work on multiple execution branches for the same task at the same time.
One task should have one primary execution branch.

## Recommended Workflow

1. create branch and worktree
2. implement changes in the worktree only
3. run validation from the worktree
4. update task / change / validation artifacts
5. merge or cherry-pick only after review

## Naming

Recommended branch pattern:

`feat/<short-scope>`

Recommended worktree path pattern:

`../ai-worktrees/<short-scope>`

## Ownership

The execution owner is responsible for:

- keeping the worktree scoped to one task
- not mixing unrelated changes
- cleaning up the worktree after merge or abandonment

## Canonical Files

Worktrees do not create a second source of truth.
All canonical paths remain inside the repository itself.

## Validation Gate

Non-trivial work is not ready to hand off until validation evidence exists in the repo.
