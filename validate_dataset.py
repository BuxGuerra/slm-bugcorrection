#!/usr/bin/env python3
"""Validates the bug dataset.

For each folder in ``dataset/`` the script:
  1. copies ``fix.py`` -> ``solution.py`` and runs pytest -> must PASS (correct tests);
  2. copies ``buggy.py`` -> ``solution.py`` and runs pytest -> must FAIL (the bug is real and detectable);
  3. removes the temporary ``solution.py``;
  4. checks that ``meta.json`` has all fields and that ``entry_point`` appears in both sources.

Usage:
    python validate_dataset.py            # validate everything
    python validate_dataset.py bug_01_*   # validate folders matching the pattern
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DATASET_DIR = Path(__file__).parent / "dataset"
REQUIRED_META_FIELDS = [
    "id",
    "title",
    "category",
    "difficulty",
    "description",
    "bug_summary",
    "entry_point",
]


def run_pytest(folder: Path) -> bool:
    """Runs pytest inside ``folder``. Returns True if all tests passed.

    Clears the `solution` bytecode and disables .pyc writing to prevent Python
    from reusing a stale .pyc: buggy.py and fix.py can have the same size and be
    copied within the same second, which confuses mtime+size invalidation.
    """
    for pyc in (folder / "__pycache__").glob("solution.*"):
        pyc.unlink()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=folder,
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.returncode == 0


def check_meta(folder: Path) -> list[str]:
    """Returns a list of problems found in meta.json (empty = ok)."""
    problems: list[str] = []
    meta_path = folder / "meta.json"
    if not meta_path.exists():
        return ["meta.json missing"]
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError as exc:
        return [f"invalid meta.json: {exc}"]

    for field in REQUIRED_META_FIELDS:
        if not meta.get(field):
            problems.append(f"field '{field}' missing/empty")

    entry = meta.get("entry_point")
    if entry:
        for src in ("buggy.py", "fix.py"):
            text = (folder / src).read_text() if (folder / src).exists() else ""
            if f"def {entry}" not in text:
                problems.append(f"entry_point '{entry}' not defined in {src}")
    return problems


def validate_folder(folder: Path) -> dict:
    """Validates a bug folder and returns a results dictionary."""
    result = {"name": folder.name, "fix_ok": False, "buggy_detected": False, "meta": []}
    solution = folder / "solution.py"
    try:
        # 1. reference solution must pass
        shutil.copy(folder / "fix.py", solution)
        result["fix_ok"] = run_pytest(folder)

        # 2. buggy version must fail
        shutil.copy(folder / "buggy.py", solution)
        result["buggy_detected"] = not run_pytest(folder)
    finally:
        if solution.exists():
            solution.unlink()

    # 3. metadata
    result["meta"] = check_meta(folder)
    return result


def main() -> int:
    if not DATASET_DIR.exists():
        print(f"ERROR: folder {DATASET_DIR} not found.", file=sys.stderr)
        return 2

    patterns = sys.argv[1:] or ["*"]
    folders = sorted(
        f
        for pat in patterns
        for f in DATASET_DIR.glob(pat)
        if f.is_dir() and (f / "test_bug.py").exists()
    )
    folders = sorted(set(folders), key=lambda p: p.name)

    if not folders:
        print("No bug folders found.", file=sys.stderr)
        return 2

    fix_ok = buggy_ok = meta_ok = 0
    failures: list[str] = []

    for folder in folders:
        r = validate_folder(folder)
        status_fix = "OK " if r["fix_ok"] else "FAILED"
        status_bug = "OK " if r["buggy_detected"] else "FAILED"
        meta_clean = not r["meta"]
        print(
            f"  {r['name']:<28} fix={status_fix}  bug-detected={status_bug}  "
            f"meta={'OK' if meta_clean else 'PROBLEMS'}"
        )
        fix_ok += r["fix_ok"]
        buggy_ok += r["buggy_detected"]
        meta_ok += meta_clean
        if not r["fix_ok"]:
            failures.append(f"{r['name']}: reference solution (fix.py) did NOT pass the tests")
        if not r["buggy_detected"]:
            failures.append(f"{r['name']}: bug was NOT detected (buggy.py passed the tests)")
        for p in r["meta"]:
            failures.append(f"{r['name']}: {p}")

    total = len(folders)
    print("\nSummary:")
    print(f"  Reference solutions passing: {fix_ok}/{total}")
    print(f"  Bugs detected:               {buggy_ok}/{total}")
    print(f"  Valid metadata:              {meta_ok}/{total}")

    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\nDataset valid. ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
