#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

string encipher(string x, int k);
//int alpha(string p);
//int ascii(int x);

int main(int argc, string argv[])
{
    // If this function fails, return 1  (Exit code)
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // If this function fails, return 1 (Exit code)
    // Array size, 100 as random number
    char argument[100];
    // strcpy, copies string to variable
    strcpy(argument, argv[1]);

    for (int i = 0; i < strlen(argument); i++)
    {
        // If not isdigit
        if (! isdigit(argument[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // atoi converts array to int
    int key = atoi(argv[1]);

    // If return == 0, printf
    string text = get_string("plaintext: ");

    printf("ciphertext: ");
    encipher(text, key);
}

string encipher(string p, int k)
// Pass plaintext + key
{
    int n = strlen(p);

    // Shift alphabetical character by key
    for (int i = 0; i < n; i++)
    {
        if (isalpha(p[i]))
        {
            if (isupper(p[i]))
            {
                // Convert to uppercase alphabetical index...A = 0, B = 1
                int x = p[i] - 65;
                // j = New index in alphabetical index...0, 1, 2
                int j = (x + k) % 26;
                // Convert to ASCII
                int l = j + 65; // new ascii
                printf("%c", l);
            }
            else
            {
                int x = p[i] - 97;
                int j = (x + k) % 26;
                int l = j + 97; 
                printf("%c", l);
            }
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
    return 0;
}