import random

# Change this to 1, 2, or 3 to test different levels
CURRENT_LEVEL = 1

# ==============================================================================
# LEVEL 1: Single CPU Scheduling
# ==============================================================================
def student_level_1_cpu(processes):
    """
    Level 1: You have 1 CPU. Processes only need the CPU and their total 
    run time is known ahead of time. No deadlocks are possible.
    
    Goal: Minimize the AVERAGE completion time of all processes.
    
    Args:
        processes: A dictionary of {process_id: work_remaining}
                   Example: {"P1": 15, "P2": 3}
                   
    Returns:
        str: The process_id of the process that should run this tick.
    """
    
    # ==========================================
    # write your level 1 code here
    # ==========================================
    
    # Placeholder: just picks a random process
    return list(processes.keys())[0] if processes else None


# ==============================================================================
# LEVEL 2: Static Resource Allocation
# ==============================================================================
def student_level_2_static(available_resources, waiting_processes):
    """
    Level 2: You have 3 resources (CPU, RAM, Disk). Processes need a combination 
    of them to run. They request everything they need upfront and hold it 
    until they finish.
    
    Goal: Maximize resource utilization to finish ALL processes in the 
    shortest total time possible (minimize total simulation ticks).
    
    Args:
        available_resources: List of available resources [CPU, RAM, Disk]
        waiting_processes: Dict of processes waiting to start.
                           Format: { process_id: (required_resources, total_work) }
                           Example: {"P1": ([2, 1, 1], 15)}
                           
    Returns:
        list: A list of process_ids that should be allocated resources and started.
    """
    approved = []
    
    # ==========================================
    # write your level 2 code here
    # ==========================================
    
    return approved


# ==============================================================================
# LEVEL 3: Dynamic Deadlock Avoidance
# ==============================================================================
class OperatingSystem:
    def __init__(self, total_resources):
        self.total_resources = total_resources
        self.available_resources = total_resources.copy()
        self.max_demand = {}
        self.allocated = {}

def student_level_3_dynamic(os_state, pending_requests):
    """
    Level 3: Processes start with 0 resources and dynamically request more 
    over time up to their max_demand. If you are not careful, circular 
    waiting will occur and the system will DEADLOCK.
    
    Goal: Approve as many requests as safely possible to minimize total 
    execution time without crashing the system.
    
    Args:
        os_state: Contains available_resources, max_demand, and allocated.
        pending_requests: { process_id: [req_CPU, req_RAM, req_Disk] }
        
    Returns:
        list: A list of process_ids whose requests are approved this tick.
    """
    approved = []
    
    # ==========================================
    # write your level 3 Banker's algorithm here
    # ==========================================
    
    return approved


# ==============================================================================
# SIMULATION TESTERS (Pre-implemented)
# ==============================================================================

def run_level_1():
    print("--- LEVEL 1: Single CPU Scheduling ---")
    random.seed(42)
    processes = {f"P{i}": random.randint(5, 20) for i in range(1, 11)}
    random.seed()
    
    # Calculate the TRUE optimal score (SJF) dynamically
    burst_times = sorted(processes.values())
    optimal_sum = 0
    current_time = 0
    for burst in burst_times:
        current_time += burst
        optimal_sum += current_time
    true_optimal_avg = optimal_sum / len(burst_times)
    
    timestamp = 0
    completion_times = {}
    
    while processes:
        timestamp += 1
        
        try:
            pid_to_run = student_level_1_cpu(processes.copy())
        except Exception as e:
            print(f"[Tick {timestamp}] Algorithm error: {e}")
            return
            
        if pid_to_run not in processes:
            print(f"[Tick {timestamp}] Invalid process_id '{pid_to_run}' returned.")
            return
            
        processes[pid_to_run] -= 1
        if processes[pid_to_run] <= 0:
            completion_times[pid_to_run] = timestamp
            del processes[pid_to_run]
            
    avg_time = sum(completion_times.values()) / len(completion_times)
    print("Status: PASSED. All processes completed.")
    print(f"Score (Average Completion Time): {avg_time:.2f} ticks.")
    
    if avg_time <= true_optimal_avg:
        print(f"Incredible! You hit the mathematical optimum of {true_optimal_avg:.2f} ticks.")
    else:
        print(f"Hint: The optimal average for this workload is {true_optimal_avg:.2f} ticks. Try Shortest Remaining Time First (SRTF)!")


def run_level_2():
    print("--- LEVEL 2: Static Resource Allocation ---")
    total_resources = [10, 10, 10]
    available_resources = total_resources.copy()
    
    random.seed(42)
    waiting_processes = {}
    for i in range(1, 16):
        req = [random.randint(1, 6) for _ in range(3)]
        work = random.randint(5, 25)
        waiting_processes[f"P{i}"] = (req, work)
    random.seed()
    
    active_processes = {} 
    timestamp = 0
    
    while waiting_processes or active_processes:
        timestamp += 1
        
        if waiting_processes:
            try:
                approved = student_level_2_static(available_resources.copy(), waiting_processes.copy())
            except Exception as e:
                print(f"[Tick {timestamp}] Algorithm error: {e}")
                return
                
            for pid in approved:
                if pid not in waiting_processes:
                    continue
                req, work = waiting_processes[pid]
                
                if any(req[i] > available_resources[i] for i in range(3)):
                    print(f"\n[Tick {timestamp}] FATAL: Approved {pid} but resources exceeded!")
                    print(f"Available: {available_resources}, Requested: {req}")
                    return
                    
                for i in range(3):
                    available_resources[i] -= req[i]
                    
                active_processes[pid] = [req, work]
                del waiting_processes[pid]
                
        # Execute 1 tick of work for all active processes
        completed = []
        for pid, data in active_processes.items():
            data[1] -= 1
            if data[1] <= 0:
                completed.append(pid)
                
        # Release resources
        for pid in completed:
            req = active_processes[pid][0]
            for i in range(3):
                available_resources[i] += req[i]
            del active_processes[pid]
            
    print("Status: PASSED. All processes completed without exceeding bounds.")
    print(f"Score (Total Time): {timestamp} ticks.")
    print("Hint: Try to implement a greedy Knapsack-like heuristic to pack resources tightly!")


def run_level_3():
    print("--- LEVEL 3: Dynamic Deadlock Avoidance ---")
    total_resources = [15, 12, 10]
    os_state = OperatingSystem(total_resources)
    
    random.seed(42)
    class ProcState: pass
    processes = {}
    
    for i in range(1, 9):
        pid = f"P{i}"
        p = ProcState()
        p.pid = pid
        p.max_demand = [random.randint(2, r) for r in total_resources]
        p.allocated = [0, 0, 0]
        p.work_remaining = random.randint(10, 30)
        p.current_request = None
        p.is_blocked = False
        processes[pid] = p
        
        os_state.max_demand[pid] = p.max_demand
        os_state.allocated[pid] = [0, 0, 0]
        
    random.seed() 
    
    timestamp = 0
    completed_processes = set()
    
    while len(completed_processes) < len(processes):
        timestamp += 1
        pending_requests = {}
        working_processes = 0
        
        for pid, p in processes.items():
            if pid in completed_processes:
                continue
                
            if p.is_blocked:
                pending_requests[pid] = p.current_request
                continue
                
            needs_more = any(p.allocated[i] < p.max_demand[i] for i in range(3))
            
            if needs_more and random.random() < 0.3:
                req = [random.randint(0, p.max_demand[i] - p.allocated[i]) for i in range(3)]
                if sum(req) > 0:
                    p.current_request = req
                    p.is_blocked = True
                    pending_requests[pid] = req
            else:
                working_processes += 1
                
        if pending_requests:
            try:
                approved = student_level_3_dynamic(os_state, pending_requests)
            except Exception as e:
                print(f"[Tick {timestamp}] Algorithm error: {e}")
                return
                
            for pid in approved:
                if pid not in pending_requests:
                    continue
                    
                req = pending_requests[pid]
                p = processes[pid]
                
                if any(req[i] > os_state.available_resources[i] for i in range(3)):
                    print(f"\n[Tick {timestamp}] FATAL: Approved request for {pid} exceeds available resources!")
                    return
                    
                for i in range(3):
                    os_state.available_resources[i] -= req[i]
                    p.allocated[i] += req[i]
                    os_state.allocated[pid][i] += req[i]
                    
                p.is_blocked = False
                p.current_request = None
                working_processes += 1

        if pending_requests and not approved and working_processes == 0:
            print(f"\n[Tick {timestamp}] FATAL: SYSTEM DEADLOCK DETECTED.")
            print("All active processes are blocked waiting for resources, and your algorithm approved none.")
            return

        for pid, p in processes.items():
            if pid in completed_processes or p.is_blocked:
                continue
            p.work_remaining -= 1
            if p.work_remaining <= 0:
                for i in range(3):
                    os_state.available_resources[i] += p.allocated[i]
                    os_state.allocated[pid][i] = 0
                completed_processes.add(pid)

        if timestamp > 5000:
            print(f"\nSimulation timed out at {timestamp} ticks. Starvation detected.")
            return

    print(f"Status: PASSED. All processes completed successfully.")
    print(f"Score (Total Time): {timestamp} ticks.")
    print("Goal: Lower this number by safely approving more concurrent requests without deadlocking!")


if __name__ == "__main__":
    if CURRENT_LEVEL == 1:
        run_level_1()
    elif CURRENT_LEVEL == 2:
        run_level_2()
    elif CURRENT_LEVEL == 3:
        run_level_3()
    else:
        print("Invalid CURRENT_LEVEL selected.")