import re
import sys

bricks = []
bricks_by_id = {}
with open(sys.argv[1]) as f:
    r = re.compile("(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
    for line in f:
        m = r.match(line)
        x1,y1,z1,x2,y2,z2 = m.groups()

        brick = {'start': {'x': int(x1), 'y': int(y1), 'z': int(z1)},
                 'end': {'x': int(x2), 'y': int(y2), 'z': int(z2)},
                 'id': len(bricks)}
        bricks.append(brick)
        bricks_by_id[brick['id']] = brick

brick_map = {}
for brick in bricks:
    for x in range(brick['start']['x'], brick['end']['x'] + 1):
        for y in range(brick['start']['y'], brick['end']['y'] + 1):
            for z in range(brick['start']['z'], brick['end']['z'] + 1):
                brick_map[(x,y,z)] = brick['id']

def find_lowest_brick(bricks):
    lowest = None
    lowest_z = None
    for brick in bricks:
        if not lowest or brick['start']['z'] < lowest_z:
            lowest = brick
            lowest_z = brick['start']['z']
            
    return lowest

def check_plane(start1, end1, start2, end2):
    if end1 < start2 or start1 > end2:
        return False

    return True

def check_intersect(bricks, check_brick, current_z):
    if current_z == 0:
        return True

    for brick in bricks:
        if current_z < brick['start']['z'] or current_z > brick['end']['z']:
            continue

        if not check_plane(check_brick['start']['x'], check_brick['end']['x'], brick['start']['x'], brick['end']['x']):
            continue

        if not check_plane(check_brick['start']['y'], check_brick['end']['y'], brick['start']['y'], brick['end']['y']):
            continue

        return True

    return False

def try_lower(brick, brick_map, steps):
    if brick['start']['z']-steps == 0:
        return False

    for x in range(brick['start']['x'], brick['end']['x'] + 1):
        for y in range(brick['start']['y'], brick['end']['y'] + 1):
            if (x,y,brick['start']['z']-steps) in brick_map:
                return False

    return True

def do_lower(brick, brick_map, steps):
    for x in range(brick['start']['x'], brick['end']['x'] + 1):
        for y in range(brick['start']['y'], brick['end']['y'] + 1):
            for z in range(brick['start']['z'], brick['end']['z'] + 1):
                del brick_map[(x,y,z)]
                
    for x in range(brick['start']['x'], brick['end']['x'] + 1):
        for y in range(brick['start']['y'], brick['end']['y'] + 1):
            for z in range(brick['start']['z'] - steps, brick['end']['z'] - steps + 1):
                brick_map[(x,y,z)] = brick['id']

    brick['start']['z'] -= steps
    brick['end']['z'] -= steps


fallen_bricks = []
while bricks:
    brick = find_lowest_brick(bricks)
    bricks.remove(brick)

    decent = 1
    while try_lower(brick, brick_map, decent):
        decent += 1
    decent -= 1
    if decent:
        do_lower(brick, brick_map, decent)
    fallen_bricks.append(brick)

def calculate_support(brick, brick_map):
    supported_by = set()
    supports = set()
    for x in range(brick['start']['x'], brick['end']['x'] + 1):
        for y in range(brick['start']['y'], brick['end']['y'] + 1):
            if (x,y,brick['start']['z'] - 1) in brick_map:
                supported_by.add(brick_map[(x,y,brick['start']['z'] - 1)])
            if (x,y,brick['end']['z'] + 1) in brick_map:
                supports.add(brick_map[(x,y,brick['end']['z'] + 1)])
    brick['supported_by'] = supported_by
    brick['supports'] = supports

for brick in fallen_bricks:
    calculate_support(brick, brick_map)

def can_be_disintegrated(brick):
    for supported in brick['supports']:
        if len(bricks_by_id[supported]['supported_by']) == 1:
            return False

    return True

to_disintigrate = 0
for brick in fallen_bricks:
    if can_be_disintegrated(brick):
        to_disintigrate += 1

print(f"part1: {to_disintigrate}")

def check_disintigrate(start_brick, bricks_by_id):
    falls = 0
    to_check_next = [start_brick]
    fallen = set()
    while to_check_next:
        to_check = to_check_next
        to_check_next = []
        for brick in to_check:
            fallen.add(brick['id'])
            for supported in brick['supports']:
                remaining_supports = bricks_by_id[supported]['supported_by'] - fallen
                if not remaining_supports:
                    falls += 1
                    to_check_next.append(bricks_by_id[supported])

    return falls

total_falls = 0
for brick in fallen_bricks:
    total_falls += check_disintigrate(brick, bricks_by_id)
print(f"part2: {total_falls}")
