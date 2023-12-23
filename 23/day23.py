import sys

trails = {}

with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            trails[(x,y)] = c
            x += 1
        if y == 0:
            width = x
        y += 1
height = y

start = (1,0)
end = (width-2, height-1)

slopes = {'<': (-1,0),
          '>': (1,0),
          '^': (0,-1),
          'v': (0,1)}

def possible_step(pos, step, next_pos, trails, ignore_slopes):
    if not next_pos in trails or trails[next_pos] == '#':
        return False

    if not ignore_slopes and trails[pos] in slopes and step != slopes[trails[pos]]:
        return False

    return True

def find_longest_path_acyclic(trails, start, end, ignore_slopes):
    states = {}
    for pos, trail in trails.items():
        if trail != '#':
            states[pos] = {'cost': 0, 'parent': None}

    next_positions = [start]
    cost = 0
    while next_positions:
        positions = next_positions
        next_positions = []
        cost += 1
        for pos in positions:
            for step in [(1,0),(-1,0),(0,1),(0,-1)]:
                next_pos = (pos[0]+step[0],pos[1]+step[1])
                if not possible_step(pos, step, next_pos, trails, ignore_slopes):
                    continue

                if next_pos == states[pos]['parent']:
                    continue

                if cost < states[next_pos]['cost']:
                    continue

                states[next_pos]['cost'] = cost
                states[next_pos]['parent'] = pos
                if next_pos == end:
                    continue
                next_positions.append(next_pos)

    return states[end]['cost']

print(f"part1: {find_longest_path_acyclic(trails, start, end, ignore_slopes=False)}")

def is_vertice(trails, pos, start, end):
    if pos in [start, end]:
        return True

    connectivity = 0
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        next_pos = (pos[0]+step[0],pos[1]+step[1])
        if next_pos in trails and trails[next_pos] != '#':
            connectivity += 1

    return connectivity > 2

def find_vertices(trails, start, end):
    vertices = set()
    for pos in trails:
        if trails[pos] != '#':
            if is_vertice(trails, pos, start, end):
                vertices.add(pos)
    return vertices

def build_edges(trails, vertice, vertices, edges):
    next_positions = [vertice]
    cost = 0
    visited = set(next_positions)
    while next_positions:
        positions = next_positions
        next_positions = []
        cost += 1
        for pos in positions:
            for step in [(1,0),(-1,0),(0,1),(0,-1)]:
                next_pos = (pos[0]+step[0],pos[1]+step[1])
                if next_pos not in trails or trails[next_pos] == '#':
                    continue
                if next_pos in visited:
                    continue
                if next_pos in vertices:
                    edges[vertice].append({'vertice': next_pos, 'cost': cost})
                    break

                visited.add(next_pos)
                next_positions.append(next_pos)


def find_edges(trails, vertices):
    edges = {}
    for vertice in vertices:
        edges[vertice] = []
        build_edges(trails, vertice, vertices, edges)
    return edges

def dfs(vertices, edges, vertice, end, path):
    best_cost = 0
    path.add(vertice)
    for edge in edges[vertice]:
        if edge['vertice'] in path:
            continue

        if edge['vertice'] == end:
            best_cost = max(best_cost, edge['cost'])
            continue

        cost = dfs(vertices, edges, edge['vertice'], end, path)
        if cost:
            best_cost = max(cost + edge['cost'], best_cost)

    path.remove(vertice)
    return best_cost

def find_longest_path_dfs(vertices, edges, start, end):
    path = set()
    return dfs(vertices, edges, start, end, path)

vertices = find_vertices(trails, start, end)
edges = find_edges(trails, vertices)

print(f"part2: {find_longest_path_dfs(vertices, edges, start, end)}")
