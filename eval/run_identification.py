"""Identification task: classify each piece of code as 'buggy' or 'correct'."""
from __future__ import annotations

import json
from pathlib import Path

from .dataset import Bug
from .extract import extract_label
from .metrics import classification_metrics
from .api_client import APIClient, APIError
from .prompts import identification_prompt


def run_identification(
    client: APIClient,
    model: str,
    bugs: list[Bug],
    out_dir: Path,
    temperature: float = 0.0,
) -> dict:
    """Classifies both variants (buggy/fix) of each bug and writes identification.jsonl."""
    records_path = out_dir / "identification.jsonl"
    pairs: list[tuple[str, str]] = []

    with records_path.open("w") as f:
        for bug in bugs:
            for variant, code, expected in (
                ("buggy", bug.buggy_code, "buggy"),
                ("fix", bug.fix_code, "correct"),
            ):
                prompt = identification_prompt(code)
                error = None
                try:
                    response = client.generate(model, prompt, temperature, seed=0)
                except APIError as exc:
                    response, error = "", str(exc)
                predicted = extract_label(response) if response else "unknown"
                pairs.append((expected, predicted))
                f.write(json.dumps({
                    "bug_id": bug.name,
                    "category": bug.category,
                    "variant": variant,
                    "expected": expected,
                    "predicted": predicted,
                    "correct": predicted == expected,
                    "error": error,
                    "raw_response": response,
                }, ensure_ascii=False) + "\n")

    metrics = classification_metrics(pairs)
    return {"task": "identification", "n_instances": len(pairs), **metrics.as_dict()}
