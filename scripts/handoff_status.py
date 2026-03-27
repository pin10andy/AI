#!/usr/bin/env python3
"""
Shared status parsing, writing, and transition helpers for handoff scripts.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path


ALLOWED_HANDOFF_STATUSES = {
    "pending",
    "in_progress",
    "review_ready",
    "approved",
    "changes_requested",
    "closed",
}

LEGAL_STATUS_TRANSITIONS = {
    "pending": {"in_progress"},
    "in_progress": {"review_ready"},
    "review_ready": {"approved", "changes_requested"},
    "changes_requested": {"pending"},
    "approved": {"closed"},
    "closed": set(),
}

STATUS_FIELD_ORDER = [
    "task_id",
    "handoff_status",
    "attempt",
    "revision",
    "worktree_branch",
    "worktree_path",
    "planning_owner",
    "execution_owner",
    "review_owner",
    "artifacts",
    "review",
    "reopen",
    "created_at",
    "updated_at",
]

ARTIFACT_FIELD_ORDER = [
    "task",
    "execution_brief",
    "change",
    "validation",
    "review_brief",
]

REVIEW_FIELD_ORDER = [
    "decision",
    "reviewed_by",
    "reviewed_at",
    "approved_by",
    "approved_at",
    "requested_by",
    "requested_at",
    "reason",
    "scope_decision",
    "required_changes",
]

REOPEN_FIELD_ORDER = [
    "reopened_by",
    "reopened_at",
    "reopen_reason",
]


def strip_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"')
    return value


def parse_scalar(raw: str) -> object:
    value = strip_value(raw)
    if value.isdigit():
        return int(value)
    return value


def _meaningful_lines(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        lines.append((indent, raw_line.strip()))
    return lines


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[object], int]:
    items: list[object] = []
    while index < len(lines):
        current_indent, line = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent:
            raise ValueError(f"Unsupported list indentation: {line}")
        if not line.startswith("- "):
            break
        items.append(parse_scalar(line[2:]))
        index += 1
    return items, index


def _parse_mapping(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, object], int]:
    mapping: dict[str, object] = {}
    while index < len(lines):
        current_indent, line = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent:
            raise ValueError(f"Unsupported mapping indentation: {line}")
        if line.startswith("- "):
            raise ValueError(f"Unexpected list item in mapping: {line}")
        if ":" not in line:
            raise ValueError(f"Invalid mapping line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        index += 1
        if value:
            mapping[key] = parse_scalar(value)
            continue
        if index >= len(lines) or lines[index][0] <= indent:
            mapping[key] = {}
            continue
        child_indent, child_line = lines[index]
        if child_line.startswith("- "):
            child, index = _parse_list(lines, index, child_indent)
        else:
            child, index = _parse_mapping(lines, index, child_indent)
        mapping[key] = child
    return mapping, index


def parse_status_yaml(path: Path) -> dict[str, object]:
    lines = _meaningful_lines(path)
    mapping, index = _parse_mapping(lines, 0, 0)
    if index != len(lines):
        raise ValueError(f"Unexpected trailing content in {path}")
    return mapping


def now_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def normalize_status(status: dict[str, object]) -> dict[str, object]:
    normalized = dict(status)
    normalized["attempt"] = int(normalized.get("attempt", 1) or 1)
    normalized["revision"] = int(normalized.get("revision", 1) or 1)

    artifacts = dict(normalized.get("artifacts", {}))
    for key in ARTIFACT_FIELD_ORDER:
        artifacts[key] = str(artifacts.get(key, ""))
    normalized["artifacts"] = artifacts

    for block in ("review", "reopen"):
        value = normalized.get(block)
        if isinstance(value, dict):
            normalized[block] = dict(value)
        elif value in (None, ""):
            normalized.pop(block, None)
        else:
            raise ValueError(f"{block} must be a mapping if present")

    return normalized


def _quote(value: object) -> str:
    if isinstance(value, int):
        return str(value)
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def _emit_block(lines: list[str], indent: int, data: dict[str, object], field_order: list[str] | None = None) -> None:
    if field_order is None:
        keys = list(data.keys())
    else:
        keys = [key for key in field_order if key in data]
        keys.extend(key for key in data if key not in keys)

    prefix = " " * indent
    for key in keys:
        value = data[key]
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            _emit_block(lines, indent + 2, value)
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for item in value:
                lines.append(f'{" " * (indent + 2)}- {_quote(item)}')
        else:
            lines.append(f"{prefix}{key}: {_quote(value)}")


def dump_status_yaml(status: dict[str, object]) -> str:
    normalized = normalize_status(status)
    lines: list[str] = []
    for key in STATUS_FIELD_ORDER:
        if key not in normalized:
            continue
        value = normalized[key]
        if isinstance(value, dict):
            lines.append(f"{key}:")
            if key == "artifacts":
                _emit_block(lines, 2, value, ARTIFACT_FIELD_ORDER)
            elif key == "review":
                _emit_block(lines, 2, value, REVIEW_FIELD_ORDER)
            elif key == "reopen":
                _emit_block(lines, 2, value, REOPEN_FIELD_ORDER)
            else:
                _emit_block(lines, 2, value)
        else:
            lines.append(f"{key}: {_quote(value)}")
    lines.append("")
    return "\n".join(lines)


def write_status_yaml(path: Path, status: dict[str, object]) -> None:
    path.write_text(dump_status_yaml(status), encoding="utf-8")


def ensure_legal_transition(current_status: str, next_status: str) -> None:
    allowed = LEGAL_STATUS_TRANSITIONS.get(current_status, set())
    if next_status not in allowed:
        raise ValueError(
            f"Illegal handoff_status transition: {current_status!r} -> {next_status!r}"
        )

