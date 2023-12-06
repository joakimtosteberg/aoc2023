import sys

with open(sys.argv[1]) as f:
    time = int(''.join(f.readline().split(':')[1].split()))
    best_distance = int(''.join(f.readline().split(':')[1].split()))

last_winner_float = time/2 + ((-time/2)**2 - best_distance)**0.5
first_winner_float = time/2 - ((-time/2)**2 - best_distance)**0.5

first_winner = int(first_winner_float+1)
last_winner = int(last_winner_float)
winners = last_winner - first_winner + 1
print(winners)


## Slow solution
# winners = 0
# for i in range(1,time):
#     distance = i*(time-i)
#     if distance > best_distance:
#         winners += 1

# print(winners)
