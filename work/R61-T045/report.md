# Verification Report: R61-T045 Bitap Algorithm Reproducible Fixture

## Tool Versions
- **Compiler**: Apple clang version 21.0.0 (clang-2100.4.1.1)
- **Python**: 3.14.7 (v3.14.7:823f0323ee6, Aug  5 2026, 07:07:01) [Clang 21.0.0 (clang-2100.1.1.101)]
- **Node**: v24.18.0
- **npm**: 11.16.0
- **Platform**: macOS-27.0.1-arm64-arm-64bit-Mach-O

## Environment & Reproducibility Management
- **Locale Pinning**: The process-global locale is pinned to `"C"` using `std::setlocale(LC_ALL, "C")` before executing pattern matching to ensure identical byte classification and character comparison across environments. The previous process-global locale is saved and restored upon completion.
- **Unsigned Character Conversion**: Input bytes are safely cast via `static_cast<unsigned char>` when indexing `patternMask`, avoiding negative array indexing on systems where `char` is signed.

## Checks Summary
| Check | Text | Pattern | Errors | Expected Index | Actual Index | Status |
|---|---|---|---|---|---|---|
| Worked Example | `"this is a simple example"` | `"example"` | 1 | `17` | `17` | PASS |
| Exact Match | `"this is a simple example"` | `"example"` | 0 | `17` | `17` | PASS |
| Length Overflow ($m > n$) | `"short"` | `"longer pattern"` | 1 | `[]` (empty) | `[]` (empty) | PASS |
| Boundary Start | `"abcdef"` | `"a"` | 0 | `[0]` | `[0]` | PASS |
| Boundary End | `"abcdef"` | `"f"` | 0 | `[5]` | `[5]` | PASS |
| Non-matching | `"hello world"` | `"xyz"` | 1 | `[]` (empty) | `[]` (empty) | PASS |
| Deliberate Wrong Result | Mismatch assertion | `999` | - | Non-zero exit | Exit code -6 | PASS |

## State Trace (`text = "this is a simple example"`, `pattern = "example"`, $m = 7$)
- At character index $i = 23$ (`'e'` in `"example"`):
  - Substring `"example"` occupies text indices $[17, 23]$.
  - Bit vector $R[1]$ has bit $(m-1) = 6$ unset ($0$), indicating a valid match with $\le 1$ errors.
  - Calculated match index: $i - m + 1 = 23 - 7 + 1 = 17$.
  - Output printed: `"Pattern found at index 17 with 1 allowed errors."`
