---
id: recursion-depth-performance
title: Recursion Depth and Performance
sidebar_label: Performance Considerations
sidebar_position: 4
description: Understanding how recursion depth affects algorithm performance.
tags: [performance, recursion, optimization]
---


# Recursion Depth and Performance

Recursion depth can affect the performance and efficiency of your program. High depths increase memory usage and may lead to stack overflows. Here are ways to optimize recursive functions.

## Optimizing Recursive Functions
1. **Tail Recursion**: Some languages optimize tail-recursive functions to reduce stack usage.
2. **Memoization**: Store previous results to reduce duplicate calls, especially in algorithms like Fibonacci.
3. **Iterative Solutions**: Convert recursive functions to iterative when feasible.

## Example: Memoization Reduces Work, Not Recursion Depth

A memoized Fibonacci function avoids recalculating the same values, but its first descent still reaches `n` before it can return. For a sufficiently large `n`, the call stack can still overflow. An iterative version performs the same recurrence in a loop and keeps only two integer values, so it avoids recursive stack growth.

```python
from functools import lru_cache


def naive_fibonacci_with_counts(n):
    calls = 0
    max_depth = 0

    def calculate(value, depth):
        nonlocal calls, max_depth
        calls += 1
        max_depth = max(max_depth, depth)
        if value < 2:
            return value
        return calculate(value - 1, depth + 1) + calculate(value - 2, depth + 1)

    result = calculate(n, 1)
    return result, calls, max_depth


def memoized_fibonacci(n):
    @lru_cache(maxsize=None)
    def calculate(value):
        if value < 2:
            return value
        return calculate(value - 1) + calculate(value - 2)

    result = calculate(n)
    return result, calculate.cache_info()


def iterative_fibonacci(n):
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


n = 6
naive_result, naive_calls, naive_depth = naive_fibonacci_with_counts(n)
memo_result, cache = memoized_fibonacci(n)
iterative_result = iterative_fibonacci(n)
assert naive_result == memo_result == iterative_result == 8
assert iterative_fibonacci(0) == 0
print(f"F({n}) = {iterative_result}")
print(f"Naive recursive calls: {naive_calls}; deepest active calls: {naive_depth}")
print(f"Memoized cache misses: {cache.misses}; hits: {cache.hits}; deepest first descent: {n}")
print(f"Iterative boundary F(0) = {iterative_fibonacci(0)}")
```

For the original input `n = 6`, the naive recursion makes `25` calls and reaches six active calls on its deepest path (`F(6)` through `F(2)` to `F(0)`). Memoization computes each input from `0` through `6` once (`7` misses) and reuses four results (`4` hits), but its deepest descent still reaches six active calls. The iterative update moves the pair `(previous, current)` through `(0, 1) → (1, 1) → (1, 2) → (2, 3) → (3, 5) → (5, 8) → (8, 13)` and returns `8` without adding recursive frames.

**Expected output:**

```text
F(6) = 8
Naive recursive calls: 25; deepest active calls: 6
Memoized cache misses: 7; hits: 4; deepest first descent: 6
Iterative boundary F(0) = 0
```
