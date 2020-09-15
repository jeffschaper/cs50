from csv import reader, DictReader
from sys import argv, exit
import re


def main():
    strs = openFiles()
    counts = getCounts(strs)
    comp = IsMatchFound(counts)


# Step 1: Open files
def openFiles():
    # Error checking
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # Open csv
    with open(argv[1], 'r') as csvFile:
        csvTable = reader(csvFile, delimiter=',')

        # Test to make sure file was opened and read correctly
        for row in csvTable:
            # Break after printing first row
            break

        # Pop name column from the list
        row.pop(0)
    return row


# Pass return value of openfiles() and sequence txt
def getCounts(strs):

    # Declaring new array
    tempArray = []
    compArray = []

    # Open txt
    txtFile = open(argv[2], 'r')
    txt = txtFile.read()

    # Loop through strs
    for i in range(len(strs)):
        Phrase1 = (strs[i])

        # Count number of times Phrase 1 repeats in txt
        counter = 0
        nextPosition = 0
        foundPosition = 0
        done = False

        while(done == False):
            # Finds the position of Phrase1
            foundPosition = txt.find(Phrase1, nextPosition)
            # next position to start looking, not next found position
            nextPosition = foundPosition + len(Phrase1)
            foundPhrase = txt[foundPosition:nextPosition]
            
            if(foundPosition == -1):
                done = True
                if not tempArray:
                    tempArray.append(0)
                else:
                    tempArray
                mx = max(tempArray)
                compArray.append(mx)
                tempArray.clear()
            # Problem starts here
            # It's double counting and not looping once a match is found
            elif(foundPhrase == Phrase1):
                # counter += 1
                # Once a match is found, loop until no match is found
                if(txt[foundPosition + len(Phrase1):nextPosition + len(Phrase1)] == Phrase1):
                    counter += 1
                # Problem ends here
                elif(txt[foundPosition + len(Phrase1):nextPosition + len(Phrase1)] != Phrase1):
                    counter += 1
                    tempArray.append(counter)
                    counter = 0                

    return compArray


def IsMatchFound(counts):

    # Open csv
    with open(argv[1], 'r') as csvFile:
        csvTable = reader(csvFile, delimiter=',')
        # Skips the heading row in csv file
        next(csvTable)

        for j in csvTable:
            # name,AGATC,AATG,TATC
            # Alice,2,8,3
            # Bob,4,1,5
            # Charlie,3,2,5
            z = 0
            successCount = 0
            for y in range(1, len(j)):
                # Problem: Only print name if ALL counts match and not just one in the list
                # If any of the counts match
                # If all of the counts match
                if (int(j[y]) == counts[z]):
                    z += 1
                    successCount += 1
                    if (successCount == len(j)-1):
                        print(j[0])
                        return True
        print("no match")
        return False


main()