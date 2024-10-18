def remove_non_digits(s):
    # Extract digits and convert to a list
    digits = [c for c in s if c.isdigit()]
    return digits

# Example usage
input_string = "1 , 0 . 0 , 1 , 1 , 0 , 0 , 1 , 0 , 0 , 1 , 1 . 1 ,0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1 , 0 , 1 , 0 , 0 , 0 , 1 , 1 , 1 , 1 , 0 , 1 , 1 , 0 , 0 , 1 , 1 , 1 . 1 . 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 0 , 1 , 0 ,1 , 1 , 0 , 1 , 1 , 0 , 1 , 0 , 1 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 0 , 1 , 1 ,1 , 0 , 0 , 1 , 0 , 1 , 0 , 1 , 1 , 1 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 ,0 , 0 , 0 , 1 , 0 , 0 , 1 , 0 , 0 , 0 , 0"
digits_array = remove_non_digits(input_string)

# Convert list to string format and print
print(f"[{', '.join(digits_array)}]")

# Print the length of the sequence
print(f"Seed Length: {len(digits_array)}")


