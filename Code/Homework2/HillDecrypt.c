#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int GetInt(void);
bool IsNumeric(char);
int stoi(char*);

int** AllocMatrix(int);
int** FindInverseMatrix(int**, int);

void FillMatrix(int**, int);
void PrintMatrix(int**, int);
void FreeMatrix(int**, int);
void GetMatrixOfMinors(int**, int**, int, int, int);

int FindDeterminant(int**, int);

int main(void)
{
    printf("Enter the dimension of your matrix: ");

    int dimension = GetInt();

    // construct matrix using dynamic arrays
    int** MatrixA = AllocMatrix(dimension);

    // fill matrix
    FillMatrix(MatrixA, dimension);

    // print matrix
    printf("----------\nYour matrix:\n");
    PrintMatrix(MatrixA, dimension);

    int** InvMatrixA = FindInverseMatrix(MatrixA, dimension);
}

int GetInt(void)
{
    char buffer[1024];

    // get input
    if(fgets(buffer, sizeof(buffer), stdin) == NULL)
    {
        printf("Error getting input\n");
        return -1;
    }

    //remove newline if present
    for(int i = 0; i < sizeof(buffer); i++)
    {
        if(buffer[i] == '\n')
        {
            buffer[i] = '\0';
        }
    }

    //ensure numeric
    for(int i = 0; i < buffer[i] != '\0'; i++)
    {
        if(!IsNumeric(buffer[i]))
        {
            printf("Invalid String\n");
            return -1;
        }
    }

    return stoi(buffer);
}

bool IsNumeric(char curChar)
{
    if((curChar >= '0' && curChar <= '9') || curChar == '-')
    {
        return true;
    }

    return false;
}

int stoi(char* string)
{
    int retVal = 0;

    for(int i = 0; string[i] != '\0'; i++)
    {
        if(string[i] == '-')
        {
            continue;
        }

        retVal += (int)(string[i] - '0');

        if(string[i + 1] != '\0')
        {
            retVal *= 10;
        }
    }

    if(string[0] == '-')
    {
        retVal *= -1;
    }

    return retVal;
}

void PrintMatrix(int** curMatrix, int dimension)
{
    // print array
    for(int i = 0; i < dimension; i++)
    {
        for(int j = 0; j < dimension; j++)
        {
            printf("%i\t", curMatrix[i][j]);
        }

        printf("\n");
    }
}

void FillMatrix(int** curMatrix, int dimension)
{
    for(int i = 0; i < dimension; i++)
    {
        for(int j = 0; j < dimension; j++)
        {
            printf("Value for (%i, %i): ", i + 1, j + 1);
            curMatrix[i][j] = GetInt();
        }
    }
}

int** AllocMatrix(int dimension)
{
    int** curMatrix = (int**)(malloc(sizeof(int*) * dimension));

    for(int i = 0; i < dimension; i++)
    {
        curMatrix[i] = (int*)(malloc(sizeof(int) * dimension));
    }

    return curMatrix;
}

int** FindInverseMatrix(int** inMatrix, int dimension)
{
    // get det of matrix
    int det = FindDeterminant(inMatrix, dimension);

    //if matrix is non invertible
    if(det == 0)
    {
        printf("Non invertible matrix!\n");
        return NULL;
    }

    // allocate memory for inverse matrix
    int** invMatrix = AllocMatrix(dimension);

    // allocate memory for matrix of minors
    int** matrixOfMinors = AllocMatrix(dimension - 1);

    // calculate the inverse
    for(int i = 0; i < dimension; i++)
    {
        for(int j = 0; j < dimension; j++)
        {
            //compute the minor for each element
            GetMatrixOfMinors(inMatrix, matrixOfMinors, dimension - 1, i, j);

            int minorDet = FindDeterminant(matrixOfMinors, dimension - 1);
            invMatrix[j][i] = ((i + j) % 2 == 0 ? 1 : -1) * minorDet / det;
        }
    }

    FreeMatrix(matrixOfMinors, dimension - 1);
    return invMatrix;

}

// create matrix of minors
//THIS CODE IS BAD!!!! FIX!!!!
void GetMatrixOfMinors(int** inMatrix, int** minor, int dimension, int row, int col)
{
    int m = 0;
    int n = 0;

    for(int i = 0; i < dimension; i++)
    {
        if(i == row)
        {
            continue;
        }

        n = 0;

        for(int j = 0; j < dimension; j++)
        {
            if(j == col)
            {
                continue;
            }
            printf("Writing to (%i, %i) with value %i\n", m, n, inMatrix[i][j]);

            minor[m][n] = inMatrix[i][j];
            PrintMatrix(minor, dimension);

            n++;
        }

        m++;
    }
}

int FindDeterminant(int** inMatrix, int dimension)
{
    // handle dim = 1
    if(dimension == 1)
    {
        return inMatrix[0][0];
    }

    // handle dim = 2
    if(dimension == 2)
    {
        return ((inMatrix[0][0] * inMatrix[1][1]) - (inMatrix[0][1] * inMatrix[1][0]));
    }

    // solve for determinant using abjugate method
    int det = 0;
    int** matrixOfMinors = AllocMatrix(dimension - 1);

    for(int j = 0; j < dimension; j++)
    {
        GetMatrixOfMinors(inMatrix, matrixOfMinors, dimension - 1, 0, j);
        det += (j % 2 == 0 ? 1 : -1) * FindDeterminant(matrixOfMinors, dimension);
    }

    // free leftoverss and return
    FreeMatrix(matrixOfMinors, dimension - 1);
    return det;
}

void FreeMatrix(int** inMatrix, int dimension)
{
    for(int i = 0; i < dimension; i++)
    {
        free(inMatrix[i]);
    }

    free(inMatrix);
}