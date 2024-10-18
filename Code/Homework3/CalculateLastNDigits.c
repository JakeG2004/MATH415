#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int ModularExponentiation(int base, int exp, int mod);
char* IntToString(int numDigits, int num);

int main()
{
    int baseNum = 0;
    int exponent = 0;
    int numDigits = 0;
    int mod = 1;

    printf("Enter base number: ");
    scanf("%i", &baseNum);

    printf("Enter exponent: ");
    scanf("%i", &exponent);

    printf("Enter number of digits: ");
    scanf("%i", &numDigits);

    // Calculate the mod to get the correct number of digits
    for (int i = 0; i < numDigits; i++)
    {
        mod *= 10;
    }

    // Calculate the result using modular exponentiation
    int result = ModularExponentiation(baseNum, exponent, mod);

    // Allocate enough memory to store the string representation of the result
    char* resString = IntToString(numDigits, result);

    printf("Result: %s\n", resString);
}

// Function for modular exponentiation
int ModularExponentiation(int base, int exp, int mod)
{
    long long result = 1; // Use long long to prevent overflow
    base = base % mod;    // In case base is greater than mod

    while (exp > 0)
    {
        // If exp is odd, multiply the base with the result
        if (exp % 2 == 1)
        {
            result = (result * base) % mod;
        }
        // Now exp must be even, so divide it by 2
        exp = exp >> 1; // Equivalent to exp / 2
        // Square the base
        base = (base * base) % mod;
    }
    return result;
}

char* IntToString(int numDigits, int num)
{
    // Allocate memory for the string plus the null terminator
    char* retStr = (char*)malloc(sizeof(char) * (numDigits + 1));

    if (retStr == NULL) {
        return NULL; // Check for memory allocation failure
    }

    retStr[numDigits] = '\0'; // Set the null terminator

    // Fill the string with digits from the least significant to the most
    for (int i = numDigits - 1; i >= 0; i--)
    {
        // Get the last digit
        retStr[i] = '0' + (num % 10);
        num /= 10; // Remove the last digit from num
    }

    return retStr;
}
