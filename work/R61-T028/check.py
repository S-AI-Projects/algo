#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T028.
Topic: Maximum Number of Balloons (LeetCode 1189)
Target Document: docs/dsa-problems/easy/maximum-number-of-balloons.md

Requirements:
1. Extract the actual published C++ code block directly from the Markdown article.
2. Compile the extracted C++ code using the available C++ compiler (g++ / clang++).
3. Execute the compiled program.
4. Assert the original worked examples' expected results ("nlaebolko" -> 1, "loonbalxballpoon" -> 2, "leetcode" -> 0).
5. Assert the new boundary example's expected result ("b" -> 0).
6. Run an extended test harness derived from the published class Solution.
7. Include deliberate wrong-result tests to demonstrate that the checker detects incorrect output.
8. Propagate compiler and subprocess failures.
9. Exit with a non-zero status whenever any assertion fails.
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
    doc_path = repo_root / "docs" / "dsa-problems" / "easy" / "maximum-number-of-balloons.md"
    if not doc_path.is_file():
        raise FileNotFoundError(f"Documentation file not found: {doc_path}")
    return doc_path


def extract_cpp_code(doc_path: Path) -> str:
    content = doc_path.read_text(encoding="utf-8")
    matches = re.findall(r"```(?:cpp|c\+\+|CPP)\s*\n(.*?)```", content, re.DOTALL)
    if not matches:
        raise ValueError(f"Could not find C++ code block in {doc_path}")

    # Find the C++ block containing class Solution and main
    code = None
    for candidate in matches:
        if "class Solution" in candidate and "maxNumberOfBalloons" in candidate and "int main(" in candidate:
            code = candidate.strip()
            break

    if not code:
        raise ValueError("Could not find complete runnable C++ Solution implementation with main() in documentation.")

    required_tokens = [
        "class Solution",
        "int maxNumberOfBalloons",
        "int main(",
        "nlaebolko",
        "loonbalxballpoon",
        "leetcode",
        "\"b\"",
    ]
    for token in required_tokens:
        if token not in code:
            raise ValueError(f"Extracted C++ code is missing required token: '{token}'")

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


def create_extended_harness(extracted_code: str) -> str:
    # Disable published main to prevent duplicate symbol conflict
    base_code = re.sub(r"\bint\s+main\s*\(", "int disabled_main(", extracted_code)

    harness_main = """

int main() {
    Solution sol;

    // Test cases
    cout << "TEST_ORIGINAL_1:" << sol.maxNumberOfBalloons("nlaebolko") << endl;
    cout << "TEST_ORIGINAL_2:" << sol.maxNumberOfBalloons("loonbalxballpoon") << endl;
    cout << "TEST_ORIGINAL_3:" << sol.maxNumberOfBalloons("leetcode") << endl;
    cout << "TEST_BOUNDARY_SINGLE_CHAR:" << sol.maxNumberOfBalloons("b") << endl;
    cout << "TEST_BOUNDARY_LENGTH_6_MISSING_N:" << sol.maxNumberOfBalloons("balloo") << endl;
    cout << "TEST_BOUNDARY_EXACT_ONE:" << sol.maxNumberOfBalloons("balloon") << endl;
    cout << "TEST_ASYMMETRIC_DEFICIT:" << sol.maxNumberOfBalloons("balloonballoo") << endl;
    cout << "TEST_BOTTLENECK_L:" << sol.maxNumberOfBalloons("bbbbbaaoooonnnnnll") << endl;
    cout << "TEST_UNRELATED_ONLY:" << sol.maxNumberOfBalloons("xyz") << endl;

    return 0;
}
"""
    return base_code + harness_main


def parse_harness_output(output_text: str) -> dict:
    results = {}
    for line in output_text.strip().splitlines():
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            results[key.strip()] = int(val.strip())
    return results


def test_deliberate_stdout_mismatch(actual_stdout: str) -> bool:
    deliberate_wrong = "Output: 999"
    try:
        assert deliberate_wrong in actual_stdout, "Deliberate wrong stdout check"
        return False
    except AssertionError:
        return True


def test_deliberate_boundary_mismatch(actual_boundary: int) -> bool:
    deliberate_wrong = 1  # Boundary "b" must return 0, not 1
    try:
        assert actual_boundary == deliberate_wrong, "Deliberate boundary mismatch check"
        return False
    except AssertionError:
        return True


def main():
    print("=== Step 1: Locating repository root and target article ===")
    repo_root = find_repo_root()
    doc_path = get_doc_path(repo_root)
    print(f"Repository Root: {repo_root}")
    print(f"Target Doc:      {doc_path}")

    print("\n=== Step 2: Extracting published C++ code from markdown ===")
    extracted_code = extract_cpp_code(doc_path)
    print(f"Extracted {len(extracted_code.splitlines())} lines of C++ code from {doc_path.name}.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        build_dir = Path(tmp_dir)

        print("\n=== Step 3: Compiling and running published C++ code ===")
        proc_pub = compile_and_run(extracted_code, "balloon_published", build_dir)
        pub_stdout = proc_pub.stdout.strip()
        print("Actual stdout from published code:")
        for line in pub_stdout.splitlines():
            print(f"  {line}")

        expected_pub_lines = [
            'Input: text = "nlaebolko"',
            'Output: 1',
            'Input: text = "loonbalxballpoon"',
            'Output: 2',
            'Input: text = "leetcode"',
            'Output: 0',
            'Input: text = "b"',
            'Output: 0',
        ]
        actual_pub_lines = [line.strip() for line in pub_stdout.splitlines() if line.strip()]

        if len(actual_pub_lines) != len(expected_pub_lines):
            print(f"[ASSERTION ERROR] Line count mismatch: expected {len(expected_pub_lines)}, got {len(actual_pub_lines)}", file=sys.stderr)
            sys.exit(1)

        for idx, (exp, act) in enumerate(zip(expected_pub_lines, actual_pub_lines)):
            if exp != act:
                print(f"[ASSERTION ERROR] Line {idx + 1} mismatch!\nExpected: '{exp}'\nActual:   '{act}'", file=sys.stderr)
                sys.exit(1)
            print(f"✓ PASS: Line {idx + 1} matches: '{act}'")

        print("\n=== Step 4: Compiling and running extended test harness ===")
        harness_code = create_extended_harness(extracted_code)
        proc_harness = compile_and_run(harness_code, "balloon_harness", build_dir)
        harness_results = parse_harness_output(proc_harness.stdout)

        expected_harness = {
            "TEST_ORIGINAL_1": 1,
            "TEST_ORIGINAL_2": 2,
            "TEST_ORIGINAL_3": 0,
            "TEST_BOUNDARY_SINGLE_CHAR": 0,
            "TEST_BOUNDARY_LENGTH_6_MISSING_N": 0,
            "TEST_BOUNDARY_EXACT_ONE": 1,
            "TEST_ASYMMETRIC_DEFICIT": 1,
            "TEST_BOTTLENECK_L": 1,
            "TEST_UNRELATED_ONLY": 0,
        }

        for key, exp_val in expected_harness.items():
            act_val = harness_results.get(key)
            if act_val is None:
                print(f"[ASSERTION ERROR] Key '{key}' missing from harness output!", file=sys.stderr)
                sys.exit(1)
            if act_val != exp_val:
                print(f"[ASSERTION ERROR] Test '{key}' mismatch: expected {exp_val}, got {act_val}", file=sys.stderr)
                sys.exit(1)
            print(f"✓ PASS: {key} = {act_val} (expected {exp_val})")

        print("\n=== Step 5: Executing deliberate wrong-result tests ===")
        stdout_fail_detected = test_deliberate_stdout_mismatch(pub_stdout)
        if not stdout_fail_detected:
            print("[ERROR] Negative test 1 failed: Checker did not detect intentional stdout mismatch!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 1 correctly detected intentional mismatch on stdout.")

        boundary_res = harness_results.get("TEST_BOUNDARY_SINGLE_CHAR", -1)
        boundary_fail_detected = test_deliberate_boundary_mismatch(boundary_res)
        if not boundary_fail_detected:
            print("[ERROR] Negative test 2 failed: Checker did not detect intentional boundary mismatch!", file=sys.stderr)
            sys.exit(1)
        print("✓ PASS: Negative test 2 correctly detected intentional mismatch on boundary result.")

    print("\n========================================================")
    print("🎉 ALL CHECKS PASSED: 'Maximum Number of Balloons' C++")
    print("   implementation and documentation verified successfully.")
    print("========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
