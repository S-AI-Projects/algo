---
id: combination-sum
title: Combination Sum
sidebar_label: Combination Sum
description: Solving the Combination Sum problem using a recursive backtracking approach.
tags:
  - DSA
  - leetcode
  - array
  - backtracking
  - recursion
companies:
  - Amazon
---

## Description:

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to `target` is less than `150` combinations for the given input.

**Example 1:**

Input: `candidates = [2,3,6,7], target = 7`
Output: `[[2,2,3],[7]]`
**Explanation:**
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

**Example 2:**

Input: `candidates = [2,3,5], target = 8`
Output: `[[2,2,2,2],[2,3,3],[3,5]]`

**Example 3:**

Input: `candidates = [2], target = 1`
Output: `[]`

## Video Explanation

<LiteYouTubeEmbed
  id="OyZFFqQtu98"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="L8. Combination Sum | Recursion | Leetcode | C++ | Java"
  lazyLoad={true}
  webp
/>

---

## Approaches:

### 1. Recursive Backtracking

Since we need to find *all* possible combinations that meet a specific condition, **Backtracking** is the most natural and optimal approach. At each step, we make a decision: we can either include the current candidate number in our combination, or skip it and move on to the next candidate.

1. **State:** We need to keep track of the current index we are exploring in the `candidates` array, the current combination of numbers we've chosen, and the `remaining_target` we are trying to reach.
2. **Base Cases:**
   - If `remaining_target == 0`, we found a valid combination! Add a copy of the current combination to our results.
   - If `remaining_target < 0` or we have explored all candidates (`index >= candidates.length`), this path is invalid, so we return and stop exploring.
3. **Recursive Step (Choices):**
   - **Include:** Add the candidate at the current index to our combination and make a recursive call. Crucially, we *do not* increment the index, because we are allowed to use the same candidate an unlimited number of times. We subtract the candidate's value from the `remaining_target`.
   - **Backtrack:** After returning from the "include" recursive call, we pop the last candidate out of our current combination to undo the choice.
   - **Skip:** Make a recursive call where we skip the current candidate by incrementing the index, keeping the `remaining_target` the same.

### Complexity
* **Time Complexity:** $O(2^{T/M})$ where $T$ is the target value and $M$ is the minimum value in the `candidates` array. In the worst case, the recursion tree can branch out exponentially, bounded by the maximum possible depth of $T/M$.
* **Space Complexity:** $O(T/M)$ for the auxiliary recursion stack space. The longest possible combination (and thus the deepest recursion tree) occurs when we repeatedly pick the smallest element.

### Mutation Testing & Invariant Analysis

Backtracking algorithms depend critically on preserving state-space traversal invariants during each recursive step.

#### 1. The Reuse Invariant
In Choice 1 (include current candidate), the algorithm allows the current number to be reused by passing the same `index` to the recursive call:
```cpp
// Correct Choice 1: retain index to allow candidate reuse
current.push_back(candidates[index]);
backtrack(candidates, target - candidates[index], res, current, index);
current.pop_back();
```
Because the problem contract allows choosing the same number an unlimited number of times, passing `index` keeps `candidates[index]` available for subsequent recursive selections until the remaining target is reduced to zero or below.

#### 2. The One-Operation Mutant
Consider an off-by-one parameter mutation in Choice 1 where `index` is prematurely incremented:
```cpp
// Mutated Choice 1: prematurely advances index to index + 1
current.push_back(candidates[index]);
backtrack(candidates, target - candidates[index], res, current, index + 1); // MUTANT
current.pop_back();
```
This mutation restricts selections to at most one occurrence per candidate (converting the algorithm into 0/1 subset sum without replacement, akin to Combination Sum II).

#### 3. Distinguishing Test & State Trace
A distinguishing test must supply an input where the target sum requires selecting at least one candidate multiple times:
- **Input:** `candidates = [2, 3, 6, 7]`, `target = 7`
- **Expected Output:** `[[2, 2, 3], [7]]`

**Step-by-Step State Evolution:**
1. **Initial State:** `backtrack(candidates, target = 7, res, current = [], index = 0)`
2. **First Choice 1:** Includes `candidates[0] = 2`, `current = [2]`, `target = 5`.
3. **Divergence Point:**
   - **Correct Implementation (`index = 0`):**
     Calls `backtrack(..., target = 5, ..., index = 0)`.
     Next Choice 1 includes `2` again: `current = [2, 2]`, `target = 3`, `index = 0`.
     Next Choice 1 includes `2`: `current = [2, 2, 2]`, `target = 1`. Next call makes `target = -1 < 0` (pruned).
     Backtracks to `current = [2, 2]`, explores Choice 2 (skip to `index = 1`, candidate `3`).
     Includes `3`: `current = [2, 2, 3]`, `target = 3 - 3 = 0`.
     Base case hit: records valid combination `[2, 2, 3]`.
     Subsequently finds `[7]`. Output contains both `[[2, 2, 3], [7]]`.
   - **Mutated Implementation (`index + 1 = 1`):**
     Calls `backtrack(..., target = 5, ..., index = 1)`.
     Candidate `2` is immediately locked out. Remaining subproblems can only choose from `[3, 6, 7]`.
     No subset of $\{3, 6, 7\}$ sums to $5$ ($5 - 3 = 2$, but `2` is unreachable).
     All sub-branches prune without finding `[2, 2, 3]`.
     The mutant only discovers `[7]`.
4. **Verification:**
   - **Golden Output:** `[[2, 2, 3], [7]]` (size: 2)
   - **Mutant Output:** `[[7]]` (size: 1)
   The test asserts `res.size() == 2` and verifies the presence of `[2, 2, 3]`, immediately catching and killing the mutant.

---

## Solutions

<Tabs groupId="programming-language">
  <TabItem value="cpp" label="C++" default>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

class Solution {
public:
    void backtrack(vector<int>& candidates, int target, vector<vector<int>>& res, vector<int>& current, int index) {
        // Base Cases
        if (target == 0) {
            res.push_back(current);
            return;
        }
        if (target < 0 || index >= candidates.size()) {
            return;
        }
        
        // Choice 1: Include the current candidate
        current.push_back(candidates[index]);
        backtrack(candidates, target - candidates[index], res, current, index);
        
        // Backtrack
        current.pop_back();
        
        // Choice 2: Skip the current candidate and move to the next
        backtrack(candidates, target, res, current, index + 1);
    }
    
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> res;
        vector<int> current;
        backtrack(candidates, target, res, current, 0);
        return res;
    }
};

int main() {
    Solution solver;

    // Worked Example 1: Literal input [2,3,6,7], target = 7
    vector<int> c1 = {2, 3, 6, 7};
    int t1 = 7;
    vector<vector<int>> res1 = solver.combinationSum(c1, t1);
    assert(res1.size() == 2);
    assert(res1[0] == vector<int>({2, 2, 3}));
    assert(res1[1] == vector<int>({7}));

    // Worked Example 2: Literal input [2,3,5], target = 8
    vector<int> c2 = {2, 3, 5};
    int t2 = 8;
    vector<vector<int>> res2 = solver.combinationSum(c2, t2);
    assert(res2.size() == 3);
    assert(res2[0] == vector<int>({2, 2, 2, 2}));
    assert(res2[1] == vector<int>({2, 3, 3}));
    assert(res2[2] == vector<int>({3, 5}));

    // Boundary Example 3: Target smaller than smallest candidate
    vector<int> c3 = {2};
    int t3 = 1;
    vector<vector<int>> res3 = solver.combinationSum(c3, t3);
    assert(res3.empty());

    // Boundary Example 4: Single candidate with multiple repeated selections
    vector<int> c4 = {3};
    int t4 = 9;
    vector<vector<int>> res4 = solver.combinationSum(c4, t4);
    assert(res4.size() == 1);
    assert(res4[0] == vector<int>({3, 3, 3}));

    // Boundary Example 5: Single candidate exact match
    vector<int> c5 = {5};
    int t5 = 5;
    vector<vector<int>> res5 = solver.combinationSum(c5, t5);
    assert(res5.size() == 1);
    assert(res5[0] == vector<int>({5}));

    cout << "Worked Example 1 result: [";
    for (size_t i = 0; i < res1.size(); ++i) {
        cout << "[";
        for (size_t j = 0; j < res1[i].size(); ++j) {
            cout << res1[i][j] << (j + 1 < res1[i].size() ? "," : "");
        }
        cout << "]" << (i + 1 < res1.size() ? "," : "");
    }
    cout << "]" << endl;

    cout << "All worked and boundary examples passed successfully!" << endl;
    return 0;
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public void backtrack(int[] candidates, int target, List<List<Integer>> res, List<Integer> current, int index) {
        // Base Cases
        if (target == 0) {
            res.add(new ArrayList<>(current));
            return;
        }
        if (target < 0 || index >= candidates.length) {
            return;
        }
        
        // Choice 1: Include the current candidate
        current.add(candidates[index]);
        backtrack(candidates, target - candidates[index], res, current, index);
        
        // Backtrack
        current.remove(current.size() - 1);
        
        // Choice 2: Skip the current candidate and move to the next
        backtrack(candidates, target, res, current, index + 1);
    }
    
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(candidates, target, res, new ArrayList<>(), 0);
        return res;
    }
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        
        def backtrack(index, current_combo, remaining_target):
            # Base Cases
            if remaining_target == 0:
                res.append(current_combo.copy())
                return
            if remaining_target < 0 or index >= len(candidates):
                return
            
            # Choice 1: Include the current candidate
            current_combo.append(candidates[index])
            backtrack(index, current_combo, remaining_target - candidates[index])
            
            # Backtrack
            current_combo.pop()
            
            # Choice 2: Skip the current candidate and move to the next
            backtrack(index + 1, current_combo, remaining_target)
            
        backtrack(0, [], target)
        return res
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
/**
 * @param {number[]} candidates
 * @param {number} target
 * @return {number[][]}
 */
const combinationSum = function(candidates, target) {
    const res = [];
    
    const backtrack = (index, currentCombo, remainingTarget) => {
        // Base Cases
        if (remainingTarget === 0) {
            res.push([...currentCombo]);
            return;
        }
        if (remainingTarget < 0 || index >= candidates.length) {
            return;
        }
        
        // Choice 1: Include the current candidate
        currentCombo.push(candidates[index]);
        backtrack(index, currentCombo, remainingTarget - candidates[index]);
        
        // Backtrack
        currentCombo.pop();
        
        // Choice 2: Skip the current candidate and move to the next
        backtrack(index + 1, currentCombo, remainingTarget);
    };
    
    backtrack(0, [], target);
    return res;
};
```

  </TabItem>
</Tabs>
