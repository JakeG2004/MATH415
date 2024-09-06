import math

def find_relatively_prime_numbers(n):
    relatively_prime_numbers = []
    for i in range(26):  # Check numbers from 0 to 25
        if math.gcd(n, i) == 1:
            relatively_prime_numbers.append(i)
    return relatively_prime_numbers

def main():
    try:
        number = int(input("Enter a number: "))

        result = find_relatively_prime_numbers(number)
        count = len(result);
        print(f"Numbers between 0 and 25 that are relatively prime to {number} are: {result}.\nThere are {count}.")

    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
