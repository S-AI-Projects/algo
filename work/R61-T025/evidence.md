# Assignment Evidence: R61-T025

**Task:** R61-T025 — Remove hidden state from the example: Kadane Algorithm  
**Issue:** #25  
**Target File:** `docs/extra/algorithms/kadane-algorithm/kadane-algo.md`  
**Branch:** `R61-T025`  
**Base:** `main` (`S-AI-Projects/algo`)  
**Evidence Folder:** `work/R61-T025/`

---

## 1. Environment & Tool Versions

- **Operating System:** macOS Darwin 25.6.0 (arm64)
- **Python:** 3.9.6
- **Node.js:** v26.13.1
- **npm:** 11.20.0
- **C++ Compiler:** Apple clang version 21.0.0 (clang-2100.1.1.101) (`g++` / clang++ `-std=c++17 -O2`)
- **Git:** 2.50.1 (Apple Git-155)

---

## 2. Documentation Updates Summary

The article `docs/extra/algorithms/kadane-algorithm/kadane-algo.md` was enhanced to remove all hidden intermediate state and provide clear, reproducible explanations:

1. **Original Worked Example Output**:
   - Explicitly reproduced the program output:
     ```text
     The maximum sum of the contiguous subarray is: 6
     ```
2. **Intermediate State Explanation**:
   - Formulated recurrence relations and defined state variables:
     - `max_current`: The maximum contiguous subarray sum ending at the current index $i$:
       $$\text{max\_current}_i = \max(\text{nums}[i], \text{max\_current}_{i-1} + \text{nums}[i])$$
     - `max_global`: The overall maximum contiguous subarray sum observed anywhere across indices $0 \dots i$:
       $$\text{max\_global}_i = \max(\text{max\_global}_{i-1}, \text{max\_current}_i)$$
3. **Step-by-Step Value Change Trace Table**:
   - Traced all 9 elements ($i = 0$ to $8$) of `nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4}`:
     - Shows candidate values (`nums[i]` vs `max_current + nums[i]`), chosen `max_current`, updated `max_global`, current subarray, and operational intuition.
4. **Identification of Maximum Subarray**:
   - Pinpointed the global maximum `max_global = 6` achieved at index 6.
   - Identified contiguous subarray `[4, -1, 2, 1]` spanning indices 3 to 6, with sum $4 + (-1) + 2 + 1 = 6$.
5. **Boundary Example Added**:
   - Evaluated single-element negative input `nums = [-7]`.
   - Traced state initialization (`max_current = -7`, `max_global = -7`) and immediate loop termination ($1 < 1$ is false).
   - Expected result `-7` verified.
   - Explained why initializing variables with `nums[0]` is essential to avoid the 0-initialization bug on all-negative arrays.
6. **Preserved Structural Integrity**:
   - Front matter, heading IDs, LiteYouTubeEmbed, algorithm characteristics, complexity analysis, code block, and related topics links preserved exactly.
   - Replaced non-standard `<bits/stdc++.h>` with standard C++ headers (`<iostream>`, `<vector>`, `<algorithm>`) to guarantee portable compilation across platforms.

---

## 3. Automated Checker (`work/R61-T025/check.py`)

The automated checker extracts the actual C++ code directly from the markdown file, compiles it using Apple clang / `g++ -std=c++17 -O2`, and verifies:
- Direct execution output matches `The maximum sum of the contiguous subarray is: 6`.
- Execution of boundary example `[-7]` returns `-7`.
- Additional test cases (all negative, all positive, single positive).
- Execution of deliberate wrong-result tests confirms detection of assertions.
- Compiler and process failures propagate with non-zero exit codes.

### Execution Output:
```text
=== Step 1: Locating repository and target document ===
Repository Root: /Users/ajaygurjar/algo
Target Doc:      /Users/ajaygurjar/algo/docs/extra/algorithms/kadane-algorithm/kadane-algo.md

=== Step 2: Extracting C++ code from documentation ===
Successfully extracted 38 lines of C++ code from markdown.

=== Step 3: Compiling and executing extracted C++ code (Original Example) ===
Actual output:
  'The maximum sum of the contiguous subarray is: 6'
✓ PASS: Original example output matches expected exactly.

=== Step 4: Compiling and testing boundary condition & test suite ===
Boundary test (nums = [-7]): returned -7
✓ PASS: Boundary example returned -7 as expected.
✓ PASS: Test case ORIGINAL_RESULT returned 6 (expected 6).
✓ PASS: Test case ALL_NEG_RESULT returned -2 (expected -2).
✓ PASS: Test case ALL_POS_RESULT returned 15 (expected 15).
✓ PASS: Test case SINGLE_POS_RESULT returned 42 (expected 42).

=== Step 5: Executing deliberate wrong-result tests ===
✓ PASS: Negative test 1 correctly detected intentional mismatch on original example output.
✓ PASS: Negative test 2 correctly detected intentional mismatch on boundary condition (0 vs -7).

========================================================
🎉 ALL CHECKS PASSED: Kadane algorithm documentation and
   implementation are fully verified, reproducible, and
   free of hidden state.
========================================================
```

---

## 4. Test Inputs, Expected & Actual Outputs

| Test ID | Input Array | Expected Output / Return | Actual Output / Return | Status |
|---|---|---|---|---|
| `ORIGINAL_STDOUT` | `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` | `"The maximum sum of the contiguous subarray is: 6"` | `"The maximum sum of the contiguous subarray is: 6"` | **PASS** |
| `ORIGINAL_RESULT` | `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` | `6` (subarray `[4, -1, 2, 1]`) | `6` | **PASS** |
| `BOUNDARY_RESULT` | `[-7]` | `-7` (subarray `[-7]`) | `-7` | **PASS** |
| `ALL_NEG_RESULT` | `[-5, -3, -8, -2, -9]` | `-2` (subarray `[-2]`) | `-2` | **PASS** |
| `ALL_POS_RESULT` | `[1, 2, 3, 4, 5]` | `15` (subarray `[1, 2, 3, 4, 5]`) | `15` | **PASS** |
| `SINGLE_POS_RESULT`| `[42]` | `42` (subarray `[42]`) | `42` | **PASS** |

---

## 5. Deliberate Wrong-Result Verification

1. **Negative Test 1 (Original Output Mismatch)**:
   - Evaluated assertion against `The maximum sum of the contiguous subarray is: 999`.
   - Result: Correctly raised `AssertionError`.
2. **Negative Test 2 (Boundary Zero-Initialization Trap)**:
   - Evaluated assertion against `0` (classic incorrect return for all-negative inputs).
   - Result: Correctly raised `AssertionError`.

---

## 6. Validation Commands

1. **Checker Execution**:
   ```bash
   python3 work/R61-T025/check.py
   ```
   *Exit code:* `0`

2. **Documentation Frontmatter Validation**:
   ```bash
   npm run validate:docs
   ```
   *Exit code:* `0` (Scanned 946 files, 0 errors, 0 warnings)

3. **Full Production Site Build**:
   ```bash
   npm run build
   ```
   *Exit code:* `0` (Built en and hi static sites without errors)
