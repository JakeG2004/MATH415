import numpy as np
from sympy import Matrix

def mod_inverse(matrix, modulus):
    # Find the modular inverse of a matrix
    matrix = Matrix(matrix)
    matrix_inv = matrix.inv_mod(modulus)
    return np.array(matrix_inv).astype(int)

def hill_decrypt(ciphertext, key_matrix):
    modulus = 26
    
    # Calculate the inverse of the key matrix
    key_matrix_inv = mod_inverse(key_matrix, modulus)
    
    # Convert ciphertext to numerical form
    ciphertext_nums = [ord(char) - ord('a') for char in ciphertext]
    
    # Reshape ciphertext into matrix form
    num_rows = len(ciphertext_nums) // key_matrix.shape[1]
    ciphertext_matrix = np.array(ciphertext_nums).reshape((num_rows, key_matrix.shape[1]))
    
    # Decrypt the ciphertext matrix
    decrypted_matrix = np.dot(ciphertext_matrix, key_matrix_inv) % modulus
    
    # Convert numerical plaintext back to letters
    decrypted_text = ''.join(chr(int(num) + ord('A')) for num in decrypted_matrix.flatten())
    
    return decrypted_text

# Example usage
key_matrix = np.array([[1, 2, 3, 4], [4, 3, 2, 1], [11, 2, 4, 6], [2, 9, 6, 4]])  # 3x3 matrix for Hill cipher
ciphertext = "zirkzwopjjoptfapuhfhadrq"

decrypted_text = hill_decrypt(ciphertext, key_matrix)
print("Decrypted text:", decrypted_text)
