import sys

with open(sys.argv[1]) as f:
    times = [int(item) for item in f.readline().split()[1:]]
    distances = [int(item) for item in f.readline().split()[1:]]


races = []
for i in(range(len(times))):
    races.append({'time': times[i],
                  'distance': distances[i]})

margin = 1
for race in races:
    winners = 0
    for i in range(1,race['time']):
        distance = i*(race['time']-i)
        if distance > race['distance']:
            winners += 1
    margin *= winners
print(margin)
