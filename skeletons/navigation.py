import random
import time
import heapq

def find_shortest_path(graph, start_node, end_node):
    """
    Finds a valid path from start_node to end_node in the given graph.
    Goal: Optimize execution time while returning a valid route.
    
    Args:
        graph: A dictionary of dictionaries representing the adjacency list. 
               Example: graph['5th_Ave_42nd_St']['5th_Ave_43rd_St'] = weight
        start_node: The starting node identifier.
        end_node: The target node identifier.
        
    Returns:
        list: A list of nodes representing the path from start_node to end_node.
    """
    path = []
    
    # ==========================================
    # write your code here
    # ==========================================
    
    return path


def load_nyc_manhattan_map(avenues=12, streets=150):
    """
    Generates a realistic grid graph simulating Manhattan, NYC.
    Avenues run North/South, Streets run East/West.
    """
    graph = {}
    nodes = []
    
    # Generate intersections
    for a in range(1, avenues + 1):
        for s in range(1, streets + 1):
            node = f"{a}th_Ave_{s}th_St"
            nodes.append(node)
            graph[node] = {}

    # Add edges with randomized "traffic" weights
    # Fixed seed to simulate a consistent city map across runs
    random.seed(42) 
    for a in range(1, avenues + 1):
        for s in range(1, streets + 1):
            node = f"{a}th_Ave_{s}th_St"
            
            # North/South along Avenues (shorter physical blocks, usually faster)
            if s < streets:
                neighbor = f"{a}th_Ave_{s+1}th_St"
                weight = random.randint(2, 6)
                graph[node][neighbor] = weight
                graph[neighbor][node] = weight
                
            # East/West along Streets (longer physical blocks, slower to cross)
            if a < avenues:
                neighbor = f"{a+1}th_Ave_{s}th_St"
                weight = random.randint(6, 15)
                graph[node][neighbor] = weight
                graph[neighbor][node] = weight
                
    # Reset seed so routing requests remain randomized
    random.seed() 
    return graph, nodes


def run_navigation_simulation():
    print("Loading Manhattan, NYC map (1,800 intersections)...")
    graph, nodes = load_nyc_manhattan_map(avenues=12, streets=150)
    
    tests = 100
    successes = 0
    total_time = 0.0
    
    print(f"Running {tests} navigation tests to evaluate algorithm performance...")
    print("Focus on reducing the average execution time per valid route!\n")
    
    for _ in range(tests):
        start, end = random.sample(nodes, 2)
        
        start_time = time.perf_counter()
        try:
            path = find_shortest_path(graph, start, end)
        except Exception as e:
            print(f"Algorithm error: {e}")
            continue
        end_time = time.perf_counter()
        
        # Validate path existence and boundaries
        if not path:
            print(f"Failed: Empty path returned ({start} to {end})")
            continue
            
        if path[0] != start or path[-1] != end:
            print(f"Failed: Path does not start/end correctly ({start} to {end})")
            continue
            
        # Ensure path is continuous and valid in the graph
        valid_path = True
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            if v not in graph[u]:
                print(f"Failed: Invalid edge in path from {u} to {v}")
                valid_path = False
                break
            
        if not valid_path:
            continue
            
        successes += 1
        total_time += (end_time - start_time)
            
    print(f"Results: {successes}/{tests} valid paths generated.")
    
    if successes > 0:
        avg_time = total_time / successes
        print(f"Average execution time per valid route: {avg_time:.6f} seconds")
        
        if successes == tests:
            print("Status: PASSED. Now try to optimize your algorithm to lower the time!")
        else:
            print("Status: FAILED. Review algorithm edge cases.")

if __name__ == "__main__":
    run_navigation_simulation()