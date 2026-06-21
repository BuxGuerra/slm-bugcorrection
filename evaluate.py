#!/usr/bin/env python3
"""Main CLI to evaluate SLMs (via llama.cpp) on bug identification and correction.

Examples:
    python evaluate.py                                   # uses config.json
    python evaluate.py --models qwen2.5-coder:1.5b --bugs 'bug_01_*' --task both
    python evaluate.py --models a,b --n-samples 5 --temperature 0.8 --task correction
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from eval.dataset import load_bugs
from eval.api_client import APIClient, APIError
from eval.run_correction import run_correction
from eval.run_identification import run_identification

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config.json"
RESULTS_DIR = ROOT / "results"


def load_config(path: Path) -> dict:
    base = {
        "model_host": "http://localhost:8080",
        "models": [],
        "n_samples": 1,
        "temperature": 0.0,
        "test_timeout_seconds": 10,
        "request_timeout_seconds": 120,
    }
    if path.exists():
        base.update(json.loads(path.read_text()))
    return base


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate SLMs via llama.cpp on bug correction/identification.")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--models", help="Comma-separated list of models (overrides the config).")
    p.add_argument("--bugs", help="Comma-separated folder patterns (e.g. 'bug_01_*,bug_2*').")
    p.add_argument("--task", choices=["correction", "identification", "both"], default="both")
    p.add_argument("--n-samples", type=int, dest="n_samples")
    p.add_argument("--temperature", type=float)
    return p.parse_args()


def safe_dirname(model: str) -> str:
    return model.replace("/", "_")


def main() -> int:
    args = parse_args()
    cfg = load_config(args.config)

    models = (
        [m.strip() for m in args.models.split(",") if m.strip()]
        if args.models
        else cfg["models"]
    )
    if not models:
        print("No models defined. Use --models or fill in 'models' in config.json.")
        return 2

    n_samples = args.n_samples if args.n_samples is not None else cfg["n_samples"]
    temperature = args.temperature if args.temperature is not None else cfg["temperature"]
    bug_patterns = [b.strip() for b in args.bugs.split(",")] if args.bugs else None

    bugs = load_bugs(bug_patterns)
    if not bugs:
        print("No bugs found for the given patterns.")
        return 2

    try:
        client = APIClient(cfg["model_host"], request_timeout=cfg["request_timeout_seconds"])
    except APIError as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"Models: {', '.join(models)}")
    print(f"Bugs: {len(bugs)} | task: {args.task} | n_samples={n_samples} temp={temperature}\n")

    report_rows: list[dict] = []
    for model in models:
        print(f"=== {model} ===")
        try:
            client.ensure_model(model)
        except APIError as exc:
            print(f"  SKIPPING: {exc}\n")
            continue

        out_dir = RESULTS_DIR / safe_dirname(model)
        out_dir.mkdir(parents=True, exist_ok=True)
        summary: dict = {"model": model}

        if args.task in ("correction", "both"):
            print("  correction...")
            corr = run_correction(
                client, model, bugs, out_dir,
                n_samples=n_samples, temperature=temperature,
                test_timeout=cfg["test_timeout_seconds"],
            )
            summary["correction"] = corr
            print(f"    pass@1={corr['pass@1']}  pass@{n_samples}={corr[f'pass@{n_samples}']}")

        if args.task in ("identification", "both"):
            print("  identification...")
            ident = run_identification(client, model, bugs, out_dir)
            summary["identification"] = ident
            print(f"    acc={ident['accuracy']}  precision={ident['precision']}  "
                  f"recall={ident['recall']}  f1={ident['f1']}")

        (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
        report_rows.append(_flatten_summary(summary, n_samples))
        print()

    if report_rows:
        _write_report(report_rows, n_samples)
        print(f"Consolidated report: {RESULTS_DIR / 'report.csv'}")
    return 0


def _flatten_summary(summary: dict, n_samples: int) -> dict:
    row = {"model": summary["model"]}
    corr = summary.get("correction")
    if corr:
        row["pass@1"] = corr["pass@1"]
        row[f"pass@{n_samples}"] = corr[f"pass@{n_samples}"]
    ident = summary.get("identification")
    if ident:
        row["id_accuracy"] = ident["accuracy"]
        row["id_precision"] = ident["precision"]
        row["id_recall"] = ident["recall"]
        row["id_f1"] = ident["f1"]
    return row


def _write_report(rows: list[dict], n_samples: int) -> None:
    fields = ["model", "pass@1", f"pass@{n_samples}",
              "id_accuracy", "id_precision", "id_recall", "id_f1"]
    fields = [f for f in fields if any(f in r for r in rows)]
    with (RESULTS_DIR / "report.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fields})


if __name__ == "__main__":
    raise SystemExit(main())
