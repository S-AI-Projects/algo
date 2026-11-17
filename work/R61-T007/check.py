#!/usr/bin/env python3
"""Compile and run the C++ coloring example extracted from the article."""
from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/extra/greedy-algorithms/Graph-Coloring.md"
EXPECTED = "Vertex\tColor\n0\t0\n1\t1\n2\t1\n3\t0\nBoundary (one vertex) stored color: 0\n"


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    block = re.search(r"### C\+\+ Implementation:\s*```cpp\s*(.*?)```", text, re.S)
    if not block:
        raise AssertionError("published C++ implementation not found")
    with tempfile.TemporaryDirectory(prefix="r61-t007-") as temp:
        cpp = Path(temp) / "published.cpp"
        exe = Path(temp) / "published"
        cpp.write_text(block.group(1), encoding="utf-8")
        subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", str(cpp), "-o", str(exe)], check=True)
        actual = subprocess.check_output([str(exe)], text=True, stderr=subprocess.STDOUT)
    if actual != EXPECTED:
        raise AssertionError(f"output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual!r}")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("V=4; edges={(0,1),(0,2),(1,3),(2,3)}\nBoundary: V=1; adjacency=[[]]\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    versions = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    (out / "tool-versions.txt").write_text(f"{versions}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: worked coloring is [0,1,1,0]; one-vertex boundary uses color 0.")


if __name__ == "__main__":
    main()
