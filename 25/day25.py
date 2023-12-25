import re
import sys

import community as community_louvain
import networkx as nx

connections = {}

with open(sys.argv[1]) as f:
    for line in f:
        l = line.strip().split(':')
        if not l[0] in connections:
            connections[l[0]] = set()
        for component in l[1].split():
            if not component in connections:
                connections[component] = set()
            connections[l[0]].add(component)
            connections[component].add(l[0])

g = nx.Graph()
for c1 in connections:
    for c2 in connections[c1]:
        g.add_edge(c1, c2, weight=1)

iter = 0
while True:
    p1 = set()
    p2 = set()
    iter = iter+1
    partition = community_louvain.best_partition(g, randomize=True, resolution=10)
    for item in partition:
        if partition[item] > 1:
            break
        if partition[item]:
            p2.add(item)
        else:
            p1.add(item)
    else:
        num_removed = 0
        for c1 in connections:
            for c2 in connections[c1]:
                if (c1 in p1) == (c2 in p2):
                    num_removed += 1
        if num_removed == 6:
            break

print(f"part1 (found after {iter} iterations): {len(p1)*len(p2)}")
