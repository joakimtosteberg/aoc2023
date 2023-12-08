import sys
import re

maze = {}

r = re.compile(r'^([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)')
with open(sys.argv[1]) as f:
    sequence = f.readline().strip()
    f.readline()
    for line in f:
        m = r.match(line)
        maze[m.group(1)] = { 'L': m.group(2),
                             'R': m.group(3) }

maze_pos = 'AAA'
sequence_pos = 0
steps = 0
while maze_pos != 'ZZZ':
    maze_pos = maze[maze_pos][sequence[sequence_pos]]
    sequence_pos = (sequence_pos + 1) % len(sequence)
    steps += 1

print(f"Reached ZZZ in {steps} steps")
