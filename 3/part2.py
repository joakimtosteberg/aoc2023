import sys

numbers = {}

gears = {}

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
            elif c == '*':
                number_pos = None
                gears[pos] = c
            else:
                number_pos = None
            pos = (pos[0] + 1, pos[1])

        pos = (0, pos[1] + 1)


def adjacent_to_gear(start_pos, number, gear_pos):
    for y in range(start_pos[1] - 1, start_pos[1] + 2):
        for x in range(start_pos[0] - 1, start_pos[0] + len(number) + 1):
            if (x,y) == gear_pos:
                return True
    return False

gear_ratios = 0
for gear_pos in gears:
    num_adjacent = 0
    gear_ratio = 1
    for num_pos, number in numbers.items():
        if adjacent_to_gear(num_pos, number, gear_pos):
            gear_ratio *= int(number)
            num_adjacent += 1
    if num_adjacent == 2:
        gear_ratios += gear_ratio

print(gear_ratios)
