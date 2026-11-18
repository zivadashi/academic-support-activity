import heapq
from collections import deque

def find_shortest_path_bfs(graph, node_coords, start_node, end_node):
    """
    Level 1: BFS (Breadth-First Search).
    Ignores edge weights entirely. Finds a path with the fewest edges, 
    but it will fail the optimal cost check and visit many nodes.
    """
    queue = deque([start_node])
    parents = {start_node: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end_node:
            break
            
        for neighbor in graph[current]:
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
                
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)
        
    return path[::-1]

def find_shortest_path_dijkstra(graph, node_coords, start_node, end_node):
    """
    Level 2: Dijkstra's Algorithm.
    Respects edge weights and finds the mathematically optimal path.
    However, it expands blindly in all directions, causing the 
    'Nodes Visited' metric to be very high compared to A*.
    """
    queue = [(0, start_node)]
    distances = {start_node: 0}
    parents = {start_node: None}
    
    while queue:
        current_cost, current_node = heapq.heappop(queue)
        
        if current_node == end_node:
            break
            
        if current_cost > distances.get(current_node, float('inf')):
            continue
            
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                parents[neighbor] = current_node
                heapq.heappush(queue, (new_cost, neighbor))
                
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)
        
    return path[::-1]

def heuristic(node1, node2, node_coords):
    """
    Calculates the Manhattan distance between two nodes.
    Multiplied by a constant to approximate edge weights and prioritize direction.
    """
    x1, y1 = node_coords[node1]
    x2, y2 = node_coords[node2]
    # Average weight is roughly 8, so scaling the distance helps A* be more aggressive
    return (abs(x1 - x2) + abs(y1 - y2)) * 5 

def find_shortest_path(graph, node_coords, start_node, end_node):
    """
    Optimized A* Search algorithm.
    """
    # Priority queue stores tuples of: (estimated_total_cost, current_cost, node)
    queue = [(0, 0, start_node)]
    distances = {start_node: 0}
    parents = {start_node: None}
    visited_count = 0
    
    while queue:
        _, current_cost, current_node = heapq.heappop(queue)
        visited_count += 1
        
        if current_node == end_node:
            break
            
        # Ignore outdated queue entries
        if current_cost > distances.get(current_node, float('inf')):
            continue
            
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                parents[neighbor] = current_node
                
                # A* Priority = actual cost so far + estimated cost to target
                priority = new_cost + heuristic(neighbor, end_node, node_coords)
                heapq.heappush(queue, (priority, new_cost, neighbor))
                
    # Reconstruct the path backwards
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)
        
    return path[::-1] # Reverse to get start -> end