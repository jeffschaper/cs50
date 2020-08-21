# import stuff

import cs50
import math
import re


# define main function
def main():

    # get string from user
    text = cs50.get_string("Text: ")

    # testing
    # print(f"letter count is: {letter_count(text)}")
    # print(f"word count is: {word_count(text)}")
    # print(f"sentence count is: {sentence_count(text)}")
    # Letter = letter_count(text)
    # Word = word_count(text)
    # Sent = sentence_count(text)
    # print(Letter)
    # print(Word)
    # print(Sent)
    # print(S)
    # print(L)
    
    # mathematical formulas
    S = (sentence_count(text) / word_count(text)) * 100
    L = (letter_count(text) / word_count(text)) * 100
    # Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    if (grade < 1):
        print("Before Grade 1")
    elif (grade >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {grade}")

# define other functions
# counts letters


def letter_count(text):
    l = list([val for val in text
              if val.isalpha()])
    lString = "".join(l)
    lCount = len(lString)
    return lCount

# counts words


def word_count(text):
    w = text.split()
    wLength = len(w)
    return wLength
# counts sentences


def sentence_count(text):
    periodCount = text.count(".")
    bangCount = text.count("!")
    questionCount = text.count("?")
    total = periodCount + bangCount + questionCount 
    return total


main()

