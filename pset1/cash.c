#include <stdio.h>
#include <cs50.h>
#include <math.h>

float dollars(void);

int main(void)
{
    // Converting dollars into cents
    int cents = round(dollars() * 100);
    int quarters = 25;
    int dimes = 10;
    int nickels = 5;
    int pennies = 1;
    int coins = 0;
    int tc = 0;
    int current = cents;
     
    while (quarters <= current)
    {
        coins = cents / quarters;
        current = cents % quarters;
        tc = coins;
    }
    while (dimes <= current)
    {
        coins = current / dimes;
        current = current % dimes;
        tc += coins;
    }
    while (nickels <= current)
    {
        coins = current / nickels;
        current = current % nickels;
        tc += coins;
    }
    while (pennies <= current)
    {
        coins = current / pennies; 
        current = current % pennies;
        tc += coins;
    }
    printf("%i\n", tc);
}

// Prompting user for change owed
float dollars(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0.00);
    return (dollars);
}