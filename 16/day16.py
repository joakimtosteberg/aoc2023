import sys

cave_map = {}

width = 0
height = 0
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            cave_map[(x,y)] = c
            x += 1
        if y == 0:
            width = x
        y += 1
    height = y


def create_beam(position, direction):
    return {'pos': position, 'dir': direction}
    
beams = [create_beam((-1,0),(1,0))]
def print_cave(cave_map, width, height, beams):
    for y in range(height):
        for x in range(width):
            for beam in beams:
                if beam['pos'] == (x,y):
                    print('#', end='')
                    break
            else:
                print(cave_map[(x,y)], end='')
        print()
    print()

def step_beam(cave_map, beam):
    beams = []
    beam['pos'] = (beam['pos'][0] + beam['dir'][0], beam['pos'][1] + beam['dir'][1])
    if beam['pos'] not in cave_map:
        return beams

    if cave_map[beam['pos']] == '/':
        beam['dir'] = (-beam['dir'][1], -beam['dir'][0])
        beams.append(beam)
    elif cave_map[beam['pos']] == '\\':
        beam['dir'] = (beam['dir'][1], beam['dir'][0])
        beams.append(beam)
    elif cave_map[beam['pos']] == '|':
        if beam['dir'][0]:
            beams.append(create_beam(beam['pos'], (0,1)))
            beams.append(create_beam(beam['pos'], (0,-1)))
        else:
            beams.append(beam)
    elif cave_map[beam['pos']] == '-':
        if beam['dir'][1]:
            beams.append(create_beam(beam['pos'], (1,0)))
            beams.append(create_beam(beam['pos'], (-1,0)))
        else:
            beams.append(beam)
    elif cave_map[beam['pos']] == '.':
        beams.append(beam)

    return beams
            

def step_beams(cave_map, beams):
    new_beams = []
    for beam in beams:
        new_beams.extend(step_beam(cave_map, beam))
    return new_beams

def save_beams(beams, states):
    new_beams = []
    for beam in beams:
        if beam['pos'] not in states:
            states[beam['pos']] = set()
        if beam['dir'] in states[beam['pos']]:
            continue
        states[beam['pos']].add(beam['dir'])
        new_beams.append(beam)
            
    return new_beams
        

def run_beams(cave_map, beams):
    states = {}
    while beams:
        beams = step_beams(cave_map, beams)
        beams = save_beams(beams, states)
    return states

states = run_beams(cave_map, beams)
print(f"part1: {len(states)}")

max_energized = 0
for x in range(width):
    beams = [create_beam((x,-1),(0,1))]
    states = run_beams(cave_map, beams)
    max_energized = max(max_energized, len(states))

    beams = [create_beam((x,height),(0,-1))]
    states = run_beams(cave_map, beams)
    max_energized = max(max_energized, len(states))

for y in range(height):
    beams = [create_beam((-1,y),(1,0))]
    states = run_beams(cave_map, beams)
    max_energized = max(max_energized, len(states))

    beams = [create_beam((width,y),(-1,0))]
    states = run_beams(cave_map, beams)
    max_energized = max(max_energized, len(states))

print(f"part2: {max_energized}")
