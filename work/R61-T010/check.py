#!/usr/bin/env python3
"""Compile the article's C++ Solution and reject a one-operation mutant."""
from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/dsa-problems/medium/number-of-provinces.md"
EXPECTED = "2\n3\n1\n"
HARNESS = r'''
int main() {
    Solution solution;
    vector<vector<int>> first{{1,1,0},{1,1,0},{0,0,1}};
    vector<vector<int>> second{{1,0,0},{0,1,0},{0,0,1}};
    vector<vector<int>> boundary{{1}};
    cout << solution.findCircleNum(first) << '\n';
    cout << solution.findCircleNum(second) << '\n';
    cout << solution.findCircleNum(boundary) << '\n';
}
'''


def compile_and_run(source: str, directory: Path, name: str) -> str:
    cpp = directory / f"{name}.cpp"
    exe = directory / name
    cpp.write_text("#include <iostream>\n#include <vector>\nusing namespace std;\n" + source + HARNESS, encoding="utf-8")
    subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", str(cpp), "-o", str(exe)], check=True)
    return subprocess.check_output([str(exe)], text=True, stderr=subprocess.STDOUT)


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    tab = text.split('<TabItem value="cpp"', 1)[1].split("</TabItem>", 1)[0]
    match = re.search(r"```cpp\s*(.*?)```", tab, re.S)
    if not match:
        raise AssertionError("published C++ Solution block not found")
    published = match.group(1)
    mutation_token = "provinces++;"
    if published.count(mutation_token) != 1:
        raise AssertionError("expected exactly one province increment to mutate")
    with tempfile.TemporaryDirectory(prefix="r61-t010-") as temp:
        directory = Path(temp)
        actual = compile_and_run(published, directory, "published")
        if actual != EXPECTED:
            raise AssertionError(f"published output mismatch: {actual!r}")
        mutant = published.replace(mutation_token, "provinces += 0;", 1)
        mutant_output = compile_and_run(mutant, directory, "mutant")
        if mutant_output == EXPECTED:
            raise AssertionError("one-operation mutant escaped the regression test")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text(
        "[[1,1,0],[1,1,0],[0,0,1]]\n[[1,0,0],[0,1,0],[0,0,1]]\n[[1]] (one-city boundary)\n",
        encoding="utf-8",
    )
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    (out / "actual.txt").write_text(actual, encoding="utf-8")
    (out / "mutation.txt").write_text(
        "Temporary mutation: provinces++; -> provinces += 0;\n"
        f"Mutant output: {mutant_output!r}\nExpected: {EXPECTED!r}\nMutation rejected: yes\n",
        encoding="utf-8",
    )
    versions = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    (out / "tool-versions.txt").write_text(f"{versions}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: examples and one-city boundary match; increment mutant rejected.")


if __name__ == "__main__":
    main()
