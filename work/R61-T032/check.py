import re
import subprocess
import sys
from pathlib import Path

DOC_PATH = Path("docs/extra/algorithms/Scheduling Algorithms/PriorityScheduling.md")


def extract_blocks(markdown_text: str):
    py_match = re.search(r"```python\n(.*?)\n```", markdown_text, re.DOTALL)
    out_match = re.search(
        r"## Example Output.*?```plaintext\n(.*?)\n```", markdown_text, re.DOTALL
    )
    if not py_match or not out_match:
        raise AssertionError("Could not find ```python block or ```plaintext Example Output block.")
    return py_match.group(1), out_match.group(1).strip()


def run_check():
    content = DOC_PATH.read_text(encoding="utf-8")
    code_block, expected_output = extract_blocks(content)

    proc = subprocess.run(
        [sys.executable, "-c", code_block],
        capture_output=True,
        text=True,
        check=True,
    )
    actual_output = proc.stdout.strip()

    assert actual_output == expected_output, (
        f"Output mismatch!\nExpected:\n{expected_output}\n\nActual:\n{actual_output}"
    )

    wrong_output = expected_output.replace("Average waiting time = 6.25", "Average waiting time = 9.99")
    assert actual_output != wrong_output, "Negative check failed to detect wrong output."

    return actual_output


if __name__ == "__main__":
    try:
        actual = run_check()
        print("PASS: Published PriorityScheduling example executed and matched expected output.")
        print(actual)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
