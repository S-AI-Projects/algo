#!/usr/bin/env python3
"""Run the JavaScript rest-parameter example extracted from the article."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/programming-fundamentals/functions/arguments-vs-parameters.md"
EXPECTED = "15\n0\n"


def main() -> None:
    node = shutil.which("node")
    if not node:
        raise SystemExit("Node.js is required (node was not found on PATH).")
    text = ARTICLE.read_text(encoding="utf-8")
    section = text.split("#### A. JavaScript (Rest Parameters)", 1)[1].split("#### B.", 1)[0]
    start = section.index("```javascript") + len("```javascript")
    code = section[start:section.index("```", start)].strip() + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as source:
        source.write(code)
        source.flush()
        actual = subprocess.check_output([node, source.name], text=True, stderr=subprocess.STDOUT)
    if actual != EXPECTED:
        raise AssertionError(f"output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual!r}")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("sumAll(1, 2, 3, 4, 5)\nsumAll()\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    version = subprocess.check_output([node, "--version"], text=True).strip()
    (out / "tool-versions.txt").write_text(f"{version}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: five-argument call and empty rest-parameter boundary match.")


if __name__ == "__main__":
    main()
