---
id: graph-coloring  
title: Graph Coloring Algorithm  
sidebar_label: Graph Coloring 
description: "In this blog post, we'll explore Graph Coloring, Graph coloring refers to the problem of coloring vertices of a graph in such a way that no two adjacent vertices have the same color. "  
tags: [dsa, algorithms, greedy algorithms,graphs]
---


### Definition:
Graph coloring is the process of assigning colors to the vertices of a graph such that no two adjacent vertices share the same color. The greedy algorithm for graph coloring assigns colors to vertices one by one, choosing the smallest available color at each step. While not always optimal, it offers an efficient solution for many graph coloring problems.

### Video Explanation

<LiteYouTubeEmbed
  id="052VkKhIaQ4"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="6.3 Graph Coloring Problem - Backtracking"
  lazyLoad={true}
  webp
/>

### Characteristics:
- **Greedy Approach**:  
  Graph coloring can be approached using a greedy algorithm. Vertices are colored one by one, assigning the smallest available color that doesn't violate the condition of adjacent vertices having the same color.

- **Non-Optimality**:  
   The greedy approach doesn’t always yield the minimum number of colors (chromatic number), but it provides a valid coloring in a time-efficient manner.

### Steps Involved:
1. **Sort Vertices by Degree**:  
    Optionally, vertices can be ordered by their degrees (highest degree first) to potentially improve the result.
   
2. **Assign Colors Greedily**:  
    Starting from the first vertex, assign the smallest available color that isn’t used by its adjacent vertices.
   
3. **Check and Color Remaining Vertices**:  
   Continue coloring each vertex using the same logic until all vertices are colored.

### Problem Statement:
 Given a graph with `n` vertices, assign colors to the vertices such that no two adjacent vertices share the same color, while using the fewest number of colors.

### Time Complexity:
- **Best, Average, and Worst Case: $O(n + m)$**  
  Where `n` is the number of vertices and `m` is the number of edges. This is dominated by traversing vertices and their adjacent edges

### Space Complexity:
- **Space Complexity: $O(n)$**  
  Space is required to store the colors assigned to each vertex.

### Example:
Consider the following Graph:
- Vertices: `{A, B, C, D}`
- Edges: `{(A, B), (A, C), (B, D), (C, D)}`

Step-by-Step Execution (vertices are processed in the order A, B, C, D):

| Vertex | Already-colored neighbors | Colors unavailable | Smallest available color |
| --- | --- | --- | --- |
| A | none | none | 1 |
| B | A (color 1) | 1 | 2 |
| C | A (color 1); B is not adjacent to C | 1 | 2 |
| D | B and C (both color 2) | 2 | 1 |

The C++ implementation stores colors as zero-based integers: color 1 is stored as `0`, and color 2 as `1`. For vertex D, both neighbors mark `available[1]`; `available[0]` remains false, so the loop selects `cr = 0`. The final stored vector is `[0, 1, 1, 0]`, which represents the table above and uses two colors. This greedy order gives a valid coloring for this graph; in general, greedy coloring does not guarantee the minimum number of colors.

The smallest valid boundary is one vertex and no edges (`V = 1`, adjacency list `[[]]`). The only vertex receives stored color `0` (display color 1), and no adjacency constraint is violated.






### C++ Implementation:
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

// Function to perform greedy graph coloring
vector<int> greedyGraphColoring(vector<vector<int>>& graph, int V) {
    // Array to store the color assigned to each vertex
    vector<int> result(V, -1);

    // Assign the first color to the first vertex
    result[0] = 0;

    // Temporary array to keep track of available colors for vertices
    vector<bool> available(V, false);

    // Assign colors to remaining vertices
    for (int u = 1; u < V; u++) {
        // Mark colors of adjacent vertices as unavailable
        for (int i = 0; i < graph[u].size(); i++) {
            int adjacent = graph[u][i];
            if (result[adjacent] != -1) {
                available[result[adjacent]] = true;
            }
        }

        // Find the first available color
        int cr;
        for (cr = 0; cr < V; cr++) {
            if (!available[cr]) {
                break;
            }
        }

        // Assign the found color to vertex u
        result[u] = cr;

        // Reset the available array for the next iteration
        for (int i = 0; i < graph[u].size(); i++) {
            int adjacent = graph[u][i];
            if (result[adjacent] != -1) {
                available[result[adjacent]] = false;
            }
        }
    }

    return result;
}

int main() {
    // Number of vertices
    int V = 4;

    // Adjacency list representing the graph
    vector<vector<int>> graph(V);

    // Define the edges of the graph
    graph[0].push_back(1); // Edge A-B
    graph[0].push_back(2); // Edge A-C
    graph[1].push_back(0); // Edge B-A
    graph[1].push_back(3); // Edge B-D
    graph[2].push_back(0); // Edge C-A
    graph[2].push_back(3); // Edge C-D
    graph[3].push_back(1); // Edge D-B
    graph[3].push_back(2); // Edge D-C

    // Call the greedy coloring function
    vector<int> result = greedyGraphColoring(graph, V);
    cout << "Vertex\tColor\n";
    for (int u = 0; u < V; u++) {
        cout << u << "\t" << result[u] << endl;
    }

    // Boundary case: a one-vertex graph needs its first available color only.
    vector<vector<int>> singleVertexGraph(1);
    vector<int> boundaryColors = greedyGraphColoring(singleVertexGraph, 1);
    assert(boundaryColors == vector<int>{0});
    cout << "Boundary (one vertex) stored color: " << boundaryColors[0] << endl;

    return 0;
}

```

### Java Implementation:
```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GraphColoring {

    // Function to perform greedy graph coloring
    public static void greedyGraphColoring(List<List<Integer>> graph, int V) {
        // Array to store the color assigned to each vertex
        int[] result = new int[V];
        Arrays.fill(result, -1);

        // Assign the first color to the first vertex
        result[0] = 0;

        // Temporary array to keep track of available colors for vertices
        boolean[] available = new boolean[V];

        // Assign colors to remaining vertices
        for (int u = 1; u < V; u++) {
            // Mark colors of adjacent vertices as unavailable
            for (int adjacent : graph.get(u)) {
                if (result[adjacent] != -1) {
                    available[result[adjacent]] = true;
                }
            }

            // Find the first available color
            int cr;
            for (cr = 0; cr < V; cr++) {
                if (!available[cr]) {
                    break;
                }
            }

            // Assign the found color to vertex u
            result[u] = cr;

            // Reset the available array for the next iteration
            for (int adjacent : graph.get(u)) {
                if (result[adjacent] != -1) {
                    available[result[adjacent]] = false;
                }
            }
        }

        // Print the result
        System.out.println("Vertex\tColor");
        for (int u = 0; u < V; u++) {
            System.out.println(u + "\t" + result[u]);
        }
    }

    public static void main(String[] args) {
        // Number of vertices
        int V = 4;

        // Adjacency list representing the graph
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < V; i++) {
            graph.add(new ArrayList<>());
        }

        // Define the edges of the graph
        graph.get(0).add(1); // Edge A-B
        graph.get(0).add(2); // Edge A-C
        graph.get(1).add(0); // Edge B-A
        graph.get(1).add(3); // Edge B-D
        graph.get(2).add(0); // Edge C-A
        graph.get(2).add(3); // Edge C-D
        graph.get(3).add(1); // Edge D-B
        graph.get(3).add(2); // Edge D-C

        // Call the greedy coloring function
        greedyGraphColoring(graph, V);
    }
}


```

### Summary:
Graph coloring is the process of assigning colors to vertices of a graph such that no two adjacent vertices share the same color. It has practical applications in areas like scheduling, register allocation, and map coloring. The problem is NP-complete, meaning there is no known efficient algorithm for finding the minimum number of colors. However, the greedy algorithm offers an approximation by assigning colors sequentially to each vertex while avoiding conflicts. Though it doesn't guarantee the minimum number of colors, it ensures an upper bound of `d+1` colors, where `d` is the maximum degree of any vertex in the graph.
