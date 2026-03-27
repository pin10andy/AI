#!/usr/bin/env python3
"""
Completion and reviewer writeback handler for handoff packages.

Phase scope: HANDOFF-004 only.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from handoff_status import ensure_legal_transition, now_timestamp, parse_status_yaml, write_status_yaml


def ok(message: str) -> None:
    print(f"[ok]   {message}")


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def require_actor(status: dict[str, object], actor: str, field: str) -> None:
    expected = str(status.get(field, "")).strip()
    if actor != expected:
        raise ValueError(f"{field} must perform this action; expected {expected!r}, got {actor!r}")


def require_status(status: dict[str, object], expected: str) -> None:
    current = str(status.get("handoff_status", "")).strip()
    if current != expected:
        raise ValueError(f"status must be {expected!r}; got {current!r}")


def ensure_artifact_exists(repo_root: Path, status: dict[str, object], artifact_key: str) -> None:
    artifacts = status.get("artifacts", {})
    if not isinstance(artifacts, dict):
        raise ValueError("artifacts block missing or malformed")
    artifact_path_str = str(artifacts.get(artifact_key, "")).strip()
    if not artifact_path_str:
        raise ValueError(f"artifacts.{artifact_key} must be set before completion")
    artifact_path = repo_root / artifact_path_str
    if not artifact_path.exists():
        raise ValueError(f"artifacts.{artifact_key} missing file: {artifact_path_str}")


def set_transition(status: dict[str, object], next_status: str) -> None:
    current = str(status.get("handoff_status", "")).strip()
    ensure_legal_transition(current, next_status)
    status["handoff_status"] = next_status
    status["updated_at"] = now_timestamp()


def load_status(repo_root: Path, task: str) -> tuple[Path, dict[str, object]]:
    status_path = repo_root / "ai" / "handoffs" / task / "status.yaml"
    if not status_path.exists():
        raise ValueError(f"missing status file: {status_path}")
    status = parse_status_yaml(status_path)
    if str(status.get("task_id", "")).strip() != task:
        raise ValueError(f"status.task_id mismatch: expected {task!r}")
    return status_path, status


def action_complete(repo_root: Path, status_path: Path, status: dict[str, object], actor: str) -> int:
    require_actor(status, actor, "execution_owner")
    require_status(status, "in_progress")
    for artifact_key in ("change", "validation", "review_brief"):
        ensure_artifact_exists(repo_root, status, artifact_key)

    set_transition(status, "review_ready")
    write_status_yaml(status_path, status)

    review_brief = str(status["artifacts"]["review_brief"])
    review_owner = str(status["review_owner"])
    task_id = str(status["task_id"])
    ok("status transitioned to review_ready")
    print("")
    print("Reviewer next steps:")
    print(f"- Review owner: {review_owner}")
    print(f"- Review brief: {review_brief}")
    print(
        f"- Approve: python3 scripts/handoff_complete.py approve --task {task_id} --actor {review_owner}"
    )
    print(
        f"- Request changes: python3 scripts/handoff_complete.py request-changes --task {task_id} --actor {review_owner} --reason \"...\" --required-change \"...\""
    )
    return 0


def action_approve(status_path: Path, status: dict[str, object], actor: str, reason: str) -> int:
    require_actor(status, actor, "review_owner")
    require_status(status, "review_ready")
    set_transition(status, "approved")
    status["review"] = {
        "decision": "approved",
        "reviewed_by": actor,
        "reviewed_at": now_timestamp(),
        "approved_by": actor,
        "approved_at": now_timestamp(),
        "reason": reason,
    }
    write_status_yaml(status_path, status)
    ok("status transitioned to approved")
    return 0


def action_request_changes(
    status_path: Path,
    status: dict[str, object],
    actor: str,
    reason: str,
    required_changes: list[str],
    scope_decision: str,
) -> int:
    require_actor(status, actor, "review_owner")
    require_status(status, "review_ready")
    if scope_decision != "same_package":
        raise ValueError(
            "requested changes exceed package scope; create a new handoff package instead of reusing this one"
        )
    if not reason.strip():
        raise ValueError("--reason is required for request-changes")
    if not required_changes:
        raise ValueError("at least one --required-change is required for request-changes")

    set_transition(status, "changes_requested")
    status["review"] = {
        "decision": "changes_requested",
        "reviewed_by": actor,
        "reviewed_at": now_timestamp(),
        "requested_by": actor,
        "requested_at": now_timestamp(),
        "reason": reason,
        "scope_decision": scope_decision,
        "required_changes": required_changes,
    }
    write_status_yaml(status_path, status)
    ok("status transitioned to changes_requested")
    return 0


def action_reopen(status_path: Path, status: dict[str, object], actor: str, reopen_reason: str) -> int:
    if actor not in {
        str(status.get("planning_owner", "")).strip(),
        str(status.get("review_owner", "")).strip(),
    }:
        raise ValueError("planning_owner or review_owner must perform reopen")
    require_status(status, "changes_requested")
    if not reopen_reason.strip():
        raise ValueError("--reopen-reason is required for reopen")

    set_transition(status, "pending")
    status["attempt"] = int(status.get("attempt", 1)) + 1
    status["revision"] = int(status.get("revision", 1)) + 1
    status["worktree_branch"] = ""
    status["worktree_path"] = ""
    status["reopen"] = {
        "reopened_by": actor,
        "reopened_at": now_timestamp(),
        "reopen_reason": reopen_reason,
    }
    write_status_yaml(status_path, status)
    ok("status transitioned to pending")
    return 0


def action_close(status_path: Path, status: dict[str, object], actor: str) -> int:
    require_actor(status, actor, "review_owner")
    require_status(status, "approved")
    set_transition(status, "closed")
    write_status_yaml(status_path, status)
    ok("status transitioned to closed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write back legal handoff status transitions.")
    parser.add_argument("--repo-root", default=".", help="Repository root")

    subparsers = parser.add_subparsers(dest="action", required=True)

    complete = subparsers.add_parser("complete", help="Transition in_progress -> review_ready")
    complete.add_argument("--task", required=True)
    complete.add_argument("--actor", required=True)

    approve = subparsers.add_parser("approve", help="Transition review_ready -> approved")
    approve.add_argument("--task", required=True)
    approve.add_argument("--actor", required=True)
    approve.add_argument("--reason", default="")

    request_changes = subparsers.add_parser(
        "request-changes",
        help="Transition review_ready -> changes_requested",
    )
    request_changes.add_argument("--task", required=True)
    request_changes.add_argument("--actor", required=True)
    request_changes.add_argument("--reason", required=True)
    request_changes.add_argument("--required-change", action="append", dest="required_changes", default=[])
    request_changes.add_argument(
        "--scope-decision",
        choices=["same_package", "new_package_required"],
        default="same_package",
    )

    reopen = subparsers.add_parser("reopen", help="Transition changes_requested -> pending")
    reopen.add_argument("--task", required=True)
    reopen.add_argument("--actor", required=True)
    reopen.add_argument("--reopen-reason", required=True)

    close = subparsers.add_parser("close", help="Transition approved -> closed")
    close.add_argument("--task", required=True)
    close.add_argument("--actor", required=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()

    try:
        status_path, status = load_status(repo_root, args.task)

        if args.action == "complete":
            return action_complete(repo_root, status_path, status, args.actor)
        if args.action == "approve":
            return action_approve(status_path, status, args.actor, args.reason)
        if args.action == "request-changes":
            return action_request_changes(
                status_path,
                status,
                args.actor,
                args.reason,
                args.required_changes,
                args.scope_decision,
            )
        if args.action == "reopen":
            return action_reopen(status_path, status, args.actor, args.reopen_reason)
        if args.action == "close":
            return action_close(status_path, status, args.actor)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))

    return fail(f"unsupported action: {args.action}")


if __name__ == "__main__":
    raise SystemExit(main())
