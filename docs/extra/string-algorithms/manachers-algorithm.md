---
id: manachers-algorithm-hub
title: Manacher's Algorithm
sidebar_label: Manacher's Algorithm
sidebar_position: 4
description: A linear time algorithm to find the longest palindromic substring in a string.
tags: [string, algorithm, palindrome, linear-time]
---

# Manacher's Algorithm

Manacher's Algorithm is a clever algorithm designed to find the longest palindromic substring in a given string in strict `O(N)` linear time.

## Intuition
The naive approach expands around every character as a center, taking `O(N^2)` time. Manacher's algorithm utilizes the symmetrical properties of palindromes to skip redundant calculations. By keeping track of the boundaries of the rightmost verified palindrome, it can determine the length of palindromes around subsequent centers without full recomputation.

## Implementation Trick
To gracefully handle both even and odd length palindromes, the standard trick is to insert a special delimiter character (e.g., `#`) between every character in the original string, plus special boundary markers at the start and end to prevent bounds checking overhead.

## Complexity Analysis
- **Time Complexity:** `O(N)` as the right boundary only ever moves to the right.
- **Space Complexity:** `O(N)` to store the array of palindrome radii.

## Runnable Python Example

```python
def manacher_longest_palindrome(s):
    if not s:
        return "", ""

    # Transform string with delimiters and boundary sentinels
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    radii = [0] * n
    center = 0
    right = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            radii[i] = min(right - i, radii[mirror])

        # Explicit bounds checks prevent out-of-range reads if input contains ^ or $
        while i - 1 - radii[i] >= 0 and i + 1 + radii[i] < n and t[i - 1 - radii[i]] == t[i + 1 + radii[i]]:
            radii[i] += 1

        if i + radii[i] > right:
            center = i
            right = i + radii[i]

    max_len = 0
    best_center = 0
    for i in range(1, n - 1):
        if radii[i] > max_len:
            max_len = radii[i]
            best_center = i

    start = (best_center - max_len) // 2
    return s[start : start + max_len], "".join(str(r) for r in radii)


def naive_sentinel_manacher(s):
    # Relies on ^ and $ never appearing in s (omits bounds checks)
    t = "^#" + "#".join(s) + "#$"
    radii = [0] * len(t)
    center = right = 0
    for i in range(1, len(t) - 1):
        if i < right:
            radii[i] = min(right - i, radii[2 * center - i])
        while t[i - 1 - radii[i]] == t[i + 1 + radii[i]]:
            radii[i] += 1
        if i + radii[i] > right:
            center, right = i, i + radii[i]
    return radii


# 1. Worked example (with tie between "bab" and "aba")
worked_pal, worked_radii = manacher_longest_palindrome("babad")
print(f"Worked ('babad'): longest={worked_pal!r}, radii={worked_radii}")

# 2. Boundary examples: total empty-result contrast ("" vs "a")
empty_pal, empty_radii = manacher_longest_palindrome("")
single_pal, single_radii = manacher_longest_palindrome("a")
print(f"Boundary (''): longest={empty_pal!r}, len={len(empty_pal)}")
print(f"Boundary ('a'): longest={single_pal!r}, len={len(single_pal)}, radii={single_radii}")

# 3. Failure-case contrast: input containing sentinel characters ("^a$")
try:
    naive_sentinel_manacher("^a$")
except IndexError as exc:
    print(f"Naive sentinel on '^a$' raised: {type(exc).__name__}")

safe_pal, _ = manacher_longest_palindrome("^a$")
print(f"Bounds-safe on '^a$': longest={safe_pal!r}")
```
