#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ExtendedEuclideanAlgorithm(int a, int b, int c, int* x, int* y);

int main(void)
{
    int xCoef = 0;
    int yCoef = 0;
    int x = 0;
    int y = 0;
    int sum = 0;

    printf("Enter the coefficient of X: ");
    scanf("%i", &xCoef);

    printf("Enter the coefficient of Y: ");
    scanf("%i", &yCoef);

    printf("Enter the sum: ");
    scanf("%i", &sum);

    ExtendedEuclideanAlgorithm(xCoef, yCoef, sum, &x, &y);

    printf("The solution is\nx = %i\ny = %i\n", x, y);
}

void ExtendedEuclideanAlgorithm(int xCoef, int yCoef, int sum, int* x, int* y) 
{
    //handle when the x coefficient is 0
    if(xCoef == 0)
    {
        //check if the y coefficient is divisible by the sum
        if((sum % yCoef) == 0)
        {
            *x = 0;
            *y = sum / yCoef;
        }

        //otherwise, there is no solution
        else
        {
            *x = 0;
            *y = 0;
        }

        return;
    }

    int x1;
    int y1;

    //recurse until solution found
    ExtendedEuclideanAlgorithm(yCoef % xCoef, xCoef, sum, &x1, &y1);

    *x = y1 - (yCoef / xCoef) * x1;
    *y = (sum - (xCoef * (*x))) / yCoef;
}