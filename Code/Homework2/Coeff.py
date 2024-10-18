def berlekamp_massey(sequence):
    """
    Berlekamp-Massey algorithm to find the coefficients of the minimal polynomial
    for a given LFSR sequence.

    :param sequence: List of integers representing the LFSR sequence
    :return: List of coefficients of the minimal polynomial
    """
    n = len(sequence)
    C = [0] * n
    B = [0] * n
    L = 0
    m = -1
    C[0] = 1
    B[0] = 1

    for i in range(n):
        d = sequence[i]
        for j in range(1, L + 1):
            d ^= C[j] * sequence[i - j]
        if d != 0:
            T = C[:]
            for j in range(i - m, n):
                C[j] ^= B[j - i + m]
            if 2 * L <= i:
                L = i + 1 - L
                m = i
                B = T

    return C[:L + 1]

# Example usage:
sequence = [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
coefficients = berlekamp_massey(sequence)
print("Coefficients:", coefficients)
print(f"Coefficients length: {len(coefficients)}")
