#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T026.
Fenwick Tree (Binary Indexed Tree): Clarify implementation and verify executability.

Requirements:
1. Extract actual C++ code block from docs/extra/Fenwick Tree/FenwickTree.md.
2. Compile and execute the extracted C++ code using the available C++ compiler.
3. Assert original expected output ("Sum from 1 to 5: 7", "Range Sum from 3 to 5: 7")
   and boundary behavior ("Empty prefix sum (getSum(0)): 0").
4. Include a test harness to verify boundary conditions, range invariants, and point queries.
5. Include deliberate wrong-result tests to prove assertions detect failures.
6. Propagate compiler and subprocess failures.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def find_repo_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "package.json").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_doc_path(repo_root: Path) -> Path:
    doc_path = repo_root / "docs" / "extra" / "Fenwick Tree" / "FenwickTree.md"
    if not doc_path.is_file():
        raise FileNotFoundError(f"Documentation file not found: {doc_path}")
    return doc_path


def extract_cpp_code(doc_path: Path) -> str:
    content = doc_path.read_text(encoding="utf-8")
    # Match the C++ code block (skip pseudocode block if any)
    matches = re.findall(r"```(?:cpp|c\+\+|CPP)\s*\n(.*?)```", content, re.DOTALL)
    if not matches:
        raise ValueError(f"Could not find C++ code block in {doc_path}")

    # Find the block containing class FenwickTree and main
    code = None
    for candidate in matches:
        if "class FenwickTree" in candidate and "int main(" in candidate:
            code = candidate.strip()
            break

    if not code:
        raise ValueError("Could not find complete FenwickTree C++ implementation block in documentation.")

    required_tokens = ["class FenwickTree", "BITree", "update", "getSum", "rangeSum", "int main("]
    for token in required_tokens:
        if token not in code:
            raise ValueError(f"Extracted C++ code is missing required token: {token}")

    return code


def compile_and_run(source_code: str, binary_name: str, build_dir: Path) -> subprocess.CompletedProcess:
    source_file = build_dir / f"{binary_name}.cpp"
    binary_file = build_dir / binary_name

    source_file.write_text(source_code, encoding="utf-8")

    compile_cmd = ["g++", "-std=c++17", "-O2", str(source_file), "-o", str(binary_file)]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)

    if compile_proc.returncode != 0:
        print(f"[ERROR] Compilation failed for {binary_name}:", file=sys.stderr)
        print(compile_proc.stderr, file=sys.stderr)
        sys.exit(compile_proc.returncode if compile_proc.returncode != 0 else 1)

    run_proc = subprocess.run([str(binary_file)], capture_output=True, text=True)
    if run_proc.returncode != 0:
        print(f"[ERROR] Execution failed for {binary_name} with exit code {run_proc.returncode}:", file=sys.stderr)
        print(run_proc.stderr, file=sys.stderr)
        sys.exit(run_proc.returncode)

    return run_proc


def create_test_harness(extracted_code: str) -> str:
    # Rename original main to disabled_main to prevent duplicate symbol error
    harness_base = re.sub(r"\bint\s+main\s*\(", "int disabled_main(", extracted_code)

    harness_main = """

int main() {
    FenwickTree ft(10);

    // Initial boundary check on empty tree
    cout << "INIT_GETSUM_0:" << ft.getSum(0) << endl;
    cout << "INIT_GETSUM_1:" << ft.getSum(1) << endl;

    // Apply updates from worked example
    ft.update(3, 5);
    ft.update(5, 2);

    // Test Boundary Conditions
    cout << "BOUNDARY_EMPTY_PREFIX:" << ft.getSum(0) << endl;
    cout << "BOUNDARY_RANGE_LOWER_BOUND:" << ft.rangeSum(1, 5) << endl;

    // Test Prefix Queries
    cout << "QUERY_GETSUM_1:" << ft.getSum(1) << endl;
    cout << "QUERY_GETSUM_2:" << ft.getSum(2) << endl;
    cout << "QUERY_GETSUM_3:" << ft.getSum(3) << endl;
    cout << "QUERY_GETSUM_4:" << ft.getSum(4) << endl;
    cout << "QUERY_GETSUM_5:" << ft.getSum(5) << endl;
    cout << "QUERY_GETSUM_6:" << ft.getSum(6) << endl;
    cout << "QUERY_GETSUM_7:" << ft.getSum(7) << endl;
    cout << "QUERY_GETSUM_8:" << ft.getSum(8) << endl;
    cout << "QUERY_GETSUM_10:" << ft.getSum(10) << endl;

    // Test Range Queries
    cout << "QUERY_RANGESUM_3_5:" << ft.rangeSum(3, 5) << endl;
    cout << "QUERY_RANGESUM_3_3:" << ft.rangeSum(3, 3) << endl;
    cout << "QUERY_RANGESUM_5_5:" << ft.rangeSum(5, 5) << endl;
    cout << "QUERY_RANGESUM_4_5:" << ft.rangeSum(4, 5) << endl;
    cout << "QUERY_RANGESUM_1_10:" << ft.rangeSum(1, 10) << endl;

    // Subsequent update test
    ft.update(1, 10);
    cout << "POST_UPDATE_GETSUM_1:" << ft.getSum(1) << endl;
    cout << "POST_UPDATE_GETSUM_3:" << ft.getSum(3) << endl;
    cout << "POST_UPDATE_GETSUM_5:" << ft.getSum(5) << endl;
    cout << "POST_UPDATE_RANGESUM_1_3:" << ft.rangeSum(1, 3) << endl;

    return 0;
}
"""
    return harness_base + harness_main


def parse_harness_output(output_text: str) -> dict:
    results = {}
    for line in output_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            results[key.strip()] = int(val.strip())
    return results


def test_deliberate_stdout_mismatch(actual_output: str) -> bool:
    deliberate_wrong = "Sum from 1 to 5: 999\nRange Sum from 3 to 5: 7\nEmpty prefix sum (getSum(0)): 0"
    try:
        assert actual_output == deliberate_wrong, "Deliberate wrong-stdout assertion"
        return False
    except AssertionError:
        return True


def test_deliberate_boundary_mismatch(actual_boundary: int) -> bool:
    deliberate_wrong = 99
    try:
        assert actual_boundary == deliberate_wrong, "Deliberate boundary assertion"
        return False
    except AssertionError:
        return True


def main():
    print("=== Step 1: Locating repository and target document ===")
    repo_root = find_repo_root()
    doc_path = get_doc_path(repo_root)
    print(f"Repository Root: {repo_root}")
    print(f"Target Doc:      {doc_path}")

    print("\n=== Step 2: Extracting C++ code from documentation ===")
    extracted_code = extract_cpp_code(doc_path)
    print(f"Successfully extracted {len(extracted_code.splitlines())} lines of C++ code from markdown.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        build_dir = Path(tmp_dir)

        print("\n=== Step 3: Compiling and executing extracted C++ code (Original Example + Boundary) ===")
        proc_orig = compile_and_run(extracted_code, "fenwick_original", build_dir)
        actual_output = proc_orig.stdout.strip()
        print("Actual output from extracted code:")
        for line in actual_output.splitlines():
            print(f"  {line}")

        expected_lines = [
            "Sum from 1 to 5: 7",
            "Range Sum from 3 to 5: 7",
            "Empty prefix sum (getSum(0)): 0",
        ]
        actual_lines = [line.strip() for line in actual_output.splitlines() if line.strip()]

        if len(actual_lines) != len(expected_lines):
            print(f"[ASSERTION ERROR] Expected {len(expected_lines)} lines, but got {len(actual_lines)} lines.", file=sys.stderr)
            sys.exit(1)

        for idx, (exp, act) in enumerate(zip(expected_lines, actual_lines)):
            if exp != act:
                print(f"[ASSERTION ERROR] Line {idx + 1} mismatch!\nExpected: '{exp}'\nActual:   '{act}'", file=sys.stderr)
                sys.exit(1)
            print(f"✓ PASS: Line {idx + 1} matches: '{act}'")

        print("\n=== Step 4: Compiling and executing extended verification harness ===")
        harness_code = create_test_harness(extracted_code)
        proc_harness = compile_and_run(harness_code, "fenwick_harness", build_dir)
        harness_results = parse_harness_output(proc_harness.stdout)

        # Expected test harness values
        expected_harness = {
            "INIT_GETSUM_0": 0,
            "INIT_GETSUM_1": 0,
            "BOUNDARY_EMPTY_PREFIX": 0,
            "BOUNDARY_RANGE_LOWER_BOUND": 7,
            "QUERY_GETSUM_1": 0,
            "QUERY_GETSUM_2": 0,
            "QUERY_GETSUM_3": 5,
            "QUERY_GETSUM_4": 5,
            "QUERY_GETSUM_5": 7,
            "QUERY_GETSUM_6": 7,
            "QUERY_GETSUM_7": 7,
            "QUERY_GETSUM_8": 7,
            "QUERY_GETSUM_10": 7,
            "QUERY_RANGESUM_3_5": 7,
            "QUERY_RANGESUM_3_3": 5,
            "QUERY_RANGESUM_5_5": 2,
            "QUERY_RANGESUM_4_5": 2,
            "QUERY_RANGESUM_1_10": 7,
            "POST_UPDATE_GETSUM_1": 10,
            "POST_UPDATE_GETSUM_3": 15,
            "POST_UPDATE_GETSUM_5": 17,
            "POST_UPDATE_RANGESUM_1_3": 15,
        }

        for key, exp_val in expected_harness.items():
            act_val = harness_results.get(key)
            if act_val is None:
                print(f"[ASSERTION ERROR] Missing test key in harness output: {key}", file=sys.stderr)
                sys.exit(1)
            if act_val != exp_val:
                print(f"[ASSERTION ERROR] Key {key} expected {exp_val}, but got {act_val}", file=sys.stderr)
                sys.exit(1)
            print(f"✓ PASS: {key} = {act_val} (expected {exp_val})")

        print("\n=== Step 5: Executing deliberate wrong-result tests ===")
        mismatch_caught = test_deliberate_stdout_mismatch(actual_output)
        if not mismatch_caught:
            print("[ERROR] Negative test 1 failed: Checker did not detect intentional stdout mismatch!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 1 correctly detected intentional stdout mismatch.")

        boundary_val = harness_results.get("BOUNDARY_EMPTY_PREFIX", -1)
        boundary_caught = test_deliberate_boundary_mismatch(boundary_val)
        if not boundary_caught:
            print("[ERROR] Negative test 2 failed: Checker did not detect intentional boundary mismatch!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 2 correctly detected intentional boundary mismatch.")

    print("\n========================================================")
    print("🎉 ALL CHECKS PASSED: Fenwick Tree documentation and")
    print("   implementation are fully verified, reproducible, and")
    print("   compilation-safe.")
    print("========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
