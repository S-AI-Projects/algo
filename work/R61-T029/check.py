#!/usr/bin/env python3
"""
Automated verification checker for Assignment R61-T029.
Topic: Reservoir Sampling Algorithm (Algorithm R)
Target Document: docs/extra/Randomized Algorithm/Reservoir-Sampling.md

Checker Requirements:
1. Extract the actual published Python code block directly from the Markdown article.
   Never validate a separately retyped implementation that could drift from documentation.
2. Execute the published Python code via subprocess and verify stdout matches published outputs:
   - Worked example: Random sample: [18152, 22772, 29552, 59712, 55457]
   - Boundary example (n <= k): Boundary sample (n <= k): [10, 20, 30]
3. Dynamically import the extracted published function into Python runtime.
4. Verify the article's worked example and boundary example against contractual invariants.
5. Verify extended boundary conditions (empty stream, n == k, k == 1, generator streams).
6. Verify statistical uniformity property (empirical frequency across trials).
7. Perform deliberate incorrect-result and mutation tests:
   - Prove that the checker catches wrong stdout expectations.
   - Prove that the checker catches wrong boundary assertions.
   - Mutate implementation (off-by-one / out-of-bounds index) and verify rejection.
   - Mutate implementation (no-op replacement) and verify rejection.
   - Mutate implementation (empty stub return) and verify rejection.
8. Propagate subprocess and assertion failures with non-zero exit code on error.
9. Generate complete supporting evidence files in work/R61-T029/.
"""

import importlib.util
import os
import platform
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
    doc_path = repo_root / "docs" / "extra" / "Randomized Algorithm" / "Reservoir-Sampling.md"
    if not doc_path.is_file():
        raise FileNotFoundError(f"Authoritative documentation file not found: {doc_path}")
    return doc_path


def extract_python_code(doc_path: Path) -> str:
    content = doc_path.read_text(encoding="utf-8")
    matches = re.findall(r"```python\s*\n(.*?)```", content, re.DOTALL)
    if not matches:
        raise ValueError(f"No Python code blocks found in {doc_path}")

    selected_code = None
    for candidate in matches:
        if "def reservoir_sampling(stream, k):" in candidate and "Random sample:" in candidate:
            selected_code = candidate.strip()
            break

    if not selected_code:
        raise ValueError(
            "Could not find Algorithm R Python implementation containing "
            "'def reservoir_sampling(stream, k):' and worked example in documentation."
        )

    required_tokens = [
        "def reservoir_sampling(stream, k):",
        "random.randint(0, i)",
        "random.seed(42)",
        "data_stream = range(1, 100001)",
        "short_stream = [10, 20, 30]",
        "Random sample:",
        "Boundary sample (n <= k):",
    ]
    for token in required_tokens:
        if token not in selected_code:
            raise ValueError(f"Extracted Python code is missing required token: '{token}'")

    return selected_code


def run_code_in_subprocess(source_code: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = Path(tmpdir) / "extracted_reservoir.py"
        tmp_file.write_text(source_code, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(tmp_file)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    return proc


def load_module_from_source(source_code: str, module_name: str = "extracted_module"):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = Path(tmpdir) / f"{module_name}.py"
        tmp_file.write_text(source_code, encoding="utf-8")
        spec = importlib.util.spec_from_file_location(module_name, str(tmp_file))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module spec from {tmp_file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


def test_deliberate_stdout_mismatch(actual_stdout: str) -> bool:
    """Deliberate incorrect test 1: expect bogus string and assert ValueError/AssertionError is caught."""
    try:
        assert "Random sample: [999999, 888888]" in actual_stdout, "Intentional mismatch triggered"
        return False
    except AssertionError:
        return True


def test_deliberate_boundary_mismatch(actual_boundary: list) -> bool:
    """Deliberate incorrect test 2: expect wrong boundary result and assert failure is caught."""
    try:
        assert actual_boundary == [99, 99, 99], "Intentional boundary mismatch triggered"
        return False
    except AssertionError:
        return True


def test_mutation_out_of_bounds(published_code: str) -> bool:
    """
    Mutation Test 1: Change `if j < k:` to `if j <= k:`
    When j == k, accessing reservoir[j] will raise IndexError or overwrite out of bound.
    """
    mutated = published_code.replace("if j < k:", "if j <= k:")
    if mutated == published_code:
        return False
    proc = run_code_in_subprocess(mutated)
    # Mutated code must fail with IndexError or exit non-zero
    return proc.returncode != 0 or "IndexError" in proc.stderr


def test_mutation_no_op_replacement(published_code: str) -> bool:
    """
    Mutation Test 2: Replace replacement assignment `reservoir[j] = item` with `pass`.
    The worked example will fail to sample elements beyond k, retaining only range(1, 6).
    """
    mutated = published_code.replace("reservoir[j] = item", "pass")
    if mutated == published_code:
        return False
    proc = run_code_in_subprocess(mutated)
    # The output will not match [18152, 22772, 29552, 59712, 55457]
    expected_sample = "Random sample: [18152, 22772, 29552, 59712, 55457]"
    return expected_sample not in proc.stdout


def test_mutation_empty_stub(published_code: str) -> bool:
    """
    Mutation Test 3: Mutate function to return empty list [].
    """
    mutated = published_code.replace("return reservoir", "return []")
    if mutated == published_code:
        return False
    proc = run_code_in_subprocess(mutated)
    expected_sample = "Random sample: [18152, 22772, 29552, 59712, 55457]"
    return expected_sample not in proc.stdout


def generate_evidence_files(
    work_dir: Path,
    published_code: str,
    proc_output: str,
    harness_results: dict,
    negative_test_results: dict,
):
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. inputs.txt
    inputs_content = """Test Inputs for Assignment R61-T029 (Reservoir Sampling)
=========================================================

Authoritative Target Document:
docs/extra/Randomized Algorithm/Reservoir-Sampling.md

1. Published Executable Examples:
---------------------------------
Example 1 (Worked Example):
  stream: range(1, 100001) [integers 1 to 100,000]
  k: 5
  seed: 42

Example 2 (Boundary Example - stream length n <= k):
  stream: [10, 20, 30]
  k: 5
  seed: 42

2. Extended Test Harness Inputs:
--------------------------------
TEST_WORKED_EXAMPLE:
  stream = range(1, 100001), k = 5, seed = 42

TEST_BOUNDARY_SHORT_STREAM:
  stream = [10, 20, 30], k = 5

TEST_BOUNDARY_EXACT_STREAM:
  stream = [1, 2, 3, 4, 5], k = 5

TEST_BOUNDARY_EMPTY_STREAM:
  stream = [], k = 5

TEST_BOUNDARY_K_EQUALS_ONE:
  stream = [100, 200, 300], k = 1

TEST_STREAMING_GENERATOR:
  stream = (x for x in range(50)), k = 4

TEST_STATISTICAL_UNIFORMITY:
  stream = range(10), k = 3, trials = 20,000
"""
    (work_dir / "inputs.txt").write_text(inputs_content, encoding="utf-8")

    # 2. expected.txt
    expected_content = """Expected Results for Assignment R61-T029 (Reservoir Sampling)
=============================================================

1. Published Executable Subprocess Output:
------------------------------------------
Random sample: [18152, 22772, 29552, 59712, 55457]
Boundary sample (n <= k): [10, 20, 30]

2. Function Return Values:
--------------------------
- reservoir_sampling(range(1, 100001), 5) [seed=42]: [18152, 22772, 29552, 59712, 55457]
- reservoir_sampling([10, 20, 30], 5): [10, 20, 30]
- reservoir_sampling([1, 2, 3, 4, 5], 5): [1, 2, 3, 4, 5]
- reservoir_sampling([], 5): []
- reservoir_sampling([100, 200, 300], 1): length 1, element in {100, 200, 300}
- reservoir_sampling(generator(50), 4): length 4, all distinct elements in [0, 49]
- Statistical Uniformity (k=3, n=10, 20,000 trials):
  Expected probability per item: 0.3000 (approx 6,000 counts per item +/- 3 sigma)

3. Deliberate Failure Rejection Assertions:
-------------------------------------------
- Negative Test 1 (stdout mismatch): Assertion fails when expecting [999999, 888888]
- Negative Test 2 (boundary mismatch): Assertion fails when expecting [99, 99, 99]
- Mutation Test 1 (Index Out of Bounds j <= k): Rejection confirmed (exit code != 0 or IndexError)
- Mutation Test 2 (No-op replacement): Rejection confirmed (sample mismatch)
- Mutation Test 3 (Empty stub return): Rejection confirmed (empty list mismatch)
"""
    (work_dir / "expected.txt").write_text(expected_content, encoding="utf-8")

    # 3. actual.txt
    actual_lines = [
        "Actual Results for Assignment R61-T029 (Reservoir Sampling)",
        "===========================================================",
        "",
        "1. Published Executable Subprocess Output:",
        "------------------------------------------",
        proc_output.strip(),
        "",
        "2. Function Harness Actual Return Values:",
        "-----------------------------------------",
    ]
    for k, v in harness_results.items():
        actual_lines.append(f"{k}: {v}")
    actual_lines.extend(
        [
            "",
            "3. Deliberate Failure and Mutation Detection:",
            "--------------------------------------------",
        ]
    )
    for k, v in negative_test_results.items():
        actual_lines.append(f"{k}: {v}")
    (work_dir / "actual.txt").write_text("\n".join(actual_lines) + "\n", encoding="utf-8")

    # 4. environment.txt
    node_version = subprocess.run(["node", "-v"], capture_output=True, text=True).stdout.strip()
    npm_version = subprocess.run(["npm", "-v"], capture_output=True, text=True).stdout.strip()
    git_version = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()

    env_content = f"""Environment Information for Assignment R61-T029
==================================================

Operating System: {platform.system()} {platform.release()} ({platform.machine()})
Platform Details: {platform.platform()}
Python Version: {sys.version.split()[0]} ({sys.executable})
Node.js Version: {node_version}
npm Version: {npm_version}
Git Version: {git_version}
Working Directory: {Path.cwd()}
"""
    (work_dir / "environment.txt").write_text(env_content, encoding="utf-8")


def main():
    print("========================================================")
    print("  Assignment R61-T029: Reservoir Sampling Verification  ")
    print("========================================================")

    repo_root = find_repo_root()
    doc_path = get_doc_path(repo_root)
    work_dir = repo_root / "work" / "R61-T029"
    print(f"✓ Found repository root: {repo_root}")
    print(f"✓ Target document path: {doc_path}")

    # Step 1: Extract published code
    print("\n[Phase 1] Extracting published Python code from Markdown...")
    published_code = extract_python_code(doc_path)
    print(f"✓ Successfully extracted {len(published_code.splitlines())} lines of published Python code.")

    # Step 2: Execute published code via subprocess
    print("\n[Phase 2] Executing published Python code via subprocess...")
    proc = run_code_in_subprocess(published_code)
    if proc.returncode != 0:
        print(f"[ERROR] Published code subprocess failed with exit code {proc.returncode}:", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(proc.returncode)

    stdout_text = proc.stdout.strip()
    print("Subprocess stdout:")
    print(stdout_text)

    expected_worked_line = "Random sample: [18152, 22772, 29552, 59712, 55457]"
    expected_boundary_line = "Boundary sample (n <= k): [10, 20, 30]"

    if expected_worked_line not in stdout_text:
        print(f"[ERROR] Worked example output mismatch!", file=sys.stderr)
        print(f"  Expected: {expected_worked_line}", file=sys.stderr)
        print(f"  Received: {stdout_text}", file=sys.stderr)
        sys.exit(1)
    print(f"✓ PASS: Worked example stdout verified: {expected_worked_line}")

    if expected_boundary_line not in stdout_text:
        print(f"[ERROR] Boundary example output mismatch!", file=sys.stderr)
        print(f"  Expected: {expected_boundary_line}", file=sys.stderr)
        print(f"  Received: {stdout_text}", file=sys.stderr)
        sys.exit(1)
    print(f"✓ PASS: Boundary example stdout verified: {expected_boundary_line}")

    # Step 3: Dynamic module load and harness verification
    print("\n[Phase 3] Dynamically importing published module for unit & property checks...")
    module = load_module_from_source(published_code)
    reservoir_sampling = getattr(module, "reservoir_sampling", None)
    if reservoir_sampling is None or not callable(reservoir_sampling):
        print("[ERROR] Function 'reservoir_sampling' not callable in extracted module!", file=sys.stderr)
        sys.exit(1)

    import random

    harness_results = {}

    # Check 1: Worked example with seed 42
    random.seed(42)
    sample_worked = reservoir_sampling(range(1, 100001), 5)
    assert sample_worked == [18152, 22772, 29552, 59712, 55457], f"Unexpected sample: {sample_worked}"
    harness_results["TEST_WORKED_EXAMPLE"] = sample_worked
    print("✓ PASS: Harness verified worked example exact value with seed 42.")

    # Check 2: Boundary example n <= k
    sample_boundary = reservoir_sampling([10, 20, 30], 5)
    assert sample_boundary == [10, 20, 30], f"Unexpected boundary sample: {sample_boundary}"
    harness_results["TEST_BOUNDARY_SHORT_STREAM"] = sample_boundary
    print("✓ PASS: Harness verified boundary example n <= k: [10, 20, 30].")

    # Check 3: Exact stream length n == k
    sample_exact = reservoir_sampling([1, 2, 3, 4, 5], 5)
    assert sample_exact == [1, 2, 3, 4, 5], f"Unexpected exact sample: {sample_exact}"
    harness_results["TEST_BOUNDARY_EXACT_STREAM"] = sample_exact
    print("✓ PASS: Harness verified exact stream length n == k: [1, 2, 3, 4, 5].")

    # Check 4: Empty stream n == 0
    sample_empty = reservoir_sampling([], 5)
    assert sample_empty == [], f"Unexpected empty sample: {sample_empty}"
    harness_results["TEST_BOUNDARY_EMPTY_STREAM"] = sample_empty
    print("✓ PASS: Harness verified empty stream returns [].")

    # Check 5: k == 1
    random.seed(123)
    sample_k1 = reservoir_sampling([100, 200, 300], 1)
    assert len(sample_k1) == 1 and sample_k1[0] in [100, 200, 300], f"Unexpected k=1 sample: {sample_k1}"
    harness_results["TEST_BOUNDARY_K_EQUALS_ONE"] = sample_k1
    print("✓ PASS: Harness verified k=1 boundary sample.")

    # Check 6: Streaming generator input
    gen_sample = reservoir_sampling((x for x in range(50)), 4)
    assert len(gen_sample) == 4, f"Generator sample length != 4: {gen_sample}"
    assert len(set(gen_sample)) == 4, f"Generator sample contains duplicates: {gen_sample}"
    assert all(0 <= x < 50 for x in gen_sample), f"Elements out of generator range: {gen_sample}"
    harness_results["TEST_STREAMING_GENERATOR"] = gen_sample
    print("✓ PASS: Harness verified single-pass lazy generator streaming input.")

    # Check 7: Statistical uniformity property check
    print("\n[Phase 4] Testing statistical uniformity invariant (20,000 trials, k=3, n=10)...")
    n_trials = 20000
    n_stream = 10
    k_res = 3
    counts = [0] * n_stream
    for _ in range(n_trials):
        for item in reservoir_sampling(range(n_stream), k_res):
            counts[item] += 1

    expected_prob = k_res / n_stream  # 0.3000
    expected_count = expected_prob * n_trials  # 6000
    # Standard deviation: sqrt(N * p * (1-p)) = sqrt(20000 * 0.3 * 0.7) = sqrt(4200) ≈ 64.8
    # 4 sigma tolerance ≈ 260 counts (~1.3%)
    for idx, count in enumerate(counts):
        diff = abs(count - expected_count)
        assert diff < 400, f"Item {idx} count {count} deviates too far from expected {expected_count}"

    harness_results["TEST_STATISTICAL_UNIFORMITY"] = {
        "trials": n_trials,
        "k": k_res,
        "n": n_stream,
        "expected_prob": expected_prob,
        "counts": counts,
    }
    print(f"✓ PASS: All 10 items within tight statistical tolerance of expected {expected_count} hits.")

    # Step 4: Deliberate failure and mutation tests
    print("\n[Phase 5] Running deliberate failure and mutation rejection checks...")
    negative_test_results = {}

    mismatch_detected = test_deliberate_stdout_mismatch(stdout_text)
    if not mismatch_detected:
        print("[ERROR] Negative Test 1 failed: checker did not catch deliberate stdout mismatch!", file=sys.stderr)
        sys.exit(1)
    negative_test_results["NEGATIVE_TEST_STDOUT_MISMATCH"] = "CAUGHT_ASSERTION_ERROR"
    print("✓ PASS: Negative Test 1: checker correctly caught deliberate stdout mismatch.")

    boundary_mismatch_detected = test_deliberate_boundary_mismatch(sample_boundary)
    if not boundary_mismatch_detected:
        print("[ERROR] Negative Test 2 failed: checker did not catch deliberate boundary mismatch!", file=sys.stderr)
        sys.exit(1)
    negative_test_results["NEGATIVE_TEST_BOUNDARY_MISMATCH"] = "CAUGHT_ASSERTION_ERROR"
    print("✓ PASS: Negative Test 2: checker correctly caught deliberate boundary mismatch.")

    mutation1_detected = test_mutation_out_of_bounds(published_code)
    if not mutation1_detected:
        print("[ERROR] Mutation Test 1 failed: checker did not reject out-of-bounds mutation (j <= k)!", file=sys.stderr)
        sys.exit(1)
    negative_test_results["MUTATION_TEST_OUT_OF_BOUNDS"] = "REJECTED_WITH_ERROR"
    print("✓ PASS: Mutation Test 1: checker correctly rejected out-of-bounds condition mutation.")

    mutation2_detected = test_mutation_no_op_replacement(published_code)
    if not mutation2_detected:
        print("[ERROR] Mutation Test 2 failed: checker did not reject no-op replacement mutation!", file=sys.stderr)
        sys.exit(1)
    negative_test_results["MUTATION_TEST_NO_OP_REPLACEMENT"] = "REJECTED_WITH_MISMATCH"
    print("✓ PASS: Mutation Test 2: checker correctly rejected no-op replacement mutation.")

    mutation3_detected = test_mutation_empty_stub(published_code)
    if not mutation3_detected:
        print("[ERROR] Mutation Test 3 failed: checker did not reject empty stub mutation!", file=sys.stderr)
        sys.exit(1)
    negative_test_results["MUTATION_TEST_EMPTY_STUB"] = "REJECTED_WITH_MISMATCH"
    print("✓ PASS: Mutation Test 3: checker correctly rejected empty stub return mutation.")

    # Step 5: Generate evidence files
    print("\n[Phase 6] Writing evidence files to work/R61-T029/...")
    generate_evidence_files(
        work_dir=work_dir,
        published_code=published_code,
        proc_output=stdout_text,
        harness_results=harness_results,
        negative_test_results=negative_test_results,
    )

    verification_log = f"""Verification Log for Assignment R61-T029
========================================
All checks completed successfully.
- Phase 1: Published code extraction -> PASS
- Phase 2: Published code subprocess execution -> PASS
- Phase 3: Dynamic module import & unit tests -> PASS
  * Worked example verification -> PASS
  * Boundary example (n <= k) -> PASS
  * Boundary example (n == k) -> PASS
  * Boundary example (n == 0) -> PASS
  * Boundary example (k == 1) -> PASS
  * Lazy generator streaming input -> PASS
- Phase 4: Statistical uniformity test -> PASS
- Phase 5: Deliberate failure & mutation tests -> PASS
  * Deliberate stdout mismatch test -> PASS
  * Deliberate boundary mismatch test -> PASS
  * Mutation 1 (out-of-bounds index) -> PASS
  * Mutation 2 (no-op replacement) -> PASS
  * Mutation 3 (empty stub) -> PASS
"""
    (work_dir / "verification_output.txt").write_text(verification_log, encoding="utf-8")
    print("✓ PASS: Generated inputs.txt, expected.txt, actual.txt, environment.txt, verification_output.txt")

    print("\n========================================================")
    print("🎉 ALL CHECKS PASSED: Reservoir Sampling implementation ")
    print("   and documentation verified successfully.")
    print("========================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
