#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T024.
Painter's Partition Problem documentation and implementation check.

Requirements:
1. Extract actual C++ example from docs/extra/binary-search-problems/painters-partition.md.
2. Compile and execute it, verifying expected output.
3. Run at least five additional bounded test cases on the extracted C++ implementation.
4. Independent combinatorial verification (avoiding simple duplicate of algorithm).
5. Include a negative test proving incorrect results are detected.
6. Exit with non-zero status on any failure.
"""

import itertools
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


def extract_cpp_code(doc_path: Path) -> str:
    if not doc_path.is_file():
        raise FileNotFoundError(f"Documentation file not found: {doc_path}")

    content = doc_path.read_text(encoding="utf-8")
    match = re.search(r"```(?:Cpp|cpp)\s*\n(.*?)```", content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find C++ code block in {doc_path}")

    cpp_code = match.group(1)

    # Basic sanity checks on extracted code
    required_symbols = ["isPossible", "minTimeToPaint", "main", "maxAllowedTime", "paintersCount", "currentTime"]
    for sym in required_symbols:
        if sym not in cpp_code:
            raise ValueError(f"Extracted C++ code is missing required symbol: {sym}")

    return cpp_code


def compile_and_run(cpp_source: str, binary_name: str, build_dir: Path) -> subprocess.CompletedProcess:
    source_file = build_dir / f"{binary_name}.cpp"
    binary_file = build_dir / binary_name

    source_file.write_text(cpp_source, encoding="utf-8")

    compile_cmd = ["g++", "-std=c++17", "-O2", str(source_file), "-o", str(binary_file)]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_res.returncode != 0:
        raise RuntimeError(f"Compilation failed for {binary_name}:\nSTDOUT:\n{compile_res.stdout}\nSTDERR:\n{compile_res.stderr}")

    run_res = subprocess.run([str(binary_file)], capture_output=True, text=True)
    return run_res


def extract_functions_without_main(cpp_code: str) -> str:
    """Extract includes and helper functions from the C++ code, omitting main()."""
    main_match = re.search(r"\bint\s+main\s*\([^)]*\)\s*\{", cpp_code)
    if main_match:
        return cpp_code[:main_match.start()]
    return cpp_code


def independent_brute_force_solver(boards: list, m: int) -> int:
    """
    Exhaustively searches all valid contiguous partitions into <= m parts
    to independently find the minimum possible maximum sum.
    This provides independent combinatorial validation without duplicating
    the greedy + binary search algorithm.
    """
    n = len(boards)
    if n == 0:
        return 0
    if m >= n:
        return max(boards)

    best_max = sum(boards)

    # Cut points: choose k-1 dividers from the n-1 interior positions (1 <= k <= m)
    for k in range(1, m + 1):
        if k == 1:
            best_max = min(best_max, sum(boards))
            continue
        for dividers in itertools.combinations(range(1, n), k - 1):
            divs = [0] + list(dividers) + [n]
            parts = [boards[divs[i]:divs[i+1]] for i in range(len(divs) - 1)]
            max_part = max(sum(part) for part in parts)
            if max_part < best_max:
                best_max = max_part

    return best_max


def generate_harness_cpp(functions_code: str, test_cases: list) -> str:
    harness = functions_code + "\n\n"
    harness += """
#include <iostream>
#include <vector>
#include <string>

struct TestCase {
    std::string name;
    std::vector<int> boards;
    int m;
    int expected;
};

int main() {
    std::vector<TestCase> cases = {
"""
    for tc in test_cases:
        boards_str = "{" + ", ".join(str(x) for x in tc["boards"]) + "}"
        name = tc["name"].replace('"', '\\"')
        harness += f'        {{"{name}", {boards_str}, {tc["m"]}, {tc["expected"]}}},\n'

    harness += """    };

    int failed_count = 0;
    for (size_t idx = 0; idx < cases.size(); ++idx) {
        auto &tc = cases[idx];
        int n = static_cast<int>(tc.boards.size());
        int actual = minTimeToPaint(tc.boards, n, tc.m);
        bool ok = (actual == tc.expected);
        std::cout << "[CPP_TEST] index=" << idx
                  << " name=\\"" << tc.name << "\\""
                  << " actual=" << actual
                  << " expected=" << tc.expected
                  << " status=" << (ok ? "PASS" : "FAIL")
                  << std::endl;
        if (!ok) failed_count++;
    }
    return (failed_count == 0) ? 0 : 1;
}
"""
    return harness


def run_checks():
    repo_root = find_repo_root()
    doc_path = repo_root / "docs" / "extra" / "binary-search-problems" / "painters-partition.md"
    work_dir = repo_root / "work" / "R61-T024"
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Running R61-T024 Checker ===")
    print(f"Repository Root: {repo_root}")
    print(f"Target Doc:      {doc_path}")

    with tempfile.TemporaryDirectory() as temp_build_str:
        build_dir = Path(temp_build_str)

        # Step 1: Extract C++ code from doc
        print("\n[Step 1] Extracting C++ code from documentation...")
        cpp_code = extract_cpp_code(doc_path)
        print("✓ Successfully extracted C++ code block containing isPossible, minTimeToPaint, and main.")

        # Step 2: Compile and run original C++ example
        print("\n[Step 2] Compiling and running original example from doc...")
        run_original = compile_and_run(cpp_code, "original_example", build_dir)
        print(f"Original execution output:\n{run_original.stdout.strip()}")
        if run_original.returncode != 0:
            print(f"ERROR: Original example exited with non-zero code {run_original.returncode}")
            sys.exit(1)

        expected_original_output = "Minimum Maximum Time is: 60"
        if expected_original_output not in run_original.stdout:
            print(f"ERROR: Expected '{expected_original_output}' in stdout, but got:\n{run_original.stdout}")
            sys.exit(1)
        print("✓ Original example output verified.")

        # Step 3: Run test suite with boundary and edge variations
        print("\n[Step 3] Running bounded test suite (boundary + 6 variations + doc example)...")
        test_cases = [
            {
                "name": "Boundary Example: 1 board {7}, 1 painter",
                "boards": [7],
                "m": 1,
                "expected": 7
            },
            {
                "name": "Variation 1: 1 board {7}, more painters than boards (m = 3)",
                "boards": [7],
                "m": 3,
                "expected": 7
            },
            {
                "name": "Variation 2: Painters equal to boards (m = n = 4)",
                "boards": [10, 20, 30, 40],
                "m": 4,
                "expected": 40
            },
            {
                "name": "Variation 3: Single painter for all boards (m = 1)",
                "boards": [5, 10, 15],
                "m": 1,
                "expected": 30
            },
            {
                "name": "Variation 4: All equal board lengths (4 boards of 10, m = 2)",
                "boards": [10, 10, 10, 10],
                "m": 2,
                "expected": 20
            },
            {
                "name": "Variation 5: Uneven boards 1..9, 3 painters (balanced partition)",
                "boards": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "m": 3,
                "expected": 17
            },
            {
                "name": "Variation 6: Strictly decreasing boards {100, 50, 20, 10}, m = 2",
                "boards": [100, 50, 20, 10],
                "m": 2,
                "expected": 100
            },
            {
                "name": "Document Example: {40, 30, 10, 20}, m = 2",
                "boards": [40, 30, 10, 20],
                "m": 2,
                "expected": 60
            }
        ]

        # Verify each case independently with brute-force solver first
        print("\n[Step 3a] Independent combinatorial partition verification...")
        for tc in test_cases:
            bf_ans = independent_brute_force_solver(tc["boards"], tc["m"])
            if bf_ans != tc["expected"]:
                print(f"ERROR: Combinatorial solver returned {bf_ans} for '{tc['name']}', expected {tc['expected']}")
                sys.exit(1)
            print(f"  ✓ Combinatorial verified: {tc['name']} -> {bf_ans}")

        # Build and run C++ test harness using the extracted functions
        print("\n[Step 3b] Compiling and running C++ test harness...")
        functions_code = extract_functions_without_main(cpp_code)
        harness_code = generate_harness_cpp(functions_code, test_cases)
        harness_res = compile_and_run(harness_code, "test_harness", build_dir)

        print(harness_res.stdout.strip())
        if harness_res.returncode != 0:
            print("ERROR: C++ test harness reported failure!")
            sys.exit(1)
        print("✓ All C++ test cases passed successfully.")

        # Step 4: Negative testing
        print("\n[Step 4] Running negative tests to ensure incorrect results are detected...")
        # Negative Test 1: Expectation mismatch in harness
        neg_test_cases = [
            {
                "name": "Negative Test: Intentionally incorrect expected value",
                "boards": [40, 30, 10, 20],
                "m": 2,
                "expected": 59  # Actual is 60; expecting 59 must fail
            }
        ]
        neg_harness_code = generate_harness_cpp(functions_code, neg_test_cases)
        neg_harness_res = compile_and_run(neg_harness_code, "neg_test_harness", build_dir)
        if neg_harness_res.returncode == 0:
            print("ERROR: Negative test failed! Harness returned success when expecting incorrect value (59 instead of 60).")
            sys.exit(1)
        print("✓ Negative Test 1 passed: Discrepancy between actual (60) and incorrect expected (59) was correctly detected.")

        # Negative Test 2: Invariant violation test (single board exceeds allowed time)
        # Testing that isPossible correctly rejects maxAllowedTime lower than maxVal
        check_infeasible = """
#include <iostream>
#include <vector>
""" + functions_code + """
int main() {
    std::vector<int> b = {40, 30, 10, 20};
    // maxVal is 40. Testing time 39 must return false.
    if (isPossible(b, 4, 2, 39)) {
        return 1; // Incorrectly said possible
    }
    // With m=2, time 59 must also return false (requires 3 painters)
    if (isPossible(b, 4, 2, 59)) {
        return 2; // Incorrectly said possible
    }
    // Time 60 must return true
    if (!isPossible(b, 4, 2, 60)) {
        return 3; // Incorrectly said impossible
    }
    std::cout << "[NEGATIVE_TEST_2_PASS] Feasibility boundaries verified." << std::endl;
    return 0;
}
"""
        neg_res2 = compile_and_run(check_infeasible, "neg_test_bounds", build_dir)
        if neg_res2.returncode != 0:
            print(f"ERROR: Negative Test 2 failed with exit code {neg_res2.returncode}")
            sys.exit(1)
        print(f"✓ Negative Test 2 passed: {neg_res2.stdout.strip()}")

    print("\n==========================================")
    print("🎉 ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("==========================================")
    sys.exit(0)


if __name__ == "__main__":
    run_checks()
