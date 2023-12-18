import re
import sys

r = re.compile(r"(.) ([0-9]+) \(#(.*)\)")
holes1 = []
holes2 = []

def get_delta(direction):
    if direction in ['U', '3']:
        return (0,-1)
    elif direction in ['D', '1']:
        return (0,1)
    elif direction in ['L', '2']:
        return (-1,0)
    elif direction in ['R', '0']:
        return (1,0)
    
with open(sys.argv[1]) as f:
    for line in f:
        m = r.match(line)
        holes1.append({'dir': get_delta(m.group(1)),
                       'size': int(m.group(2))})
        holes2.append({'dir': get_delta(m.group(3)[5]),
                       'size': int(m.group(3)[0:5], 16)})


def sholace_area(holes):
    pos = (0,0)
    double_area = 2
    for hole in holes:
        next_pos = (pos[0] + hole['dir'][0] * hole['size'], pos[1] + hole['dir'][1] * hole['size'])
        double_area += pos[0]*next_pos[1] - pos[1]*next_pos[0] + hole['size']
        pos = next_pos
    return int(double_area / 2)

print(f"part1: {sholace_area(holes1)}")
print(f"part2: {sholace_area(holes2)}")
