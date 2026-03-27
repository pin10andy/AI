#!/usr/bin/env python3
"""
Minimal task artifact linkage validator.

Checks that a task, change record, and validation record all exist and that the
change / validation files mention the task id or task path.

stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TASK_ID_RE = re.compile(r'^\s*task_id:\s*"?(?P<value>[^"\n]+)"?\s*$', re.MULTILINE)
VALIDATION_FILE_RE = re.compile(
    r'^\s*validation_file:\s*"?(?P<value>[^"\n]+)"?\s*$',
    re.MULTILINE,
)
STATUS_RE = re.compile(r'^\s*status:\s*(?P<value>[a-z_]+)\s*$', re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[ok]   {message}")


def extract(pattern: re.Pattern[str], text: str, label: str) -> str | None:
    match = pattern.search(text)
    if not match:
        fail(f"Could not find {label}")
        return None
    return match.group("value").strip()


def mentions_task(text: str, task_id: str, task_relpath: str) -> bool:
    return task_id in text or task_relpath in text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate task/change/validation linkage.")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--task", required=True, help="Task file path, relative to repo root")
    parser.add_argument("--change", required=True, help="Change record path, relative to repo root")
    parser.add_argument(
        "--validation",
        required=True,
        help="Validation record path, relative to repo root",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_path = (repo_root / args.task).resolve()
    change_path = (repo_root / args.change).resolve()
    validation_path = (repo_root / args.validation).resolve()

    failures = 0

    for path, label in (
        (task_path, "task"),
        (change_path, "change record"),
        (validation_path, "validation record"),
    ):
        if path.exists():
            ok(f"{label} exists: {path.relative_to(repo_root)}")
        else:
            fail(f"{label} missing: {path.relative_to(repo_root)}")
            failures += 1

    if failures:
        return 1

    task_text = read_text(task_path)
    change_text = read_text(change_path)
    validation_text = read_text(validation_path)

    task_id = extract(TASK_ID_RE, task_text, "task_id")
    validation_file = extract(VALIDATION_FILE_RE, task_text, "validation_file")
    status = extract(STATUS_RE, task_text, "status")
    task_relpath = str(task_path.relative_to(repo_root))

    if task_id:
        ok(f"task_id found: {task_id}")
    else:
        failures += 1

    if status:
        ok(f"task status found: {status}")
    else:
        failures += 1

    if validation_file:
        expected_validation = str(validation_path.relative_to(repo_root))
        if validation_file == expected_validation:
            ok(f"task.validation.validation_file matches: {expected_validation}")
        else:
            fail(
                "task.validation.validation_file mismatch: "
                f"expected {expected_validation}, got {validation_file}"
            )
            failures += 1
    else:
        failures += 1

    if task_id and mentions_task(change_text, task_id, task_relpath):
        ok("change record mentions task id or task path")
    else:
        fail("change record does not mention task id or task path")
        failures += 1

    if task_id and mentions_task(validation_text, task_id, task_relpath):
        ok("validation record mentions task id or task path")
    else:
        fail("validation record does not mention task id or task path")
        failures += 1

    if failures:
        print(f"\nResult: FAIL ({failures} issue(s))")
        return 1

    print("\nResult: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
