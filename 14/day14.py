import sys

rock_map = {}
width = 0
height = 0
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            rock_map[(x,y)] = c
            x = x + 1
        width = x
        y = y + 1
    height = y

def tilt(rock_map, width, height, direction):
    if direction == 'N':
        pos = (0,1)
        step_delta = (1,0)
        row_delta = (0,1)
        delta_stone = (0,-1)
    elif direction == 'S':
        pos = (0,height-2)
        step_delta = (1,0)
        row_delta = (0,-1)
        delta_stone = (0,1)
    elif direction == 'E':
        pos = (width-2,0)
        step_delta = (0,1)
        row_delta = (-1,0)
        delta_stone = (1,0)
    elif direction == 'W':
        pos = (1,0)
        step_delta = (0,1)
        row_delta = (1,0)
        delta_stone = (-1,0)

    while pos in rock_map:
        while pos in rock_map:
            next_pos = (pos[0]+delta_stone[0],pos[1]+delta_stone[1])
            steps = 0
            if rock_map[pos] == 'O':
                while next_pos in rock_map and rock_map[next_pos] == '.':
                    next_pos = (next_pos[0]+delta_stone[0],next_pos[1]+delta_stone[1])
                    steps += 1
                if steps:
                    rock_map[pos] = '.'
                    rock_map[(pos[0]+delta_stone[0]*steps, pos[1]+delta_stone[1]*steps)] = 'O'
            pos = (pos[0] + step_delta[0], pos[1] + step_delta[1])
        step_delta = (-step_delta[0], -step_delta[1])
        pos = (pos[0] + step_delta[0] + row_delta[0], pos[1] + step_delta[1] + row_delta[1])

def get_load(rock_map, width, heigth):
    load = 0
    for y in range(height):
        for x in range(width):
            if rock_map[(x,y)] == 'O':
                load += height - y
    return load

def print_map(rock_map, widht, height):
    for y in range(height):
        for x in range(width):
            print(rock_map[(x,y)], end='')
        print()
    print()
    print()

def run_cycle(rock_map, width, height, first=False):
    tilt(rock_map, width, height, 'N')
    if first:
        print(f"part1: {get_load(rock_map, width, height)}")
    tilt(rock_map, width, height, 'W')
    tilt(rock_map, width, height, 'S')
    tilt(rock_map, width, height, 'E')

def to_state(rock_map, width, height):
    state = ""
    for y in range(height):
        for x in range(width):
            state += rock_map[(x,y)]
        state += "\n"
    return state

def to_map(state):
    y = 0
    rock_map = {}
    for line in state.split('\n'):
        x = 0
        for c in line.strip():
            rock_map[(x,y)] = c
            x = x + 1
        y = y + 1
    return rock_map


cycles = 1000000000
states = {}

states[to_state(rock_map, width, height)] = 0
run_cycle(rock_map, width, height, True)
states[to_state(rock_map, width, height)] = 1
for i in range(2,cycles+1):
    run_cycle(rock_map, width, height)
    state = to_state(rock_map, width, height)
    if state in states:
        print(f"Found loop after iteration {i}")
        iteration_start = states[state]
        iteration_end = i
        break
    states[state] = i

cycle_len = (iteration_end - iteration_start)
final_cycle = iteration_start + (cycles - iteration_start) % cycle_len

for state, iteration in states.items():
    if iteration == final_cycle:
        final_state = state
        break

final_map = to_map(final_state)
print(f"part2: {get_load(final_map, width, height)}")
