import sys
import re

seeds = []
maps = {}
with open(sys.argv[1]) as f:
    for seed in f.readline().strip().split():
        if seed.isnumeric():
            seeds.append(int(seed))
    map_re = re.compile(r"(.*)-to-(.*) map:")
    cur = None
    for line in f:
        data = line.strip()
        if not data:
            continue
        m = map_re.match(data)
        if m:
            maps[m.group(1)] = {'to': m.group(2), 'mappings': []}
            cur = maps[m.group(1)]
        else:
            mappings = data.split()
            cur['mappings'].append({'dst': int(mappings[0]),
                                    'src': int(mappings[1]),
                                    'len': int(mappings[2])})

def get_next(mappings, value):
    for mapping in mappings:
        if value >= mapping['src'] and value < mapping['src'] + mapping['len']:
            return mapping['dst'] + value - mapping['src']
    return value

lowest = None
for seed in seeds:
    cur_type = 'seed'
    value = seed
    while cur_type in maps:
        value = get_next(maps[cur_type]['mappings'], value)
        cur_type = maps[cur_type]['to']

    lowest = value if lowest is None else min(lowest, value)

    print(f"{seed} => {value}")

print(f"lowest: {lowest}")
