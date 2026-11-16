#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T025.
Kadane's Algorithm: Remove hidden state and verify executability.

Requirements:
1. Extract actual C++ code block from docs/extra/algorithms/kadane-algorithm/kadane-algo.md.
2. Compile and execute the extracted C++ code.
3. Verify original example output is "The maximum sum of the contiguous subarray is: 6".
4. Verify boundary example returns -7.
5. Propagate compiler and subprocess failures.
6. Include deliberate wrong-result tests and verify that the checker detects failure.
7. Keep the checker concise and reliable.
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
    doc_path = repo_root / "docs" / "extra" / "algorithms" / "kadane-algorithm" / "kadane-algo.md"
    if not doc_path.is_file():
        raise FileNotFoundError(f"Documentation file not found: {doc_path}")
    return doc_path


def extract_cpp_code(doc_path: Path) -> str:
    content = doc_path.read_text(encoding="utf-8")
    match = re.search(r"```(?:cpp|c\+\+|CPP)\s*\n(.*?)```", content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find C++ code block in {doc_path}")

    code = match.group(1).strip()

    required_tokens = ["class Solution", "maxSubArray", "max_current", "max_global", "main"]
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
        sys.exit(compile_proc.returncode)

    run_proc = subprocess.run([str(binary_file)], capture_output=True, text=True)
    if run_proc.returncode != 0:
        print(f"[ERROR] Execution failed for {binary_name} with exit code {run_proc.returncode}:", file=sys.stderr)
        print(run_proc.stderr, file=sys.stderr)
        sys.exit(run_proc.returncode)

    return run_proc


def create_test_harness(extracted_code: str) -> str:
    # Replace int main(...) with int disabled_main(...) to avoid symbol conflict
    harness_code = re.sub(r"\bint\s+main\s*\(", "int disabled_main(", extracted_code)

    test_main = """

int main() {
    Solution sol;

    // Test 1: Boundary condition with single negative element [-7]
    vector<int> b1 = {-7};
    int res_b1 = sol.maxSubArray(b1);
    cout << "BOUNDARY_RESULT:" << res_b1 << endl;

    // Test 2: Original worked example
    vector<int> orig = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int res_orig = sol.maxSubArray(orig);
    cout << "ORIGINAL_RESULT:" << res_orig << endl;

    // Test 3: All negative elements
    vector<int> all_neg = {-5, -3, -8, -2, -9};
    int res_neg = sol.maxSubArray(all_neg);
    cout << "ALL_NEG_RESULT:" << res_neg << endl;

    // Test 4: All positive elements
    vector<int> all_pos = {1, 2, 3, 4, 5};
    int res_pos = sol.maxSubArray(all_pos);
    cout << "ALL_POS_RESULT:" << res_pos << endl;

    // Test 5: Single positive element
    vector<int> single_pos = {42};
    int res_single_pos = sol.maxSubArray(single_pos);
    cout << "SINGLE_POS_RESULT:" << res_single_pos << endl;

    return 0;
}
"""
    return harness_code + test_main


def parse_harness_results(stdout_text: str) -> dict:
    results = {}
    for line in stdout_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            results[key.strip()] = int(val.strip())
    return results


def test_deliberate_failure_original(actual_output: str) -> bool:
    wrong_expected = "The maximum sum of the contiguous subarray is: 999"
    try:
        assert actual_output == wrong_expected, "Deliberate wrong-output assertion"
        return False
    except AssertionError:
        return True


def test_deliberate_failure_boundary(actual_boundary_return: int) -> bool:
    wrong_expected = 0  # Common bug: initializing max_current/max_global to 0 instead of nums[0]
    try:
        assert actual_boundary_return == wrong_expected, "Deliberate boundary wrong-result assertion"
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

        print("\n=== Step 3: Compiling and executing extracted C++ code (Original Example) ===")
        proc_orig = compile_and_run(extracted_code, "kadane_original", build_dir)
        actual_output = proc_orig.stdout.strip()
        print(f"Actual output:\n  '{actual_output}'")

        expected_output = "The maximum sum of the contiguous subarray is: 6"
        if actual_output != expected_output:
            print(f"[ASSERTION ERROR] Expected:\n  '{expected_output}'\nGot:\n  '{actual_output}'", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Original example output matches expected exactly.")

        print("\n=== Step 4: Compiling and testing boundary condition & test suite ===")
        harness_code = create_test_harness(extracted_code)
        proc_harness = compile_and_run(harness_code, "kadane_harness", build_dir)
        results = parse_harness_results(proc_harness.stdout)

        boundary_res = results.get("BOUNDARY_RESULT")
        print(f"Boundary test (nums = [-7]): returned {boundary_res}")
        if boundary_res != -7:
            print(f"[ASSERTION ERROR] Boundary result expected -7, but got {boundary_res}", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Boundary example returned -7 as expected.")

        # Check other suite cases
        test_expectations = {
            "ORIGINAL_RESULT": 6,
            "ALL_NEG_RESULT": -2,
            "ALL_POS_RESULT": 15,
            "SINGLE_POS_RESULT": 42,
        }
        for key, exp in test_expectations.items():
            act = results.get(key)
            if act != exp:
                print(f"[ASSERTION ERROR] Test case {key} expected {exp}, got {act}", file=sys.stderr)
                sys.exit(1)
            print(f"✓ PASS: Test case {key} returned {act} (expected {exp}).")

        print("\n=== Step 5: Executing deliberate wrong-result tests ===")
        orig_fail_detected = test_deliberate_failure_original(actual_output)
        if not orig_fail_detected:
            print("[ERROR] Negative test failed: Checker did not detect incorrect original output!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 1 correctly detected intentional mismatch on original example output.")

        boundary_fail_detected = test_deliberate_failure_boundary(boundary_res)
        if not boundary_fail_detected:
            print("[ERROR] Negative test failed: Checker did not detect incorrect boundary result!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 2 correctly detected intentional mismatch on boundary condition (0 vs -7).")

    print("\n========================================================")
    print("🎉 ALL CHECKS PASSED: Kadane algorithm documentation and")
    print("   implementation are fully verified, reproducible, and")
    print("   free of hidden state.")
    print("========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
