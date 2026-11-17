#!/usr/bin/env python3
"""Run the exact Fibonacci example from the recursion article."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/Recursion-depths/performance-consideration.md"
EXPECTED = (
    "F(6) = 8\n"
    "Naive recursive calls: 25; deepest active calls: 6\n"
    "Memoized cache misses: 7; hits: 4; deepest first descent: 6\n"
    "Iterative boundary F(0) = 0\n"
)


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    start = text.index("```python") + len("```python")
    code = text[start:text.index("```", start)].strip() + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as source:
        source.write(code)
        source.flush()
        actual = subprocess.check_output([sys.executable, source.name], text=True, stderr=subprocess.STDOUT)
    if actual != EXPECTED:
        raise AssertionError(f"output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual!r}")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("n=6\nBoundary n=0\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    (out / "tool-versions.txt").write_text(f"{sys.version.splitlines()[0]}\n", encoding="utf-8")
    print("PASS: Fibonacci values, call counts, cache counts, and boundary match.")


if __name__ == "__main__":
    main()
