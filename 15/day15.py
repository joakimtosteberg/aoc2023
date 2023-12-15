import re
import sys

def calc_hash(string):
    hash_val = 0
    for c in string:
        hash_val += ord(c)
        hash_val *= 17
        hash_val %= 256
    return hash_val

with open(sys.argv[1]) as f:
    initialization_sequence = f.readline().strip().split(',')

hash_sum = 0
for init_val in initialization_sequence:
    hash_sum += calc_hash(init_val)
        
print(f"part1: {hash_sum}")


def remove_lens(box, label):
    for item in box:
        if item['label'] == label:
            box.remove(item)
            break

def add_lens(box, label, focal):
    for item in box:
        if item['label'] == label:
            item['focal'] = focal
            return
    box.append({'label': label, 'focal': focal})

boxes = [ [] for _ in range(256)]
r = re.compile("^(.*)(?:-|(?:=(.*)))")
for init_val in initialization_sequence:
    m = r.match(init_val)
    label = m.group(1)
    box = boxes[calc_hash(label)]
    focal = m.group(2)
    if focal is None:
        remove_lens(box, label)
    else:
        add_lens(box, label, int(focal))

total_focus_power = 0
for i in range(len(boxes)):
    box = boxes[i]
    for j in range(len(box)):
        lens = box[j]
        focus_power = (i+1)*(j+1)*lens['focal']
        total_focus_power += focus_power
        
print(f"part2: {total_focus_power}")
