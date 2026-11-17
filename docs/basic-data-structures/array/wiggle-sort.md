---
id: wiggle-sort
title: Wiggle Sort Algorithm
sidebar_label: Wiggle Sort
sidebar_position: 10
description: "An optimized O(N) single-pass algorithm to sort an array into a wave-like pattern."
tags: [array, java, dsa, algorithms, sorting]
---

# Wiggle Sort

Wiggle Sort is an algorithm that reorders an array such that the elements alternate between being smaller and larger than their adjacent elements. The final array satisfies the condition: `arr[0] <= arr[1] >= arr[2] <= arr[3]...`

## Video Explanation

<LiteYouTubeEmbed
  id="vGsyTE4s34w"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Wiggle Sort - Leetcode 280 - Python"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

## Characteristics
- **Time Complexity:** $O(N)$. The array is traversed exactly once, swapping adjacent elements if they violate the wiggle condition.
- **Space Complexity:** $O(1)$, as the sorting is done entirely in-place.

## Step-by-Step Derivation

The algorithm iterates through the array and inspects each adjacent pair `(nums[i], nums[i + 1])`:
- At an **even index** ($i = 0, 2, 4, \dots$), the element should be less than or equal to the next element: `nums[i] <= nums[i + 1]`. If `nums[i] > nums[i + 1]`, they are swapped.
- At an **odd index** ($i = 1, 3, 5, \dots$), the element should be greater than or equal to the next element: `nums[i] >= nums[i + 1]`. If `nums[i] < nums[i + 1]`, they are swapped.

Crucially, swapping `nums[i]` and `nums[i + 1]` never violates the previously established condition between `nums[i - 1]` and `nums[i]`:
- If $i$ is even and a swap occurs, `new nums[i] < old nums[i] <= nums[i - 1]`, maintaining `nums[i - 1] >= new nums[i]`.
- If $i$ is odd and a swap occurs, `new nums[i] > old nums[i] >= nums[i - 1]`, maintaining `nums[i - 1] <= new nums[i]`.

---

### Worked Example

- **Input:** `nums = [3, 5, 2, 1, 6, 4]`
- **Expected Output:** `[3, 5, 1, 6, 2, 4]`

#### Execution Walkthrough

| Iteration | Parity | Check | Subarray Inspected | Condition Met? | Action | Array State |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Initial | - | - | - | - | Initial state | `[3, 5, 2, 1, 6, 4]` |
| $i = 0$ | Even | `nums[0] > nums[1]` | `[3, 5]` | $3 > 5$ is False ($3 \le 5$) | None | `[3, 5, 2, 1, 6, 4]` |
| $i = 1$ | Odd | `nums[1] < nums[2]` | `[5, 2]` | $5 < 2$ is False ($5 \ge 2$) | None | `[3, 5, 2, 1, 6, 4]` |
| $i = 2$ | Even | `nums[2] > nums[3]` | `[2, 1]` | $2 > 1$ is True | `swap(nums, 2, 3)` | `[3, 5, 1, 2, 6, 4]` |
| $i = 3$ | Odd | `nums[3] < nums[4]` | `[2, 6]` | $2 < 6$ is True | `swap(nums, 3, 4)` | `[3, 5, 1, 6, 2, 4]` |
| $i = 4$ | Even | `nums[4] > nums[5]` | `[2, 4]` | $2 > 4$ is False ($2 \le 4$) | None | `[3, 5, 1, 6, 2, 4]` |

1. **Step 1 ($i = 0$, even index):** Compare `nums[0] = 3` and `nums[1] = 5`. Since $3 \le 5$, the requirement `nums[0] <= nums[1]` is satisfied. No swap is performed. Intermediate array: `[3, 5, 2, 1, 6, 4]`.
2. **Step 2 ($i = 1$, odd index):** Compare `nums[1] = 5` and `nums[2] = 2`. Since $5 \ge 2$, the requirement `nums[1] >= nums[2]` is satisfied. No swap is performed. Intermediate array: `[3, 5, 2, 1, 6, 4]`.
3. **Step 3 ($i = 2$, even index):** Compare `nums[2] = 2` and `nums[3] = 1`. Since $2 > 1$, this violates `nums[2] <= nums[3]`. We call `swap(nums, 2, 3)`, exchanging elements at index 2 and index 3. Intermediate array becomes: `[3, 5, 1, 2, 6, 4]`. Note that `nums[1] >= nums[2]` ($5 \ge 1$) remains valid.
4. **Step 4 ($i = 3$, odd index):** Compare `nums[3] = 2` and `nums[4] = 6`. Since $2 < 6$, this violates `nums[3] >= nums[4]`. We call `swap(nums, 3, 4)`, exchanging elements at index 3 and index 4. Intermediate array becomes: `[3, 5, 1, 6, 2, 4]`. Note that `nums[2] <= nums[3]` ($1 \le 6$) remains valid.
5. **Step 5 ($i = 4$, even index):** Compare `nums[4] = 2` and `nums[5] = 4`. Since $2 \le 4$, the requirement `nums[4] <= nums[5]` is satisfied. No swap is performed. Intermediate array: `[3, 5, 1, 6, 2, 4]`.

**Final Result:** `[3, 5, 1, 6, 2, 4]`, which satisfies $3 \le 5 \ge 1 \le 6 \ge 2 \le 4$.

---

### Boundary Example: Single-Element Array

- **Input:** `nums = [1]`
- **Expected Output:** `[1]`

#### Boundary Analysis
- **Contract Check:** The method begins with the defensive validation:
  ```java
  if (nums == null || nums.length <= 1) {
      return; 
  }
  ```
- **Execution Trace:** When `nums = [1]`, `nums.length` is 1, causing `nums.length <= 1` to evaluate to `true`.
- **Result:** The method returns immediately without entering the loop or mutating the array.
- **Contract Adherence:** A single-element array contains no adjacent pairs and vacuously satisfies the alternating wiggle condition `arr[0] <= arr[1] >= ...`, adhering to the algorithm contract in $O(1)$ time and $O(1)$ space.

## Java Implementation

```java
import java.util.Arrays;

public class WiggleSort {

    /**
     * Sorts the array in-place into a wiggle pattern.
     * @param nums the array of integers to be wiggle sorted.
     */
    public static void sort(int[] nums) {
        // Defensive check to prevent NullPointerException
        if (nums == null || nums.length <= 1) {
            return; 
        }

        for (int i = 0; i < nums.length - 1; i++) {
            // If index is even, current element should be <= next element
            // If index is odd, current element should be >= next element
            if ((i % 2 == 0) ? nums[i] > nums[i + 1] : nums[i] < nums[i + 1]) {
                swap(nums, i, i + 1);
            }
        }
    }

    private static void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    public static void main(String[] args) {
        // Worked Example: standard unsorted array
        int[] nums = {3, 5, 2, 1, 6, 4};
        sort(nums);
        System.out.println("Worked Example Output: " + Arrays.toString(nums));

        // Boundary Example: single-element array (handled by nums.length <= 1 check)
        int[] boundary = {1};
        sort(boundary);
        System.out.println("Boundary Example Output: " + Arrays.toString(boundary));
    }
}
```
