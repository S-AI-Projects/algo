#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T028.
Topic: Maximum Number of Balloons (LeetCode 1189)
Target Document: docs/dsa-problems/easy/maximum-number-of-balloons.md

Requirements:
1. Extract the actual published C++ code block directly from the Markdown article.
2. Compile the extracted C++ code using the available C++ compiler (g++ / clang++).
3. Execute the compiled program.
4. Assert the original worked examples' expected results:
   - "nlaebolko" -> 1
   - "loonbalxballpoon" -> 2
   - "leetcode" -> 0
5. Assert the new boundary example's expected result:
   - "b" -> 0
6. Run an extended test harness derived from the published class Solution.
7. Perform genuine C++ mutation tests:
   - Extract published C++ code.
   - Create temporary, intentionally incorrect/mutated versions of the extracted code.
   - Compile and execute the mutated C++ implementations.
   - Run the exact validation logic and confirm it rejects the incorrect implementations.
   - Confirm the original published implementation passes cleanly.
   - Ensure temporary files are cleaned up without modifying the markdown or leaving artifacts.
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
        return compile_proc

    run_proc = subprocess.run([str(binary_file)], capture_output=True, text=True)
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
    cout << "TEST_SINGLE_L_O_DEFICIT:" << sol.maxNumberOfBalloons("balon") << endl;

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


def validate_implementation(source_code: str, label: str, build_dir: Path) -> tuple:
    """
    Validates a C++ implementation against:
    1. Compilation success.
    2. Published stdout output (Examples 1-4).
    3. Extended harness test cases.
    Returns (True, "All checks passed") on success, or (False, error_message) on failure.
    """
    # 1. Compile & run published driver
    proc_pub = compile_and_run(source_code, f"{label}_pub", build_dir)
    if proc_pub.returncode != 0:
        return False, f"Compilation or runtime failed for {label}: returncode {proc_pub.returncode}\n{proc_pub.stderr}"

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
    actual_pub_lines = [line.strip() for line in proc_pub.stdout.strip().splitlines() if line.strip()]

    if len(actual_pub_lines) != len(expected_pub_lines):
        return False, f"Published line count mismatch: expected {len(expected_pub_lines)}, got {len(actual_pub_lines)}"

    for idx, (exp, act) in enumerate(zip(expected_pub_lines, actual_pub_lines)):
        if exp != act:
            return False, f"Published stdout line {idx + 1} mismatch: expected '{exp}', got '{act}'"

    # 2. Compile & run extended harness
    harness_code = create_extended_harness(source_code)
    proc_harness = compile_and_run(harness_code, f"{label}_harness", build_dir)
    if proc_harness.returncode != 0:
        return False, f"Harness compilation or runtime failed for {label}: returncode {proc_harness.returncode}\n{proc_harness.stderr}"

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
        "TEST_SINGLE_L_O_DEFICIT": 0,
    }

    for key, exp_val in expected_harness.items():
        act_val = harness_results.get(key)
        if act_val is None:
            return False, f"Harness missing key: {key}"
        if act_val != exp_val:
            return False, f"Harness mismatch for {key}: expected {exp_val}, got {act_val}"

    return True, "All checks passed"


def run_mutation_tests(extracted_code: str, build_dir: Path) -> None:
    """
    Genuine C++ mutation tests:
    Creates intentionally faulty versions of the C++ implementation, compiles them,
    runs the validation, and asserts that the checker REJECTS the faulty code.
    """
    print("\n--- Running Mutation Test Suite ---")

    # Mutation 1: Uniform Multiplicity Fallacy (ignoring factor of 2 for 'l' and 'o')
    mutated_1 = extracted_code.replace("count['l' - 'a'] / 2", "count['l' - 'a']")
    mutated_1 = mutated_1.replace("count['o' - 'a'] / 2", "count['o' - 'a']")
    if mutated_1 == extracted_code:
        print("[ERROR] Mutation 1 pattern replacement failed to modify code!", file=sys.stderr)
        sys.exit(1)

    passed_1, reason_1 = validate_implementation(mutated_1, "mutation_no_division", build_dir)
    if passed_1:
        print("[ERROR] Mutation 1 was NOT rejected! Checker failed to detect missing division by 2 bug.", file=sys.stderr)
        sys.exit(1)
    print(f"✓ PASS: Mutation 1 (uniform multiplicity without /2) was correctly REJECTED:")
    print(f"        -> {reason_1}")

    # Mutation 2: Boundary / Deficit Fallacy (counting only 'b' without checking other letters)
    mutated_2 = re.sub(r"return\s+min\(\{[^}]+\}\);", "return count['b' - 'a'];", extracted_code)
    if mutated_2 == extracted_code:
        print("[ERROR] Mutation 2 pattern replacement failed to modify code!", file=sys.stderr)
        sys.exit(1)

    passed_2, reason_2 = validate_implementation(mutated_2, "mutation_only_count_b", build_dir)
    if passed_2:
        print("[ERROR] Mutation 2 was NOT rejected! Checker failed to detect 'only count b' bug.", file=sys.stderr)
        sys.exit(1)
    print(f"✓ PASS: Mutation 2 (single-character 'b' fallacy) was correctly REJECTED:")
    print(f"        -> {reason_2}")

    # Mutation 3: Always return zero (stub bug)
    mutated_3 = re.sub(r"return\s+min\(\{[^}]+\}\);", "return 0;", extracted_code)
    if mutated_3 == extracted_code:
        print("[ERROR] Mutation 3 pattern replacement failed to modify code!", file=sys.stderr)
        sys.exit(1)

    passed_3, reason_3 = validate_implementation(mutated_3, "mutation_always_zero", build_dir)
    if passed_3:
        print("[ERROR] Mutation 3 was NOT rejected! Checker failed to detect 'always zero' bug.", file=sys.stderr)
        sys.exit(1)
    print(f"✓ PASS: Mutation 3 (always return zero) was correctly REJECTED:")
    print(f"        -> {reason_3}")


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

        print("\n=== Step 3: Validating published C++ implementation ===")
        is_valid, message = validate_implementation(extracted_code, "published_solution", build_dir)
        if not is_valid:
            print(f"[ASSERTION ERROR] Published C++ code failed validation:\n{message}", file=sys.stderr)
            sys.exit(1)

        print("✓ PASS: Published C++ implementation passed all assertions:")
        print("  - Example 1 ('nlaebolko' -> 1)")
        print("  - Example 2 ('loonbalxballpoon' -> 2)")
        print("  - Example 3 ('leetcode' -> 0)")
        print("  - Example 4 Boundary ('b' -> 0)")
        print("  - Extended Harness (10 test cases including missing 'n', exact 'balloon', and asymmetric deficits)")

        print("\n=== Step 4: Executing genuine C++ mutation tests ===")
        run_mutation_tests(extracted_code, build_dir)

    print("\n========================================================")
    print("🎉 ALL CHECKS PASSED: 'Maximum Number of Balloons' C++")
    print("   implementation, published outputs, and mutation")
    print("   rejection tests verified successfully.")
    print("========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
