#!/usr/bin/env python3
"""
Artifact Governance Check — Google Ads

Validates that the repo complies with artifact governance policies:
  - ai/policies/artifact-naming-policy.md
  - ai/policies/artifact-write-policy.md
  - ai/registry/storage-map.yaml

Usage:
  python3 scripts/check_artifact_governance.py [--repo-root /path/to/repo]

Exit codes:
  0 = all checks pass
  1 = one or more checks failed

stdlib only — no external dependencies.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

CANONICAL_OUTPUT_ROOT = "ai/outputs/google-ads"
SCRATCH_ROOT = "scratch/google-ads"
VALIDATION_DIR = "ai/validation"
REPORTS_DIR = "ai/reports"
REGISTRY_FILE = "ai/registry/artifacts.yaml"

# Registered lanes: (brand, product, lane)
REGISTERED_LANES = [
    ("lovefu", "hillbed", "evergreen-purchase-pmax"),
    ("lovefu", "experience-store", "evergreen-store-visit-pmax"),
]

# Required subdirs per lane
LANE_SUBDIRS = ["golden", "approved-references", "pipeline", "deliverables"]

# Artifact filename patterns (compiled regexes)
NAMING_PATTERNS = {
    "golden": re.compile(
        r"^[a-z0-9][a-z0-9\-]*\.output\.(json|md)$"
    ),
    "approved-reference": re.compile(
        r"^[a-z0-9][a-z0-9\-]*\.ref-\d{2}\.output\.(json|md)$"
    ),
    "pipeline-stage": re.compile(
        r"^(input|builder|interpreter|interpretation|packager|portfolio)\.(json|md)$"
    ),
    "pipeline-taskdir": re.compile(
        r"^\d{4}-\d{2}-\d{2}-[a-z0-9\-]+$"
    ),
    "deliverable": re.compile(
        r"^[a-z0-9][a-z0-9\-]*\.deliverable\.[a-z]+$"
    ),
    "validation": re.compile(
        r"^\d{4}-\d{2}-\d{2}-[a-z0-9\-]+\.md$"
    ),
    "report": re.compile(
        r"^\d{4}-\d{2}-\d{2}-[a-z0-9\-]+\.md$"
    ),
}

# Filename anti-patterns (things that should NOT appear)
ANTI_PATTERNS = [
    re.compile(r"[A-Z]"),           # uppercase
    re.compile(r"_"),               # underscores
    re.compile(r"\s"),              # spaces
    re.compile(r"[\u4e00-\u9fff]"), # CJK characters
]

# Required fields in artifact registry entries
REQUIRED_ARTIFACT_FIELDS = [
    "artifact_id", "task_id", "artifact_type", "brand", "product",
    "lane", "status", "canonical_path", "source_brief",
    "generated_by", "owner", "created_at",
]

# Google Ads related file patterns in repo root (violations)
ROOT_GADS_PATTERNS = [
    re.compile(r"(?i)lovefu", re.IGNORECASE),
    re.compile(r"(?i)google.?ads", re.IGNORECASE),
    re.compile(r"(?i)pipeline.?v\d", re.IGNORECASE),
    re.compile(r"(?i)rsa", re.IGNORECASE),
    re.compile(r"(?i)pmax", re.IGNORECASE),
]


# ── Check infrastructure ─────────────────────────────────────────────────────

class CheckResult:
    def __init__(self, name: str):
        self.name = name
        self.passed: list[str] = []
        self.failed: list[str] = []
        self.warnings: list[str] = []

    def pass_(self, msg: str):
        self.passed.append(msg)

    def fail(self, msg: str):
        self.failed.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.failed) == 0


def print_result(r: CheckResult):
    status = "PASS" if r.ok else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"[{status}] {r.name}")
    print(f"{'=' * 60}")
    for msg in r.passed:
        print(f"  [ok]   {msg}")
    for msg in r.failed:
        print(f"  [FAIL] {msg}")
    for msg in r.warnings:
        print(f"  [warn] {msg}")


# ── Checks ───────────────────────────────────────────────────────────────────

def check_no_gads_in_root(repo: Path) -> CheckResult:
    """Check that no Google Ads output artifacts exist in repo root."""
    r = CheckResult("No Google Ads artifacts in repo root")

    for item in repo.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue
        name = item.name
        for pat in ROOT_GADS_PATTERNS:
            if pat.search(name):
                # Exclude known non-artifact files
                if name in ("CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md"):
                    continue
                r.fail(f"Google Ads artifact in repo root: {name}")
                break
        else:
            continue

    if not r.failed:
        r.pass_("No Google Ads artifacts found in repo root")
    return r


def check_directory_structure(repo: Path) -> CheckResult:
    """Check that canonical output directories exist with required subdirs."""
    r = CheckResult("Canonical directory structure")

    output_root = repo / CANONICAL_OUTPUT_ROOT
    if not output_root.exists():
        r.fail(f"Output root missing: {CANONICAL_OUTPUT_ROOT}")
        return r
    r.pass_(f"Output root exists: {CANONICAL_OUTPUT_ROOT}")

    for brand, product, lane in REGISTERED_LANES:
        lane_path = output_root / brand / product / lane
        if not lane_path.exists():
            r.fail(f"Lane directory missing: {lane_path.relative_to(repo)}")
            continue
        r.pass_(f"Lane directory exists: {brand}/{product}/{lane}")

        for subdir in LANE_SUBDIRS:
            sub = lane_path / subdir
            if not sub.exists():
                r.fail(f"Required subdir missing: {sub.relative_to(repo)}")
            else:
                r.pass_(f"  subdir exists: {subdir}/")

    # Check scratch directory
    scratch = repo / SCRATCH_ROOT
    if not scratch.exists():
        r.fail(f"Scratch directory missing: {SCRATCH_ROOT}")
    else:
        r.pass_(f"Scratch directory exists: {SCRATCH_ROOT}")

    return r


def check_naming_compliance(repo: Path) -> CheckResult:
    """Check that files in canonical output paths follow naming policy."""
    r = CheckResult("Artifact naming compliance")

    output_root = repo / CANONICAL_OUTPUT_ROOT
    if not output_root.exists():
        r.warn("Output root missing, skipping naming check")
        return r

    file_count = 0
    for brand, product, lane in REGISTERED_LANES:
        lane_path = output_root / brand / product / lane

        # Check golden/
        golden_dir = lane_path / "golden"
        if golden_dir.exists():
            for f in golden_dir.iterdir():
                if f.name == ".gitkeep":
                    continue
                file_count += 1
                if NAMING_PATTERNS["golden"].match(f.name):
                    r.pass_(f"golden: {f.name}")
                else:
                    r.fail(f"golden: bad name: {f.name}")
                _check_anti_patterns(r, f.name, "golden")

        # Check approved-references/
        ref_dir = lane_path / "approved-references"
        if ref_dir.exists():
            for f in ref_dir.iterdir():
                if f.name == ".gitkeep":
                    continue
                file_count += 1
                if NAMING_PATTERNS["approved-reference"].match(f.name):
                    r.pass_(f"approved-ref: {f.name}")
                else:
                    r.fail(f"approved-ref: bad name: {f.name}")
                _check_anti_patterns(r, f.name, "approved-ref")

        # Check pipeline/
        pipeline_dir = lane_path / "pipeline"
        if pipeline_dir.exists():
            for item in pipeline_dir.iterdir():
                if item.name == ".gitkeep":
                    continue
                if item.is_dir():
                    # Should be a task_id directory
                    if NAMING_PATTERNS["pipeline-taskdir"].match(item.name):
                        r.pass_(f"pipeline taskdir: {item.name}/")
                    else:
                        r.fail(f"pipeline taskdir: bad name: {item.name}/")
                    # Check stage files inside
                    for sf in item.iterdir():
                        file_count += 1
                        if NAMING_PATTERNS["pipeline-stage"].match(sf.name):
                            r.pass_(f"  stage file: {sf.name}")
                        else:
                            r.fail(f"  stage file: bad name: {sf.name}")
                else:
                    file_count += 1
                    r.fail(f"pipeline: flat file (should be in task subdir): {item.name}")

        # Check deliverables/
        deliv_dir = lane_path / "deliverables"
        if deliv_dir.exists():
            for f in deliv_dir.iterdir():
                if f.name == ".gitkeep":
                    continue
                file_count += 1
                if NAMING_PATTERNS["deliverable"].match(f.name):
                    r.pass_(f"deliverable: {f.name}")
                else:
                    r.fail(f"deliverable: bad name: {f.name}")
                _check_anti_patterns(r, f.name, "deliverable")

    if file_count == 0:
        r.warn("No artifact files found in canonical paths (directories are empty)")

    return r


def _check_anti_patterns(r: CheckResult, name: str, context: str):
    """Check a filename against anti-patterns."""
    for pat in ANTI_PATTERNS:
        if pat.search(name):
            r.fail(f"{context}: anti-pattern in filename: {name} (matches {pat.pattern})")


def check_no_scratch_in_outputs(repo: Path) -> CheckResult:
    """Check that scratch/temp files are not inside ai/outputs/."""
    r = CheckResult("No scratch files in official outputs")

    output_root = repo / CANONICAL_OUTPUT_ROOT
    if not output_root.exists():
        r.warn("Output root missing, skipping")
        return r

    scratch_indicators = ["scratch", "temp", "tmp", "test", "debug", "draft"]
    found_any = False

    for root, dirs, files in os.walk(output_root):
        for name in files:
            if name == ".gitkeep":
                continue
            found_any = True
            lower = name.lower()
            for ind in scratch_indicators:
                if ind in lower:
                    r.fail(f"Possible scratch file in outputs: {os.path.join(root, name)}")
                    break

    if not r.failed:
        if found_any:
            r.pass_("No scratch-like files found in official output paths")
        else:
            r.pass_("Output directories are clean (empty, pre-migration)")

    return r


def check_registry_fields(repo: Path) -> CheckResult:
    """Check that artifact registry entries have all required fields."""
    r = CheckResult("Artifact registry field completeness")

    registry_path = repo / REGISTRY_FILE
    if not registry_path.exists():
        r.fail(f"Registry file missing: {REGISTRY_FILE}")
        return r

    # Simple YAML parsing (stdlib only, no pyyaml dependency)
    # We parse the artifacts list by looking for entries starting with "  - artifact_id:"
    content = registry_path.read_text(encoding="utf-8")

    # Find all artifact entries
    artifact_blocks = []
    current_block: list[str] = []
    in_artifacts = False
    in_unregistered = False

    for line in content.split("\n"):
        if line.strip() == "artifacts:":
            in_artifacts = True
            continue
        if line.strip() in ("unregistered:", "archived:"):
            in_artifacts = False
            in_unregistered = True
            if current_block:
                artifact_blocks.append(current_block)
                current_block = []
            continue
        if in_unregistered:
            continue

        if in_artifacts:
            if line.startswith("  - "):
                if current_block:
                    artifact_blocks.append(current_block)
                current_block = [line]
            elif current_block and (line.startswith("    ") or line.strip() == ""):
                current_block.append(line)

    if current_block:
        artifact_blocks.append(current_block)

    if not artifact_blocks:
        r.warn("No artifact entries found in registry")
        return r

    r.pass_(f"Found {len(artifact_blocks)} artifact entries")

    for block in artifact_blocks:
        # Extract fields from block
        fields_found = set()
        artifact_id = "unknown"
        for line in block:
            stripped = line.strip().lstrip("- ")
            if ":" in stripped:
                key = stripped.split(":")[0].strip()
                fields_found.add(key)
                if key == "artifact_id":
                    artifact_id = stripped.split(":", 1)[1].strip().strip('"')

        missing = []
        for req in REQUIRED_ARTIFACT_FIELDS:
            if req not in fields_found:
                missing.append(req)

        if missing:
            r.fail(f"Artifact '{artifact_id}' missing fields: {', '.join(missing)}")
        else:
            r.pass_(f"Artifact '{artifact_id}' has all required fields")

    return r


def check_legacy_flat_outputs(repo: Path) -> CheckResult:
    """Check ai/outputs/ for flat (non-governed) Google Ads files."""
    r = CheckResult("Legacy flat outputs inventory")

    outputs_dir = repo / "ai" / "outputs"
    if not outputs_dir.exists():
        r.warn("ai/outputs/ does not exist")
        return r

    flat_files = []
    for item in outputs_dir.iterdir():
        if item.is_file() and not item.name.startswith("."):
            flat_files.append(item.name)

    if flat_files:
        r.warn(f"{len(flat_files)} legacy flat files remain in ai/outputs/ (pending migration)")
        for f in flat_files:
            r.warn(f"  legacy: {f}")
    else:
        r.pass_("No legacy flat files in ai/outputs/")

    return r


def check_validation_naming(repo: Path) -> CheckResult:
    """Check that validation files follow naming convention."""
    r = CheckResult("Validation file naming")

    val_dir = repo / VALIDATION_DIR
    if not val_dir.exists():
        r.warn(f"{VALIDATION_DIR} does not exist")
        return r

    for item in val_dir.iterdir():
        if item.is_file() and not item.name.startswith("."):
            if item.name.endswith("-template.md"):
                continue  # skip templates
            if item.suffix == ".yaml":
                # baseline files are yaml, allowed
                r.pass_(f"baseline: {item.name}")
                continue
            if NAMING_PATTERNS["validation"].match(item.name):
                r.pass_(f"validation: {item.name}")
            else:
                r.fail(f"validation: bad name: {item.name}")

    return r


def check_write_path_test(repo: Path) -> CheckResult:
    """Simulate a write-path test: verify that writing to canonical paths works."""
    r = CheckResult("Write-path test (simulated)")

    test_lane = repo / CANONICAL_OUTPUT_ROOT / "lovefu" / "hillbed" / "evergreen-purchase-pmax"

    # Test 1: Can write to golden/
    golden_test = test_lane / "golden" / ".write-test"
    try:
        golden_test.write_text("write-path-test", encoding="utf-8")
        golden_test.unlink()
        r.pass_("golden/ is writable")
    except Exception as e:
        r.fail(f"golden/ not writable: {e}")

    # Test 2: Can create pipeline task subdir
    pipeline_test_dir = test_lane / "pipeline" / "2026-03-16-governance-test"
    try:
        pipeline_test_dir.mkdir(exist_ok=True)
        test_file = pipeline_test_dir / "builder.json"
        test_file.write_text('{"test": true}', encoding="utf-8")
        # Verify naming passes
        if NAMING_PATTERNS["pipeline-stage"].match(test_file.name):
            r.pass_("pipeline/ task subdir writable, stage file name valid")
        else:
            r.fail("pipeline/ stage file name invalid")
        # Cleanup
        test_file.unlink()
        pipeline_test_dir.rmdir()
    except Exception as e:
        r.fail(f"pipeline/ write test failed: {e}")

    # Test 3: Can write to deliverables/
    deliv_test = test_lane / "deliverables" / ".write-test"
    try:
        deliv_test.write_text("write-path-test", encoding="utf-8")
        deliv_test.unlink()
        r.pass_("deliverables/ is writable")
    except Exception as e:
        r.fail(f"deliverables/ not writable: {e}")

    # Test 4: Can write to scratch
    scratch_test = repo / SCRATCH_ROOT / ".write-test"
    try:
        scratch_test.write_text("write-path-test", encoding="utf-8")
        scratch_test.unlink()
        r.pass_("scratch/ is writable")
    except Exception as e:
        r.fail(f"scratch/ not writable: {e}")

    # Test 5: Validation dir writable
    val_test = repo / VALIDATION_DIR / ".write-test"
    try:
        val_test.write_text("write-path-test", encoding="utf-8")
        val_test.unlink()
        r.pass_("ai/validation/ is writable")
    except Exception as e:
        r.fail(f"ai/validation/ not writable: {e}")

    return r


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Artifact governance check")
    parser.add_argument(
        "--repo-root", default=None,
        help="Repository root (default: auto-detect from script location)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )
    args = parser.parse_args()

    if args.repo_root:
        repo = Path(args.repo_root).resolve()
    else:
        repo = Path(__file__).resolve().parent.parent

    if not (repo / "CLAUDE.md").exists():
        print(f"Error: {repo} does not look like the AI repo root", file=sys.stderr)
        sys.exit(2)

    print(f"Artifact Governance Check")
    print(f"Repo: {repo}")
    print(f"Date: 2026-03-16")

    checks = [
        check_no_gads_in_root(repo),
        check_directory_structure(repo),
        check_naming_compliance(repo),
        check_no_scratch_in_outputs(repo),
        check_registry_fields(repo),
        check_legacy_flat_outputs(repo),
        check_validation_naming(repo),
        check_write_path_test(repo),
    ]

    for c in checks:
        print_result(c)

    # Summary
    total_pass = sum(len(c.passed) for c in checks)
    total_fail = sum(len(c.failed) for c in checks)
    total_warn = sum(len(c.warnings) for c in checks)
    all_ok = all(c.ok for c in checks)

    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Checks run: {len(checks)}")
    print(f"  Passed:     {total_pass}")
    print(f"  Failed:     {total_fail}")
    print(f"  Warnings:   {total_warn}")
    print(f"  Overall:    {'PASS' if all_ok else 'FAIL'}")

    if args.json:
        result = {
            "repo": str(repo),
            "overall": "pass" if all_ok else "fail",
            "checks": [
                {
                    "name": c.name,
                    "status": "pass" if c.ok else "fail",
                    "passed": c.passed,
                    "failed": c.failed,
                    "warnings": c.warnings,
                }
                for c in checks
            ],
            "summary": {
                "total_checks": len(checks),
                "total_passed": total_pass,
                "total_failed": total_fail,
                "total_warnings": total_warn,
            },
        }
        print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
