import os

os.environ["MPLBACKEND"] = "Agg"

import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

DOC_PATH = Path("docs/extra/machine-learning/HierarchialClustering.md")


def extract_blocks(markdown_text: str):
    py_match = re.search(r"```python\n(.*?)\n```", markdown_text, re.DOTALL)
    out_match = re.search(
        r"#### Expected Output\s+```text\n(.*?)\n```", markdown_text, re.DOTALL
    )
    if not py_match or not out_match:
        raise AssertionError("Could not find ```python block or #### Expected Output block.")
    return py_match.group(1), out_match.group(1).strip()


def run_check():
    content = DOC_PATH.read_text(encoding="utf-8")
    code_block, expected_output = extract_blocks(content)

    stdout_buffer = io.StringIO()
    namespace = {}
    with redirect_stdout(stdout_buffer):
        exec(code_block, namespace)

    actual_output = stdout_buffer.getvalue().strip()

    assert actual_output == expected_output, (
        f"Output mismatch!\nExpected:\n{expected_output}\n\nActual:\n{actual_output}"
    )

    # Deliberate wrong result check must fail
    wrong_output = expected_output.replace("[1 2]", "[1 1]")
    assert actual_output != wrong_output, "Negative check failed to detect wrong output."

    return expected_output, actual_output


if __name__ == "__main__":
    try:
        expected, actual = run_check()
        print("PASS: Published example executed and matched expected output.")
        print(actual)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
