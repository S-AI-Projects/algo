---
id: intersection-linked-lists
sidebar_position: 1
title: "Find the Intersection Point of Two Linked Lists in C++"
description: "This tutorial explains how to find the intersection point of two singly linked lists using C++."
sidebar_label: "Linked List Intersection"
tags: [dsa, linked-lists, intersection]
---

## Linked List Intersection:

This tutorial provides a C++ implementation to find the intersection point of two singly linked lists. Intersection occurs when two lists share the same nodes after a certain point.

### Problem Statement:

Given two singly linked lists, find the node where the two linked lists intersect. Intersection is determined by node identity, not by node value.

### Video Explanation

<LiteYouTubeEmbed
  id="u4FWXfgS8jw"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Intersection point of two Linked Lists | Amazon | Microsoft | Brute | Better | Optimal1 | Optimal2"
  lazyLoad={true}
  webp
/>

### Approach:

1. Count the nodes in both lists.
2. Calculate the difference in their lengths.
3. Advance the pointer in the longer list by that difference so both pointers have the same number of nodes left.
4. Traverse both lists together. The first pair of identical node addresses is the intersection; return its value. Return `-1` if the lists do not share a node.

### C++ Implementation:

The first example has `list1 = 10 -> 15 -> 30` and `list2 = 3 -> 6 -> 9 -> 15 -> 30`. Their lengths are 3 and 5, so the longer list advances by 2 nodes (`3` and `6`). The first aligned comparison is `9` against `10`; the next pointers are both the shared node containing `15`.

```cpp
#include <cassert>
#include <iostream>

class Node {
public:
    int data;
    Node* next;

    explicit Node(int value, Node* nextNode = nullptr)
        : data(value), next(nextNode) {}
};

int getCount(Node* head) {
    int count = 0;
    Node* current = head;
    while (current != nullptr) {
        count++;
        current = current->next;
    }
    return count;
}

int findIntersection(int diff, Node* longer, Node* shorter) {
    Node* currentLonger = longer;
    Node* currentShorter = shorter;

    for (int i = 0; i < diff; i++) {
        if (currentLonger == nullptr) {
            return -1;
        }
        currentLonger = currentLonger->next;
    }

    while (currentLonger != nullptr && currentShorter != nullptr) {
        if (currentLonger == currentShorter) {
            return currentLonger->data;
        }
        currentLonger = currentLonger->next;
        currentShorter = currentShorter->next;
    }

    return -1;
}

int getIntersectionNode(Node* head1, Node* head2) {
    const int count1 = getCount(head1);
    const int count2 = getCount(head2);

    if (count1 > count2) {
        return findIntersection(count1 - count2, head1, head2);
    }
    return findIntersection(count2 - count1, head2, head1);
}

int main() {
    // The two lists share the same Node objects starting at the node with value 15.
    Node sharedTail(30);
    Node sharedNode(15, &sharedTail);
    Node list1(10, &sharedNode);
    Node list2Third(9, &sharedNode);
    Node list2Second(6, &list2Third);
    Node list2(3, &list2Second);

    assert(getCount(&list1) == 3);
    assert(getCount(&list2) == 5);
    assert(getIntersectionNode(&list1, &list2) == 15);
    std::cout << "The intersection point is " << getIntersectionNode(&list1, &list2) << '\n';

    // Equal values do not mean the lists intersect when their nodes are distinct.
    Node disjointList1Tail(30);
    Node disjointList1(15, &disjointList1Tail);
    Node disjointList2(15);
    assert(getIntersectionNode(&disjointList1, &disjointList2) == -1);
    std::cout << "The intersection point for lists without a shared node is "
              << getIntersectionNode(&disjointList1, &disjointList2) << '\n';

    return 0;
}
```

### Example and boundary case

For the shared-node example, the lists are:

```text
List 1: 10 -> 15 -> 30 -> NULL
List 2: 3 -> 6 -> 9 -> 15 -> 30 -> NULL
```

The lengths are 3 and 5. Advancing the longer list by 2 nodes aligns the remaining nodes; after comparing `9` with `10`, both pointers reach the same node containing `15`.

The boundary case uses two separate nodes that both contain `15`:

```text
List 1: 15 -> 30 -> NULL
List 2: 15 -> NULL
```

Because the lists share no node address, the result is `-1` even though their first nodes have equal values.

Expected output:

```text
The intersection point is 15
The intersection point for lists without a shared node is -1
```

### Complexity

- Time: `O(m + n)`, where `m` and `n` are the list lengths.
- Extra space: `O(1)`.

### Applications

- Linked-list algorithms: finding a shared tail is a common pointer-manipulation operation.
- Networking: identifying shared routes or path segments.
- Geometry: detecting paths that converge on the same represented object.
