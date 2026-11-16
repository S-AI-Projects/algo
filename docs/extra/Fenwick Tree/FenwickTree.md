---
id: fenwick-tree
title: "Introduction to Fenwick Tree (Binary Indexed Tree)"
sidebar_label: "Fenwick Tree"
sidebar_position: 1
description: "Information on Fenwick Tree (Binary Indexed Tree) Algorithm"
tags: [Algorithm, Fenwick Tree, Binary Indexed Tree]
---

# Fenwick Tree (Binary Indexed Tree)
## Overview
The Fenwick Tree, also known as a Binary Indexed Tree (BIT), is a data structure used for efficiently calculating prefix sums and updating elements. It offers a significant performance boost when dealing with cumulative frequency tables, making it ideal for scenarios where frequent updates and prefix sum queries are required.

## Video Explanation

<LiteYouTubeEmbed
  id="CWDQJGaN1gY"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Fenwick Tree or Binary Indexed Tree"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

## Use Cases
- **Efficient Range Queries**: Commonly used in situations where range sums and point updates are frequent.
- **Inversion Counting in Arrays**: Used in competitive programming to count inversions in arrays.
- **Data Compression**: Supports cumulative frequency counting, which helps in data compression algorithms.
- **2D Queries**: Fenwick Trees can also be extended to 2D data structures, allowing applications in grid-based problems.

## Algorithm Details
### Key Concepts
1. **Binary Indexed Representation**: Fenwick Trees leverage binary representation for efficient sum and update operations.
2. **Operations**:
   - **Update**: Modify the value of a specific element.
   - **Query**: Compute the cumulative sum up to a specific index.

### Time Complexity
- Both update and query operations are `O(log N)` where `N` is the number of elements, due to the logarithmic depth of the tree.

## Pseudocode

```cpp
// Function to add 'val' to index 'i' (1-based index)
function update(i, val):
    while i <= n:
        BITree[i] += val
        i += (i & -i)

// Function to get sum from index 1 to i (1-based index)
function getSum(i):
    sum = 0
    while i > 0:
        sum += BITree[i]
        i -= (i & -i)
    return sum
```

## Example Code in C++
Here’s a C++ implementation of the Fenwick Tree:

```cpp
#include <iostream>
#include <vector>
using namespace std;

class FenwickTree {
private:
    vector<int> BITree;
    int n;

public:
    // Initialize Fenwick Tree with n elements
    FenwickTree(int size) {
        n = size;
        BITree.resize(n + 1, 0);
    }

    // Update index 'i' with value 'val'
    void update(int i, int val) {
        while (i <= n) {
            BITree[i] += val;
            i += (i & -i);
        }
    }

    // Get cumulative sum from index 1 to 'i'
    int getSum(int i) {
        int sum = 0;
        while (i > 0) {
            sum += BITree[i];
            i -= (i & -i);
        }
        return sum;
    }

    // Get sum from index 'l' to 'r'
    int rangeSum(int l, int r) {
        return getSum(r) - getSum(l - 1);
    }
};

int main() {
    FenwickTree ft(10);
    ft.update(3, 5);   // Update index 3 with +5
    ft.update(5, 2);   // Update index 5 with +2

    cout << "Sum from 1 to 5: " << ft.getSum(5) << endl;
    cout << "Range Sum from 3 to 5: " << ft.rangeSum(3, 5) << endl;
    cout << "Empty prefix sum (getSum(0)): " << ft.getSum(0) << endl;

    return 0;
}
```

### Output:

```text
Sum from 1 to 5: 7
Range Sum from 3 to 5: 7
Empty prefix sum (getSum(0)): 0
```

## Explanation of the Code

- **1-Based Indexing & Tree Structure**: The Fenwick Tree uses 1-based indexing of size `n + 1`. Index `0` is a dummy sentinel node representing an empty prefix.
- **Lowest Set Bit (`i & -i`)**: In two's complement arithmetic, `-i = (~i) + 1`. The bitwise AND operation `i & -i` isolates the lowest significant set bit (LSB) of `i` (the greatest power of 2 that divides `i`). This LSB represents the length of the continuous interval of indices covered by `BITree[i]`:
  $$\text{Interval for } BITree[i] = (i - (i \ \& \ -i), i]$$
- **Update Operation (`update(i, val)`)**: Updates the tree from a specific index by propagating the change to subsequent indices using `i += (i & -i)`. Adding the LSB moves up the tree hierarchy to each parent/ancestor node whose responsibility interval covers index `i`. Because each step increases the index by at least its lowest power-of-two bit, the loop executes at most $\lceil \log_2(n) \rceil$ times ($O(\log N)$).
- **Query Operation (`getSum(i)`)**: Accumulates the sum of elements up to a specific index by traversing backward using `i -= (i & -i)`. Subtracting the LSB removes the rightmost set bit from `i`, hopping backward across non-overlapping power-of-two intervals until reaching `0`. The number of iterations equals the number of set bits in the binary representation of `i`, taking at most $\lfloor \log_2(i) \rfloor + 1$ steps ($O(\log N)$).
- **Range Sum Query (`rangeSum(l, r)`)**: Computes the sum of elements between two 1-based indices `l` and `r` using the difference of prefix sums:
  $$\text{rangeSum}(l, r) = \sum_{k=l}^r A[k] = \text{getSum}(r) - \text{getSum}(l - 1)$$
  When $l = 1$, the subtraction relies on `getSum(0) == 0` to return `getSum(r)` directly without special-case conditional branches.

## Example Walkthrough

Consider an array initialized with $n = 10$ elements, all initially $0$. The internal `BITree` vector is sized to $n + 1 = 11$ elements initialized to $0$:

$$\text{BITree} = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]$$

### 1. Step-by-Step Update: `ft.update(3, 5)`

We add value $+5$ at index $3$. The loop propagates through all covering nodes:

| Iteration | Current $i$ | Binary ($i$) | LSB `(i & -i)` | Target Node | Old Value | Update Action | New Value | Next Index ($i + \text{LSB}$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 3 | `00011` | 1 (`00001`) | `BITree[3]` | 0 | `BITree[3] += 5` | 5 | $3 + 1 = 4$ |
| 2 | 4 | `00100` | 4 (`00100`) | `BITree[4]` | 0 | `BITree[4] += 5` | 5 | $4 + 4 = 8$ |
| 3 | 8 | `01000` | 8 (`01000`) | `BITree[8]` | 0 | `BITree[8] += 5` | 5 | $8 + 8 = 16$ |
| 4 | 16 | `10000` | - | - | - | Terminate ($16 > 10$) | - | - |

**Intermediate `BITree` state after Update 1:**
$$\text{BITree} = [0, 0, 0, \mathbf{5}, \mathbf{5}, 0, 0, 0, \mathbf{5}, 0, 0]$$

---

### 2. Step-by-Step Update: `ft.update(5, 2)`

We add value $+2$ at index $5$. The loop propagates through all covering nodes:

| Iteration | Current $i$ | Binary ($i$) | LSB `(i & -i)` | Target Node | Old Value | Update Action | New Value | Next Index ($i + \text{LSB}$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 5 | `00101` | 1 (`00001`) | `BITree[5]` | 0 | `BITree[5] += 2` | 2 | $5 + 1 = 6$ |
| 2 | 6 | `00110` | 2 (`00010`) | `BITree[6]` | 0 | `BITree[6] += 2` | 2 | $6 + 2 = 8$ |
| 3 | 8 | `01000` | 8 (`01000`) | `BITree[8]` | 5 | `BITree[8] += 2` | 7 | $8 + 8 = 16$ |
| 4 | 16 | `10000` | - | - | - | Terminate ($16 > 10$) | - | - |

---

### 3. Complete Intermediate BIT State Table

Following both updates, here is the exact state across all indices $0 \dots 10$:

| Index ($i$) | Binary ($i$) | Interval Responsible | Stored Value `BITree[i]` | Contributing Updates |
|:---:|:---:|:---:|:---:|:---|
| 0 | `00000` | $[0, 0]$ (Sentinel) | 0 | Boundary dummy node |
| 1 | `00001` | $[1, 1]$ | 0 | None (unmodified) |
| 2 | `00010` | $[1, 2]$ | 0 | None (unmodified) |
| 3 | `00011` | $[3, 3]$ | 5 | `ft.update(3, 5)` |
| 4 | `00100` | $[1, 4]$ | 5 | `ft.update(3, 5)` |
| 5 | `00101` | $[5, 5]$ | 2 | `ft.update(5, 2)` |
| 6 | `00110` | $[5, 6]$ | 2 | `ft.update(5, 2)` |
| 7 | `00111` | $[7, 7]$ | 0 | None (unmodified) |
| 8 | `01000` | $[1, 8]$ | 7 | `ft.update(3, 5)` ($+5$) and `ft.update(5, 2)` ($+2$) |
| 9 | `01001` | $[9, 9]$ | 0 | None (unmodified) |
| 10 | `01010` | $[9, 10]$ | 0 | None (unmodified) |

---

### 4. Step-by-Step Query: `ft.getSum(5)`

To compute the prefix sum from index $1$ to $5$:

| Iteration | Current $i$ | Binary ($i$) | LSB `(i & -i)` | Interval Added | Value Added `BITree[i]` | Running Sum | Next Index ($i - \text{LSB}$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 5 | `00101` | 1 (`00001`) | $[5, 5]$ | 2 | $0 + 2 = 2$ | $5 - 1 = 4$ |
| 2 | 4 | `00100` | 4 (`00100`) | $[1, 4]$ | 5 | $2 + 5 = 7$ | $4 - 4 = 0$ |
| 3 | 0 | `00000` | - | - | - | 7 | Terminate ($0 \ngtr 0$) |

- **Result**: $\text{getSum}(5) = 7$.

---

### 5. Range Query: `ft.rangeSum(3, 5)`

Using the range query formula:
$$\text{rangeSum}(3, 5) = \text{getSum}(5) - \text{getSum}(2)$$

1. Compute $\text{getSum}(2)$:
   - Iteration 1: $i = 2$ (`00010`), $\text{LSB} = 2$. Add `BITree[2] = 0`. Running sum $= 0$. Next $i = 2 - 2 = 0$.
   - Iteration 2: $i = 0$. Loop terminates. Returns $0$.
2. Compute difference:
   $$\text{rangeSum}(3, 5) = 7 - 0 = 7$$
- **Result**: `Range Sum from 3 to 5: 7`.

---

### 6. Boundary Example: Empty Prefix Query (`ft.getSum(0) == 0`)

The boundary case tests an empty prefix query at $i = 0$:

```cpp
ft.getSum(0); // Returns 0
```

#### Execution Trace:
1. **Loop Condition**: The query initializes `sum = 0`. The loop condition `while (i > 0)` evaluates `0 > 0`, which is `false`.
2. **Termination**: The loop body never executes, immediately returning `sum = 0`.
3. **Boundary Verification**:
   - **Correctness**: The sum of elements in an empty prefix contains zero elements and evaluates to $0$.
   - **Sentinel Safety**: Index `0` never evaluates `i & -i` (which would yield $0$ and cause an infinite loop if $i = 0$ were allowed inside the loop).
   - **Simplifies Range Queries**: Because `getSum(0)` cleanly evaluates to $0$, any 1-based range query starting at index $1$ works seamlessly:
     $$\text{rangeSum}(1, r) = \text{getSum}(r) - \text{getSum}(0) = \text{getSum}(r) - 0 = \text{getSum}(r)$$

## Real-World Example
In competitive programming and applications dealing with real-time data processing, such as live leaderboard rankings or real-time transaction data, Fenwick Trees provide a fast and memory-efficient way to maintain cumulative values.
