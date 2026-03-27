#!/usr/bin/env bash
# sync-skills.sh
# 將 ai/skill-src/ 中的 skill 同步到各工具的部署目錄
# 這是唯一正確的 skill 部署方式 — 請勿手動複製

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_SRC="${REPO_ROOT}/ai/skill-src"

# 部署目標
CLAUDE_SKILLS="${REPO_ROOT}/.claude/skills"
AGENTS_SKILLS="${REPO_ROOT}/.agents/skills"
OPENCLAW_RUNTIME="${REPO_ROOT}/runtime/openclaw"

echo "=== Skill Sync ==="
echo "Source: ${SKILL_SRC}"
echo ""

# 確保目標目錄存在
mkdir -p "${CLAUDE_SKILLS}" "${AGENTS_SKILLS}"

# 遍歷每個 skill
for skill_dir in "${SKILL_SRC}"/*/; do
    skill_name=$(basename "${skill_dir}")
    echo "Syncing skill: ${skill_name}"

    # 1. Claude
    mkdir -p "${CLAUDE_SKILLS}/${skill_name}"
    cp -r "${skill_dir}"* "${CLAUDE_SKILLS}/${skill_name}/"
    echo "  → .claude/skills/${skill_name}/"

    # 2. Agents (Codex)
    mkdir -p "${AGENTS_SKILLS}/${skill_name}"
    cp -r "${skill_dir}"* "${AGENTS_SKILLS}/${skill_name}/"
    echo "  → .agents/skills/${skill_name}/"

    # 3. OpenClaw
    mkdir -p "${OPENCLAW_RUNTIME}/${skill_name}/skills"
    cp -r "${skill_dir}"* "${OPENCLAW_RUNTIME}/${skill_name}/skills/"
    echo "  → runtime/openclaw/${skill_name}/skills/"

    echo ""
done

echo "=== Sync Complete ==="
echo ""
echo "Synced skills:"
ls -1 "${SKILL_SRC}" | while read -r s; do echo "  - ${s}"; done
echo ""
echo "Targets updated:"
echo "  - .claude/skills/"
echo "  - .agents/skills/"
echo "  - runtime/openclaw/"
