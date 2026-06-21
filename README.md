# slm-bugcorrection

Evaluation of **small language models (SLMs)** on bug identification and correction in Python.

The repository currently contains the first two stages of the project: the bug **dataset** and the
**evaluation harness** that runs models via llama.cpp.

## Structure

```
dataset/
  bug_01_off_by_one/
    buggy.py      # code with the bug (input given to the SLM)
    fix.py        # reference fix: correct version
    test_bug.py   # pytest tests (oracle); import the `solution` module
    meta.json     # bug metadata
  bug_02_.../
  ...
validate_dataset.py  # validates the whole dataset
eval/                # evaluation harness (Stage 2)
evaluate.py          # main CLI
config.json
requirements.txt
```

There are **20 bugs**, each a small self-contained function, covering a varied mix of categories
(off-by-one, boolean logic, type conversion, recursion, floating point, swallowed exception, etc.).

## The `solution.py` convention

The tests (`test_bug.py`) do **not** import from `buggy.py` or `fix.py` directly. They import from a
neutral module called `solution`:

```python
from solution import sum_range
```

The `solution.py` file is the **target under evaluation** and only exists temporarily in the folder:

- copy `fix.py` → `solution.py` and the tests **pass** (correct reference);
- copy `buggy.py` → `solution.py` and at least one test **fails** (the bug is real);
- the SLM later generates `solution.py` and it is tested in exactly the same way.

This keeps `buggy.py`/`fix.py` stable and decouples the tests from the concrete file.

## Stage 1 — Dataset

```bash
pip install -r requirements.txt
python validate_dataset.py        # expect 20/20 for reference solutions and detected bugs
```

Manual spot-check of one bug:

```bash
cd dataset/bug_01_off_by_one
cp fix.py solution.py   && pytest -q   # passes
cp buggy.py solution.py && pytest -q   # fails
rm solution.py
```

### Adding a new bug

1. Create `dataset/bug_NN_<category>/` with `buggy.py`, `fix.py`, `test_bug.py` and `meta.json`.
2. In `test_bug.py`, import the function(s) from `solution`.
3. Make sure the tests **pass with `fix.py`** and **fail with `buggy.py`**.
4. Run `python validate_dataset.py bug_NN_*` to validate.

## Stage 2 — Evaluation with SLMs (llama.cpp)

The harness in `eval/` runs models via [llama.cpp](https://llama-cpp.com/) (local) on two tasks:

- **Identification** (binary classification): the model receives a piece of code and answers
  `CORRECT` or `BUG`. Evaluated over the 20 `buggy.py` (expected: buggy) + 20 `fix.py`
  (expected: correct) → accuracy, precision, recall, F1.
- **Correction**: the model receives `buggy.py` (without seeing the tests) and returns the corrected
  code; the oracle is the test suite. Reports **pass@1** and **pass@k**.

### Prerequisites

```bash
pip install -r requirements.txt
llama-cli -m model-name.gguf    # server running with the models loaded
```

### Running

Models can be defined in `config.json` (the `models` field) or via `--models`:

```bash
# uses config.json
python evaluate.py

# overriding via CLI
python evaluate.py --models qwen2.5-coder:1.5b,llama3.2:1b --task both

# pass@k: multiple samples with temperature
python evaluate.py --models qwen2.5-coder:1.5b --n-samples 5 --temperature 0.8 --task correction

# subset of bugs
python evaluate.py --models qwen2.5-coder:1.5b --bugs 'bug_01_*,bug_2*'
```

Outputs in `results/<model>/` (`correction.jsonl`, `identification.jsonl`, `summary.json`) and the
consolidated `results/report.csv` (one row per model).

### Harness tests

```bash
python -m pytest eval/test_eval.py -q   # metric/extraction sanity checks (no llama.cpp)
```
