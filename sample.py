import csv

arrival_data = {}

with open("data/sample_arrivals.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        print(line)
