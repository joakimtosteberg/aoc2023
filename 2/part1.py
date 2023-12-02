import sys

contents = {'red': 12, 'green': 13, 'blue': 14}

possible_games = {}

with open(sys.argv[1]) as f:
    for line in f:
        data = line.split(':')
        game_id = int(data[0].split(' ')[1])
        possible_games[game_id] = True
        cube_sets = data[1].split(';')
        for cube_set in cube_sets:
            for cubes in cube_set.split(','):
                cube_info = cubes.strip().split(' ')
                amount = int(cube_info[0])
                color = cube_info[1]
                if amount > contents[color]:
                    possible_games[game_id] = False


game_sum = 0
for id, possible in possible_games.items():
    if possible:
        game_sum += id

print(game_sum)
