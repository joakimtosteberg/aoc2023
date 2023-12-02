import sys


games = {}

with open(sys.argv[1]) as f:
    for line in f:
        data = line.split(':')
        game_id = int(data[0].split(' ')[1])
        games[game_id] = {'red': 0, 'green': 0, 'blue': 0}
        cube_sets = data[1].split(';')
        for cube_set in cube_sets:
            for cubes in cube_set.split(','):
                cube_info = cubes.strip().split(' ')
                amount = int(cube_info[0])
                color = cube_info[1]
                games[game_id][color] = max(games[game_id][color], amount)


total_power = 0
for game in games.values():
    power = game['red']*game['green']*game['blue']
    total_power += power

print(total_power)
