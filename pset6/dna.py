from csv import reader, DictReader
from sys import argv, exit
import re

def main():
    strs = openFiles()
    counts = getCounts(strs)
    comp = IsMatchFound(counts)
    
    # print(strs)
    # print(counts)
    print(comp)

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
    array = []

    # Open txt
    txtFile = open(argv[2], 'r')
    txt = txtFile.read()

    # Loop through strs
    for i in range(len(strs)):
        Phrase1 = (strs[i])

        # Count number of times Phrase 1 repeats in txt
        counter = 0
        txtPosition = 0
        position = 0
        done = False

        while(done == False):
            # Finds the position of x
            position = txt.find(Phrase1, txtPosition)
            # find method should return -1 if not found
            if(position == -1):
                # Stop loop
                done = True
                # Append number to the new array
                array.append(counter)
            else:
                 # Increment by 1
                counter += 1
                # Start looking at the new starting position
                txtPosition = position + len(Phrase1)
    
    return array


def IsMatchFound(counts):
    
    # Open csv
    with open(argv[1], 'r') as csvFile:
        csvTable = reader(csvFile, delimiter=',')
        
        #[4,1,5]
        x = 0


        
        for j in csvTable:
        # name,AGATC,AATG,TATC
        # Alice,2,8,3
        # Bob,4,1,5
        # Charlie,3,2,5
            if (len(j) == 4):
                #use x to skip the first row in csvTable, don't need it.
                x += 1
                if (x > 1):
                        
                    if (int(j[1]) == counts[0]):
                        if (int(j[2]) == counts[1]):
                            if (int(j[3]) == counts[2]):
                                print(j[0])
        
                                return True
            elif (len(j) == 9):
                x += 1
                if (x > 1):
                        
                    if (int(j[1]) == counts[0]):
                        if (int(j[2]) == counts[1]):
                            if (int(j[3]) == counts[2]):
                                if (int(j[4]) == counts[3]):
                                    if (int(j[5]) == counts[4]):
                                        if (int(j[6]) == counts[5]):
                                            if (int(j[7]) == counts[6]):
                                                if (int(j[8]) == counts[7]):
                                                    print(j[0])
                                                    return True

    print("no match")                     
    return False
main()