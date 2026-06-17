"""Correction task: the model fixes buggy.py; the oracle is the test suite."""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from .dataset import Bug
from .extract import extract_code
from .metrics import pass_at_k
from .ollama_client import OllamaClient, OllamaError
from .prompts import correction_prompt
from .run_tests import run_candidate


def run_correction(
    client: OllamaClient,
    model: str,
    bugs: list[Bug],
    out_dir: Path,
    n_samples: int = 1,
    temperature: float = 0.0,
    test_timeout: int = 10,
) -> dict:
    """Runs correction for all bugs and writes correction.jsonl. Returns a summary."""
    records_path = out_dir / "correction.jsonl"
    per_bug: list[dict] = []

    with records_path.open("w") as f:
        for bug in bugs:
            prompt = correction_prompt(bug.buggy_code)
            correct = 0
            for i in range(n_samples):
                # greedy when n=1; varying seed when sampling for pass@k
                seed = None if (n_samples == 1 and temperature == 0.0) else i
                error = None
                try:
                    response = client.generate(model, prompt, temperature, seed=seed)
                except OllamaError as exc:
                    response, error = "", str(exc)
                code = extract_code(response) if response else ""
                result = run_candidate(bug.path, code, timeout=test_timeout) if code else None
                passed = bool(result and result.passed)
                correct += int(passed)
                f.write(json.dumps({
                    "bug_id": bug.name,
                    "category": bug.category,
                    "difficulty": bug.difficulty,
                    "sample": i,
                    "passed": passed,
                    "timed_out": bool(result and result.timed_out),
                    "error": error,
                    "extracted_code": code,
                    "raw_response": response,
                }, ensure_ascii=False) + "\n")

            per_bug.append({
                "bug_id": bug.name,
                "category": bug.category,
                "difficulty": bug.difficulty,
                "n": n_samples,
                "c": correct,
                "pass@1": pass_at_k(n_samples, correct, 1),
                f"pass@{n_samples}": pass_at_k(n_samples, correct, n_samples),
            })

    return _aggregate(per_bug, n_samples)


def _aggregate(per_bug: list[dict], n_samples: int) -> dict:
    by_category: dict[str, list[float]] = {}
    by_difficulty: dict[str, list[float]] = {}
    for r in per_bug:
        by_category.setdefault(r["category"], []).append(r["pass@1"])
        by_difficulty.setdefault(r["difficulty"], []).append(r["pass@1"])
    return {
        "task": "correction",
        "n_bugs": len(per_bug),
        "n_samples": n_samples,
        "pass@1": round(mean(r["pass@1"] for r in per_bug), 4) if per_bug else 0.0,
        f"pass@{n_samples}": round(mean(r[f"pass@{n_samples}"] for r in per_bug), 4) if per_bug else 0.0,
        "by_category": {k: round(mean(v), 4) for k, v in sorted(by_category.items())},
        "by_difficulty": {k: round(mean(v), 4) for k, v in sorted(by_difficulty.items())},
        "per_bug": per_bug,
    }
