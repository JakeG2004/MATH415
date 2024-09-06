#include <stdio.h>

int main(void)
{
    char ciphertext[] = "ycvejqwvhqtdtwvwu";
    char buffer[sizeof(ciphertext)];

    //for each key
    for(int i = 1; i < 26; i++)
    {
        //shift each character in the string by the key
        for(int j = 0; j < sizeof(ciphertext) - 1; j++)
        {
            buffer[j] = ((ciphertext[j] - i));

            if(buffer[j] < 'a')
            {
                buffer[j] = 'z' - ('a' - buffer[j]);
            }
        }

        buffer[sizeof(buffer)] = '\n';

        printf("Key: %i Value: %s", i, buffer);
    }
}