import sys

hands = {}

def get_type(hand):
    counts = []
    for c in hand:
        counts.append(hand.count(c))
    counts.sort(reverse=True)
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3:
        if counts[3] == 2:
            return 4
        return 3
    if counts[0] == 2:
        if counts[2] == 2:
            return 2
        return 1
    return 0


strengths = {
    'A': 'M',
    'K': 'L',
    'Q': 'K',
    'J': 'J',
    'T': 'I',
    '9': 'H',
    '8': 'G',
    '7': 'F',
    '6': 'E',
    '5': 'D',
    '4': 'C',
    '3': 'B',
    '2': 'A'
}
def get_strength(hand):
    strength = ""
    for c in hand:
        strength += strengths[c]

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
