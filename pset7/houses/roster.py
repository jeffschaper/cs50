import sys
from cs50 import SQL

# Error checking
if (len(sys.argv) != 2):
    exit(1)

db = SQL("sqlite:///students.db")
house = sys.argv[1]
results = db.execute("SELECT first, middle, last, house, birth FROM students WHERE house = ? ORDER BY last, first", house)

for row in results:
    updatedLast = row["last"] + ","
    # print(updatedLast)

    if (row["middle"] == None):
        print(row["first"], updatedLast, "born", row["birth"])
    else:
        print(row["first"], row["middle"], updatedLast, "born", row["birth"])