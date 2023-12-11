import sys

galaxies = []
empty_rows = set()
empty_columns = set()
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        empty_row = True
        for c in line.strip():
            if y == 0 and x not in empty_columns:
                empty_columns.add(x)
            if c == '#':
                empty_row = False
                galaxies.append((x,y))
                empty_columns.discard(x)
            x += 1
        if empty_row:
            empty_rows.add(y)
        y += 1


def get_distance(g1, g2, empty_rows, empty_columns, growth_factor):
    x_min = min(g1[0], g2[0])
    x_max = max(g1[0], g2[0])
    y_min = min(g1[1], g2[1])
    y_max = max(g1[1], g2[1])

    dist = 0
    for x in range(x_min, x_max):
        dist += 1
        if x in empty_columns:
            dist += (growth_factor-1)

    for y in range(y_min, y_max):
        dist += 1
        if y in empty_rows:
            dist += (growth_factor-1)

    return dist

total_dist = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        total_dist += get_distance(galaxies[i], galaxies[j], empty_rows, empty_columns, 2)

print(f"part1: {total_dist}")

total_dist = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        total_dist += get_distance(galaxies[i], galaxies[j], empty_rows, empty_columns, 1000000)

print(f"part2: {total_dist}")
