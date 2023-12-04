import sys
import re

regexp = re.compile(r"^Card\s+(\d+):\s+(.*)\s+\|\s+(.*)$")
points = 0

cards = {}
max_card_no = 0
with open(sys.argv[1]) as f:
    for line in f:
        m = regexp.match(line)
        card = int(m.group(1))
        winning = set([int(number) for number in m.group(2).split()])
        card_numbers = set([int(number) for number in m.group(3).split()])
        winners = (card_numbers & winning)
        cards[card] = {'count': 1, 'matching': len(winners)}
        max_card_no = card

for card_no in range(1,max_card_no + 1):
    card = cards[card_no]
    for copy_card_no in range(card_no + 1, card_no + 1 + card['matching']):
        if copy_card_no in cards:
            cards[copy_card_no]['count'] += card['count']

count = 0
for card in cards.values():
    count += card['count']

print(count)
