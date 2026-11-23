---
id: javadfs
title: Depth-First Search (DFS) Using Java
sidebar_label: Depth-First Search (DFS) Using Java
description: "In this blog post, we'll explore Depth-First Search (DFS) using Java, a graph traversal algorithm used to explore vertices and edges by going as deep as possible before backtracking."
tags: [dsa, algorithms, graph, traversal]
---

### Definition:

Depth-First Search (DFS) is a graph traversal algorithm used to explore vertices and edges in a depthward motion, meaning it goes as deep as possible into a graph before backtracking. DFS starts from a source node and follows paths until there are no unvisited nodes left in that path. Once it reaches a dead-end (i.e., no more unvisited neighbors), it backtracks to explore other paths. It is widely applied in graph-related problems like pathfinding, cycle detection, and solving mazes.

### Video Explanation

<LiteYouTubeEmbed
  id="Qzf1a--rhp8"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="G-6. Depth-First Search (DFS) | C++ and Java | Traversal Technique in Graphs"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Recursive or Stack-Based Traversal**:
  - DFS can be implemented recursively using a function call stack or iteratively using an explicit stack. At each node, it marks the node as visited and explores all its unvisited neighbors before backtracking.

- **Preorder Traversal**:
  - DFS visits a node before its neighbors, which can resemble preorder traversal in trees. This makes it useful in applications such as topological sorting or checking the existence of cycles in directed graphs.

- **Backtracking**:
  - DFS naturally involves backtracking. After fully exploring all paths from the current node, DFS backtracks to previously visited nodes to explore any remaining unvisited neighbors.

### Traversal Mechanics and Invariants:

Understanding how recursive DFS operates requires examining two core mechanisms: adjacency list traversal order and cycle prevention via the `visited` array.

#### 1. Adjacency List Exploration and Traversal Order

In an adjacency list representation `List<List<Integer>> adjList`, each vertex index stores a list of its outgoing or adjacent neighbors. When DFS visits vertex $u$:
1. Vertex $u$ is marked as visited immediately upon entry (`visited[u] = true`).
2. DFS iterates through `adjList.get(u)` in insertion order.
3. For each neighbor $v$ of $u$, if $v$ has not yet been visited (`!visited[v]`), DFS suspends the current loop at $u$, places a new activation frame on the call stack, and immediately begins exploring from $v$.
4. Only when the entire subgraph reachable from $v$ has been exhausted does the execution return to $u$, which then resumes iterating through its remaining neighbors.

Because DFS prioritizes depth over breadth, it travels along a branch until reaching a node whose neighbors are all already visited (a dead end) before backtracking.

#### 2. Role of the `visited` Array in Cycle Prevention

In undirected graphs (or directed graphs containing cycles), an edge between vertex $u$ and vertex $v$ exists in both `adjList.get(u)` and `adjList.get(v)`. Without tracking visited vertices:
- Visiting vertex 0 triggers a recursive call to its neighbor 1.
- Vertex 1 examines its neighbors and finds vertex 0.
- Vertex 1 would recursively invoke `dfs(0)`, which in turn calls `dfs(1)`, creating an infinite recursion cycle that quickly terminates with a `java.lang.StackOverflowError`.

The boolean array `visited` of size $V$ maintains the invariant that each vertex enters the recursion stack at most once. The guard condition:
```java
if (!visited[neighbor]) {
    dfs(neighbor, adjList, visited);
}
```
ensures that previously visited vertices are skipped in $O(1)$ time, guaranteeing both termination and linear time complexity.

### Step-by-Step State Walkthrough:

Consider the worked example graph with $V = 5$ vertices ($0, 1, 2, 3, 4$) and undirected edges $(0, 1), (0, 2), (1, 3), (1, 4)$.

The adjacency list representation is:
- **Node 0**: `[1, 2]`
- **Node 1**: `[0, 3, 4]`
- **Node 2**: `[0]`
- **Node 3**: `[1]`
- **Node 4**: `[1]`

Starting the traversal from **Node 0** produces the following trace:

| Step | Call Stack | Current Node | Action / Neighbor Inspected | Visited Array `[0, 1, 2, 3, 4]` | Printed Output |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `[dfs(0)]` | 0 | Mark 0 visited; inspect neighbor 1 (unvisited). | `[T, F, F, F, F]` | `0` |
| 2 | `[dfs(0), dfs(1)]` | 1 | Mark 1 visited; inspect neighbor 0 (`visited[0] == true`, skip). | `[T, T, F, F, F]` | `0 1` |
| 3 | `[dfs(0), dfs(1)]` | 1 | Inspect neighbor 3 (unvisited). Recurse into `dfs(3)`. | `[T, T, F, F, F]` | `0 1` |
| 4 | `[dfs(0), dfs(1), dfs(3)]` | 3 | Mark 3 visited; inspect neighbor 1 (`visited[1] == true`, skip). All neighbors examined; backtrack to `dfs(1)`. | `[T, T, F, T, F]` | `0 1 3` |
| 5 | `[dfs(0), dfs(1)]` | 1 | Resume at 1; inspect neighbor 4 (unvisited). Recurse into `dfs(4)`. | `[T, T, F, T, F]` | `0 1 3` |
| 6 | `[dfs(0), dfs(1), dfs(4)]` | 4 | Mark 4 visited; inspect neighbor 1 (`visited[1] == true`, skip). All neighbors examined; backtrack to `dfs(1)`. | `[T, T, F, T, T]` | `0 1 3 4` |
| 7 | `[dfs(0), dfs(1)]` | 1 | All neighbors of 1 (`[0, 3, 4]`) examined; backtrack to `dfs(0)`. | `[T, T, F, T, T]` | `0 1 3 4` |
| 8 | `[dfs(0)]` | 0 | Resume at 0; inspect next neighbor 2 (unvisited). Recurse into `dfs(2)`. | `[T, T, F, T, T]` | `0 1 3 4` |
| 9 | `[dfs(0), dfs(2)]` | 2 | Mark 2 visited; inspect neighbor 0 (`visited[0] == true`, skip). All neighbors examined; backtrack to `dfs(0)`. | `[T, T, T, T, T]` | `0 1 3 4 2` |
| 10 | `[dfs(0)]` | 0 | All neighbors of 0 (`[1, 2]`) examined; traversal complete. | `[T, T, T, T, T]` | `0 1 3 4 2` |

Final traversal order: `0 -> 1 -> 3 -> 4 -> 2`.

### Time Complexity:

- **Best, Average, and Worst Case: $O(V + E)$**
Here, $V$ represents the number of vertices, and $E$ represents the number of edges. The algorithm visits each vertex and examines each edge exactly once (or twice in an undirected graph) because the `visited` array prevents redundant recursive calls.

### Space Complexity:

- **Space Complexity: $O(V)$**  
  In the worst case (such as a skewed or linear chain graph), the recursion call stack can reach depth $V$. In addition, the boolean `visited` array requires $O(V)$ auxiliary space.

### Java Implementation:

```java
import java.util.*;

public class DepthFirstSearch {
    
    // Function to perform DFS traversal
    public static void dfs(int node, List<List<Integer>> adjList, boolean[] visited) {
        visited[node] = true;
        System.out.print(node + " ");

        for (int neighbor : adjList.get(node)) {
            if (!visited[neighbor]) {
                dfs(neighbor, adjList, visited);
            }
        }
    }

    public static void main(String[] args) {
        // Worked Example: 5-node connected graph
        int n = 5;  // number of nodes
        List<List<Integer>> adjList = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adjList.add(new ArrayList<>());
        }

        // Adding edges to the adjacency list
        adjList.get(0).add(1);
        adjList.get(0).add(2);
        adjList.get(1).add(0);
        adjList.get(1).add(3);
        adjList.get(1).add(4);
        adjList.get(2).add(0);
        adjList.get(3).add(1);
        adjList.get(4).add(1);

        // Mark all vertices as unvisited
        boolean[] visited = new boolean[n];
        int startNode = 0;
        
        System.out.println("DFS traversal starting from node " + startNode + ": ");
        dfs(startNode, adjList, visited);
        System.out.println();

        // Boundary Example: Single isolated node graph (n = 1, no edges)
        int nBoundary = 1;
        List<List<Integer>> boundaryAdjList = new ArrayList<>();
        boundaryAdjList.add(new ArrayList<>());
        boolean[] boundaryVisited = new boolean[nBoundary];
        int boundaryStartNode = 0;

        System.out.println("DFS traversal for single-node boundary graph starting from node " + boundaryStartNode + ": ");
        dfs(boundaryStartNode, boundaryAdjList, boundaryVisited);
        System.out.println();
    }
}
```

### Example Output:

```text
DFS traversal starting from node 0:
0 1 3 4 2
DFS traversal for single-node boundary graph starting from node 0:
0
```

### Boundary Considerations:

- **Single-Node Graph ($V = 1$, $E = 0$)**: When a graph contains only a single vertex with no edges, the adjacency list is empty (`[]`). DFS visits and prints the vertex, encounters an empty neighbor loop, and cleanly terminates without making recursive calls or causing index errors.
- **Disconnected Components**: If a graph has disconnected components, calling `dfs(startNode)` will only visit vertices in the connected component containing `startNode`. To traverse the entire disconnected graph, an outer loop iterating over all vertices $i \in [0, V - 1]$ invoking `dfs(i)` whenever `!visited[i]` is required.
