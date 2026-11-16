# Assignment Evidence: R61-T026

**Task:** R61-T026 — Clarify the implementation: FenwickTree  
**Issue:** https://github.com/S-AI-Projects/algo/issues/26  
**Target File:** `docs/extra/Fenwick Tree/FenwickTree.md`  
**Branch:** `R61-T026`  
**Base:** `main` (`S-AI-Projects/algo`)  
**Evidence Folder:** `work/R61-T026/`

---

## 1. Environment & Tool Versions

- **Operating System:** macOS Darwin 25.6.0 (arm64)
- **Python:** 3.9.6 (`/usr/bin/python3`)
- **Node.js:** v26.13.1 (`/opt/homebrew/bin/node`)
- **npm:** 11.20.0 (`/opt/homebrew/bin/npm`)
- **C++ Compiler:** Apple clang version 21.0.0 (clang-2100.1.1.101) (`g++` / `clang++` `-std=c++17 -O2`)
- **Git:** 2.50.1 (Apple Git-155)

---

## 2. Documentation Updates Summary

The article `docs/extra/Fenwick Tree/FenwickTree.md` was enhanced to clarify the implementation, explain intermediate bitwise states, and document boundary query behaviors:

1. **Preserved Original Worked Input and Expected Output**:
   - The original calls in `main()`:
     - `ft.update(3, 5);`
     - `ft.update(5, 2);`
     - `cout << "Sum from 1 to 5: " << ft.getSum(5) << endl;`
     - `cout << "Range Sum from 3 to 5: " << ft.rangeSum(3, 5) << endl;`
   - Preserved the literal output:
     ```text
     Sum from 1 to 5: 7
     Range Sum from 3 to 5: 7
     ```
2. **Clear Operation Mechanics (`update(i, val)` and `getSum(i)`)**:
   - **Lowest Set Bit (`i & -i`)**: Explained two's complement arithmetic (`-i = (~i) + 1`), showing how bitwise AND isolates the rightmost set bit (the length of the interval covered by `BITree[i]`).
   - **Update Operation (`update(i, val)`)**: Detailed propagation via `i += (i & -i)`, ascending through ancestor nodes covering index $i$ in at most $\lceil \log_2(n) \rceil$ steps ($O(\log N)$).
   - **Query Operation (`getSum(i)`)**: Detailed prefix accumulation via `i -= (i & -i)`, hopping backward across non-overlapping power-of-two intervals until reaching `0` in at most $\lfloor \log_2(i) \rfloor + 1$ steps ($O(\log N)$).
   - **Range Query Operation (`rangeSum(l, r)`)**: Derived prefix subtraction formula $\sum_{k=l}^r A[k] = \text{getSum}(r) - \text{getSum}(l - 1)$.
3. **Exact Intermediate BIT Indices and Values**:
   - Traced `ft.update(3, 5)` step-by-step: indices 3, 4, 8 updated to 5.
   - Traced `ft.update(5, 2)` step-by-step: indices 5 and 6 updated to 2, index 8 updated to $5 + 2 = 7$.
   - Provided complete state table of `BITree` across all indices $0 \dots 10$:
     `[0, 0, 0, 5, 5, 2, 2, 0, 7, 0, 0]`.
   - Traced query `ft.getSum(5)` step-by-step: index 5 adds 2, index 4 adds 5 $\Rightarrow$ sum = 7.
   - Traced range query `ft.rangeSum(3, 5) = getSum(5) - getSum(2) = 7 - 0 = 7`.
4. **Boundary Example (Empty Prefix Query `getSum(0) == 0`)**:
   - Added `cout << "Empty prefix sum (getSum(0)): " << ft.getSum(0) << endl;` to `main()`.
   - Documented why `while (i > 0)` terminates immediately at $i = 0$, returning `0` safely without invalid indexing.
   - Explained how this guarantees `rangeSum(1, r) = getSum(r) - getSum(0) = getSum(r)` requires zero branching or edge-case handling.
5. **Structural Integrity**:
   - Preserved front matter, existing headings, IDs, video embed (`<LiteYouTubeEmbed ... />`), and unrelated sections.

---

## 3. Automated Checker (`work/R61-T026/check.py`)

The automated checker extracts the actual C++ code directly from `docs/extra/Fenwick Tree/FenwickTree.md`, compiles it using Apple clang / `g++ -std=c++17 -O2`, and verifies:
- Direct program output matches:
  ```text
  Sum from 1 to 5: 7
  Range Sum from 3 to 5: 7
  Empty prefix sum (getSum(0)): 0
  ```
- Extended test harness confirms boundary query `getSum(0) == 0`, lower bound range query `rangeSum(1, 5) == 7`, prefix queries, range queries, and subsequent update behavior.
- Deliberate wrong-result tests confirm that assertions trigger on intentional stdout and boundary mismatches.
- Subprocess and compiler errors propagate with non-zero exit codes.

### Execution Output:
```text
=== Step 1: Locating repository and target document ===
Repository Root: /Users/ajaygurjar/algo
Target Doc:      /Users/ajaygurjar/algo/docs/extra/Fenwick Tree/FenwickTree.md

=== Step 2: Extracting C++ code from documentation ===
Successfully extracted 51 lines of C++ code from markdown.

=== Step 3: Compiling and executing extracted C++ code (Original Example + Boundary) ===
Actual output from extracted code:
  Sum from 1 to 5: 7
  Range Sum from 3 to 5: 7
  Empty prefix sum (getSum(0)): 0
✓ PASS: Line 1 matches: 'Sum from 1 to 5: 7'
✓ PASS: Line 2 matches: 'Range Sum from 3 to 5: 7'
✓ PASS: Line 3 matches: 'Empty prefix sum (getSum(0)): 0'

=== Step 4: Compiling and executing extended verification harness ===
✓ PASS: INIT_GETSUM_0 = 0 (expected 0)
✓ PASS: INIT_GETSUM_1 = 0 (expected 0)
✓ PASS: BOUNDARY_EMPTY_PREFIX = 0 (expected 0)
✓ PASS: BOUNDARY_RANGE_LOWER_BOUND = 7 (expected 7)
✓ PASS: QUERY_GETSUM_1 = 0 (expected 0)
✓ PASS: QUERY_GETSUM_2 = 0 (expected 0)
✓ PASS: QUERY_GETSUM_3 = 5 (expected 5)
✓ PASS: QUERY_GETSUM_4 = 5 (expected 5)
✓ PASS: QUERY_GETSUM_5 = 7 (expected 7)
✓ PASS: QUERY_GETSUM_6 = 7 (expected 7)
✓ PASS: QUERY_GETSUM_7 = 7 (expected 7)
✓ PASS: QUERY_GETSUM_8 = 7 (expected 7)
✓ PASS: QUERY_GETSUM_10 = 7 (expected 7)
✓ PASS: QUERY_RANGESUM_3_5 = 7 (expected 7)
✓ PASS: QUERY_RANGESUM_3_3 = 5 (expected 5)
✓ PASS: QUERY_RANGESUM_5_5 = 2 (expected 2)
✓ PASS: QUERY_RANGESUM_4_5 = 2 (expected 2)
✓ PASS: QUERY_RANGESUM_1_10 = 7 (expected 7)
✓ PASS: POST_UPDATE_GETSUM_1 = 10 (expected 10)
✓ PASS: POST_UPDATE_GETSUM_3 = 15 (expected 15)
✓ PASS: POST_UPDATE_GETSUM_5 = 17 (expected 17)
✓ PASS: POST_UPDATE_RANGESUM_1_3 = 15 (expected 15)

=== Step 5: Executing deliberate wrong-result tests ===
✓ PASS: Negative test 1 correctly detected intentional stdout mismatch.
✓ PASS: Negative test 2 correctly detected intentional boundary mismatch.

========================================================
🎉 ALL CHECKS PASSED: Fenwick Tree documentation and
   implementation are fully verified, reproducible, and
   compilation-safe.
========================================================
```

---

## 4. Test Inputs, Expected & Actual Outputs

| Test ID | Input / Operation | Expected Output / Value | Actual Output / Value | Status |
|---|---|---|---|---|
| `ORIGINAL_LINE_1` | `cout << ft.getSum(5)` | `"Sum from 1 to 5: 7"` | `"Sum from 1 to 5: 7"` | **PASS** |
| `ORIGINAL_LINE_2` | `cout << ft.rangeSum(3, 5)` | `"Range Sum from 3 to 5: 7"` | `"Range Sum from 3 to 5: 7"` | **PASS** |
| `BOUNDARY_LINE_3` | `cout << ft.getSum(0)` | `"Empty prefix sum (getSum(0)): 0"` | `"Empty prefix sum (getSum(0)): 0"` | **PASS** |
| `BOUNDARY_EMPTY_PREFIX` | `ft.getSum(0)` | `0` | `0` | **PASS** |
| `BOUNDARY_RANGE_LOWER_BOUND` | `ft.rangeSum(1, 5)` | `7` | `7` | **PASS** |
| `QUERY_GETSUM_3` | `ft.getSum(3)` | `5` | `5` | **PASS** |
| `QUERY_GETSUM_4` | `ft.getSum(4)` | `5` | `5` | **PASS** |
| `QUERY_GETSUM_5` | `ft.getSum(5)` | `7` | `7` | **PASS** |
| `QUERY_RANGESUM_3_5` | `ft.rangeSum(3, 5)` | `7` | `7` | **PASS** |
| `POST_UPDATE_GETSUM_5`| `update(1, 10)` -> `getSum(5)` | `17` | `17` | **PASS** |

---

## 5. Deliberate Wrong-Result Verification

1. **Negative Test 1 (Stdout Mismatch)**:
   - Evaluated assertion against `"Sum from 1 to 5: 999\n..."`.
   - Result: Correctly detected mismatch and raised `AssertionError`.
2. **Negative Test 2 (Boundary Sentinel Mismatch)**:
   - Evaluated assertion against `99` for `getSum(0)`.
   - Result: Correctly detected mismatch and raised `AssertionError`.

---

## 6. Validation Commands

1. **Checker Execution**:
   ```bash
   python3 work/R61-T026/check.py
   ```
   *Exit code:* `0`

2. **Documentation Frontmatter Validation**:
   ```bash
   npm run validate:docs
   ```
   *Exit code:* `0` (Scanned 946 files, 0 errors, 0 warnings)

3. **Combined Task Validation Requirement**:
   ```bash
   python3 work/R61-T026/check.py && npm run build
   ```
   *Exit code:* `0`
