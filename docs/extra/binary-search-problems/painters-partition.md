---
id: painters-partition
title: "Painter's Partition Problem"
sidebar_label: "Binary Search"
sidebar_position: 2
description: "Solving the Painter's Partition Problem using Binary Search on the answer space."
tags: [Algorithm, Problem, Binary Search]
---

## Problem - Statement
- You are given an array of N boards, where each element represents the length of a board.
- You have M painters available to paint these boards.
- Each painter takes 1 unit of time to paint 1 unit of board length.
🎯 The Goal
- Minimize the maximum time taken by any painter to finish the job, given that boards must be assigned in a continuous manner.

## Video Explanation

<LiteYouTubeEmbed
  id="YTTdLgyqOLY"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Lecture 15: Book Allocation Problem || Aggressive Cows Problem || Binary Search Advanced Problems"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

## Why Binary Search
- The answer (minimum time) lies within a defined, sorted range.
- **Monotonicity**: If a job can be done in time $T$, it can definitely be done in any time greater than $T$.
- **Efficiency**: Instead of checking every possible time, we use Binary Search to find the optimal limit in $O(\log(\text{Range}))$.

## Loop Invariant in `isPossible()`

The helper function `isPossible(vector<int> &boards, int n, int m, int maxAllowedTime)` determines whether all $n$ contiguous boards can be assigned to at most $m$ painters such that no individual painter paints more than `maxAllowedTime` total length.

### Invariant Statement

At the start of each iteration $i$ (for $0 \le i \le n$) of the loop:

1. **Processed Prefix**: Boards `boards[0]` through `boards[i - 1]` have been contiguously partitioned among painters without altering their original array order.
2. **`paintersCount`**: Represents the exact number of painters allocated so far to paint the prefix `boards[0 ... i - 1]`.
3. **`currentTime`**: Represents the total board length accumulated by the current (active) painter for their contiguous slice.
4. **Capacity Constraint**: No painter used so far has been assigned a total length exceeding `maxAllowedTime`. That is, every finished painter segment has length $\le \text{maxAllowedTime}$, and the currently active painter has $0 \le \text{currentTime} \le \text{maxAllowedTime}$.
5. **Greedy Assignment**: Boards are assigned greedily. A painter continues to take consecutive boards as long as adding the next board does not exceed `maxAllowedTime`. A new painter is started if and only if adding the next board would violate the limit. Because splitting any segment earlier would only increase or maintain the number of painters needed, this greedy allocation requires the minimum number of painters for any contiguous partition under `maxAllowedTime`.

### Inductive Proof of the Invariant

- **Initialization ($i = 0$):**
  - Before the loop starts, `paintersCount = 1` and `currentTime = 0`.
  - The prefix of processed boards is empty (0 boards).
  - No painter has exceeded `maxAllowedTime`, and 0 length is assigned to painter 1. The invariant holds trivially.

- **Maintenance (from iteration $i$ to $i + 1$):**
  - If `boards[i] > maxAllowedTime`, no painter could ever paint this single board without exceeding the limit. The function immediately returns `false`, correctly identifying infeasibility.
  - If `currentTime + boards[i] <= maxAllowedTime`:
    - Board $i$ is assigned to the current painter, updating `currentTime = currentTime + boards[i]`.
    - No new painter is allocated (`paintersCount` remains unchanged).
    - The capacity constraint continues to hold because the updated `currentTime` is $\le \text{maxAllowedTime}$.
  - If `currentTime + boards[i] > maxAllowedTime`:
    - The current painter cannot accept board $i$ without exceeding `maxAllowedTime`.
    - Since boards must be contiguous, a new painter must be allocated: `paintersCount++`.
    - The new painter starts with board $i$: `currentTime = boards[i]`.
    - Since `boards[i] <= maxAllowedTime`, the new painter does not exceed `maxAllowedTime`.
  - In both scenarios, the prefix `boards[0 ... i]` is contiguously assigned, no painter exceeds `maxAllowedTime`, and greedy optimality is preserved for iteration $i + 1$.

- **Termination ($i = n$):**
  - The loop finishes after inspecting all $n$ boards.
  - `paintersCount` reflects the minimal number of painters required to paint all $n$ boards contiguously without any painter exceeding `maxAllowedTime`.
  - The configuration is feasible if and only if `paintersCount <= m`.

---

## Feasibility and Binary Search in `minTimeToPaint()`

The function `minTimeToPaint()` uses binary search on the answer space to find the minimum possible maximum time.

### Monotonicity of Feasibility

Let $P(T)$ be the predicate `isPossible(boards, n, m, T)`.
- If $P(T) = \text{true}$, then at most $m$ painters can paint all boards with maximum load $\le T$. If we allow a larger limit $T' > T$, the exact same board partition is still valid because every painter's load is $\le T < T'$. Hence, $P(T') = \text{true}$ for all $T' \ge T$.
- If $P(T) = \text{false}$, it is impossible to partition the boards among $m$ painters with ceiling $T$. Tightening the limit to $T'' < T$ cannot make it possible. Hence, $P(T'') = \text{false}$ for all $T'' \le T$.

Because $P(T)$ is monotonic ($\text{false}, \dots, \text{false}, \text{true}, \dots, \text{true}$), the optimal answer is the first value $T$ where $P(T) = \text{true}$.

### Search Space Bounds

- **Lower Bound (`start = maxVal`):**
  - $\text{maxVal} = \max_{0 \le i < n}(\text{boards}[i])$.
  - Because boards are indivisible, the painter assigned the largest individual board must spend at least $\text{maxVal}$ time. Thus, no valid maximum time can be smaller than $\text{maxVal}$.
- **Upper Bound (`end = sum`):**
  - $\text{sum} = \sum_{i=0}^{n-1} \text{boards}[i]$.
  - If only $m = 1$ painter is available (or all boards are assigned to one painter), that painter takes $\text{sum}$ units of time. This is the worst-case upper bound.

### Binary Search Reduction

1. Compute $mid = start + (end - start) / 2$.
2. Test feasibility with `isPossible(boards, n, m, mid)`:
   - **Feasible (`true`):** $mid$ is achievable with at most $m$ painters. We record `ans = mid` as the best answer found so far and try to find a smaller feasible maximum by searching the left subrange: `end = mid - 1`.
   - **Infeasible (`false`):** $mid$ is too restrictive (requires more than $m$ painters). Any limit $\le mid$ will also fail, so we search the right subrange: `start = mid + 1`.
3. When `start > end`, `ans` contains the globally minimal maximum painting time.

---

## Code Implementation
```Cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

// This function checks if the configuration is possible for a given max time
bool isPossible(vector<int> &boards, int n, int m, int maxAllowedTime) {
    int paintersCount = 1;
    int currentTime = 0;

    for (int i = 0; i < n; i++) {
        if (boards[i] > maxAllowedTime) return false;
        if (currentTime + boards[i] <= maxAllowedTime) {
            currentTime += boards[i];
        } else {
            paintersCount++;
            currentTime = boards[i];
        }
    }
    return paintersCount <= m;
}

int minTimeToPaint(vector<int> &boards, int n, int m) {
    int sum = 0, maxVal = 0;
    for (int length : boards) {
        sum += length;
        maxVal = max(maxVal, length);
    }

    int start = maxVal, end = sum, ans = -1;

    while (start <= end) {
        int mid = start + (end - start) / 2;

        if (isPossible(boards, n, m, mid)) {
            ans = mid;
            end = mid - 1; // Try to find a smaller maximum
        } else {
            start = mid + 1; // Increase limit to make it possible
        }
    }
    return ans;
}

int main() {
    vector<int> boards = {40, 30, 10, 20};
    int m = 2;
    int n = boards.size();
    int result = minTimeToPaint(boards, n, m);
    cout << "Minimum Maximum Time is: " << result << endl;
    return 0;
}
```

## Key Logic
- **Continuous Assignment**: Unlike the Aggressive Cows problem, the boards must be picked in the order they appear in the array.
- **Search Range**: The minimum possible time is the largest single board (max(arr)), and the maximum is the sum of all boards (sum(arr)).
- **IsPossible Function**: A greedy check to see how many painters are required if no painter can exceed mid time.
- **Time Complexity**: $O(N \cdot \log(\text{Sum of lengths}))$, where $N$ is the number of boards and the range is the total length.
- **Space Complexity**: $O(1)$ auxiliary space beyond the input array.

---

## Worked Example

### Default Example
- **Input:** `boards = {40, 30, 10, 20}`, `m = 2`
- **Bounds:**
  - `start = max(40, 30, 10, 20) = 40`
  - `end = 40 + 30 + 10 + 20 = 100`
- **Execution Trace:**
  1. $mid = 40 + (100 - 40) / 2 = 70$:
     - Painter 1: $\{40\}$, `currentTime = 40`. Next board 30 exceeds 70 ($40 + 30 = 70 \le 70$), so Painter 1 takes $\{40, 30\}$, `currentTime = 70`.
     - Next board 10 exceeds 70 ($70 + 10 = 80 > 70$), Painter 2 takes $\{10, 20\}$, `currentTime = 30`.
     - `paintersCount = 2 <= 2` $\to$ Feasible (`true`).
     - Record `ans = 70`, search left: `end = 69`.
  2. $mid = 40 + (69 - 40) / 2 = 54$:
     - Painter 1: $\{40\}$, next board 30 exceeds 54 ($40 + 30 = 70 > 54$).
     - Painter 2: $\{30, 10\}$, next board 20 exceeds 54 ($40 + 20 = 60 > 54$).
     - Painter 3: $\{20\}$.
     - `paintersCount = 3 > 2` $\to$ Infeasible (`false`).
     - Search right: `start = 55`.
  3. $mid = 55 + (69 - 55) / 2 = 62$:
     - Painter 1: $\{40\}$, Painter 2: $\{30, 10, 20\} = 60 \le 62$.
     - `paintersCount = 2 <= 2` $\to$ Feasible (`true`).
     - Record `ans = 62`, search left: `end = 61`.
  4. $mid = 55 + (61 - 55) / 2 = 58$:
     - Painter 1: $\{40\}$, Painter 2: $\{30, 10\} = 40$, Painter 3: $\{20\}$.
     - `paintersCount = 3 > 2` $\to$ Infeasible (`false`).
     - Search right: `start = 59`.
  5. $mid = 59 + (61 - 59) / 2 = 60$:
     - Painter 1: $\{40\} = 40 \le 60$.
     - Painter 2: $\{30, 10, 20\} = 60 \le 60$.
     - `paintersCount = 2 <= 2` $\to$ Feasible (`true`).
     - Record `ans = 60`, search left: `end = 59`.
  6. $start = 59 > end = 59$: Loop terminates.
- **Expected Output:**
  ```text
  Minimum Maximum Time is: 60
  ```

---

## Boundary Cases and Test Variations

### Clear Boundary Example: Single Board, Single Painter
- **Input:** `boards = {7}`, `m = 1`
- **Analysis:**
  - `start = 7`, `end = 7`.
  - $mid = 7$: Painter 1 is assigned board $\{7\}$, total length 7.
  - `paintersCount = 1 <= 1` $\to$ Feasible.
  - `ans = 7`, `end = 6`. Loop terminates since $start (7) > end (6)$.
- **Expected Output:** `7`

### Bounded Test Variations

#### 1. Single Board with Multiple Painters ($m > n$)
- **Input:** `boards = {7}`, `m = 3`
- **Description:** There are more painters available than boards. Because a single board cannot be split between multiple painters, only one painter can be assigned the board.
- **Assignment:** Painter 1 gets $\{7\}$ (load = 7); painters 2 and 3 remain unallocated.
- **Expected Output:** `7`

#### 2. Number of Painters Equals Number of Boards ($m = n$)
- **Input:** `boards = {10, 20, 30, 40}`, `m = 4`
- **Description:** Each painter can be assigned exactly one board. The bottleneck is the painter receiving the longest single board.
- **Assignment:** Painter 1 gets $\{10\}$, Painter 2 gets $\{20\}$, Painter 3 gets $\{30\}$, Painter 4 gets $\{40\}$.
- **Expected Output:** `40` (equal to $\max(\text{boards})$)

#### 3. Single Painter for Multiple Boards ($m = 1$)
- **Input:** `boards = {5, 10, 15}`, `m = 1`
- **Description:** Only one painter is available to paint all boards. The painter must paint every board sequentially.
- **Assignment:** Painter 1 gets $\{5, 10, 15\}$ (total load = $5 + 10 + 15 = 30$).
- **Expected Output:** `30` (equal to $\sum \text{boards}$)

#### 4. Uniform Board Lengths
- **Input:** `boards = {10, 10, 10, 10}`, `m = 2`
- **Description:** All boards have identical lengths. Two painters can divide the four boards equally.
- **Assignment:** Painter 1 gets $\{10, 10\}$ (load = 20); Painter 2 gets $\{10, 10\}$ (load = 20).
- **Expected Output:** `20`

#### 5. Uneven Boards with Balanced Partition
- **Input:** `boards = {1, 2, 3, 4, 5, 6, 7, 8, 9}`, `m = 3`
- **Description:** Total sum is 45. We seek to partition the 9 contiguous boards among 3 painters to minimize the maximum painter load.
- **Assignment:**
  - Painter 1: $\{1, 2, 3, 4, 5\}$ (load = $15$)
  - Painter 2: $\{6, 7\}$ (load = $13$)
  - Painter 3: $\{8, 9\}$ (load = $17$)
  - The maximum load among the three painters is $\max(15, 13, 17) = 17$. If limit were 16, Painter 3 could only take $\{8\}$, requiring a 4th painter for $\{9\}$.
- **Expected Output:** `17`

#### 6. Strictly Decreasing Board Lengths
- **Input:** `boards = {100, 50, 20, 10}`, `m = 2`
- **Description:** The first board is large, while remaining boards taper off. The single largest board dictates the lower bound.
- **Assignment:**
  - Painter 1: $\{100\}$ (load = 100)
  - Painter 2: $\{50, 20, 10\}$ (load = 80)
  - Maximum load is $\max(100, 80) = 100$.
- **Expected Output:** `100`
