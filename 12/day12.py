import sys

states = []

with open(sys.argv[1]) as f:
    for line in f:
        pair = line.split()
        springs = pair[0]
        groups = [int(group) for group in pair[1].split(',')]
        sequences = [{'type': springs[0], 'len': 0}]
        for c in springs:
            if sequences[-1]['type'] == c:
                sequences[-1]['len'] += 1
            else:
                sequences.append({'type': c, 'len': 1})

        
        states.append({'sequences': sequences, 'groups': groups, 'springs': springs})

def group_fits_at(group, springs, start_pos):
    if start_pos + group > len(springs):
        return False

    for pos in range(start_pos + 1, start_pos + group):
        if springs[pos] not in ['#', '?']:
            return False

    if start_pos + group == len(springs):
        return True

    return springs[start_pos + group] in ['.', '?']
        
def find_permutations(springs, groups, dp, start_pos = 0):
    dp_pair = (start_pos, len(groups))
    if dp_pair in dp:
        return dp[dp_pair]
    if not groups:
        for c in springs[start_pos:]:
            if c == '#':
                return 0
        return 1

    group = groups[0]
    permutations = 0
    for pos in range(start_pos,len(springs)):
        if springs[pos] == '.':
            continue
        if group_fits_at(group, springs, pos):
            permutations += find_permutations(springs, groups[1:], dp, pos+group+1)
        if springs[pos] == '#':
            break

    dp[dp_pair] = permutations
    return permutations

total_permutations = 0
for state in states:
    total_permutations += find_permutations(state['springs'], state['groups'], {})
print(f"part1: {total_permutations}")

total_permutations = 0
for state in states:
    total_permutations += find_permutations(((state['springs'] + '?') * 5)[:-1], state['groups'] * 5, {})
print(f"part2: {total_permutations}")
