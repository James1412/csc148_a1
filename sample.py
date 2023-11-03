import csv

class Person:
    start: int
    target: int
    def __init__(self, start, target):
        self.start = start
        self.target = target

arrival_data = {}

with open("data/sample_arrivals.csv") as csvfile:
    reader = csv.reader(csvfile)
    i = 1
    for line in reader:
        start = []
        target = []
        round_num = int(line[0])
        people = []
        for j in range(1, len(line), 2):
            start.append(line[j])
        for k in range(2, len(line), 2):
            target.append(line[k])
        for start_item, target_item in zip(start, target):
            new_person = Person(start_item, target_item)
        people.append(new_person)
        arrival_data[round_num] = people

sorted_arrival_data = {
    k: arrival_data[k]
    for k in sorted(arrival_data)
}

print(sorted_arrival_data.values())
