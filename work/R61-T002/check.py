#!/usr/bin/env python3
"""Compile and run the C++ solution extracted from the published tab."""
from pathlib import Path
import re
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "docs/dsa-problems/easy/left-and-right-sum-differences.md"
EXPECTED = "15 1 11 22\n0\n"


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    cpp_tab = text.split('<TabItem value="cpp"', 1)[1].split("</TabItem>", 1)[0]
    match = re.search(r"```cpp\s*(.*?)```", cpp_tab, re.S)
    if not match:
        raise AssertionError("C++ solution block not found")
    source = "#include <cstdlib>\n#include <iostream>\n#include <vector>\nusing namespace std;\n" + match.group(1)
    source += r'''
int main() {
    Solution solution;
    vector<int> worked{10, 4, 8, 3};
    vector<int> boundary{1};
    auto print = [](const vector<int>& values) {
        for (size_t i = 0; i < values.size(); ++i) {
            if (i) cout << ' ';
            cout << values[i];
        }
        cout << '\n';
    };
    print(solution.leftRightDifference(worked));
    print(solution.leftRightDifference(boundary));
}
'''
    with tempfile.TemporaryDirectory(prefix="r61-t002-") as temp:
        cpp = Path(temp) / "published.cpp"
        exe = Path(temp) / "published"
        cpp.write_text(source, encoding="utf-8")
        subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", str(cpp), "-o", str(exe)], check=True)
        actual = subprocess.check_output([str(exe)], text=True)
        if actual != EXPECTED:
            raise AssertionError(f"output mismatch\nexpected: {EXPECTED!r}\nactual:   {actual!r}")
        (Path(__file__).parent / "actual.txt").write_text(actual, encoding="utf-8")
    out = Path(__file__).parent
    (out / "inputs.txt").write_text("nums=[10, 4, 8, 3]\nnums=[1] (single-element boundary)\n", encoding="utf-8")
    (out / "expected.txt").write_text(EXPECTED, encoding="utf-8")
    versions = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    (out / "tool-versions.txt").write_text(f"{versions}\nPython {sys.version.split()[0]}\n", encoding="utf-8")
    print("PASS: published C++ solution produced both documented arrays.")


if __name__ == "__main__":
    main()
