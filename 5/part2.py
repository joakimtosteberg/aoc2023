import sys
import re
from operator import itemgetter

seeds = []
maps = {}
with open(sys.argv[1]) as f:
    data = f.readline().strip().split()
    for i in range(1, len(data), 2):
        seeds.append({'start': int(data[i]), 'end': int(data[i]) + int(data[i+1])})
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
            dst_start = int(mappings[0])
            src_start = int(mappings[1])
            length = int(mappings[2])
            cur['mappings'].append({'dst_start': dst_start,
                                    'dst_end': dst_start + length,
                                    'src_start': src_start,
                                    'src_end': src_start + length,
                                    'remap': dst_start - src_start})

for value in maps.values():
    value['mappings'].sort(key=itemgetter('src_start'))


def map_values(values, mappings):
    new_values = []
    for value in sorted(values, key=itemgetter('start')):
        for mapping in mappings:
            start = max(value['start'], mapping['src_start'])
            end = min(value['end'], mapping['src_end'])
            if start > end:
                continue
            
            if start > value['start']:
                new_values.append({'start': value['start'],
                                   'end': start})

            new_values.append({'start': start + mapping['remap'],
                               'end': end + mapping['remap']})

            if end < value['end']:
                value = {'start': end,
                         'end': value['end']}
            else:
                value = None
                break
        if value:
            new_values.append(value)
            
    return new_values

values=seeds
cur_type='seed'
while cur_type in maps:
    values = map_values(values, maps[cur_type]['mappings'])
    cur_type = maps[cur_type]['to']
print(sorted(values, key=itemgetter('start'))[0]['start'])

