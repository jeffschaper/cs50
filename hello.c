#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt to get user entered string
    string s = get_string("What is your name?\n");
    // Placehloder for a string followed by filling
    printf("hello, %s\n", s);
}