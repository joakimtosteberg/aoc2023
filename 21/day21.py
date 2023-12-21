import sys

garden = {}
start = None

with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            if c == '.':
                garden[(x,y)] = '.'
            elif c == '#':
                garden[(x,y)] = '#'
            elif c == 'S':
                garden[(x,y)] = '.'
                start = (x,y)
            x += 1
        if y == 0:
            width = x
        y += 1
height = y

with open(sys.argv[1]) as f:
    for line in f:
        pass

garden_steps = {start: 0}

next_positions = [start]
num_steps = 1
wanted_steps = 64
odd = 0
even = 1
while next_positions:
    positions = next_positions
    next_positions = []
    for position in positions:
        for step in [(0,1),(0,-1),(1,0),(-1,0)]:
            next_position = (position[0]+step[0],position[1]+step[1])
            if next_position not in garden or garden[next_position] != '.' or next_position in garden_steps:
                continue
            garden_steps[next_position] = num_steps
            next_positions.append(next_position)

    if num_steps % 2 == 0:
        even += len(next_positions)
    else:
        odd += len(next_positions)

    if num_steps == wanted_steps:
        if num_steps % 2 == 0:
            print(f"part1: {even}")
        else:
            print(f"part1: {odd}")
        break

    num_steps += 1

next_positions = [start]
num_steps = 1
odd = 0
even = 1

garden_steps = {start: 0}
wanted_steps = 26501365
offset = wanted_steps % width
needed_steps = int((wanted_steps - offset) / width)

search_steps = set([offset, offset + width, offset + width * 2])
plots_visited = []

while True:
    positions = next_positions
    next_positions = []
    for position in positions:
        for step in [(0,1),(0,-1),(1,0),(-1,0)]:
            next_position = (position[0]+step[0], position[1]+step[1])
            inf_position = (next_position[0] % width, next_position[1] % height)
            if inf_position not in garden or garden[inf_position] != '.' or next_position in garden_steps:
                continue
            garden_steps[next_position] = num_steps
            next_positions.append(next_position)


    if num_steps % 2 == 0:
        even += len(next_positions)
    else:
        odd += len(next_positions)

    if num_steps in search_steps:
        search_steps.remove(num_steps)
        plots_visited.append(even if num_steps % 2 == 0 else odd)

    if not search_steps:
        break


    num_steps += 1


# f(x) = ax^2 + bx + c
# f(0) = c
# f(1) = a + b + c
# f(2) = 4a + 2b + c

# b = f(1) - a - c
# 4a = f(2) - 2b -c => a = f(2)/4 - b/2 - c/4

# b = f(1) - (f(2)/4 - b/2 - c/4) - c = f(1) - f(2)/4 + b/2 + c/4 - c
# b/2 = f(1) - f(2) / 4 - 3c/4
# b = 2*f(1) - f(2) / 2 - 3c/2 = (4*f(1)-f(2) - 3c) / 2

# a = f(1) - b - c

c = plots_visited[0]
b = int((4*plots_visited[1] - plots_visited[2] - 3*c) / 2)
a = plots_visited[1] - b - c


f = lambda x : a*x**2 + b*x + c
print(f"part2: {f(needed_steps)}")
