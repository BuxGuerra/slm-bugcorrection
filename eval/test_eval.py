"""Sanity tests for the harness that do not depend on llama.cpp.

Run from the project root:  python -m pytest eval/test_eval.py -q
"""
from eval.extract import extract_code, extract_label
from eval.metrics import classification_metrics, pass_at_k
from eval.run_tests import run_candidate
from eval.dataset import load_bugs


def test_pass_at_k_all_correct():
    assert pass_at_k(5, 5, 1) == 1.0
    assert pass_at_k(5, 5, 5) == 1.0


def test_pass_at_k_none_correct():
    assert pass_at_k(5, 0, 1) == 0.0
    assert pass_at_k(5, 0, 5) == 0.0


def test_pass_at_k_partial():
    # 1 out of 2 correct: pass@1 = 0.5
    assert abs(pass_at_k(2, 1, 1) - 0.5) < 1e-9


def test_extract_code_fenced():
    resp = "Sure!\n```python\ndef f():\n    return 1\n```\nDone."
    assert extract_code(resp) == "def f():\n    return 1"


def test_extract_code_no_fence():
    assert extract_code("def f(): return 1") == "def f(): return 1"


def test_extract_label():
    assert extract_label("BUG") == "buggy"
    assert extract_label("CORRECT") == "correct"
    assert extract_label("This code has a BUG on line 2.") == "buggy"
    assert extract_label("The code is CORRECT.") == "correct"
    assert extract_label("not sure") == "unknown"


def test_classification_metrics_perfect():
    pairs = [("buggy", "buggy"), ("correct", "correct")]
    m = classification_metrics(pairs)
    assert m.accuracy == 1.0
    assert m.precision == 1.0
    assert m.recall == 1.0
    assert m.f1 == 1.0


def test_run_candidate_consistency():
    """fix.py passes and buggy.py fails — consistency with Stage 1."""
    bug = load_bugs(["bug_01_*"])[0]
    assert run_candidate(bug.path, bug.fix_code).passed is True
    assert run_candidate(bug.path, bug.buggy_code).passed is False
