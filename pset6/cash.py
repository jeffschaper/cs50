# import stuff
import cs50
import math


def main():
    cents = round(dollars() * 100)
    quarters = 25
    dimes = 10
    nickels = 5
    pennies = 1
    coins = 0
    total_coins = 0
    current = cents

    while (quarters <= current):
        coins = math.floor(cents / quarters)
        current = cents % quarters
        total_coins = coins

    while (dimes <= current):
        coins = math.floor(current / dimes)
        current = current % dimes
        total_coins += coins

    while (nickels <= current):
        coins = math.floor(current / nickels)
        current = current % nickels
        total_coins += coins

    while (pennies <= current):
        coins = math.floor(current / pennies)
        current = current % pennies
        total_coins += coins

    print(math.floor(total_coins))
# define dollar conversion from change owed


def dollars():
    while True:
        dollars = cs50.get_float("Change owed: ")
        if (dollars > 0.00):
            break
    return dollars


main()