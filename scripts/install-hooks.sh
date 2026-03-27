#!/usr/bin/env bash
# install-hooks.sh
# Installs versioned git hooks from scripts/hooks/ into .git/hooks/
#
# Usage:
#   bash scripts/install-hooks.sh
#
# This script is idempotent — safe to run multiple times.
# It will back up any existing hooks before overwriting.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_SRC="${REPO_ROOT}/scripts/hooks"
HOOKS_DST="${REPO_ROOT}/.git/hooks"

echo "=== Install Git Hooks ==="
echo "Source: ${HOOKS_SRC}"
echo "Target: ${HOOKS_DST}"
echo ""

if [ ! -d "$HOOKS_SRC" ]; then
    echo "Error: hooks source directory not found: ${HOOKS_SRC}"
    exit 1
fi

if [ ! -d "$HOOKS_DST" ]; then
    echo "Error: .git/hooks directory not found — are you in a git repo?"
    exit 1
fi

installed=0

for hook in "${HOOKS_SRC}"/*; do
    hook_name=$(basename "$hook")

    # Skip non-files
    [ ! -f "$hook" ] && continue

    target="${HOOKS_DST}/${hook_name}"

    # Back up existing hook if it differs
    if [ -f "$target" ]; then
        if diff -q "$hook" "$target" > /dev/null 2>&1; then
            echo "  [skip] ${hook_name} (already up to date)"
            continue
        else
            backup="${target}.backup.$(date +%Y%m%d%H%M%S)"
            cp "$target" "$backup"
            echo "  [backup] ${hook_name} → $(basename "$backup")"
        fi
    fi

    cp "$hook" "$target"
    chmod +x "$target"
    echo "  [installed] ${hook_name}"
    installed=$((installed + 1))
done

echo ""
if [ "$installed" -eq 0 ]; then
    echo "All hooks already up to date."
else
    echo "Installed ${installed} hook(s)."
fi
echo ""
echo "Hooks are now active. To verify:"
echo "  ls -la .git/hooks/pre-commit"
echo "  ls -la .git/hooks/post-commit"
echo ""
echo "To test the pre-commit hook:"
echo "  python3 scripts/check_artifact_governance.py"
echo ""
echo "To test the post-commit hook notification:"
echo "  .git/hooks/post-commit"
