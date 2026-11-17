#!/usr/bin/env python3
"""Compile and run the published Levenshtein implementation and comparison."""
from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/algorithms/string-algorithms/levenshtein-distance-algorithm.md"
EXPECTED_LINES = [
    "Levenshtein distance: 3",
    "Rolling-row distance: 3",
    "Empty-string boundary: 7",
]


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    block = re.search(r"### C\+\+ Implementation:\s*```cpp\s*(.*?)```", text, re.S)
    if not block:
        raise AssertionError("published C++ implementation not found")
    with tempfile.TemporaryDirectory(prefix="r61-t003-") as temp:
        source = Path(temp) / "published.cpp"
        executable = Path(temp) / "published"
        source.write_text(block.group(1), encoding="utf-8")
        subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", str(source), "-o", str(executable)], check=True)
        actual = subprocess.check_output([str(executable)], text=True, stderr=subprocess.STDOUT)
    for expected in EXPECTED_LINES:
        if expected not in actual.splitlines():
            raise AssertionError(f"missing output {expected!r}; actual output:\n{actual}")
    out = Path(__file__).parent
    inputs = '"kitten" -> "sitting"\n"" -> "sitting"\n'
    (out / "inputs.txt").write_text(inputs, encoding="utf-8")
    (out / "expected.txt").write_text("\n".join(EXPECTED_LINES) + "\n", encoding="utf-8")
    (out / "actual.txt").write_text("\n".join(line for line in actual.splitlines() if line in EXPECTED_LINES) + "\n", encoding="utf-8")
    versions = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    (out / "tool-versions.txt").write_text(f"{versions}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: both published methods return 3; empty-string distance is 7.")


if __name__ == "__main__":
    main()
