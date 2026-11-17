# Issue #27: R61-T027 — Derive the Result Step by Step: Wiggle Sort

## Overview
This task completes GitHub Issue #27 for task `R61-T027` in the `S-AI-Projects/algo` repository on branch `student/e26b07f0757`. The assigned work enhances `docs/basic-data-structures/array/wiggle-sort.md` by adding a clear, beginner-friendly, and technically rigorous step-by-step derivation of the Wiggle Sort algorithm, providing a complete walkthrough of intermediate array states and operations, incorporating the literal worked example (`nums = [3, 5, 2, 1, 6, 4] -> [3, 5, 1, 6, 2, 4]`) and a defensive contract boundary example (`nums = [1] -> [1]`), adding a runnable `main` driver to the Java implementation, and establishing an automated verification suite with negative test capabilities.

## Implementation Details

### Target Article
- **File**: `docs/basic-data-structures/array/wiggle-sort.md`
- **Anchors**: `Wiggle Sort`, `sort`, `swap`

### Content Additions
1. **Step-by-Step Derivation**:
   - Outlines the single-pass greedy invariant:
     - Even index $i$: requires `nums[i] <= nums[i + 1]`; swaps if `nums[i] > nums[i + 1]`.
     - Odd index $i$: requires `nums[i] >= nums[i + 1]`; swaps if `nums[i] < nums[i + 1]`.
   - Explains why local swaps preserve previous relationships without cascading reversals.
   - Provides a comprehensive execution table tracing each iteration index $i$, parity, condition evaluated, subarray inspected, action taken, and intermediate array state.
   - Provides a narrative explanation of each step ($i = 0$ through $4$).

2. **Documented Worked Example**:
   - **Input:** `nums = [3, 5, 2, 1, 6, 4]`
   - **Output:** `[3, 5, 1, 6, 2, 4]`
   - Matches the canonical LeetCode 280 test case referenced in the embedded video.

3. **Boundary Condition Example**:
   - **Input:** `nums = [1]`
   - **Output:** `[1]`
   - Tests the algorithm's defensive guard:
     ```java
     if (nums == null || nums.length <= 1) {
         return; 
     }
     ```
   - Analyzes why single-element and empty arrays vacuously satisfy the alternating wave contract in $O(1)$ time and $O(1)$ space.

4. **Runnable Java Implementation**:
   - Kept `sort` and `swap` identical to the existing authoritative logic.
   - Added `import java.util.Arrays;` and a `public static void main(String[] args)` method demonstrating execution of both the worked example and the boundary case.

## Automated Verification Suite

### `work/R61-T027/check.py`
The validation script:
1. Reads `docs/basic-data-structures/array/wiggle-sort.md` directly.
2. Extracts the actual Java code block using regex (avoiding duplicate retyped copies).
3. Automatically detects the installed Java runtime (`/opt/homebrew/opt/openjdk/bin/java`, `JAVA_HOME`, or standard `PATH`).
4. Executes the extracted Java code in an isolated temporary directory.
5. Verifies stdout against exact expected lines:
   - `Worked Example Output: [3, 5, 1, 6, 2, 4]`
   - `Boundary Example Output: [1]`
6. Performs a negative verification test: compares output against a deliberately incorrect expectation (`[3, 5, 2, 1, 6, 4]`) and verifies that an `AssertionError` is raised.
7. Returns exit code 0 on complete pass, or non-zero on failure.

## Test Results
- `python3 work/R61-T027/check.py`: **PASS** (both examples matched, negative test confirmed)
- `npm run validate:docs`: **PASS** (946 docs scanned, 0 errors, 0 warnings)
- `npm run build`: **PASS** (production site and i18n locales built successfully)
