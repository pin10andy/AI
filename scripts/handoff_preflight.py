#!/usr/bin/env python3
"""
Preflight validator for a handoff package.

Phase scope: HANDOFF-002 only.
Validates that the handoff package has the minimum structure required for an
execution owner to start work.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from handoff_status import ALLOWED_HANDOFF_STATUSES, parse_status_yaml

TASK_ID_RE = re.compile(r'^\s*task_id:\s*"?(?P<value>[^"\n]+)"?\s*$', re.MULTILINE)

def ok(message: str) -> None:
    print(f"[ok]   {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def warn(message: str) -> None:
    print(f"[warn] {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a handoff package before execution.")
    parser.add_argument("--task", required=True, help="Handoff task id, e.g. handoff-pipeline-001")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument(
        "--require-status",
        help="Fail unless status.yaml.handoff_status matches this value exactly",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    handoff_dir = repo_root / "ai" / "handoffs" / args.task
    status_path = handoff_dir / "status.yaml"

    failures = 0

    if handoff_dir.exists():
        ok(f"handoff directory exists: {handoff_dir.relative_to(repo_root)}")
    else:
        fail(f"handoff directory missing: {handoff_dir.relative_to(repo_root)}")
        return 1

    if status_path.exists():
        ok(f"status file exists: {status_path.relative_to(repo_root)}")
    else:
        fail(f"status file missing: {status_path.relative_to(repo_root)}")
        return 1

    try:
        status = parse_status_yaml(status_path)
    except Exception as exc:  # noqa: BLE001
        fail(f"could not parse status.yaml: {exc}")
        return 1

    for field in (
        "task_id",
        "handoff_status",
        "attempt",
        "revision",
        "planning_owner",
        "execution_owner",
        "review_owner",
        "created_at",
        "updated_at",
        "artifacts",
    ):
        if field in status:
            ok(f"status field present: {field}")
        else:
            fail(f"status field missing: {field}")
            failures += 1

    task_id = str(status.get("task_id", ""))
    handoff_status = str(status.get("handoff_status", ""))
    artifacts = status.get("artifacts", {})
    attempt = status.get("attempt", "")
    revision = status.get("revision", "")

    if task_id == args.task:
        ok(f"status.task_id matches requested task: {args.task}")
    else:
        fail(f"status.task_id mismatch: expected {args.task}, got {task_id or '<empty>'}")
        failures += 1

    if handoff_status in ALLOWED_HANDOFF_STATUSES:
        ok(f"handoff_status allowed: {handoff_status}")
    else:
        fail(f"handoff_status invalid: {handoff_status or '<empty>'}")
        failures += 1

    if isinstance(attempt, int) and attempt >= 1:
        ok(f"attempt valid: {attempt}")
    else:
        fail(f"attempt invalid: {attempt!r}")
        failures += 1

    if isinstance(revision, int) and revision >= 1:
        ok(f"revision valid: {revision}")
    else:
        fail(f"revision invalid: {revision!r}")
        failures += 1

    if args.require_status:
        if handoff_status == args.require_status:
            ok(f"handoff_status satisfies required value: {args.require_status}")
        else:
            fail(
                "handoff_status requirement failed: "
                f"expected {args.require_status}, got {handoff_status or '<empty>'}"
            )
            failures += 1

    if not isinstance(artifacts, dict):
        fail("artifacts block missing or malformed")
        return 1

    for artifact_key in ("task", "execution_brief"):
        artifact_path_str = str(artifacts.get(artifact_key, "")).strip()
        if not artifact_path_str:
            fail(f"artifacts.{artifact_key} missing")
            failures += 1
            continue

        artifact_path = repo_root / artifact_path_str
        if artifact_path.exists():
            ok(f"artifacts.{artifact_key} exists: {artifact_path_str}")
        else:
            fail(f"artifacts.{artifact_key} missing file: {artifact_path_str}")
            failures += 1

    task_path_str = str(artifacts.get("task", "")).strip()
    if task_path_str:
        task_path = repo_root / task_path_str
        if task_path.exists():
            task_text = task_path.read_text(encoding="utf-8")
            match = TASK_ID_RE.search(task_text)
            if match and match.group("value").strip() == args.task:
                ok("task artifact task_id matches handoff task id")
            else:
                fail("task artifact task_id does not match handoff task id")
                failures += 1

    for owner_field in ("planning_owner", "execution_owner", "review_owner"):
        if str(status.get(owner_field, "")).strip():
            ok(f"{owner_field} populated")
        else:
            fail(f"{owner_field} empty")
            failures += 1

    for optional_artifact in ("change", "validation", "review_brief"):
        artifact_path_str = str(artifacts.get(optional_artifact, "")).strip()
        if not artifact_path_str:
            warn(f"artifacts.{optional_artifact} not set yet")
            continue
        artifact_path = repo_root / artifact_path_str
        if artifact_path.exists():
            ok(f"artifacts.{optional_artifact} exists: {artifact_path_str}")
        else:
            warn(f"artifacts.{optional_artifact} not created yet: {artifact_path_str}")

    if failures:
        print(f"\nResult: FAIL ({failures} issue(s))")
        return 1

    print("\nResult: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
