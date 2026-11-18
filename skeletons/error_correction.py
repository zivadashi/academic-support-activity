import numpy as np
import random
import time

# Change this to 1, 2, or 3 to test different levels
CURRENT_LEVEL = 1

# ==============================================================================
# LEVEL 1: Minimum Distance Search
# ==============================================================================
def student_level_1_distance(corrupted_batch, valid_codewords):
    """
    Level 1: You are given a small batch of corrupted vectors and a list of 
    all mathematically valid codewords. Each corrupted vector has exactly 1 error.
    
    Goal: Fix the vectors by finding the closest valid codeword (Minimum Hamming Distance).
    
    Args:
        corrupted_batch: A 2D numpy array (batch_size, 7).
        valid_codewords: A 2D numpy array containing all 16 valid codewords.
        
    Returns:
        A 2D numpy array of the fixed vectors.
    """
    fixed_batch = corrupted_batch.copy()
    
    # ==========================================
    # write your level 1 code here
    # ==========================================
    
    return fixed_batch


# ==============================================================================
# LEVEL 2: Syndrome Decoding (Linear Algebra)
# ==============================================================================
def student_level_2_syndrome(corrupted_batch, H_matrix):
    """
    Level 2: The brute-force distance search is too slow for large systems.
    Instead, use the Parity-Check Matrix (H).
    
    Goal: 
    1. Compute the Syndrome for each vector: S = (v * H^T) mod 2
    2. The resulting Syndrome matches exactly one column in H. The index 
       of that column is the index of the flipped bit!
    3. Flip that bit back to fix the vector.
    
    Args:
        corrupted_batch: A 2D numpy array (batch_size, 7).
        H_matrix: The 3x7 Parity-Check Matrix.
        
    Returns:
        A 2D numpy array of the fixed vectors.
    """
    fixed_batch = corrupted_batch.copy()
    
    # ==========================================
    # write your level 2 code here
    # ==========================================
    
    return fixed_batch


# ==============================================================================
# LEVEL 3: The Missing Matrix & Ultimate Optimization
# ==============================================================================
def student_level_3_deduction(corrupted_batch, G_matrix):
    """
    Level 3: In the real world, you only receive the Generator Matrix (G) used 
    to encode the data. You must deduce H mathematically and decode a MASSIVE batch.
    
    Goal:
    1. G is provided in standard form: G = [I_k | P]
    2. Deduce H using the rule: H = [-P^T | I_{n-k}]. (Note: in modulo 2, -1 = 1).
    3. Fix 100,000 vectors simultaneously. 
    4. NO PYTHON LOOPS ALLOWED. You must use pure Numpy broadcasting and 
       matrix multiplication to beat the execution time limit.
    
    Args:
        corrupted_batch: A 2D numpy array (100000, 7).
        G_matrix: The 4x7 Generator Matrix.
        
    Returns:
        A 2D numpy array of the fixed vectors.
    """
    fixed_batch = corrupted_batch.copy()
    
    # ==========================================
    # write your level 3 code here
    # ==========================================
    
    return fixed_batch


# ==============================================================================
# SIMULATION TESTERS (Pre-implemented)
# ==============================================================================

# Standard (7,4) Hamming Code Matrices for testing
P_MATRIX = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1]
])
G_MATRIX = np.hstack((np.eye(4, dtype=int), P_MATRIX))
H_MATRIX = np.hstack((P_MATRIX.T, np.eye(3, dtype=int)))

def generate_test_data(batch_size):
    """Generates ground truth and corrupted data for testing."""
    # Generate all 16 valid codewords
    data_bits = np.array([[int(x) for x in format(i, '04b')] for i in range(16)])
    valid_codewords = (data_bits @ G_MATRIX) % 2
    
    # Generate random batch
    indices = np.random.randint(0, 16, size=batch_size)
    original_batch = valid_codewords[indices].copy()
    corrupted_batch = original_batch.copy()
    
    # Insert exactly 1 error per vector
    error_indices = np.random.randint(0, 7, size=batch_size)
    batch_indices = np.arange(batch_size)
    corrupted_batch[batch_indices, error_indices] ^= 1 
    
    return original_batch, corrupted_batch, valid_codewords

def evaluate_results(original, fixed, start_time, end_time, time_limit=None):
    if fixed.shape != original.shape:
        print(f"Failed: Expected output shape {original.shape}, got {fixed.shape}")
        return
        
    correct_rows = np.all(fixed == original, axis=1)
    successes = np.sum(correct_rows)
    total = original.shape[0]
    exec_time = end_time - start_time
    
    print(f"Successes: {successes}/{total}")
    print(f"Execution Time: {exec_time:.6f} seconds")
    
    if successes == total:
        if time_limit and exec_time > time_limit:
            print(f"Status: FAILED. You exceeded the time limit of {time_limit}s.")
            print("You need to remove Python loops and use pure Numpy broadcasting.")
        else:
            print("Status: PASSED!")
    else:
        print("Status: FAILED. Algorithm did not correctly fix all vectors.")


def run_level_1():
    print("--- LEVEL 1: Minimum Distance Search ---")
    batch_size = 500
    original, corrupted, valid_codewords = generate_test_data(batch_size)
    
    start_time = time.perf_counter()
    try:
        fixed = student_level_1_distance(corrupted.copy(), valid_codewords)
    except Exception as e:
        print(f"Algorithm error: {e}")
        return
    end_time = time.perf_counter()
    
    evaluate_results(original, fixed, start_time, end_time)


def run_level_2():
    print("--- LEVEL 2: Syndrome Decoding (Linear Algebra) ---")
    batch_size = 5000
    original, corrupted, _ = generate_test_data(batch_size)
    
    start_time = time.perf_counter()
    try:
        fixed = student_level_2_syndrome(corrupted.copy(), H_MATRIX.copy())
    except Exception as e:
        print(f"Algorithm error: {e}")
        return
    end_time = time.perf_counter()
    
    evaluate_results(original, fixed, start_time, end_time)


def run_level_3():
    print("--- LEVEL 3: The Missing Matrix & Ultimate Optimization ---")
    batch_size = 100000
    print(f"Processing {batch_size} vectors...")
    original, corrupted, _ = generate_test_data(batch_size)
    
    start_time = time.perf_counter()
    try:
        fixed = student_level_3_deduction(corrupted.copy(), G_MATRIX.copy())
    except Exception as e:
        print(f"Algorithm error: {e}")
        return
    end_time = time.perf_counter()
    
    # Strict time limit to force pure Numpy solutions (no loops)
    evaluate_results(original, fixed, start_time, end_time, time_limit=0.15)


if __name__ == "__main__":
    if CURRENT_LEVEL == 1:
        run_level_1()
    elif CURRENT_LEVEL == 2:
        run_level_2()
    elif CURRENT_LEVEL == 3:
        run_level_3()
    else:
        print("Invalid CURRENT_LEVEL selected.")