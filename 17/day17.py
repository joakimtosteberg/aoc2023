import sys

loss_map = {}
width = 0
height = 0
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            loss_map[(x,y)] = int(c)
            x += 1
        if y == 0:
            width = x
        y += 1
height = y


def print_map(loss_map, width, height):
    for y in range(height):
        for x in range(width):
            print(loss_map[(x,y)], end='')
        print()
    print()

class State:
    def __init__(self, x, y, dx, dy, loss = 0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.loss = loss

def step(state, min_steps, max_steps, width, height, end_pos, loss_map, loss_states):
    next_states = []
    loss = state.loss
    for step in range(1,max_steps+1):
        pos = (state.x + state.dx * step, state.y + state.dy * step)
        if pos == end_pos:
            loss_state = pos
        else:
            loss_state = (pos[0], pos[1], True if state.dx else False)
        if loss_state not in loss_states:
            break
        loss += loss_map[pos]
        if loss >= loss_states[end_pos]:
            break

        if step < min_steps:
            continue

        if loss < loss_states[loss_state]:
            loss_states[loss_state] = loss
            if pos == end_pos:
                break
            next_states.append(State(pos[0], pos[1], 0 if state.dx else 1, 0 if state.dy else 1, loss))
            next_states.append(State(pos[0], pos[1], 0 if state.dx else -1, 0 if state.dy else -1, loss))

    return next_states




def find_loss(loss_map, min_steps, max_steps):
    states = [State(x=0, y=0, dx=0, dy=1), State(x=0, y=0, dx=1, dy=0)]
    loss_states = {}
    end_pos = (width-1, height-1)
    for y in range(0,height):
        for x in range(0,width):
            if x == width-1 and y == height - 1:
                loss_states[(x,y)] = 999999999999999
            else:
                loss_states[(x,y,True)] = 999999999999999
                loss_states[(x,y,False)] = 999999999999999

    while states:
        next_states = []
        for state in states:
            next_states.extend(step(state, min_steps, max_steps, width, height, end_pos, loss_map, loss_states))
        states = next_states

    return loss_states[end_pos]

print(f"part1: {find_loss(loss_map, 0, 3)}")
print(f"part2: {find_loss(loss_map, 4, 10)}")
