import numpy as np

# ==============================================================================
# LEVEL 1: Minimum Distance Search
# ==============================================================================
def student_level_1_distance(corrupted_batch, valid_codewords):
    """
    Finds the closest valid codeword for each corrupted vector using 
    Hamming distance.
    """
    fixed_batch = np.zeros_like(corrupted_batch)
    
    for i, vec in enumerate(corrupted_batch):
        # Compute Hamming distance against all valid codewords
        distances = np.sum(valid_codewords != vec, axis=1)
        best_idx = np.argmin(distances)
        fixed_batch[i] = valid_codewords[best_idx]
        
    return fixed_batch


# ==============================================================================
# LEVEL 2: Syndrome Decoding (Linear Algebra)
# ==============================================================================
def student_level_2_syndrome(corrupted_batch, H_matrix):
    """
    Computes syndromes via matrix multiplication and uses a dictionary 
    lookup to locate and flip the erroneous bit.
    """
    fixed_batch = corrupted_batch.copy()
    
    # Map each column of H (as a tuple) to its corresponding bit index
    syndrome_to_index = {
        tuple(H_matrix[:, col]): col for col in range(H_matrix.shape[1])
    }
    
    # Compute all syndromes at once: S = (v * H^T) mod 2
    syndromes = (corrupted_batch @ H_matrix.T) % 2
    
    for i, syn in enumerate(syndromes):
        syn_tuple = tuple(syn)
        if syn_tuple in syndrome_to_index:
            error_idx = syndrome_to_index[syn_tuple]
            fixed_batch[i, error_idx] ^= 1
            
    return fixed_batch


# ==============================================================================
# LEVEL 3: The Missing Matrix & Ultimate Optimization
# ==============================================================================
def student_level_3_deduction(corrupted_batch, G_matrix):
    """
    Deduces H from G and fixes 100,000 vectors simultaneously using 
    pure vectorized Numpy operations (no Python loops).
    """
    fixed_batch = corrupted_batch.copy()
    k, n = G_matrix.shape
    r = n - k
    
    # 1. Deduce H = [P^T | I_r] from standard form G = [I_k | P]
    P = G_matrix[:, k:]
    H_matrix = np.hstack((P.T, np.eye(r, dtype=int)))
    
    # 2. Compute syndromes for the entire batch
    syndromes = (corrupted_batch @ H_matrix.T) % 2
    
    # 3. Convert binary syndromes and H columns to integers for vectorized lookup
    powers = 2 ** np.arange(r - 1, -1, -1)
    col_ints = H_matrix.T @ powers
    syndrome_ints = syndromes @ powers
    
    # Build a 1D lookup array: syndrome_int -> error bit index (-1 = no error)
    lookup = np.full(2 ** r, -1, dtype=int)
    lookup[col_ints] = np.arange(n)
    
    # 4. Flip the erroneous bits across all rows simultaneously
    error_indices = lookup[syndrome_ints]
    has_error = error_indices != -1
    row_indices = np.where(has_error)[0]
    
    fixed_batch[row_indices, error_indices[has_error]] ^= 1
    
    return fixed_batch