# ==========================================
# LEVEL 1: Shortest Remaining Time First
# ==========================================
def student_level_1_cpu(processes):
    """
    Selects the process with the minimum remaining work.
    This mathematically guarantees the lowest average completion time (SJF/SRTF).
    """
    if not processes:
        return None
    return min(processes, key=processes.get)


# ==========================================
# LEVEL 2: Greedy Knapsack Allocation
# ==========================================
def student_level_2_static(available_resources, waiting_processes):
    """
    Sorts processes by their required work time (ascending).
    Approves as many as possible that fit in the current available resources.
    """
    approved = []
    current_avail = available_resources.copy()
    
    # Sort by work time (x[1][1] is total_work)
    sorted_processes = sorted(waiting_processes.items(), key=lambda x: x[1][1])
    
    for pid, (req, _) in sorted_processes:
        # Check if we have enough of all 3 resources
        if all(req[i] <= current_avail[i] for i in range(3)):
            approved.append(pid)
            # Deduct to see if we can fit more processes in this tick
            for i in range(3):
                current_avail[i] -= req[i]
                
    return approved


# ==========================================
# LEVEL 3: Banker's Algorithm (Deadlock Avoidance)
# ==========================================
def student_level_3_dynamic(os_state, pending_requests):
    """
    Simulates granting the request, then verifies if the system 
    remains in a 'Safe State' using the Banker's Algorithm logic.
    """
    approved = []
    
    # Work with copies so we can simulate allocations
    avail = os_state.available_resources.copy()
    alloc = {pid: list(res) for pid, res in os_state.allocated.items()}
    
    def is_safe_state(test_avail, test_alloc):
        work = test_avail.copy()
        finish = {pid: False for pid in os_state.max_demand}
        
        while True:
            progress = False
            for pid in finish:
                if not finish[pid]:
                    # Calculate what this process still might need
                    need = [os_state.max_demand[pid][i] - test_alloc[pid][i] for i in range(3)]
                    
                    # If it can finish with the currently available 'work' pool
                    if all(need[i] <= work[i] for i in range(3)):
                        # Simulate process finishing and returning ALL its resources
                        for i in range(3):
                            work[i] += test_alloc[pid][i]
                        finish[pid] = True
                        progress = True
            
            # If we looped through all processes and none could finish, break
            if not progress:
                break
                
        # System is safe ONLY if all processes can theoretically finish
        return all(finish.values())

    # Try to approve pending requests one by one
    for pid, req in pending_requests.items():
        if all(req[i] <= avail[i] for i in range(3)):
            
            # 1. Simulate Allocation
            for i in range(3):
                avail[i] -= req[i]
                alloc[pid][i] += req[i]
                
            # 2. Check if the resulting state is Safe
            if is_safe_state(avail, alloc):
                approved.append(pid)
            else:
                # 3. Revert allocation if unsafe
                for i in range(3):
                    avail[i] += req[i]
                    alloc[pid][i] -= req[i]
                    
    return approved