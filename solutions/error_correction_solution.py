import numpy as np

def decode_batch_naive(corrupted_batch, valid_codewords):
    """
    Level 1: Pure Python Nested Loops.
    Calculates Hamming distance manually for every single vector.
    Extremely slow for large batches (O(N * M * K) pure Python iterations).
    """
    fixed_batch = np.zeros_like(corrupted_batch)
    
    for i in range(len(corrupted_batch)):
        corrupted_vec = corrupted_batch[i]
        best_match = None
        min_dist = float('inf')
        
        # Compare against every valid codeword
        for valid_vec in valid_codewords:
            dist = 0
            # Manually count bit differences
            for bit in range(len(corrupted_vec)):
                if corrupted_vec[bit] != valid_vec[bit]:
                    dist += 1
                    
            if dist < min_dist:
                min_dist = dist
                best_match = valid_vec
                
        fixed_batch[i] = best_match
        
    return fixed_batch

def decode_batch_intermediate(corrupted_batch, valid_codewords):
    """
    Level 2: Intermediate Numpy.
    Iterates over the batch, but uses Numpy arrays to calculate 
    distances for each row simultaneously.
    Faster than Level 1, but slower than Level 3 (Pure Broadcasting).
    """
    fixed_batch = np.zeros_like(corrupted_batch)
    
    for i in range(len(corrupted_batch)):
        corrupted_vec = corrupted_batch[i]
        
        # corrupted_vec is broadcast against all valid_codewords at once
        # diffs shape: (Num_Codewords, Vector_Length)
        diffs = (corrupted_vec != valid_codewords)
        
        # Sum the boolean differences along the rows to get Hamming distances
        distances = np.sum(diffs, axis=1)
        
        # Find the index of the minimum distance
        best_idx = np.argmin(distances)
        
        fixed_batch[i] = valid_codewords[best_idx]
        
    return fixed_batch

def decode_batch(corrupted_batch, valid_codewords):
    """
    Blazing fast implementation using pure Numpy linear algebra and broadcasting.
    No Python loops are used, allowing massive batch processing in milliseconds.
    """
    # Shapes:
    # corrupted_batch: (Batch_Size, Vector_Length)
    # valid_codewords: (Num_Codewords, Vector_Length)
    
    # Reshape for 3D broadcasting: 
    # Compare every corrupted vector against EVERY valid codeword simultaneously
    # diff shape: (Batch_Size, Num_Codewords, Vector_Length)
    diff = corrupted_batch[:, np.newaxis, :] != valid_codewords[np.newaxis, :, :]
    
    # Sum along the last axis to get the Hamming distance
    # distances shape: (Batch_Size, Num_Codewords)
    distances = np.sum(diff, axis=2)
    
    # Find the index of the codeword with the minimum Hamming distance for each row
    # best_match_indices shape: (Batch_Size,)
    best_match_indices = np.argmin(distances, axis=1)
    
    # Return the fully corrected batch
    return valid_codewords[best_match_indices]