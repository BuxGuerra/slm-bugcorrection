"""Loads the bug folders from the dataset."""
from __future__ import annotations

import json
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"


@dataclass
class Bug:
    """Represents a bug folder from the dataset."""

    name: str
    path: Path
    meta: dict

    @property
    def buggy_code(self) -> str:
        return (self.path / "buggy.py").read_text()

    @property
    def fix_code(self) -> str:
        return (self.path / "fix.py").read_text()

    @property
    def category(self) -> str:
        return self.meta.get("category", "?")

    @property
    def difficulty(self) -> str:
        return self.meta.get("difficulty", "?")


def load_bugs(patterns: list[str] | None = None, dataset_dir: Path = DATASET_DIR) -> list[Bug]:
    """Loads the bug folders matching any of the patterns (default: all)."""
    patterns = patterns or ["*"]
    bugs: list[Bug] = []
    for folder in sorted(dataset_dir.iterdir()):
        if not folder.is_dir() or not (folder / "test_bug.py").exists():
            continue
        if not any(fnmatch(folder.name, pat) for pat in patterns):
            continue
        meta = json.loads((folder / "meta.json").read_text())
        bugs.append(Bug(name=folder.name, path=folder, meta=meta))
    return bugs
