#!/usr/bin/env python3
"""
End-to-end validation harness for canonical handoff package flows.

Phase scope: HANDOFF-005 only.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from handoff_status import dump_status_yaml, parse_status_yaml


TASK_ID = "handoff-pipeline-001"
TASK_ARTIFACT = "ai/tasks/2026-03-27-auto-handoff-mechanism.yaml"
EXECUTION_BRIEF = "ai/handoffs/handoff-pipeline-001/execution-brief.md"
CHANGE_ARTIFACT = "ai/changes/2026-03-27-auto-handoff-mechanism.md"
VALIDATION_ARTIFACT = "ai/validation/2026-03-27-auto-handoff-mechanism.md"
REVIEW_BRIEF = "ai/handoffs/handoff-pipeline-001/review-brief.md"
SCRIPT_NAMES = [
    "handoff_status.py",
    "handoff_preflight.py",
    "orchestrator.py",
    "handoff_complete.py",
]


class ScenarioFailure(RuntimeError):
    pass


def run(
    cmd: list[str],
    *,
    cwd: Path,
    expected_returncode: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != expected_returncode:
        raise ScenarioFailure(
            f"Command failed (expected {expected_returncode}, got {result.returncode}): "
            f"{' '.join(cmd)}\n{result.stdout}"
        )
    return result


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ScenarioFailure(message)


def create_status(*, handoff_status: str, worktree_branch: str = "", worktree_path: str = "") -> dict[str, object]:
    return {
        "task_id": TASK_ID,
        "handoff_status": handoff_status,
        "attempt": 1,
        "revision": 1,
        "worktree_branch": worktree_branch,
        "worktree_path": worktree_path,
        "planning_owner": "claude",
        "execution_owner": "codex",
        "review_owner": "claude",
        "artifacts": {
            "task": TASK_ARTIFACT,
            "execution_brief": EXECUTION_BRIEF,
            "change": CHANGE_ARTIFACT,
            "validation": VALIDATION_ARTIFACT,
            "review_brief": REVIEW_BRIEF,
        },
        "created_at": "2026-03-27T00:00:00",
        "updated_at": "2026-03-27T16:05:00+08:00",
    }


def init_repo(status: dict[str, object]) -> Path:
    repo_root = Path(tempfile.mkdtemp(prefix="handoff-e2e-")).resolve()
    for relative in (
        "ai/handoffs/handoff-pipeline-001",
        "ai/tasks",
        "ai/changes",
        "ai/validation",
        "scripts",
    ):
        (repo_root / relative).mkdir(parents=True, exist_ok=True)

    script_root = Path(__file__).resolve().parent
    for script_name in SCRIPT_NAMES:
        shutil.copy2(script_root / script_name, repo_root / "scripts" / script_name)

    (repo_root / TASK_ARTIFACT).write_text(
        'task:\n'
        f'  task_id: "{TASK_ID}"\n'
        "  status: in_progress\n"
        "  validation:\n"
        f'    validation_file: "{VALIDATION_ARTIFACT}"\n',
        encoding="utf-8",
    )
    (repo_root / EXECUTION_BRIEF).write_text("# Execution brief\n", encoding="utf-8")
    write_status(repo_root, status)

    run(["git", "init"], cwd=repo_root)
    run(["git", "config", "user.name", "pin10andy"], cwd=repo_root)
    run(["git", "config", "user.email", "pin10andy@gmail.com"], cwd=repo_root)
    run(["git", "add", "."], cwd=repo_root)
    run(["git", "commit", "-m", "init"], cwd=repo_root)
    return repo_root


def status_path(repo_root: Path) -> Path:
    return repo_root / "ai" / "handoffs" / TASK_ID / "status.yaml"


def load_status(repo_root: Path) -> dict[str, object]:
    return parse_status_yaml(status_path(repo_root))


def write_status(repo_root: Path, status: dict[str, object]) -> None:
    status_path(repo_root).write_text(dump_status_yaml(status), encoding="utf-8")


def write_outputs(repo_root: Path) -> None:
    for relpath, contents in (
        (CHANGE_ARTIFACT, "# change\n"),
        (VALIDATION_ARTIFACT, "# validation\n"),
        (REVIEW_BRIEF, "# review\n"),
    ):
        path = repo_root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")


def remove_runtime_slot(repo_root: Path, *, branch_name: str, worktree_relpath: str) -> None:
    worktree_path = (repo_root / worktree_relpath).resolve()
    if worktree_path.exists():
        run(["git", "worktree", "remove", "--force", str(worktree_path)], cwd=repo_root)

    branch_check = subprocess.run(
        ["git", "show-ref", "--verify", f"refs/heads/{branch_name}"],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if branch_check.returncode == 0:
        run(["git", "branch", "-D", branch_name], cwd=repo_root)


def scenario_happy_path() -> tuple[bool, str]:
    repo_root = init_repo(create_status(handoff_status="pending"))
    try:
        run(
            [
                "python3",
                "scripts/orchestrator.py",
                "--repo-root",
                str(repo_root),
                "--task",
                TASK_ID,
                "--no-launch",
                "--worktree-root",
                str(repo_root / "worktrees"),
            ],
            cwd=repo_root,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "in_progress", "happy path did not enter in_progress")
        write_outputs(repo_root)
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "complete",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
            ],
            cwd=repo_root,
        )
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "approve",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reason",
                "Happy path accepted",
            ],
            cwd=repo_root,
        )
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "close",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
            ],
            cwd=repo_root,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "closed", "happy path did not end in closed")
        return True, "pending -> in_progress -> review_ready -> approved -> closed"
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)


def scenario_retry_path() -> tuple[bool, str]:
    repo_root = init_repo(create_status(handoff_status="pending"))
    try:
        worktree_root = repo_root / "worktrees"
        run(
            [
                "python3",
                "scripts/orchestrator.py",
                "--repo-root",
                str(repo_root),
                "--task",
                TASK_ID,
                "--no-launch",
                "--worktree-root",
                str(worktree_root),
            ],
            cwd=repo_root,
        )
        write_outputs(repo_root)
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "complete",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
            ],
            cwd=repo_root,
        )
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "request-changes",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reason",
                "Need a narrower same-package revision",
                "--required-change",
                "Tighten acceptance criteria",
                "--required-change",
                "Refresh validation evidence",
            ],
            cwd=repo_root,
        )
        requested = load_status(repo_root)
        first_round_review = dict(requested.get("review", {}))
        branch_name = str(requested["worktree_branch"])
        worktree_relpath = str(requested["worktree_path"])
        ensure(str(requested["handoff_status"]) == "changes_requested", "retry path did not enter changes_requested")
        ensure(first_round_review.get("decision") == "changes_requested", "retry path missing first-round review decision")
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "reopen",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reopen-reason",
                "Rework remains within original package scope",
            ],
            cwd=repo_root,
        )
        reopened = load_status(repo_root)
        ensure(str(reopened["handoff_status"]) == "pending", "retry path did not reopen to pending")
        ensure(int(reopened["attempt"]) == 2, "retry path did not increment attempt")
        ensure(int(reopened["revision"]) == 2, "retry path did not increment revision")
        remove_runtime_slot(repo_root, branch_name=branch_name, worktree_relpath=worktree_relpath)
        run(
            [
                "python3",
                "scripts/orchestrator.py",
                "--repo-root",
                str(repo_root),
                "--task",
                TASK_ID,
                "--no-launch",
                "--worktree-root",
                str(worktree_root),
            ],
            cwd=repo_root,
        )
        write_outputs(repo_root)
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "complete",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
            ],
            cwd=repo_root,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "retry path did not end at review_ready")
        second_round_review = status.get("review", {})
        ensure(isinstance(second_round_review, dict), "retry path lost review block after second review_ready")
        for key in ("decision", "requested_by", "requested_at", "reason", "scope_decision", "required_changes"):
            ensure(
                second_round_review.get(key) == first_round_review.get(key),
                f"retry path did not preserve first-round review.{key}",
            )
        return True, "pending -> in_progress -> review_ready -> changes_requested -> pending -> in_progress -> review_ready"
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)


def scenario_reviewer_only_gates() -> tuple[bool, str]:
    repo_root = init_repo(
        create_status(
            handoff_status="review_ready",
            worktree_branch="handoff/handoff-pipeline-001",
            worktree_path="worktrees/handoff-pipeline-001",
        )
    )
    try:
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "approve",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "approve failure changed package state")
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "request-changes",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
                "--reason",
                "Invalid actor",
                "--required-change",
                "Do not allow this",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "request-changes failure changed package state")
        return True, "non-reviewer approve/request-changes rejected and package state preserved"
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)


def scenario_illegal_transitions() -> tuple[bool, str]:
    repo_root = init_repo(create_status(handoff_status="pending"))
    try:
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "complete",
                "--task",
                TASK_ID,
                "--actor",
                "codex",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "close",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )

        review_ready_status = create_status(
            handoff_status="review_ready",
            worktree_branch="handoff/handoff-pipeline-001",
            worktree_path="worktrees/handoff-pipeline-001",
        )
        write_status(repo_root, review_ready_status)
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "reopen",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reopen-reason",
                "Illegal transition",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "illegal transitions changed package state")
        return True, "complete on pending, close on pending, and reopen on review_ready all failed"
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)


def scenario_new_package_required() -> tuple[bool, str]:
    repo_root = init_repo(
        create_status(
            handoff_status="review_ready",
            worktree_branch="handoff/handoff-pipeline-001",
            worktree_path="worktrees/handoff-pipeline-001",
        )
    )
    try:
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "request-changes",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reason",
                "Requires a wider redesign",
                "--required-change",
                "Redefine package scope",
                "--scope-decision",
                "new_package_required",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "new_package_required refusal changed package state")
        run(
            [
                "python3",
                "scripts/handoff_complete.py",
                "--repo-root",
                str(repo_root),
                "reopen",
                "--task",
                TASK_ID,
                "--actor",
                "claude",
                "--reopen-reason",
                "Should not reopen out-of-scope package",
            ],
            cwd=repo_root,
            expected_returncode=1,
        )
        status = load_status(repo_root)
        ensure(str(status["handoff_status"]) == "review_ready", "out-of-scope refusal did not preserve package state")
        return True, "new_package_required refusal preserved review_ready state and blocked reopen"
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run canonical handoff E2E validation scenarios.")
    parser.parse_args()

    scenarios = [
        ("happy_path", scenario_happy_path),
        ("retry_path", scenario_retry_path),
        ("reviewer_only_gate_failures", scenario_reviewer_only_gates),
        ("illegal_transition_failures", scenario_illegal_transitions),
        ("new_package_required_refusal", scenario_new_package_required),
    ]

    rows: list[tuple[str, str, str]] = []
    for name, scenario in scenarios:
        try:
            _, detail = scenario()
            rows.append((name, "PASS", detail))
        except Exception as exc:  # noqa: BLE001
            rows.append((name, "FAIL", str(exc)))

    name_width = max(len("Path"), *(len(name) for name, _, _ in rows))
    result_width = max(len("Result"), *(len(result) for _, result, _ in rows))
    print(f'{"Path".ljust(name_width)}  {"Result".ljust(result_width)}  Detail')
    print(f'{"-" * name_width}  {"-" * result_width}  {"-" * 60}')
    failed = False
    for name, result, detail in rows:
        print(f"{name.ljust(name_width)}  {result.ljust(result_width)}  {detail}")
        failed = failed or result != "PASS"

    if failed:
        print("\nResult: FAIL")
        return 1

    print("\nResult: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
