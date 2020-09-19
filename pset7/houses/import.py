import sys
import csv
from cs50 import SQL


# Error checking
if len(sys.argv) != 2:
    exit(1)

# Open CSV
with open(sys.argv[1], 'r') as data:
    # Create DictReader
    reader = csv.DictReader(data)
    # Iterate over CSV file
    for row in reader:

        # Parse name
        # If middle name does not exist in CSV file
        if(len(row["name"].split()) == 2):
            first = row["name"].split()[0]
            last = row["name"].split()[1]
            middle = None

            # Testing

            # print(first)
            # print(last)
            # print(middle)
            # row.update({"name": first + ' ' +  middle + ' ' + last})
            # print(row["name"])

        else:
            # If middle name does exist in CSV file
            first = row["name"].split()[0]
            last = row["name"].split()[2]
            middle = row["name"].split()[1]

        # Testing

        # print(first)
        # print(last)
        # print(middle)

        # Create database connection
        db = SQL("sqlite:///students.db")

        # Insert values into database
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", first, middle, last, row["house"], row["birth"])