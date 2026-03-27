#!/usr/bin/env python3
"""
Minimal orchestrator for handoff-pipeline execution.

Phase scope: HANDOFF-003 only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

from handoff_status import now_timestamp, parse_status_yaml, write_status_yaml


def resolve_worktree_root(repo_root: Path, explicit_root: str | None) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get("AI_WORKTREE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    common_dir = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()
    common_dir_path = Path(common_dir).resolve()
    common_repo_root = common_dir_path.parent
    return (common_repo_root.parent / "ai-worktrees").resolve()


def branch_exists(repo_root: Path, branch: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show-ref", "--verify", f"refs/heads/{branch}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def ensure_clean_slot(target_path: Path) -> None:
    if target_path.exists():
        contents = list(target_path.iterdir())
        if contents:
            raise RuntimeError(f"Worktree path already exists and is not empty: {target_path}")


def run_preflight(repo_root: Path, task: str, require_status: str) -> None:
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "handoff_preflight.py"),
        "--repo-root",
        str(repo_root),
        "--task",
        task,
        "--require-status",
        require_status,
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Preflight failed:\n{result.stdout}")


def build_codex_prompt(task: str, execution_brief_relpath: str) -> str:
    return (
        "Read AGENTS.md first, then execute the assigned handoff package.\n\n"
        f"Task: {task}\n"
        f"Execution brief: {execution_brief_relpath}\n\n"
        "Treat repo artifacts as source of truth. Do not redefine governance."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Start Codex execution from a handoff package.")
    parser.add_argument("--task", required=True, help="Handoff task id, e.g. handoff-pipeline-001")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--worktree-root", help="Override worktree root path")
    parser.add_argument("--codex-bin", default="codex", help="Codex executable")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print actions only")
    parser.add_argument("--no-launch", action="store_true", help="Create worktree but do not start Codex")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    handoff_dir = repo_root / "ai" / "handoffs" / args.task
    status_path = handoff_dir / "status.yaml"

    if not status_path.exists():
        print(f"[FAIL] Missing status file: {status_path.relative_to(repo_root)}")
        return 1

    run_preflight(repo_root, args.task, "pending")

    status = parse_status_yaml(status_path)
    handoff_status = str(status.get("handoff_status", "")).strip()
    execution_owner = str(status.get("execution_owner", "")).strip()

    if handoff_status != "pending":
        print(f"[FAIL] Orchestrator can only start when handoff_status == pending; got {handoff_status!r}")
        return 1

    if execution_owner != "codex":
        print(f"[FAIL] execution_owner must be codex for this orchestrator; got {execution_owner!r}")
        return 1

    if str(status.get("worktree_branch", "")).strip() or str(status.get("worktree_path", "")).strip():
        print("[FAIL] status.yaml already contains worktree assignment; refusing to overwrite existing claim")
        return 1

    worktree_root = resolve_worktree_root(repo_root, args.worktree_root)
    target_path = worktree_root / args.task
    target_path_rel = os.path.relpath(target_path, repo_root)
    branch_name = f"handoff/{args.task}"

    if branch_exists(repo_root, branch_name):
        print(f"[FAIL] branch already exists: {branch_name}")
        return 1

    try:
        ensure_clean_slot(target_path)
    except RuntimeError as exc:
        print(f"[FAIL] {exc}")
        return 1

    if args.dry_run:
        print(f"[ok]   preflight passed with required status pending")
        print(f"[ok]   execution_owner is codex")
        print(f"[ok]   worktree root resolved to: {worktree_root}")
        print(f"[ok]   derived worktree path: {target_path_rel}")
        print(f"[ok]   derived branch: {branch_name}")
        print("Result: PASS (dry-run)")
        return 0

    worktree_root.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "add", str(target_path), "-b", branch_name],
        check=True,
    )

    status["handoff_status"] = "in_progress"
    status["worktree_branch"] = branch_name
    status["worktree_path"] = target_path_rel
    status["updated_at"] = now_timestamp()
    write_status_yaml(status_path, status)

    execution_brief_relpath = str(status["artifacts"]["execution_brief"])
    prompt = build_codex_prompt(args.task, execution_brief_relpath)

    print(f"[ok]   worktree created: {target_path_rel}")
    print(f"[ok]   status transitioned to in_progress")

    if args.no_launch:
        print("[ok]   no-launch enabled; Codex was not started")
        return 0

    subprocess.run([args.codex_bin, prompt], cwd=target_path, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
