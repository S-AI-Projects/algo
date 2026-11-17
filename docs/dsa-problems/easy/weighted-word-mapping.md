---
id: weighted-word-mapping
title: "Weighted Word Mapping"
sidebar_label: "Weighted Word Mapping"
description: "Solution to the Weighted Word Mapping problem across C++, JavaScript, Java, and Python with complexity analysis."
tags: [String, Array, Simulation, POTD]
---

## Problem Description

You are given an array of strings `words`, where each string represents a word containing lowercase English letters. You are also given an integer array `weights` of length 26, where `weights[i]` represents the weight of the $i$-th lowercase English letter. 

The weight of a word is defined as the sum of the weights of its characters. 

For each word, take its weight modulo 26 and map the result to a lowercase English letter using reverse alphabetical order ($0 \rightarrow \text{'z'}$, $1 \rightarrow \text{'y'}$, ..., $25 \rightarrow \text{'a'}$). 

Return a string formed by concatenating the mapped characters for all words in order.

### Example 1:
**Input:** `words` = `["abcd","def","xyz"]`
`weights` = `[5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2]`
**Output:** `"rij"`
**Explanation:** - The weight of `"abcd"` is $5 + 3 + 12 + 14 = 34$. The result modulo 26 is $34 \pmod{26} = 8$, which maps to `'r'`.
- The weight of `"def"` is $14 + 1 + 2 = 17$. The result modulo 26 is $17 \pmod{26} = 17$, which maps to `'i'`.
- The weight of `"xyz"` is $7 + 7 + 2 = 16$. The result modulo 26 is $16 \pmod{26} = 16$, which maps to `'j'`.
Thus, the string formed by concatenating the mapped characters is `"rij"`.

## Video Explanation

<LiteYouTubeEmbed
  id="JLemlFGtqow"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Weighted Word Mapping | Leetcode 3838 | Java | Hindi"
  lazyLoad={true}
  webp
/>

---

## Intuition & Approach

The problem asks us to simulate a specific mapping process for each word. The process is straightforward:
1. Iterate through each word and calculate its total weight by looking up the value of each character in the `weights` array.
2. Find the remainder of the total weight when divided by 26 (`total_weight % 26`).
3. Map this remainder to a character in reverse alphabetical order. Since `'z'` corresponds to 0, `'y'` to 1, etc., we can simply subtract the remainder from the ASCII value of `'z'` and convert it back to a character.
4. Append the mapped character to the final result string.

### Complexity
- **Time Complexity:** $O(N)$, where $N$ is the total number of characters across all words in the array. We visit each character exactly once to calculate the sum.
- **Space Complexity:** $O(W)$, where $W$ is the number of words. The output string will contain exactly one character per word. Auxiliary space is $O(1)$.

### Resource Scaling & Copy/View Semantics:

1. **Pass-by-Reference & Zero-Copy Traversal**:
   - In C++, iterating via `for (const string& word : words)` accesses each string by const reference. Iterating by value (`for (string word : words)`) would trigger a deep copy of each string and its heap buffer, causing $O(W \times L)$ redundant allocations.
   - Similarly, the outer parameters are accepted as `const vector<string>&` and `const vector<int>&` to avoid cloning the collections on function call.

2. **Buffer Reservation vs. Dynamic Reallocation**:
   - Since each word maps to exactly one output character, the output size is strictly known in advance ($W = \text{words.size()}$). Calling `result.reserve(words.size())` allocates the required buffer upfront in a single heap operation.
   - Omitting `reserve()` forces `std::string` to undergo geometric capacity doubling and heap reallocations as elements are appended.

3. **Fixed-Cost Operation & Type Behavior**:
   - **Array Indexing**: `weights[c - 'a']` executes as an $O(1)$ direct array index offset calculation into contiguous memory.
   - **Modular Arithmetic Invariant**: `sum = (sum + weights[c - 'a']) % 26` ensures the accumulator remains bounded strictly within $[0, 25]$, avoiding integer overflow regardless of word length.
   - **Reverse Alphabetical Projection**: `(char)('z' - rem)` performs deterministic $O(1)$ ASCII arithmetic mapping remainder $0 \rightarrow \text{'z'}$ and $25 \rightarrow \text{'a'}$.

---

## Solutions

<Tabs groupId="programming-language">
  <TabItem value="cpp" label="C++" default>

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cassert>

using namespace std;

class Solution {
public:
    string mapWordWeights(const vector<string>& words, const vector<int>& weights) {
        string result = "";
        result.reserve(words.size()); // Pre-allocate buffer to avoid dynamic reallocations
        
        for (const string& word : words) { // Const reference avoids redundant string copies
            int sum = 0;
            for (char c : word) {
                sum = (sum + weights[c - 'a']) % 26;
            }
            int rem = sum;
            result += (char)('z' - rem);
        }
        return result;
    }
};

int main() {
    Solution sol;

    // Worked Example 1 from problem description
    vector<string> words = {"abcd", "def", "xyz"};
    vector<int> weights = {5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2};

    string result = sol.mapWordWeights(words, weights);
    cout << "Worked Example Output: " << result << endl;
    assert(result == "rij");

    // Boundary Case 1: Minimum remainder (0 maps to 'z')
    vector<string> boundaryZero = {"a"};
    vector<int> weightsZero(26, 0);
    assert(sol.mapWordWeights(boundaryZero, weightsZero) == "z");

    // Boundary Case 2: Maximum remainder (25 maps to 'a')
    vector<string> boundaryMax = {"a"};
    vector<int> weightsMax(26, 25);
    assert(sol.mapWordWeights(boundaryMax, weightsMax) == "a");

    // Boundary Case 3: Empty words array
    vector<string> emptyWords = {};
    assert(sol.mapWordWeights(emptyWords, weights) == "");

    // Small experiment: Measure capacity reallocation count with and without reserve()
    string unreserved;
    size_t unreservedReallocs = 0;
    size_t prevCap = unreserved.capacity();
    for (int i = 0; i < 100; ++i) {
        unreserved += 'a';
        if (unreserved.capacity() != prevCap) {
            unreservedReallocs++;
            prevCap = unreserved.capacity();
        }
    }

    string reserved;
    reserved.reserve(100);
    size_t reservedCap = reserved.capacity();
    size_t reservedReallocs = 0;
    for (int i = 0; i < 100; ++i) {
        reserved += 'a';
        if (reserved.capacity() != reservedCap) {
            reservedReallocs++;
        }
    }
    cout << "Capacity Reallocations without reserve (100 appends): " << unreservedReallocs << endl;
    cout << "Capacity Reallocations with reserve (100 appends): " << reservedReallocs << endl;
    assert(reservedReallocs == 0);

    return 0;
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
class Solution {
    public String mapWordWeights(String[] words, int[] weights) {
        StringBuilder result = new StringBuilder();
        for (String word : words) {
            int sum = 0;
            for (char c : word.toCharArray()) {
                sum = (sum + weights[c - 'a']) % 26;
            }
            int rem = sum;
            result.append((char)('z' - rem));
        }
        return result.toString();
    }
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
class Solution:
    def mapWordWeights(self, words: list[str], weights: list[int]) -> str:
        result = []
        for word in words:
            total_weight = sum(weights[ord(c) - ord('a')] for c in word)
            rem = total_weight % 26
            result.append(chr(ord('z') - rem))
            
        return "".join(result)
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
/**
 * @param {string[]} words
 * @param {number[]} weights
 * @return {string}
 */
var mapWordWeights = function(words, weights) {
    let result = "";
    for (let word of words) {
        let sum = 0;
        for (let char of word) {
            sum = (sum + weights[char.charCodeAt(0) - 97]) % 26;
        }
        let rem = sum;
        result += String.fromCharCode(122 - rem); // 'z' is 122
    }
    return result;
};
```

  </TabItem>
</Tabs>
