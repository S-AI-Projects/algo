---
id: maximum-number-of-balloons
title: "Maximum Number of Balloons"
sidebar_label: Maximum Number of Balloons
description: "Finding the maximum number of instances of the word 'balloon' that can be formed from a given string."
tags: [DSA, leetcode, hash-table, string, counting]
---

## Description:

Given a string `text`, you want to use the characters of `text` to form as many instances of the word **"balloon"** as possible.

You can use each character in `text` **at most once**. Return the maximum number of instances that can be formed.

### Problem Contract & Constraints:

- **Input:** `text` (a string of lowercase English letters)
- **Constraints:**
  - $1 \le \text{text.length} \le 10^4$
  - `text` consists of lowercase English letters only (`'a'` through `'z'`).
- **Output:** An integer representing the maximum number of complete instances of `"balloon"` that can be constructed simultaneously.

---

### Examples:

**Example 1:**

Input: `text = "nlaebolko"`  
Output: `1`  
**Explanation:** We can form one instance of the word "balloon".

**Example 2:**

Input: `text = "loonbalxballpoon"`  
Output: `2`  
**Explanation:** We can form two instances of the word "balloon".

**Example 3:**

Input: `text = "leetcode"`  
Output: `0`  
**Explanation:** We cannot form the word "balloon".

**Example 4 (Boundary Example):**

Input: `text = "b"`  
Output: `0`  
**Explanation:** The input has length $1 < 7$ (where 7 is the length of `"balloon"`). Because characters `'a'`, `'l'`, `'o'`, and `'n'` are entirely absent, the limiting count is 0.

## Video Explanation

<LiteYouTubeEmbed
  id="G9xeB2-7PqY"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Maximum Number of Balloons - Leetcode 1189 - Python"
  lazyLoad={true}
  webp
/>

---

## Approaches:

### 1. Frequency Counting Array

To determine how many times the word **"balloon"** can be formed, we must analyze the frequency of each required character in `text`.

#### Character Multiplicity Requirements:

The word **"balloon"** consists of 7 characters with the following breakdown:
- `'b'`: requires **1** occurrence per word
- `'a'`: requires **1** occurrence per word
- `'l'`: requires **2** occurrences per word
- `'o'`: requires **2** occurrences per word
- `'n'`: requires **1** occurrence per word

Every other character in `text` (such as `'x'`, `'k'`, `'e'`, or `'p'`) is unrelated and contributes 0 toward forming `"balloon"`.

#### Derivation of the Limiting Formula:

Because each character can be used at most once, the maximum number of complete `"balloon"` instances is constrained by the single most deficient constituent letter relative to its required multiplicity.

For characters appearing once (`'b'`, `'a'`, `'n'`), each occurrence yields up to 1 potential word:
$$\text{available}(c) = \text{count}[c]$$

For characters appearing twice (`'l'`, `'o'`), each word requires a complete pair. We compute how many full pairs are available using integer floor division:
$$\text{available}('l') = \left\lfloor \frac{\text{count}['l']}{2} \right\rfloor, \quad \text{available}('o') = \left\lfloor \frac{\text{count}['o']}{2} \right\rfloor$$

The total number of full instances is determined by the minimum limiting frequency across all required letters:
$$\text{result} = \min\left(\text{count}['b'], \text{count}['a'], \left\lfloor \frac{\text{count}['l']}{2} \right\rfloor, \left\lfloor \frac{\text{count}['o']}{2} \right\rfloor, \text{count}['n']\right)$$

---

### Step-by-Step Concrete Walkthroughs

#### Trace 1: Original Worked Example (`text = "loonbalxballpoon"`)

1. **Count Frequencies:**
   - `'a'`: 2
   - `'b'`: 2
   - `'l'`: 4
   - `'o'`: 4
   - `'n'`: 2
   - Unrelated: `'p'`: 1, `'x'`: 1

2. **Evaluate Formations:**

| Target Character | Multiplicity Needed | Total Count in Text | Integer Division | Usable Sets |
| :---: | :---: | :---: | :---: | :---: |
| `'b'` | 1 | 2 | $2 / 1$ | 2 |
| `'a'` | 1 | 2 | $2 / 1$ | 2 |
| `'l'` | 2 | 4 | $\lfloor 4 / 2 \rfloor$ | 2 |
| `'o'` | 2 | 4 | $\lfloor 4 / 2 \rfloor$ | 2 |
| `'n'` | 1 | 2 | $2 / 1$ | 2 |

3. **Bottleneck Calculation:**
   $$\min(2, 2, 2, 2, 2) = 2$$
   Unrelated characters `'x'` and `'p'` are ignored and do not affect the result.

---

#### Trace 2: Original Worked Example (`text = "nlaebolko"`)

1. **Count Frequencies:**
   - `'a'`: 1
   - `'b'`: 1
   - `'l'`: 2
   - `'o'`: 2
   - `'n'`: 1
   - Unrelated: `'e'`: 1, `'k'`: 1

2. **Evaluate Formations:**

| Target Character | Multiplicity Needed | Total Count in Text | Integer Division | Usable Sets |
| :---: | :---: | :---: | :---: | :---: |
| `'b'` | 1 | 1 | $1 / 1$ | 1 |
| `'a'` | 1 | 1 | $1 / 1$ | 1 |
| `'l'` | 2 | 2 | $\lfloor 2 / 2 \rfloor$ | 1 |
| `'o'` | 2 | 2 | $\lfloor 2 / 2 \rfloor$ | 1 |
| `'n'` | 1 | 1 | $1 / 1$ | 1 |

3. **Bottleneck Calculation:**
   $$\min(1, 1, 1, 1, 1) = 1$$

---

#### Trace 3: Asymmetric Limiting Deficit (`text = "balloonballoo"`)

Consider a string with ample `'b'`, `'a'`, `'l'`, and `'o'`, but missing a second `'n'`:
- Counts: `'b'`: 2, `'a'`: 2, `'l'`: 4, `'o'`: 4, `'n'`: 1
- Usable sets:
  - `b`: 2
  - `a`: 2
  - `l`: $\lfloor 4 / 2 \rfloor = 2$
  - `o`: $\lfloor 4 / 2 \rfloor = 2$
  - `n`: $1$
- **Result:** $\min(2, 2, 2, 2, 1) = 1$. The single deficit in `'n'` caps the entire formation at 1.

---

#### Common Misconceptions & Pitfalls

1. **Uniform Multiplicity Fallacy:**
   Assuming each character in `"balloon"` only needs to appear once. A string with $\text{count}['l'] = 1$ cannot provide the two `'l'`s required for a single `"balloon"`. Integer division $\lfloor \text{count}['l'] / 2 \rfloor$ correctly handles the doubled requirement.
2. **Total Count Aggregation Fallacy:**
   Summing all matching characters and dividing by 7 (e.g., $\lfloor \sum \text{counts} / 7 \rfloor$). For example, `text = "bbbbbaaoooonnnnn"` has 16 matching letters ($16 / 7 = 2$), but 0 instances of `'l'`. Surplus letters cannot substitute for missing ones; the minimum limiting component governs the result.
3. **Unrelated / Noise Characters:**
   Unrelated characters (like `'x'`, `'k'`, `'e'`) do not prevent or decrease valid balloon formations. They are simply disregarded during the evaluation.
4. **Contract Scope:**
   The problem specifies lowercase English letters. Non-alphabetic symbols or uppercase letters (such as `'B'`) are outside the problem contract.

### Complexity

* **Time Complexity:** $O(N)$ where $N$ is the length of the string `text`. We iterate through `text` once to count frequencies, followed by an $O(1)$ minimum calculation across the 5 target characters.
* **Space Complexity:** $O(1)$ because the frequency array has a fixed size of 26 integers, which is constant and independent of the input size.

---

## Solutions

<Tabs groupId="programming-language">
  <TabItem value="cpp" label="C++" default>

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int maxNumberOfBalloons(string text) {
        vector<int> count(26, 0);
        
        // Count frequencies of all characters
        for (char c : text) {
            count[c - 'a']++;
        }
        
        // Find the minimum limiting character
        return min({
            count['b' - 'a'], 
            count['a' - 'a'], 
            count['l' - 'a'] / 2, 
            count['o' - 'a'] / 2, 
            count['n' - 'a']
        });
    }
};

int main() {
    Solution solution;

    // Example 1 (Original worked example)
    string text1 = "nlaebolko";
    cout << "Input: text = \"" << text1 << "\"" << endl;
    cout << "Output: " << solution.maxNumberOfBalloons(text1) << endl;

    // Example 2 (Original worked example)
    string text2 = "loonbalxballpoon";
    cout << "Input: text = \"" << text2 << "\"" << endl;
    cout << "Output: " << solution.maxNumberOfBalloons(text2) << endl;

    // Example 3 (Original worked example)
    string text3 = "leetcode";
    cout << "Input: text = \"" << text3 << "\"" << endl;
    cout << "Output: " << solution.maxNumberOfBalloons(text3) << endl;

    // Example 4 (Boundary example: single character string)
    string text4 = "b";
    cout << "Input: text = \"" << text4 << "\"" << endl;
    cout << "Output: " << solution.maxNumberOfBalloons(text4) << endl;

    return 0;
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
class Solution {
    public int maxNumberOfBalloons(String text) {
        int[] count = new int[26];
        
        // Count frequencies of all characters
        for (char c : text.toCharArray()) {
            count[c - 'a']++;
        }
        
        // Find the minimum limiting character
        return Math.min(count['b' - 'a'], 
               Math.min(count['a' - 'a'], 
               Math.min(count['l' - 'a'] / 2, 
               Math.min(count['o' - 'a'] / 2, count['n' - 'a']))));
    }
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from collections import Counter

class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        # Count frequencies of all characters
        count = Counter(text)
        
        # Find the minimum limiting character
        return min(
            count['b'], 
            count['a'], 
            count['l'] // 2, 
            count['o'] // 2, 
            count['n']
        )
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
/**
 * @param {string} text
 * @return {number}
 */
var maxNumberOfBalloons = function(text) {
    const count = { b: 0, a: 0, l: 0, o: 0, n: 0 };
    
    // Count frequencies of all characters
    for (const char of text) {
        if (char in count) {
            count[char]++;
        }
    }
    
    // Find the minimum limiting character
    return Math.min(
        count.b,
        count.a,
        Math.floor(count.l / 2),
        Math.floor(count.o / 2),
        count.n
    );
};
```

  </TabItem>
</Tabs>

### Example Output

```text
Input: text = "nlaebolko"
Output: 1
Input: text = "loonbalxballpoon"
Output: 2
Input: text = "leetcode"
Output: 0
Input: text = "b"
Output: 0
```
