import sys
import re

regexp = re.compile(r"^Card\s+(\d+):\s+(.*)\s+\|\s+(.*)$")
points = 0
with open(sys.argv[1]) as f:
    for line in f:
        m = regexp.match(line)
        card = int(m.group(1))
        winning = set([int(number) for number in m.group(2).split()])
        card_numbers = set([int(number) for number in m.group(3).split()])
        winners = (card_numbers & winning)
        if winners:
            points += (2**(len(winners) - 1))

print(points)
