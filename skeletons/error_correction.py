import numpy as np
import random
import time

MAX_ERRORS = 2

# ==========================================
# 1. Define your valid codewords here:
# (Hint: Will these specific vectors survive level 2?)
# ==========================================
VALID_CODEWORDS = [
    np.array([0,0,0,0,0,0,0]),
    np.array([1,1,0,1,0,0,1]),
    np.array([0,1,1,0,1,1,1]),
    np.array([1,0,1,1,1,1,0])
]

def decode_batch(corrupted_batch, valid_codewords):
    """
    Fixes errors for a large batch of corrupted vectors.
    
    Args:
        corrupted_batch: A 2D numpy array of shape (batch_size, vector_length).
        valid_codewords: A 2D numpy array containing the valid codewords.
        
    Returns:
        A 2D numpy array of the fixed vectors, same shape as corrupted_batch.
    """
    # ==========================================
    # write your code here
    # ==========================================
    fixed_batch = corrupted_batch.copy()
    
    return fixed_batch


def run_simulation():
    # Convert to 2D numpy array for efficient batch processing
    valid_codewords = np.array(VALID_CODEWORDS)
    
    batch_size = 10000
    max_errors = MAX_ERRORS
    
    print(f"Starting simulation. Processing batches of {batch_size} vectors...\n")
    print("Focus on reducing your Execution Time!\n")
    
    for num_errors in range(1, max_errors + 1):
        print(f"--- Level {num_errors}: Testing with {num_errors} error(s) per vector ---")
        
        # 1. Generate test data
        original_list = [random.choice(VALID_CODEWORDS) for _ in range(batch_size)]
        original_batch = np.array(original_list)
        corrupted_batch = original_batch.copy()
        
        vector_length = valid_codewords.shape[1]
        
        for i in range(batch_size):
            error_indices = random.sample(range(vector_length), num_errors)
            for idx in error_indices:
                corrupted_batch[i, idx] = (corrupted_batch[i, idx] + 1) % 2
                
        # 2. Run the algorithm
        start_time = time.perf_counter()
        try:
            fixed_batch = decode_batch(corrupted_batch.copy(), valid_codewords)
        except Exception as e:
            print(f"Algorithm error: {e}\n")
            break
        end_time = time.perf_counter()
        
        # 3. Validate results
        if fixed_batch.shape != original_batch.shape:
            print(f"Failed: Expected output shape {original_batch.shape}, got {fixed_batch.shape}\n")
            break
            
        # Check if all bits in a row match the ground truth
        correct_rows = np.all(fixed_batch == original_batch, axis=1)
        successes = np.sum(correct_rows)
        
        print(f"Successes: {successes}/{batch_size}")
        
        if successes == batch_size:
            exec_time = end_time - start_time
            print(f"Execution Time: {exec_time:.6f} seconds")
            print(f"Level {num_errors} passed!\n")
        else:
            print(f"Failed at level {num_errors}.")
            if (num_errors > 1):
                # Only relevant for level 2 onward
                print("If you are sure your logic is correct, ask yourself:")
                print("Is it mathematically possible to correct this many errors with the current codewords?")
                print("Hint: Check the minimum Hamming distance between your VALID_CODEWORDS.\n")
            break

if __name__ == "__main__":
    run_simulation()