"""Extracts code and classification label from model responses."""
from __future__ import annotations

import re

_CODE_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_code(response: str) -> str:
    """Extracts code from a model response.

    Prefers the first ```-fenced block (with or without the language tag).
    If there is no block, returns the raw text (stripped of surrounding whitespace).
    """
    match = _CODE_FENCE.search(response)
    if match:
        return match.group(1).strip("\n")
    return response.strip()


def extract_label(response: str) -> str:
    """Extracts the classification label.

    Returns "buggy", "correct" or "unknown". The BUG check comes first because
    responses often contain the word explicitly; "CORRECT" does not contain "BUG".
    """
    upper = response.upper()
    has_bug = re.search(r"\bBUG\b", upper) is not None
    has_correct = re.search(r"\bCORRECT\b", upper) is not None
    if has_bug and not has_correct:
        return "buggy"
    if has_correct and not has_bug:
        return "correct"
    if has_bug and has_correct:
        # ambiguous: use whichever appears first in the text
        return "buggy" if upper.find("BUG") < upper.find("CORRECT") else "correct"
    return "unknown"
