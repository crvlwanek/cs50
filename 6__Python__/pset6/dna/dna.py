import sys
import csv

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py database.csv sequence.txt")

database = sys.argv[1]
with open(database) as file:
    db_data = [row for row in csv.DictReader(file)]

sequence = sys.argv[2]
with open(sequence) as file:
    seq_data = file.read()

counts = {}
for key in db_data[0].keys():
    if key == 'name':
        continue
    most = 1
    while key * most in seq_data:
        most += 1
    counts[key] = str(most - 1)

found = False
for row in db_data:
    name = row.pop('name')
    if row.items() == counts.items():
        found = True
        print(name)
        break

if not found:
    print("No match")