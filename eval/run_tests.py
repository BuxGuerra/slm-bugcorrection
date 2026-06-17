"""Runs a bug's tests against a candidate piece of code (the model output)."""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestResult:
    passed: bool
    timed_out: bool
    returncode: int | None
    output: str


def run_candidate(bug_dir: Path, code: str, timeout: int = 10) -> TestResult:
    """Writes `code` as solution.py in `bug_dir`, runs pytest and returns the result.

    Reuses the `solution.py` convention and the stale-.pyc safeguard from Stage 1
    (clears __pycache__/solution.* + PYTHONDONTWRITEBYTECODE=1), with a timeout for
    code that enters an infinite loop.
    """
    solution = bug_dir / "solution.py"
    try:
        solution.write_text(code if code.endswith("\n") else code + "\n")
        for pyc in (bug_dir / "__pycache__").glob("solution.*"):
            pyc.unlink()
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=bug_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            output = exc.output
            if isinstance(output, bytes):
                output = output.decode(errors="replace")
            return TestResult(False, True, None, output or "")
        return TestResult(proc.returncode == 0, False, proc.returncode, proc.stdout + proc.stderr)
    finally:
        if solution.exists():
            solution.unlink()
