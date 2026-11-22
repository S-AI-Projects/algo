---
id: uniform-cost-search  
sidebar_position: 4  
title: Uniform-Cost Search  
sidebar_label: Uniform-Cost  
---

### Definition:

**Uniform-Cost Search (UCS)** is a search algorithm that expands the node with the lowest cost first, ensuring that it finds the least-cost path in weighted graphs. UCS is similar to Dijkstra's algorithm but is often applied in AI and pathfinding scenarios.

UCS is optimal when every traversed edge has a non-negative cost. This is a precondition of the algorithm, not a universal rule that all other inputs are invalid. The example below uses non-negative edge costs. When the start is already the goal, the least-cost path is the empty path, so its cost is `0`.

### Video Explanation**
<LiteYouTubeEmbed
  id="dRMvK76xQJI"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Uniform Cost Search"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Lowest Cost Path**: Always expands the node with the lowest path cost.
- **Optimal**: Guarantees an optimal solution for paths with non-negative weights.
- **Uninformed**: Does not use heuristics and is a type of uninformed search.


### How Uniform-Cost Search Works:

1. **Initialize**: Start with the root node.
2. **Expand Node**: Choose the node with the lowest cumulative path cost.
3. **Add Neighbors**: Add unvisited neighbors with updated path costs.
4. **Repeat**: Continue until reaching the goal or emptying the priority queue.

### Time Complexity:

- **Time Complexity**: \(O(b^d)\) where `b` is the branching factor and `d` is the depth of the goal.

### Space Complexity:

- **Space Complexity**: \(O(b^d)\)

### Advantages of Uniform-Cost Search:

- **Optimal Path**: Finds the least-cost path for weighted graphs.
- **No Heuristic Needed**: Effective without heuristic guidance.

### Disadvantages of Uniform-Cost Search:

- **Inefficient for Large Graphs**: Can be slow for large search spaces.
- **High Memory Use**: Stores all frontier nodes in memory.

### Uniform-Cost Search Algorithm (Java Implementation):

In the worked graph, the direct route from node 1 to node 3 costs 8. UCS first explores node 2 at cost 2, then reaches node 3 for a total cost of 5. The boundary case starts and ends at node 1, so no edge is traversed.

```java
import java.util.*;

class GraphNode {
    final int id;
    final List<Edge> neighbors = new ArrayList<>();

    GraphNode(int id) {
        this.id = id;
    }

    void connectTo(GraphNode neighbor, int edgeCost) {
        neighbors.add(new Edge(neighbor, edgeCost));
    }
}

class Edge {
    final GraphNode to;
    final int cost;

    Edge(GraphNode to, int cost) {
        if (cost < 0) throw new IllegalArgumentException("UCS requires non-negative edge costs");
        this.to = to;
        this.cost = cost;
    }
}

class QueueEntry {
    final GraphNode node;
    final int cost;

    QueueEntry(GraphNode node, int cost) {
        this.node = node;
        this.cost = cost;
    }
}

class UniformCostSearch {
    public static int ucs(GraphNode start, GraphNode goal) {
        PriorityQueue<QueueEntry> pq = new PriorityQueue<>(Comparator.comparingInt(entry -> entry.cost));
        Map<GraphNode, Integer> bestCost = new HashMap<>();
        pq.add(new QueueEntry(start, 0));
        bestCost.put(start, 0);

        while (!pq.isEmpty()) {
            QueueEntry current = pq.poll();
            if (current.cost != bestCost.get(current.node)) continue;
            if (current.node == goal) return current.cost;

            for (Edge edge : current.node.neighbors) {
                int nextCost = current.cost + edge.cost;
                if (nextCost < bestCost.getOrDefault(edge.to, Integer.MAX_VALUE)) {
                    bestCost.put(edge.to, nextCost);
                    pq.add(new QueueEntry(edge.to, nextCost));
                }
            }
        }
        return -1; // Goal is unreachable from the start.
    }
}

class UniformCostSearchDemo {
    public static void main(String[] args) {
        GraphNode start = new GraphNode(1);
        GraphNode middle = new GraphNode(2);
        GraphNode goal = new GraphNode(3);

        start.connectTo(goal, 8);
        start.connectTo(middle, 2);
        middle.connectTo(goal, 3);

        System.out.println("Worked example cost: " + UniformCostSearch.ucs(start, goal));
        System.out.println("Start equals goal cost: " + UniformCostSearch.ucs(start, start));
    }
}
```
### Applications of Uniform-Cost Search:
Pathfinding in AI: Used for finding the shortest path in robotics.
Network Routing: Ensures the lowest cost route in weighted networks.
Resource Allocation: Finds optimal paths with resource constraints.
### Summary:
Uniform-Cost Search is optimal and complete for finding the lowest-cost path in weighted graphs, widely used in AI and networking.
