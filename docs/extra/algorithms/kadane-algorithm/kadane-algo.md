---
id: kadanes-algorithm
sidebar_position: 16
title: "Kadane's Algorithm"
sidebar_label: Maximum Subarray Sum
---

### Definition:

Kadane's Algorithm is an efficient algorithm to find the maximum sum of a contiguous subarray in an array of integers. It operates by iterating through the array while keeping track of the current subarray sum and the maximum sum encountered so far.

### Video Explanation 

<LiteYouTubeEmbed
  id="AHZpyENo7k4"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Kadane's Algorithm | Maximum Subarray Sum | Finding and Printing"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Single-Pass Algorithm**:  
  The algorithm processes the array in a single pass:
  - It iteratively updates the maximum sum of the subarray ending at each position.
- **Linear Time Complexity**:  
  The algorithm runs in O(N) time, where N is the number of elements in the array.
- **Constant Space Complexity**:  
  It only requires a few extra variables, resulting in O(1) space complexity.

### Time Complexity:

- **Best Case: $O(N)$**  
  The algorithm processes each element once during the traversal.
- **Average Case: $O(N)$**  
  It consistently runs in linear time for any arrangement of elements.
- **Worst Case: $O(N)$**  
  Regardless of the input distribution, the time complexity remains linear.

### Space Complexity:

- **Space Complexity: $O(1)$**  
  The algorithm uses a constant amount of extra space.

### Approach:

The algorithm follows these steps:

1. **Initialization**:
   - Initialize two variables `max_current` and `max_global` with the value of the first element.
2. **Traverse the Array**:
   - For each element (starting from the second), update `max_current` as the maximum of the current element or the sum of `max_current` and the current element.
   - Update `max_global` to be the maximum of `max_global` and `max_current`.
3. **Result**:
   - `max_global` holds the maximum sum of the contiguous subarray.

### C++ Implementation:

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    // Function to find the maximum sum of a contiguous subarray
    int maxSubArray(vector<int>& nums) {
        int max_current = nums[0], max_global = nums[0];

        for (size_t i = 1; i < nums.size(); i++) {
            // Update max_current to include current element or start fresh from current element
            max_current = max(nums[i], max_current + nums[i]);

            // Update max_global if the current subarray sum is higher
            max_global = max(max_global, max_current);
        }

        return max_global;
    }
};

int main() {
    vector<int> nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};

    // Create an instance of Solution class
    Solution sol;

    // Find the maximum sum of the contiguous subarray
    int max_sum = sol.maxSubArray(nums);

    // Print the result
    cout << "The maximum sum of the contiguous subarray is: " << max_sum << endl;

    return 0;
}
```

### Output:

```text
The maximum sum of the contiguous subarray is: 6
```

### Step-by-Step Worked Example:

To remove any hidden state, we trace the exact evolution of the intermediate variables `max_current` and `max_global` across every element of the input array `nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4}`:

- **State Definitions**:
  - `max_current`: The maximum contiguous subarray sum ending at the current index $i$. At each element, we determine whether to extend the existing contiguous subarray (`max_current + nums[i]`) or discard the accumulated sum and start a new contiguous subarray starting at `nums[i]` (`nums[i]`):
    $$\text{max\_current}_i = \max(\text{nums}[i], \text{max\_current}_{i-1} + \text{nums}[i])$$
  - `max_global`: The global maximum contiguous subarray sum encountered across all indices $0 \dots i$:
    $$\text{max\_global}_i = \max(\text{max\_global}_{i-1}, \text{max\_current}_i)$$

#### State Trace Table:

| Index ($i$) | Element (`nums[i]`) | Candidate 1 (`nums[i]`) | Candidate 2 (`max_current + nums[i]`) | Updated `max_current` | Updated `max_global` | Contiguous Subarray Ending at $i$ | Status / Explanation |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| Init | - | - | - | `-2` | `-2` | `[-2]` | Initialized to first element `nums[0] = -2`. |
| 1 | `1` | `1` | $-2 + 1 = -1$ | `1` | `1` | `[1]` | $\max(1, -1) = 1$. Resetting to start fresh at `1` is better than extending negative sum. `max_global` updated to `1`. |
| 2 | `-3` | `-3` | $1 + (-3) = -2$ | `-2` | `1` | `[1, -3]` | $\max(-3, -2) = -2$. Extending previous subarray. `max_global` remains `1`. |
| 3 | `4` | `4` | $-2 + 4 = 2$ | `4` | `4` | `[4]` | $\max(4, 2) = 4$. Resetting to start fresh at `4` is optimal. `max_global` updated to `4`. |
| 4 | `-1` | `-1` | $4 + (-1) = 3$ | `3` | `4` | `[4, -1]` | $\max(-1, 3) = 3$. Extending previous subarray. `max_global` remains `4`. |
| 5 | `2` | `2` | $3 + 2 = 5$ | `5` | `5` | `[4, -1, 2]` | $\max(2, 5) = 5$. Extending previous subarray. `max_global` updated to `5`. |
| 6 | `1` | `1` | $5 + 1 = 6$ | `6` | `6` | `[4, -1, 2, 1]` | $\max(1, 6) = 6$. Extending previous subarray. `max_global` reaches peak sum `6`. |
| 7 | `-5` | `-5` | $6 + (-5) = 1$ | `1` | `6` | `[4, -1, 2, 1, -5]` | $\max(-5, 1) = 1$. Extending previous subarray. `max_global` remains `6`. |
| 8 | `4` | `4` | $1 + 4 = 5$ | `5` | `6` | `[4, -1, 2, 1, -5, 4]` | $\max(4, 5) = 5$. Extending previous subarray. `max_global` remains `6`. |

#### Identifying the Maximum Subarray:

From the intermediate state trace, the maximum global value `max_global = 6` is reached at index $6$. 

Tracing backward from index $6$ to the point where the current subarray began (index $3$, where `max_current` started fresh at `nums[3] = 4`):
- **Maximum Subarray**: `[4, -1, 2, 1]` (spanning indices $3$ through $6$)
- **Maximum Subarray Sum**: $4 + (-1) + 2 + 1 = 6$

### Boundary Example:

Consider the boundary case with a single negative integer:
- **Input**: `nums = [-7]`
- **Array Size**: $N = 1$

#### Execution Trace:
1. **Initialization**:
   - `max_current = nums[0] = -7`
   - `max_global = nums[0] = -7`
2. **Loop Condition**:
   - The loop condition `for (size_t i = 1; i < nums.size(); i++)` evaluates `1 < 1`, which is `false`. The loop body terminates immediately without executing.
3. **Result**:
   - The function returns `max_global = -7`.
   - **Expected Output / Result**: `-7`
   - **Maximum Contiguous Subarray**: `[-7]` with sum `-7`.

#### Boundary Insights:
- **Single-Element Boundaries ($N = 1$)**: Confirms that single-element arrays terminate gracefully without out-of-bounds index operations or illegal pointer arithmetic.
- **Negative Value Initialization**: If `max_current` or `max_global` were improperly initialized to `0` instead of `nums[0]`, the algorithm would incorrectly output `0` (which corresponds to an empty subarray, violating the non-empty contiguous subarray requirement). Initializing with `nums[0]` ensures all-negative arrays are evaluated correctly.

## Related Topics

- **[Moore's Voting Algorithm](../moores-voting-algorithm/moore-voting-algo.md)**: Optimal $O(N)$ algorithm for majority element detection.
- **[Two Pointers & Sliding Window](../two-pointers-sliding-window.md)**: Techniques for subarray and window processing ($O(N)$).
- **[Monotonic Stack & Queue](../monotonic-stack-queue.md)**: Efficient structure for next greater element and sliding window maximum ($O(N)$).
