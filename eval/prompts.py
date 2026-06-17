"""Prompt templates for the correction and identification tasks."""
from __future__ import annotations

CORRECTION_PROMPT = """\
The following Python code contains a bug. Fix it.

Respond ONLY with the corrected Python code, inside a single code block:

```python
# corrected code here
```

Do not write explanations, extra comments, or any text outside the code block.

```python
{code}
```
"""

IDENTIFICATION_PROMPT = """\
Analyze the following Python code and decide whether it is correct or contains a bug.

Respond with ONLY ONE word, with no explanation:
- `CORRECT` if the code is correct;
- `BUG` if the code contains a bug.

```python
{code}
```
"""


def correction_prompt(code: str) -> str:
    return CORRECTION_PROMPT.format(code=code.rstrip("\n"))


def identification_prompt(code: str) -> str:
    return IDENTIFICATION_PROMPT.format(code=code.rstrip("\n"))
