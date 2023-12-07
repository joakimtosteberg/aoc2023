import sys

hands = {}

cards = {
    'A': 'M',
    'K': 'L',
    'Q': 'K',
    'T': 'J',
    '9': 'I',
    '8': 'H',
    '7': 'G',
    '6': 'F',
    '5': 'E',
    '4': 'D',
    '3': 'C',
    '2': 'B',
    'J': 'A'
}

def get_count_with_joker(values):
    
    pass

def get_type(hand):
    counts = {card: 0 for card in cards}
    jokers = 0
    for c in hand:
        if c == 'J':
            jokers += 1
        else:
            counts[c] += 1
    counts = dict(sorted(counts.items(), key=lambda e: (e[1]), reverse=True))
    keys = list(counts.keys())
    values = list(counts.values())
    if values[0] + jokers == 5:
        return 6
    if values[0] + jokers == 4:
        return 5
    if values[0] + jokers == 3:
        if values[1] == 2:
            return 4
        return 3
    if values[0] + jokers == 2:
        if values[1] == 2:
            return 2
        return 1
    return 0

def get_strength(hand):
    strength = ""
    for c in hand:
        strength += cards[c]

    return strength

with open(sys.argv[1]) as f:
    for line in f:
        hand = line.split()
        hands[hand[0]] = {'bid': int(hand[1]),
                          'type': get_type(hand[0]),
                          'strength': get_strength(hand[0])}

ranked_hands = sorted(hands.items(), key=lambda e: (e[1]['type'],
                                                    e[1]['strength']))

total_winnings = 0
for i in range(len(ranked_hands)):
    winnings = (i+1) * ranked_hands[i][1]['bid']
    total_winnings += winnings
print(total_winnings)
