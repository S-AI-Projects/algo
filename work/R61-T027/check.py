#!/usr/bin/env python3
"""
Validation check for Issue #27 (R61-T027) - Wiggle Sort Step-by-Step Derivation and Execution

This script:
1. Extracts the actual Java WiggleSort implementation directly from
   docs/basic-data-structures/array/wiggle-sort.md.
2. Identifies and validates the Java runtime (OpenJdk / repository setup).
3. Executes the extracted Java code in an isolated temporary environment.
4. Asserts the expected output for the worked example ([3, 5, 1, 6, 2, 4])
   and the boundary example ([1]).
5. Verifies that a deliberately incorrect expected result triggers an AssertionError (negative testing).
6. Exits with non-zero status on any failure and prints clear expected-versus-actual results.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile


def get_doc_path():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    doc_path = os.path.join(repo_root, "docs", "basic-data-structures", "array", "wiggle-sort.md")
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Target markdown article not found at: {doc_path}")
    return doc_path


def extract_java_example(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all ```java ... ``` blocks
    pattern = r"```java\s*\n(.*?)```"
    code_blocks = re.findall(pattern, content, re.DOTALL)

    target_block = None
    for block in code_blocks:
        if (
            "class WiggleSort" in block
            and "public static void sort" in block
            and "public static void main" in block
        ):
            target_block = block
            break

    if not target_block:
        raise ValueError(
            "Could not find the executable WiggleSort Java block containing sort() and main() "
            "in docs/basic-data-structures/array/wiggle-sort.md"
        )

    return target_block.strip()


def find_java_binary():
    # 1. Environment variable JAVA_HOME
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidate = os.path.join(java_home, "bin", "java")
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    # 2. Check Homebrew / standard paths
    well_known_paths = [
        "/opt/homebrew/opt/openjdk/bin/java",
        "/usr/local/opt/openjdk/bin/java",
        "/opt/homebrew/bin/java",
        "/usr/bin/java",
    ]
    for p in well_known_paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            # Test if it can run
            try:
                test_proc = subprocess.run([p, "-version"], capture_output=True, text=True)
                if test_proc.returncode == 0:
                    return p
            except Exception:
                pass

    # 3. PATH lookup
    path_java = shutil.which("java")
    if path_java:
        try:
            test_proc = subprocess.run([path_java, "-version"], capture_output=True, text=True)
            if test_proc.returncode == 0:
                return path_java
        except Exception:
            pass

    raise RuntimeError("Valid Java runtime binary not found. Please ensure OpenJDK is installed.")


def execute_java_code(java_bin, code_str):
    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = os.path.join(tmpdir, "WiggleSort.java")
        with open(java_file, "w", encoding="utf-8") as f:
            f.write(code_str)

        run_proc = subprocess.run(
            [java_bin, java_file],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        return run_proc


def parse_clean_lines(stdout_text):
    lines = []
    for line in stdout_text.splitlines():
        trimmed = line.strip()
        if trimmed:
            lines.append(trimmed)
    return lines


def test_deliberate_failure(actual_lines):
    """
    Negative verification: verify that a deliberate mismatch raises AssertionError.
    """
    deliberate_incorrect_expected = [
        "Worked Example Output: [3, 5, 2, 1, 6, 4]",  # Deliberately un-sorted
        "Boundary Example Output: [1]",
    ]
    try:
        assert actual_lines == deliberate_incorrect_expected, "Deliberate mismatch triggered as expected"
        # If no assertion error, the negative test failed
        return False
    except AssertionError:
        return True


def main():
    print("================================================================================")
    print(" R61-T027 Automated Verification: Wiggle Sort Step-by-Step Derivation")
    print("================================================================================")

    # Step 1: Locate article
    print("\n--- Step 1: Locating target markdown documentation ---")
    doc_path = get_doc_path()
    print(f"Article path: {doc_path}")

    # Step 2: Extract code
    print("\n--- Step 2: Extracting Java implementation from markdown ---")
    java_code = extract_java_example(doc_path)
    total_lines = len(java_code.splitlines())
    print(f"Extracted {total_lines} lines of Java source from docs/basic-data-structures/array/wiggle-sort.md.")
    print("Source preview (first 10 lines):")
    for line in java_code.splitlines()[:10]:
        print(f"  {line}")
    print("  ...")

    # Step 3: Find Java runtime
    print("\n--- Step 3: Detecting Java runtime ---")
    java_bin = find_java_binary()
    print(f"Java binary located: {java_bin}")
    v_proc = subprocess.run([java_bin, "-version"], capture_output=True, text=True)
    version_output = (v_proc.stdout + v_proc.stderr).strip().splitlines()
    for line in version_output:
        print(f"  {line}")

    # Step 4: Execute extracted Java code
    print("\n--- Step 4: Executing extracted Java code ---")
    proc = execute_java_code(java_bin, java_code)
    if proc.returncode != 0:
        print("ERROR: Java execution failed!", file=sys.stderr)
        print(f"Return code: {proc.returncode}", file=sys.stderr)
        print(f"Stdout:\n{proc.stdout}", file=sys.stderr)
        print(f"Stderr:\n{proc.stderr}", file=sys.stderr)
        sys.exit(proc.returncode)

    actual_lines = parse_clean_lines(proc.stdout)
    print("Actual stdout lines received:")
    for line in actual_lines:
        print(f"  > {line}")

    # Step 5: Assert expected results
    print("\n--- Step 5: Asserting expected output values ---")
    expected_lines = [
        "Worked Example Output: [3, 5, 1, 6, 2, 4]",
        "Boundary Example Output: [1]",
    ]

    print("Comparing Expected vs. Actual:")
    all_match = True
    for exp, act in zip(expected_lines, actual_lines):
        match = (exp == act)
        status = "MATCH (PASS)" if match else "MISMATCH (FAIL)"
        print(f"  Expected: '{exp}'")
        print(f"  Actual:   '{act}'")
        print(f"  Status:   {status}\n")
        if not match:
            all_match = False

    if len(actual_lines) != len(expected_lines):
        print(
            f"ERROR: Line count mismatch! Expected {len(expected_lines)} lines, got {len(actual_lines)}.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not all_match:
        print("ASSERTION FAILURE: Output does not match expected results!", file=sys.stderr)
        sys.exit(1)

    print("PASS: Both worked example and boundary example match expected output.")

    # Step 6: Negative test
    print("\n--- Step 6: Performing negative test with incorrect expectation ---")
    negative_passed = test_deliberate_failure(actual_lines)
    if not negative_passed:
        print("ERROR: Negative test failed! Incorrect expectation did not raise AssertionError.", file=sys.stderr)
        sys.exit(1)
    print("PASS: Deliberate incorrect result properly triggered AssertionError.")

    print("\n================================================================================")
    print(" ALL CHECKS PASSED: Wiggle Sort derivation and execution verified successfully!")
    print("================================================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
