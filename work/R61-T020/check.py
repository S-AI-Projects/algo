#!/usr/bin/env python3
"""Run the published Huffman example and prove it catches a merge mutant."""
import json
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/extra/algorithms/greedy-algorithms/commonly-asked-greedy-questions.md"
OUT = Path(__file__).with_name("results.json")
EXPECTED = """A: 1100
B: 1101
C: 100
D: 101
E: 111
F: 0
single symbol: {'X': '0'}
empty input: {}
"""


def run(source, path):
    path.write_text(source)
    return subprocess.run(
        [sys.executable, str(path)], text=True, capture_output=True, check=False
    )


def main():
    source = DOC.read_text()
    snippets = re.findall(r"```python\s*\n(.*?)\n```", source, re.S)
    if len(snippets) != 1:
        raise AssertionError(f"Expected one published Python example, found {len(snippets)}")
    example = snippets[0]

    with tempfile.TemporaryDirectory() as temp_dir:
        script = Path(temp_dir) / "huffman_example.py"
        correct = run(example, script)
        if correct.returncode:
            raise subprocess.CalledProcessError(
                correct.returncode, correct.args, correct.stdout, correct.stderr
            )
        if correct.stdout != EXPECTED:
            raise AssertionError(f"Expected output {EXPECTED!r}, got {correct.stdout!r}")

        # One-operation mutant: combining frequencies with multiplication instead of addition.
        mutant = example.replace("left_frequency + right_frequency", "left_frequency * right_frequency")
        if mutant == example:
            raise AssertionError("Could not apply the deliberate merge-weight mutant")
        mutant_result = run(mutant, Path(temp_dir) / "huffman_mutant.py")
        mutant_detected = mutant_result.returncode != 0 or mutant_result.stdout != EXPECTED
        if not mutant_detected:
            raise AssertionError("Example check did not distinguish the merge-weight mutant")

    result = {
        "article_example": {"expected_stdout": EXPECTED, "actual_stdout": correct.stdout},
        "boundary_cases": {"single_symbol": "{'X': '0'}", "empty_input": "{}"},
        "runtime": {"python": platform.python_version(), "executable": sys.executable},
        "mutant_test": {
            "mutation": "left_frequency + right_frequency -> left_frequency * right_frequency",
            "mutant_exit_code": mutant_result.returncode,
            "mutant_stdout": mutant_result.stdout,
            "detected": mutant_detected,
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
