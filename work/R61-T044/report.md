# Verification Report: R61-T044 Odd-Even Sort Invariant Explanation

## Tool Versions
- **Java**: openjdk version "27.0.1.0.3" 2026-10-24
- **Javac**: javac 27.0.1.0.3
- **Python**: 3.14.7 (v3.14.7:823f0323ee6, Aug  5 2026, 07:07:01) [Clang 21.0.0 (clang-2100.1.1.101)]
- **Node**: v24.18.0
- **npm**: 11.16.0
- **Platform**: macOS-27.0.1-arm64-arm-64bit-Mach-O

## Invariant Formalization
1. **Odd Phase**: $\forall i \in \{1, 3, \dots\}$ where $i < n - 1$, after the pass, $arr[i] \le arr[i+1]$.
2. **Even Phase**: $\forall i \in \{0, 2, \dots\}$ where $i < n - 1$, after the pass, $arr[i] \le arr[i+1]$.
3. **Monotonic Convergence**: Each iteration performing $\ge 1$ swap strictly reduces inversion count $\text{inv}(arr)$.
4. **Termination Invariant**: Loop terminates when zero swaps occur across both phases, guaranteeing $\forall i \in [0, n-2], arr[i] \le arr[i+1]$ and multiset conservation.

## Checks Summary
| Check | Input | Expected | Actual | Invariant Verified | Status |
|---|---|---|---|---|---|
| Worked Example | `[5, 3, 1, 4, 2]` | `[1, 2, 3, 4, 5]` | `[1, 2, 3, 4, 5]` | Yes | PASS |
| Boundary 1 (Empty array, $n=0$) | `[]` | `[]` | `[]` | Yes (Trivial) | PASS |
| Boundary 2 (Single element, $n=1$) | `[42]` | `[42]` | `[42]` | Yes (Trivial) | PASS |
| Variation 3 (Already sorted) | `[1, 2, 3, 4, 5]` | `[1, 2, 3, 4, 5]` | `[1, 2, 3, 4, 5]` | Yes (0 swaps) | PASS |
| Variation 4 (Reverse sorted) | `[5, 4, 3, 2, 1]` | `[1, 2, 3, 4, 5]` | `[1, 2, 3, 4, 5]` | Yes (Max inversions) | PASS |
| Variation 5 (Duplicate elements) | `[4, 2, 2, 4, 1, 3]` | `[1, 2, 2, 3, 4, 4]` | `[1, 2, 2, 3, 4, 4]` | Yes (Weak order) | PASS |
| Variation 6 (Negative & zero) | `[-3, 0, -1, 5, -2]` | `[-3, -2, -1, 0, 5]` | `[-3, -2, -1, 0, 5]` | Yes | PASS |
| Variation 7 (Two inverted) | `[2, 1]` | `[1, 2]` | `[1, 2]` | Yes | PASS |
| Deliberate Wrong Result | `[5, 3, 1, 4, 2]` | Exit code != 0 (AssertionError) | Exit code 1 | N/A (Negative Test) | PASS |

## Concrete State Trace (`arr = (5, 3, 1, 4, 2)`)
- Initial: `arr = [5, 3, 1, 4, 2]`, $\text{inv}(arr) = 7$.
- **Iteration 1**:
  - Odd Phase:
    - `i=1`: `arr[1]=3 > arr[2]=1` -> swap -> `[5, 1, 3, 4, 2]`, `isSorted=false`
    - `i=3`: `arr[3]=4 > arr[4]=2` -> swap -> `[5, 1, 3, 2, 4]`, `isSorted=false`
  - Even Phase:
    - `i=0`: `arr[0]=5 > arr[1]=1` -> swap -> `[1, 5, 3, 2, 4]`, `isSorted=false`
    - `i=2`: `arr[2]=3 > arr[3]=2` -> swap -> `[1, 5, 2, 3, 4]`, `isSorted=false`
- **Iteration 2**:
  - Odd Phase:
    - `i=1`: `arr[1]=5 > arr[2]=2` -> swap -> `[1, 2, 5, 3, 4]`, `isSorted=false`
    - `i=3`: `arr[3]=3 <= arr[4]=4` -> no swap
  - Even Phase:
    - `i=0`: `arr[0]=1 <= arr[1]=2` -> no swap
    - `i=2`: `arr[2]=5 > arr[3]=3` -> swap -> `[1, 2, 3, 5, 4]`, `isSorted=false`
- **Iteration 3**:
  - Odd Phase:
    - `i=1`: `arr[1]=2 <= arr[2]=3` -> no swap
    - `i=3`: `arr[3]=5 > arr[4]=4` -> swap -> `[1, 2, 3, 4, 5]`, `isSorted=false`
  - Even Phase:
    - `i=0`: `arr[0]=1 <= arr[1]=2` -> no swap
    - `i=2`: `arr[2]=3 <= arr[3]=4` -> no swap
- **Iteration 4**:
  - Odd Phase: zero swaps (`isSorted` remains `true`)
  - Even Phase: zero swaps (`isSorted` remains `true`)
  - Loop terminates with $arr = [1, 2, 3, 4, 5]$ and invariant completely established.
