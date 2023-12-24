import re
import sys
import numpy
import z3

hailstones = []
with open(sys.argv[1]) as f:
    r = re.compile(r'(\d+), +(\d+), +(\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)')
    for line in f:
        m = r.match(line)
        x,y,z,dx,dy,dz = m.groups()
        hailstones.append({'x': int(x), 'y': int(y), 'z': int(z),
                           'dx': int(dx), 'dy': int(dy), 'dz': int(dz)})

def paths_intersects(h1, h2, axis_min, axis_max):
    if h1['dx']/h2['dx'] == h1['dy']/h2['dy']:
        return False
    A = numpy.array([[h1['dx'], -h2['dx']],
                      [h1['dy'], -h2['dy']]])
    b = numpy.array([[h2['x'] - h1['x']],
                     [h2['y'] - h1['y']]])
    x = numpy.linalg.solve(A,b)

    x_intersect = h1['x'] + x[0]*h1['dx']
    y_intersect = h1['y'] + x[0]*h1['dy']

    if x_intersect >= axis_min and x_intersect <= axis_max and y_intersect >= axis_min and y_intersect <= axis_max and min(x) >= 0:
        return True

    return False

num_intersects = 0
for i in range(len(hailstones)):
    for j in range(i+1, len(hailstones)):
        if paths_intersects(hailstones[i], hailstones[j], 200000000000000, 400000000000000):
            num_intersects += 1

print(f"part1: {num_intersects}")

solver = z3.Solver()
xs = z3.Int('xs')
ys = z3.Int('ys')
zs = z3.Int('zs')
dxs = z3.Int('dxs')
dys = z3.Int('dys')
dzs = z3.Int('dzs')
for i in range(len(hailstones)):
    x = hailstones[i]['x']
    y = hailstones[i]['y']
    z = hailstones[i]['z']
    dx = hailstones[i]['dx']
    dy = hailstones[i]['dy']
    dz = hailstones[i]['dz']
    t = z3.Int(f't{i}')
    solver.add(x + t*dx == xs + t * dxs)
    solver.add(y + t*dy == ys + t * dys)
    solver.add(z + t*dz == zs + t * dzs)

if solver.check() == z3.sat:
    model = solver.model()
    print(f"part2: {z3.simplify(model[xs] + model[ys] + model[zs])}")
else:
    print("No solutions available")
