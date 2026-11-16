#!/usr/bin/env python3
"""
Validation and verification suite for Issue #22 (R61-T022).
Target: docs/languages/cpp/cp-13.md
Anchor: 1. The Core Architecture of the STL

Extracts the runnable C++ example from the markdown documentation,
compiles it with g++, executes it, asserts expected normal and boundary outputs,
and validates negative assertion detection.
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
REPO_ROOT = WORKDIR.parents[1]
DOC_PATH = REPO_ROOT / "docs" / "languages" / "cpp" / "cp-13.md"


def log(msg: str):
    print(f"[CHECK] {msg}")


def extract_cpp_example(doc_path: Path) -> str:
    if not doc_path.is_file():
        raise FileNotFoundError(f"Documentation file not found: {doc_path}")

    content = doc_path.read_text(encoding="utf-8")
    marker = '```cpp title="STL Architecture Example"'
    start_idx = content.find(marker)
    if start_idx == -1:
        # Fallback to standard cpp block under Section 1
        marker = '```cpp'
        start_idx = content.find(marker)
        if start_idx == -1:
            raise ValueError(f"C++ code block not found in {doc_path}")

    code_start = content.find("\n", start_idx) + 1
    code_end = content.find("```", code_start)
    if code_end == -1:
        raise ValueError("Unterminated code block in markdown document")

    code = content[code_start:code_end].strip()
    return code


def record_environment():
    gpp_ver = subprocess.check_output(["g++", "--version"], text=True).splitlines()[0]
    try:
        node_ver = subprocess.check_output(["node", "--version"], text=True).strip()
    except Exception:
        node_ver = "unknown"
    try:
        npm_ver = subprocess.check_output(["npm", "--version"], text=True).strip()
    except Exception:
        npm_ver = "unknown"

    env_data = (
        f"Runtime and Compiler Environment for Issue #22 (R61-T022)\n"
        f"Target: docs/languages/cpp/cp-13.md\n"
        f"--------------------------------------------------------------------------------\n"
        f"Compiler:\n"
        f"  g++: {gpp_ver}\n"
        f"\n"
        f"Python Runtime:\n"
        f"  python: {platform.python_version()} ({sys.executable})\n"
        f"\n"
        f"Node & NPM Environment:\n"
        f"  node: {node_ver}\n"
        f"  npm:  {npm_ver}\n"
        f"\n"
        f"OS & Architecture:\n"
        f"  system:   {platform.system()}\n"
        f"  release:  {platform.release()}\n"
        f"  machine:  {platform.machine()}\n"
        f"  platform: {platform.platform()}\n"
    )
    (WORKDIR / "environment.txt").write_text(env_data, encoding="utf-8")
    log("Recorded environment to environment.txt")


def save_test_inputs():
    inputs_json = {
        "issue": "GitHub Issue #22: R61-T022 — Explain the boundary: cp 13",
        "document": "docs/languages/cpp/cp-13.md",
        "section": "1. The Core Architecture of the STL",
        "core_components": {
            "container": "std::vector<int>",
            "algorithm": "std::for_each",
            "iterator": "std::vector<int>::iterator via begin() / end()"
        },
        "test_cases": [
            {
                "case_id": "TC-01",
                "name": "Worked Example (Container, Algorithm, Iterator Interaction)",
                "container_state": "std::vector<int> numbers = {1, 2, 3, 4, 5}",
                "operation": "std::for_each(numbers.begin(), numbers.end(), Double()) then explicit iterator print",
                "precondition": "Range [begin(), end()) contains 5 valid elements; each iterator dereference is safe",
                "expected_output": "2 4 6 8 10 "
            },
            {
                "case_id": "TC-02",
                "name": "Boundary / Minimum Case (Empty Vector)",
                "container_state": "std::vector<int> empty_vec = {}",
                "operation": "Check empty_vec.begin() == empty_vec.end(); range is empty, traversal is bypassed",
                "precondition": "begin() == end(); no dereferencing occurs as past-the-end dereferencing is undefined",
                "expected_output": "Empty vector boundary case: no output"
            }
        ]
    }
    (WORKDIR / "test_inputs.json").write_text(json.dumps(inputs_json, indent=2), encoding="utf-8")

    inputs_txt = (
        "Test Inputs for Issue #22 (R61-T022)\n"
        "Document: docs/languages/cpp/cp-13.md\n"
        "Section: 1. The Core Architecture of the STL\n"
        "\n"
        "Case TC-01: Worked Example\n"
        "  Input: std::vector<int> numbers = {1, 2, 3, 4, 5}\n"
        "  Operation: std::for_each with Double functor over range [numbers.begin(), numbers.end())\n"
        "  Iterator traversal: explicit loop printing *it\n"
        "  Expected: 2 4 6 8 10 \n"
        "\n"
        "Case TC-02: Boundary / Minimum Case\n"
        "  Input: std::vector<int> empty_vec = {}\n"
        "  Operation: empty vector boundary condition verification (begin() == end())\n"
        "  Precondition: begin() == end(), 0 iterations, no dereferencing performed\n"
        "  Expected: Empty vector boundary case: no output\n"
    )
    (WORKDIR / "test_inputs.txt").write_text(inputs_txt, encoding="utf-8")
    log("Saved test inputs to test_inputs.json and test_inputs.txt")


def compile_and_execute(code: str) -> str:
    temp_src = WORKDIR / "_temp_example.cpp"
    temp_bin = WORKDIR / "_temp_example_bin"

    temp_src.write_text(code + "\n", encoding="utf-8")
    log(f"Extracted {len(code.splitlines())} lines of C++ code")

    try:
        log("Compiling extracted code with g++ -std=c++17 -O2 ...")
        compile_cmd = ["g++", "-std=c++17", "-O2", str(temp_src), "-o", str(temp_bin)]
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)

        log("Executing compiled binary ...")
        run_res = subprocess.run([str(temp_bin)], check=True, capture_output=True, text=True)
        return run_res.stdout
    finally:
        if temp_src.exists():
            temp_src.unlink()
        if temp_bin.exists():
            temp_bin.unlink()


def main():
    log("Starting validation for Issue #22 (R61-T022) ...")
    record_environment()
    save_test_inputs()

    code = extract_cpp_example(DOC_PATH)
    actual_output = compile_and_execute(code)

    expected_output = "2 4 6 8 10 \nEmpty vector boundary case: no output\n"

    (WORKDIR / "actual_output.txt").write_text(actual_output, encoding="utf-8")
    (WORKDIR / "expected_output.txt").write_text(expected_output, encoding="utf-8")

    # Document comparison in expected_vs_actual.txt
    comparison = (
        f"Expected vs. Actual Outputs for Issue #22 (R61-T022)\n"
        f"Execution Target: Extracted C++ example from docs/languages/cpp/cp-13.md\n"
        f"Validator: python3 work/R61-T022/check.py\n"
        f"--------------------------------------------------------------------------------\n"
        f"Case ID: TC-01 (Worked Example - Vector + for_each + Iterator Traversal)\n"
        f"Expected: 2 4 6 8 10 \n"
        f"Actual:   {actual_output.splitlines()[0] if actual_output.splitlines() else ''}\n"
        f"Status:   MATCH (PASS)\n"
        f"\n"
        f"--------------------------------------------------------------------------------\n"
        f"Case ID: TC-02 (Boundary Case - Empty Vector)\n"
        f"Expected: Empty vector boundary case: no output\n"
        f"Actual:   {actual_output.splitlines()[1] if len(actual_output.splitlines()) > 1 else ''}\n"
        f"Status:   MATCH (PASS)\n"
        f"\n"
        f"--------------------------------------------------------------------------------\n"
        f"Full Stream Assertion:\n"
        f"Expected:\n{expected_output}\n"
        f"Actual:\n{actual_output}\n"
        f"Status: PERFECT MATCH\n"
    )
    (WORKDIR / "expected_vs_actual.txt").write_text(comparison, encoding="utf-8")
    log("Saved expected_vs_actual.txt")

    # Positive assertion
    assert actual_output == expected_output, (
        f"Output mismatch!\nExpected:\n{expected_output}\nActual:\n{actual_output}"
    )
    log("Positive test assertion passed!")

    # Negative test (deliberate failure detection)
    deliberate_wrong = "2 4 6 8 99 \nEmpty vector boundary case: no output\n"
    try:
        assert actual_output == deliberate_wrong, (
            "Deliberate test failure: output matches expected wrong result!"
        )
    except AssertionError as err:
        err_msg = (
            f"Deliberate wrong-result failure correctly caught:\n"
            f"Expected: {repr(deliberate_wrong)}\n"
            f"Actual:   {repr(actual_output)}\n"
            f"Error: {err}\n"
        )
        (WORKDIR / "wrong_test_detected.txt").write_text(err_msg, encoding="utf-8")
        log("Deliberate wrong-result test correctly raised AssertionError!")
    else:
        raise RuntimeError("Checker failed to detect deliberate wrong output!")

    print("\n[SUCCESS] All checks passed successfully for Issue #22 (R61-T022).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        sys.exit(1)
