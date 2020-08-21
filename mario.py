# Import stuff
from sys import exit
from cs50 import get_int


def main():
    ui = height()
    row = 1
    # AKA height
    for row in range(ui):
        # AKA width
        for column in range(ui - (row + 1)):
            # prints # and removes new line at the end
            print(" ", end="")
        for dot in range(row + 1):
            print("#", end="")
        # prints a new line
        print()

# height function


def height():
    # Need to loop until an appropriate answer is given
    while True:
        # casting default stirng input to int
        user_input = get_int("Height: ")
        if user_input > 0 and user_input < 9:
            # break the loop if True otherwise ask again
            break
    return user_input
    # success
    exit(0)


main()
