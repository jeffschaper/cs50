#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        // Prompt for height
        n = get_int("Height: ");
    }
    // Prompt for height while this is true
    // Not &&, use || n less than 1 or n greater than 9; includes 1 and 8
    while (n < 1 || n > 8);

    // Printing rows n times
    for (int r = 1; r <= n; r++)
    {
        // Print " " when d < height - row
        for (int d = 1; d <= (n - r); d++)
        {
            printf(" ");
        }

        //Printing columns n times; Check condition c < r; columns less than rows
        for (int c = 0; c < r; c++)
        {
            printf("#");
        }
        printf("\n");
    }
}