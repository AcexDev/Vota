poll = {
    "Java": 3,
    "Python": 15,
    "Javascript": 17,
    "C#": 2
}

total = 50
percentages = {
            choice : round(votes/total * 100) if total > 0 else 0 for choice, votes in poll.items()
        }

print(percentages)
print(round(2/3))

list_1 = [1,2,3,4]
list_2 = ["A", "B", "C", "D"]

for a, b in zip(list_1, list_2):
    print(f"{a}: {b}")