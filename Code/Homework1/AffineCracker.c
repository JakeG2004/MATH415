#include <stdio.h>

void ShiftLowerToNumeric(char inString[], char outString[], int size);
void ShiftNumericToLower(char inString[], char outString[], int size);

int SolveForAlpha(int C1, int C2, int P1, int P2);
int SolveForBeta(int alpha, int C1, int P1);
int FindMultInverse(int alpha);

int main(void)
{
    char ciphertext[] = "edsgickxhuklzveqzvkxwkzukcvuh";
    char shiftedCipherText[sizeof(ciphertext)];

    char firstTwoLetters[3] = "if";
    char shiftedFirstTwoLetters[sizeof(firstTwoLetters)];

    char buffer[sizeof(ciphertext)];

    char plaintext[sizeof(ciphertext)];

    int alpha;
    int beta;
    int alphaInverse;

    int C1;
    int C2;

    int P1;
    int P2;

    //shift ranges
    ShiftLowerToNumeric(ciphertext, shiftedCipherText, sizeof(ciphertext));
    ShiftLowerToNumeric(firstTwoLetters, shiftedFirstTwoLetters, sizeof(firstTwoLetters));

    P1 = shiftedFirstTwoLetters[0];
    P2 = shiftedFirstTwoLetters[1];

    C1 = shiftedCipherText[0];
    C2 = shiftedCipherText[1];

    //calculate our alpha + beta values
    alpha = SolveForAlpha(C1, C2, P1, P2);
    beta = SolveForBeta(alpha, C1, P1);

    printf("Alpha: %i, Beta: %i\n", alpha, beta);

    alphaInverse = FindMultInverse(alpha);

    //error check
    if(alphaInverse = -1)
    {
        printf("Unable to find multiplicative inverse! Aborting...\n");
        exit();
    }

    //write plaintext
    for(int i = 0; i < sizeof(buffer); i++)
    {
        buffer[i] = alphaInverse * (shiftedCipherText[i] - beta + 26) % 26;
    }

    ShiftNumericToLower(buffer, plaintext, sizeof(buffer));

    printf("Plaintext: %s\n", plaintext);
}

//test every value from 1 - 26, testing for multiplicative inverse
int FindMultInverse(int alpha)
{
    alpha = alpha % 26;

    for(int i = 1; i < 26; i++)
    {
        if((alpha * i) % 26 == 1)
        {
            return i;
        }
    }

    //return -1 if not found
    return -1;
}

int SolveForAlpha(int C1, int C2, int P1, int P2)
{
    int tmp = (C1 - C2);

    while(tmp % (P1 - P2) != 0)
    {
        tmp += 26;
    }

    tmp /= (P1 - P2);

    return tmp;
}

int SolveForBeta(int alpha, int C1, int P1)
{
    int tmp = (C1 - (alpha * P1)) % 26;

    while(tmp < 0)
    {
        tmp += 26;
    }

    return tmp;
}

void ShiftLowerToNumeric(char inString[], char outString[], int size)
{
    for(int i = 0; i < size; i++)
    {
        outString[i] = inString[i] - 'a';
    }

    outString[size - 1] = '\0';
}

void ShiftNumericToLower(char inString[], char outString[], int size)
{
    for(int i = 0; i < size; i++)
    {
        outString[i] = inString[i] + 'a';
    }

    outString[size - 1] = '\0';
}