---
id: graph-reversal 
title: Graph-reversal
sidebar_label: Graph-reversal 
description: "Reverse a directed graph so that the incoming edges will be converted to outgoing edges betwwen the same nodes."  
tags: [dsa, algorithms, graph]
---

### Problem Statement:
Suppose we have a directed graph, we have to find its reverse so if an edge goes from i to j, it now goes from j to i. Here input will be an adjacency list, and if there are n nodes, the nodes will be (0, 1, ..., n-1).

<AdsComponent />

### Approach:
The approach to transposing a directed graph involves creating a new structure to hold reversed edges. For each vertex, the algorithm iterates through its outgoing edges and appends the vertex to the list of the target vertex in the new structure. This efficiently constructs the transposed graph in linear time relative to the number of vertices and edges.

### Algorithm Steps:

1. **Initialize Result Structure**:
   - Create a list (or vector) `ans` of empty lists, with a size equal to the number of vertices in the graph.

2. **Iterate Over Each Vertex**:
   - For each vertex `i` in the graph:
     - Retrieve the list of vertices that `i` points to (i.e., its outgoing edges).

3. **Reverse Edges**:
   - For each vertex `x` in the outgoing edges of vertex `i`:
     - Append vertex `i` to the list at index `x` in `ans`. This step captures the transposition of the edge from `x` to `i`.

4. **Return Transposed Graph**:
   - Return the `ans` list, which now represents the transposed graph.

These steps succinctly outline the algorithm's approach to transforming the directed graph into its transpose.
### Time Complexity:
- The time complexity of the program is `O(V + E)`, where `V` is the number of vertices and `E` is the number of edges, as it processes each vertex and edge once.

### Sample Input:

```
    {{1, 2}, {4}, {4}, {1, 2}, {3}}
```
### Sample Output:

```
    [[], [0, 3], [0, 3], [4], [1, 2]]
```

<AdsComponent />

### Explanation of Sample:

- The input `graph = [[1,2],[4],[4],[1,2],[3]]` represents a directed graph as an adjacency list where:
  
    - Node 0 points to nodes 1 and 2.
    - Node 1 points to node 4.
    - Node 2 points to node 4.
    - Node 3 points to nodes 1 and 2.
    - Node 4 points to node 3.

- The reversed graph representation is `ans = [[], [0, 3], [0, 3], [4], [1, 2]]`, which means:
  
    - Node 0 has no outgoing edges.
    - Nodes 1 and 2 have outgoing edges to nodes 0 and 3.
    - Node 3 has an outgoing edge to node 4.
    - Node 4 has outgoing edges to nodes 1 and 2.

### Diagrammatic Representation of the input:
![directed_graph](https://github.com/user-attachments/assets/b3a8fc46-e508-45a0-bf97-458c2054f085)

### Diagrammatic Representation of the output:
![directed_graph1](https://github.com/user-attachments/assets/7cb03236-3f1a-49cc-b2ce-6ef73aac7fa4)

<AdsComponent />

### C++ Implementation:

```cpp
#include <iostream>
#include <vector>

using namespace std;

class Solution {
public:
    vector<vector<int>> solve(const vector<vector<int>>& graph) {
        const int vertexCount = static_cast<int>(graph.size());
        vector<vector<int>> reversedGraph(vertexCount);

        // Flip each directed edge (sourceVertex -> targetVertex) into (targetVertex -> sourceVertex)
        for (int sourceVertex = 0; sourceVertex < vertexCount; ++sourceVertex) {
            for (int targetVertex : graph[sourceVertex]) {
                reversedGraph[targetVertex].push_back(sourceVertex);
            }
        }
        return reversedGraph;
    }
};

void printAdjacencyList(const vector<vector<int>>& adj) {
    for (const auto& neighbors : adj) {
        cout << "[ ";
        for (int vertex : neighbors) {
            cout << vertex << " ";
        }
        cout << "]" << endl;
    }
}

int main() {
    Solution ob;

    // Worked example from Sample Input (5 vertices: 0..4)
    vector<vector<int>> graph = {{1, 2}, {4}, {4}, {1, 2}, {3}};
    vector<vector<int>> result = ob.solve(graph);
    cout << "Worked example (5 nodes):" << endl;
    printAdjacencyList(result);

    // Boundary example: smallest non-empty graph (n = 1, single isolated node 0)
    vector<vector<int>> singleNodeGraph = {{}};
    vector<vector<int>> singleNodeResult = ob.solve(singleNodeGraph);
    cout << "Boundary example (1 isolated node):" << endl;
    printAdjacencyList(singleNodeResult);

    return 0;
}
```

### Intermediate States & Boundary Case

- **Refactored Edge-Reversal Operation:** Naming the outer index `sourceVertex` and inner neighbor `targetVertex` makes it explicit that an outgoing edge `sourceVertex -> targetVertex` in `graph` becomes `targetVertex -> sourceVertex` via `reversedGraph[targetVertex].push_back(sourceVertex)`.
- **Exact Intermediate States on `{{1, 2}, {4}, {4}, {1, 2}, {3}}`:**
  - Initialized `reversedGraph` (`n = 5`): `[[], [], [], [], []]`
  - After `sourceVertex = 0` (edges `0->1, 0->2`): `[[], [0], [0], [], []]`
  - After `sourceVertex = 1` (edge `1->4`): `[[], [0], [0], [], [1]]`
  - After `sourceVertex = 2` (edge `2->4`): `[[], [0], [0], [], [1, 2]]`
  - After `sourceVertex = 3` (edges `3->1, 3->2`): `[[], [0, 3], [0, 3], [], [1, 2]]`
  - After `sourceVertex = 4` (edge `4->3`): `[[], [0, 3], [0, 3], [4], [1, 2]]`
- **Boundary Case (`n = 1` isolated vertex `{{}}`):** Consistent with the `0..n-1` vertex contract, a 1-node graph with no outgoing edges executes the outer loop once and the inner neighbor loop zero times, returning `[[]]`.

### Example Output

```plaintext
Worked example (5 nodes):
[ ]
[ 0 3 ]
[ 0 3 ]
[ 4 ]
[ 1 2 ]
Boundary example (1 isolated node):
[ ]
```
