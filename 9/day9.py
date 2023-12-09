import itertools
import sys

def create_difference(history):
    differences = []
    for i in range(len(history) - 1):
        differences.append(history[i+1] - history[i])
    return differences

def get_differences(values):
    differences = []
    while True:
        values = create_difference(values)
        differences.append(values)
        if all(value == 0 for value in values):
            return differences

def predict(history, differences, reverse = False):
    value = 0
    for difference in reversed(differences):
        if reverse:
            value = difference[0] - value
        else:
            value = value + difference[-1]

    if reverse:
        return history[0] - value
    else:
        return value + history[-1]

histories = []
with open(sys.argv[1]) as f:
    for line in f:
        history = [int(n) for n in line.split()]
        histories.append({'history': history,
                          'differences': get_differences(history)})

prediction_sum = 0
for history in histories:
    prediction = predict(history['history'], history['differences'])
    prediction_sum += prediction

print(f"part1: {prediction_sum}")

prediction_sum = 0
for history in histories:
    prediction = predict(history['history'], history['differences'], True)
    prediction_sum += prediction

print(f"part2: {prediction_sum}")
