import sys

network = {}
start = None
width = 0
height = 0
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            connections = []
            if c == '|':
                connections.extend([(x, y+1), (x,y-1)])
            elif c == '-':
                connections.extend([(x+1, y), (x-1,y)])
            elif c == 'L':
                connections.extend([(x+1, y), (x,y-1)])
            elif c == 'J':
                connections.extend([(x-1, y), (x,y-1)])
            elif c == '7':
                connections.extend([(x-1, y), (x,y+1)])
            elif c == 'F':
                connections.extend([(x+1, y), (x,y+1)])
            elif c == 'S':
                start = (x,y)
                connections.extend([(x+1, y), (x-1,y),(x,y+1),(x,y-1)])

            network[(x,y)] = connections
            x += 1

        y += 1
    width = x
    height = y


def search(network, start_position):
    track = {}
    next_positions = [start_position]
    while next_positions:
        positions = next_positions
        next_positions = []
        for pos in positions:
            for next_pos in network[pos['cur']]:
                # Avoid going backwards or outside map
                if next_pos not in network or next_pos == pos['prev']:
                    continue

                # Pipe not connecting to another pipe
                if pos['cur'] not in network[next_pos]:
                    continue

                # Found loop, done
                if next_pos in track:
                    return {'track': track, 'end1': pos['cur'], 'end2': next_pos}

                track[next_pos] = pos['cur']
                next_positions.append({'cur': next_pos, 'prev': pos['cur']})
    
result = search(network, {'cur': start, 'prev': start})


loop = [start]

pos = result['end1']
network[start] = []
while True:
    loop.append(pos)
    if result['track'][pos] == start:
        network[start].append(pos)
        break
    pos = result['track'][pos]

pos = result['end2']
while True:
    loop.append(pos)
    if result['track'][pos] == start:
        network[start].append(pos)
        break
    pos = result['track'][pos]

print(f"part1: {int(len(loop) / 2)}")

def floodfill(start_pos, area_map, width, height, loop, area_id):
    size = 1
    next_positions = [start_pos]
    area_map[start_pos] = area_id
    inside = True
    while next_positions:
        positions = next_positions
        next_positions = []
        for pos in positions:
            for step in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0]+step[0],pos[1]+step[1])
                if next_pos in area_map:
                    continue

                if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= width or next_pos[1] >= height:
                    inside = False
                    continue

                if next_pos not in loop:
                    area_map[next_pos] = area_id
                    if next_pos[0] % 2 == 0 and next_pos[1] % 2 == 0:
                        size += 1
                    next_positions.append(next_pos)
                else:
                    area_map[next_pos] = '.'
                    
    return {'size': size, 'inside': inside}

padded_loop = set()
for pos in loop:
    new_pos = (pos[0]*2, pos[1]*2)
    padded_loop.add(new_pos)
    for connection in network[pos]:
        new_connection = (pos[0]+connection[0],pos[1]+connection[1])
        padded_loop.add(new_connection)


padded_width = width*2 - 1
padded_height = height*2 - 1

def print_loop(loop, width, height, padded):
    for y in range(height):
        for x in range(width):
            if (x,y) in loop:
                print('.', end='')
            elif padded and (x%2==1 or y%2==1):
                print(' ', end='')
            else:
                print('#', end='')
        print()

#print_loop(loop, width, height, False)
#print()
#print_loop(padded_loop, width*2-1, height*2-1, True)


area_map = {}
area_sizes = {}
area_id = 0
for pos in network:
    padded_pos = (pos[0]*2, pos[1]*2)
    if padded_pos in padded_loop:
        continue

    if padded_pos not in area_map:
        area_sizes[area_id] = floodfill(padded_pos, area_map, padded_width, padded_height, padded_loop, area_id)
        area_id += 1


def print_map(area_map, width, height):
    for y in range(0,height,2):
        for x in range(0,width,2):
            print(area_map[(x,y)] if (x,y) in area_map else ' ', end='')
        print()

#print_map(area_map, width*2-1, height*2-1)
inside_area = 0
for item in area_sizes.values():
    if item['inside']:
        inside_area += item['size']
print(f"part2: {inside_area}")
