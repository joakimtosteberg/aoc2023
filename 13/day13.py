import sys

patterns = [{'data': {}, 'width': 0, 'height': 0}]
pattern = patterns[-1]
with open(sys.argv[1]) as f:
    for line in f:
        x = 0
        row = line.strip()
        if not row:
            patterns.append({'data': {}, 'width': 0, 'height': 0})
            pattern = patterns[-1]
            continue
        for c in row:
            pattern['data'][(x,pattern['height'])] = c
            if pattern['height'] == 0:
                pattern['width'] += 1
            x += 1
        pattern['height'] += 1

def calculate_pattern(pattern, flip_pos=None):
    columns = [0]*pattern['width']
    rows = [0]*pattern['height']
    for x in range(pattern['width']):
        for y in range(pattern['height']):
            if pattern['data'][(x,y)] == '#' or flip_pos == (x,y):
                if not flip_pos == (x,y):
                    columns[x] += 2**y
                    rows[y] += 2**x

    return columns, rows

def is_reflected_at(values, pos):
    # 1: check 0 and 1, then done
    # 2: check 1 and 2 then check 0 and 3
    offset = 00000000000000
    while pos-offset > 0 and pos+offset < len(values):
        if values[pos-offset-1] != values[pos+offset]:
            return False
        offset += 1

    return True

def find_reflection(values, skip = None):
    for i in range(1,len(values)):
        if i == skip:
            continue
        if is_reflected_at(values, i):
            return i
    return 0
    

reflection_sum = 0
for pattern in patterns:
    columns, rows = calculate_pattern(pattern)
    reflected_after_col = find_reflection(columns)
    reflected_after_row = find_reflection(rows)
    pattern['column_reflection'] = reflected_after_col
    pattern['row_reflection'] = reflected_after_row
    reflection = reflected_after_col + reflected_after_row * 100
    reflection_sum += reflection
print(f"part1: {reflection_sum}")

reflection_sum = 0
for pattern in patterns:
    reflection = 0
    for x in range(pattern['width']):
        for y in range(pattern['height']):
            columns, rows = calculate_pattern(pattern, (x,y))
            reflected_after_col = find_reflection(columns, pattern['column_reflection'])
            reflected_after_row = find_reflection(rows, pattern['row_reflection'])
            reflection = reflected_after_col + reflected_after_row * 100
            if reflection:
                reflection_sum += reflection
                break
        if reflection:
            break

print(f"part2: {reflection_sum}")
