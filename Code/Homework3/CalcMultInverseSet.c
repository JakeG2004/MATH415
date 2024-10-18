#include <stdio.h>
#include <stdlib.h>

int findMultiplicativeInverse(int a, int m);
int GCD(int x, int y) ;

int main() 
{
    int xCoef = 216;  // Coefficient of x in the equation
    int remainder = 66; // Remainder
    int mod = 606; // Modulus

    // Calculate the GCD of the x coefficient and modulus
    int gcd = GCD(xCoef, mod);

    // Check if there are solutions based on the GCD
    if(remainder % gcd != 0) 
    {
        printf("No solutions\n");
        return 0; // Exit the program
    }

    // Reduce the coefficients
    int redXCoef = xCoef / gcd;
    int redRemainder = remainder / gcd;
    int redMod = mod / gcd;

    // Compute the GCD of the reduced coefficients
    gcd = GCD(redXCoef, redMod);

    // Check if an inverse exists
    if(gcd != 1) 
    {
        printf("No multiplicative inverse exists\n");
        return 0; // Exit the program
    }

    // Find the multiplicative inverse using the quotients
    int inverse = findMultiplicativeInverse(redXCoef, redMod);

    // Calculate the particular solution
    int baseSolution = (inverse * redRemainder) % redMod;

    // Ensure the base solution is non-negative
    if(baseSolution < 0) 
    {
        baseSolution += redMod;
    }

    // Display the solution set
    printf("The solutions are:\n");
    for(int i = 0; baseSolution + i * redMod < mod; i++) 
    {
        printf("%i\n", baseSolution + i * redMod);
    }

    return 0;
}

// GCD function that also collects quotients
int GCD(int x, int y) 
{
    while(y != 0) {
        int remainder = x % y;
        int quotient = x / y;

        // Reassign vars and repeat
        x = y;
        y = remainder;
    }

    return x; // Return the GCD
}

// Function to find the multiplicative inverse
int findMultiplicativeInverse(int a, int m) 
{
    int x = 0; // This will hold the inverse
    int y = 1; // This will help find the inverse
    int original_m = m; // Store the original modulus for later use

    while(a > 1) 
    {
        // q is quotient
        int q = a / m;
        int t = m;

        // m is remainder now, process same as Euclid's algorithm
        m = a % m;
        a = t;

        // Update x and y
        t = x;
        x = y - q * x;
        y = t;
    }

    // Make sure x is positive
    if (y < 0) 
    {
        y += original_m;
    }

    return y; // Return the multiplicative inverse
}
