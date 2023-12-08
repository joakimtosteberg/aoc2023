import sys
import re

maze = {}

r = re.compile(r'^([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)')
with open(sys.argv[1]) as f:
    sequence = f.readline().strip()
    f.readline()
    for line in f:
        m = r.match(line)
        maze[m.group(1)] = { 'L': m.group(2),
                             'R': m.group(3)}


sequence_pos = 0
steps = 0

def get_cycle(node, sequence, maze):
    sequence_pos = 0
    steps = 0
    track = {node: {0: 0}}
    end_steps = None
    while True:
        node = maze[node][sequence[sequence_pos]]
        sequence_pos = (sequence_pos + 1) % len(sequence)
        if node in track and sequence_pos in track[node]:
            return end_steps, steps - track[node][sequence_pos] + 1

        steps += 1
        if node[2] == 'Z':
            end_steps = steps
        if not node in track:
            track[node] = {}
        
        track[node][sequence_pos] = steps


cycles = []

max_start = 0
length = 0
found_cycle = {'start': 0}
for node in maze:
    if node[2] == 'A':
        cycle_start, cycle_length = get_cycle(node, sequence, maze)
        cycle = {'start': cycle_start,
                 'length': cycle_length}
        if cycle['start'] > found_cycle['start']:
            found_cycle = cycle
        cycles.append(cycle)

cycles.remove(found_cycle)


def eliminate_one(cycles, found_cycle):
    loops = 0
    for cycle in cycles:
        cycle['end'] = None

    while True:
        done = False
        for cycle in cycles:
            cycle_pos = found_cycle['start'] - cycle['start'] + found_cycle['length'] * loops
            cycle_pos = cycle_pos % cycle['length']

            if cycle_pos == 0:
                if cycle['end'] is not None:
                    done = cycle
                    break
                else:
                    cycle['end'] = loops

        if done:
            cycles.remove(done)
            return cycles, {'start': found_cycle['start'] + done['end'] * found_cycle['length'], 'length': (loops-done['end']) * found_cycle['length']}
        loops += 1

while cycles:
    cycles, found_cycle = eliminate_one(cycles, found_cycle)

print(found_cycle['start'])
