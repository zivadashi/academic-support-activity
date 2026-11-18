import random
import time
import heapq


def find_shortest_path(graph, node_coords, start_node, end_node):
    """
    Finds a valid path from start_node to end_node in the given graph.
    
    Goal: 
    Optimize your algorithm to reduce BOTH the execution time and the 
    number of nodes visited, while keeping the overall route cost low.
    
    Args:
        graph: A dictionary of dictionaries representing the adjacency list. 
               Example: graph['Ave_5_St_42']['Ave_5_St_43'] = weight
        node_coords: A dictionary mapping node names to their (X, Y) coordinates.
                     Example: node_coords['Ave_5_St_42'] = (5, 42)
                     Hint: Use these to calculate distances for an A* heuristic!
        start_node: The starting node identifier.
        end_node: The target node identifier.
        
    Returns:
        list: A list of nodes representing the path from start_node to end_node.
    """
    path = []
        
    return path


class TrackedGraph(dict):
    """
    A dictionary wrapper that silently tracks how many unique nodes 
    the algorithm accesses (expands) during its execution.
    """
    def __init__(self, mapping=(), **kwargs):
        super().__init__(mapping, **kwargs)
        self.expanded_nodes = set()
        
    def __getitem__(self, key):
        self.expanded_nodes.add(key)
        return super().__getitem__(key)
        
    def reset_tracking(self):
        self.expanded_nodes.clear()
        
    def get_visited_count(self):
        return len(self.expanded_nodes)


def load_nyc_manhattan_map(avenues=12, streets=150):
    """
    Generates a realistic grid graph simulating Manhattan, NYC.
    """
    raw_graph = {}
    node_coords = {}
    nodes = []
    
    for a in range(1, avenues + 1):
        for s in range(1, streets + 1):
            node = f"Ave_{a}_St_{s}"
            nodes.append(node)
            raw_graph[node] = {}
            node_coords[node] = (a, s)

    random.seed(42) 
    for a in range(1, avenues + 1):
        for s in range(1, streets + 1):
            node = f"Ave_{a}_St_{s}"
            
            if s < streets:
                neighbor = f"Ave_{a}_St_{s+1}"
                weight = random.randint(2, 6)
                raw_graph[node][neighbor] = weight
                raw_graph[neighbor][node] = weight
                
            if a < avenues:
                neighbor = f"Ave_{a+1}_St_{s}"
                weight = random.randint(6, 15)
                raw_graph[node][neighbor] = weight
                raw_graph[neighbor][node] = weight
                
    random.seed() 
    return raw_graph, node_coords, nodes


def run_navigation_simulation():
    print("Loading Manhattan, NYC map (1,800 intersections)...")
    raw_graph, node_coords, nodes = load_nyc_manhattan_map(avenues=12, streets=150)
    
    # Wrap the raw dictionary in our invisible tracking class
    tracked_graph = TrackedGraph(raw_graph)
    
    tests = 100
    successes = 0
    total_time = 0.0
    total_visited = 0
    total_path_cost = 0
    
    print(f"Running {tests} navigation tests to evaluate algorithm performance...")
    print("Focus on reducing execution time and nodes visited!\n")
    
    for _ in range(tests):
        start, end = random.sample(nodes, 2)
        
        tracked_graph.reset_tracking()
        start_time = time.perf_counter()
        
        try:
            path = find_shortest_path(tracked_graph, node_coords, start, end)
        except Exception as e:
            print(f"Algorithm error: {e}")
            continue
            
        end_time = time.perf_counter()
        
        # Pull the metric directly from our wrapper
        nodes_expanded = tracked_graph.get_visited_count()
        
        if not path:
            print(f"Failed: Empty path returned ({start} to {end})")
            continue
            
        if path[0] != start or path[-1] != end:
            print(f"Failed: Path does not start/end correctly ({start} to {end})")
            continue
            
        valid_path = True
        current_path_cost = 0
        
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            if v not in raw_graph[u]:
                print(f"Failed: Invalid edge in path from {u} to {v}")
                valid_path = False
                break
            current_path_cost += raw_graph[u][v]
            
        if not valid_path:
            continue
            
        successes += 1
        total_time += (end_time - start_time)
        total_visited += nodes_expanded
        total_path_cost += current_path_cost
            
    print(f"Results: {successes}/{tests} valid paths generated.\n")
    
    if successes > 0:
        avg_time = total_time / successes
        avg_visited = total_visited / successes
        avg_cost = total_path_cost / successes
        
        print("=== PERFORMANCE METRICS ===")
        print(f"Average Execution Time: {avg_time:.6f} seconds")
        print(f"Average Nodes Visited:  {avg_visited:.1f} nodes per route")
        print(f"Average Route Cost:     {avg_cost:.1f} traffic weight")
        print("===========================\n")
        
        if successes == tests:
            print("Status: PASSED.")
            print("Next steps:")
            print("1. Are you visiting hundreds of nodes? Try implementing A*.")
            print("2. Ensure your optimizations don't accidentally increase the 'Route Cost'!")
        else:
            print("Status: FAILED. Review algorithm edge cases.")

if __name__ == "__main__":
    run_navigation_simulation()