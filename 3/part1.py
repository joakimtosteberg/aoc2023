import sys

numbers = {}

symbols = {}

with open(sys.argv[1]) as f:
    pos = (0,0)
    for line in f:
        number_pos = None
        for c in line.strip():
            if c.isdigit():
                if number_pos:
                    numbers[number_pos] += c
                else:
                    number_pos = pos
                    numbers[number_pos] = c
            elif c != '.':
                number_pos = None
                symbols[pos] = c
            else:
                number_pos = None
            pos = (pos[0] + 1, pos[1])

        pos = (0, pos[1] + 1)


def adjacent_to_symbol(start_pos, number, symbols):
    for y in range(start_pos[1] - 1, start_pos[1] + 2):
        for x in range(start_pos[0] - 1, start_pos[0] + len(number) + 1):
            if (x,y) in symbols:
                return True
    return False

part_sum = 0
for pos, number in numbers.items():
    if adjacent_to_symbol(pos, number, symbols):
        part_sum += int(number)

print(part_sum)
