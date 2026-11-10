import numpy as np
import random


def fix_errors(corrupted_vector, valid_codewords):
    fixed_vector = corrupted_vector.copy()
    
    # ==========================================
    # write your code here
    # ==========================================
    
    return fixed_vector


def run_simulation():
    # Note: To successfully correct 2 errors, you might need to add data to the codewords
    valid_codewords = [
        np.array([0,0,0,0,0,0,0]),
        np.array([1,1,0,1,0,0,1]),
        np.array([0,1,1,0,1,1,1]),
        np.array([1,0,1,1,1,1,0])
    ]
    
    tests_per_level = 100
    max_errors = 2
    
    print("Starting simulation...\n")
    
    for num_errors in range(1, max_errors + 1):
        print(f"--- Level {num_errors}: Testing with {num_errors} error(s) ---")
        successes = 0
        
        for i in range(tests_per_level):
            original = random.choice(valid_codewords).copy()
            corrupted = original.copy()
            
            # Inserting random unique errors
            error_indices = random.sample(range(len(original)), num_errors)
            for idx in error_indices:
                corrupted[idx] = (corrupted[idx] + 1) % 2
            
            fixed = fix_errors(corrupted, valid_codewords)
            
            if np.array_equal(fixed, original):
                successes += 1
                
        print(f"Successes: {successes}/{tests_per_level}")
        
        if successes == tests_per_level:
            print(f"Level {num_errors} passed!\n")
        else:
            print(f"Failed at level {num_errors}. Your algorithm needs improvement.\n")
            break

if __name__ == "__main__":
    run_simulation()