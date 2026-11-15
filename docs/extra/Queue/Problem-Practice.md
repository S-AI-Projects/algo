---
id: Practice-Problems-on-queue
title: Queue Practice Problems
sidebar_label: Queue Practice Problems
sidebar_position: 9
description: Here are some practice problems for queuing data structure divided into topic and width.
tags: [DSA, algorithms, Queue, dsa]
---

### Basic Queue Problems:

- [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/description)
- [Stack using two Queues](https://www.geeksforgeeks.org/problems/stack-using-two-queues/1)
- [Queue Reversal](https://www.geeksforgeeks.org/problems/queue-reversal/1)
- [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator/description/)

#### Worked Example & Method Comparison: Queue Reversal

A canonical problem under **Basic Queue Problems** is **Queue Reversal** (reversing the elements of a FIFO queue so that the last element becomes the first). Below, we compare two independently understandable approaches on the exact same fixture:

1. **Method 1 (Iterative with Explicit Auxiliary Stack)**:
   - Dequeues all elements into an explicit stack data structure (LIFO).
   - Pops each element from the stack and re-enqueues it into the queue.
   - **Intermediate Representation**: An explicit heap-allocated list/stack storing $N$ elements simultaneously.
   - **Time Complexity**: $O(N)$ with $2N$ data transfers; **Space Complexity**: $O(N)$ explicit auxiliary heap memory.

2. **Method 2 (Recursive with Runtime Call Stack)**:
   - Recursively pops the front element, reverses the remaining sub-queue, and appends the stored element to the back as call frames unwind.
   - **Intermediate Representation**: Implicit activation records (call frames) on the execution call stack holding local `front` references.
   - **Time Complexity**: $O(N)$ with $N$ recursive call frames; **Space Complexity**: $O(N)$ call stack memory without allocating an auxiliary data structure.

```python
from collections import deque

def reverse_queue_iterative(q: deque) -> deque:
    """Method 1: Iterative reversal using an explicit auxiliary stack."""
    stack = []
    while q:
        stack.append(q.popleft())
    while stack:
        q.append(stack.pop())
    return q

def reverse_queue_recursive(q: deque) -> deque:
    """Method 2: Recursive reversal using the runtime call stack."""
    if not q:
        return q
    front = q.popleft()
    reverse_queue_recursive(q)
    q.append(front)
    return q

# Worked example on fixture [10, 20, 30, 40, 50]
q_iter = deque([10, 20, 30, 40, 50])
q_rec = deque([10, 20, 30, 40, 50])

print("Iterative reversal:", list(reverse_queue_iterative(q_iter)))  # Output: [50, 40, 30, 20, 10]
print("Recursive reversal:", list(reverse_queue_recursive(q_rec)))  # Output: [50, 40, 30, 20, 10]

# Worked example assertions (both methods produce identical results)
assert list(reverse_queue_iterative(deque([10, 20, 30, 40, 50]))) == [50, 40, 30, 20, 10]
assert list(reverse_queue_recursive(deque([10, 20, 30, 40, 50]))) == [50, 40, 30, 20, 10]

# Boundary case 1: Empty queue (length 0)
assert list(reverse_queue_iterative(deque([]))) == []
assert list(reverse_queue_recursive(deque([]))) == []

# Boundary case 2: Single-element queue (length 1)
assert list(reverse_queue_iterative(deque([42]))) == [42]
assert list(reverse_queue_recursive(deque([42]))) == [42]
```

### Circular Queue Problems:

- [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/description/)
- [Design Circular Deque](https://leetcode.com/problems/design-circular-deque/description/)
- [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/description/)

### Priority Queue Problems:

- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/description/)
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/description/)
- [Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/description/)
- [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/)
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/description/)

### Deque (Double-Ended Queue) Problems:

- [Deque Implementations](https://www.geeksforgeeks.org/problems/deque-implementations/1)
- [Palindrome Check Using Deque](https://leetcode.com/problems/valid-palindrome/description/)
- [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/description/)
- [Design Front Middle Back Queue](https://leetcode.com/problems/design-front-middle-back-queue/description/)
- [First negative in every window of size k](https://www.geeksforgeeks.org/problems/first-negative-integer-in-every-window-of-size-k3345/1)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/description/)

### Easy

- [Stack using two queues](https://www.geeksforgeeks.org/problems/stack-using-two-queues/1?page=1&category=Queue&sortBy=difficulty)
- [Queue using stack](https://www.geeksforgeeks.org/problems/queue-using-stack/1?page=1&category=Queue&sortBy=difficulty)
- [Reverse First K elements of Queue](https://www.geeksforgeeks.org/problems/reverse-first-k-elements-of-queue/1?page=1&category=Queue&sortBy=difficulty)
- [Generate Binary Numbers](https://www.geeksforgeeks.org/problems/generate-binary-numbers-1587115620/1?page=1&category=Queue&sortBy=difficulty)
- [Minimum Cost of ropes](https://www.geeksforgeeks.org/problems/minimum-cost-of-ropes-1587115620/1?page=1&category=Queue&sortBy=difficulty)

### Medium

- [IPL 2021 - Match Day 2](https://www.geeksforgeeks.org/problems/ipl-2021-match-day-2--141634/1?page=1&category=Queue&sortBy=difficulty)
- [First negative in every window of size k](https://www.geeksforgeeks.org/problems/first-negative-integer-in-every-window-of-size-k3345/1?page=1&category=Queue&sortBy=difficulty)
- [Print Binary Tree levels in sorted order
  ](https://www.geeksforgeeks.org/problems/print-binary-tree-levels-in-sorted-order3241/1?page=2&category=Queue&sortBy=difficulty)
- [Restricted Pacman](https://www.geeksforgeeks.org/problems/restricted-pacman--141631/1?page=2&category=Queue&sortBy=difficulty)
- [Count the Reversals](https://www.geeksforgeeks.org/problems/count-the-reversals0401/1?page=2&category=Queue&sortBy=difficulty)

### Hard

- [LRU Cache](https://www.geeksforgeeks.org/problems/lru-cache/1?page=2&category=Queue&sortBy=difficulty)
- [Steps by Knight](https://www.geeksforgeeks.org/problems/steps-by-knight5927/1?page=2&category=Queue&sortBy=difficulty)
- [Complete Binary Tree](https://www.geeksforgeeks.org/problems/complete-binary-tree/1?page=2&category=Queue&sortBy=difficulty)
- [Card Rotation](https://www.geeksforgeeks.org/problems/card-rotation5834/1?page=2&category=Queue&sortBy=difficulty)
- [Police and Thieves](https://www.geeksforgeeks.org/problems/police-and-thieves--141631/1?page=2&category=Queue&sortBy=difficulty)
