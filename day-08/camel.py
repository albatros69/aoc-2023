#! /usr/bin/env python

import sys
from itertools import cycle
from math import lcm

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

path = lines[0]
graphe = {}
for l in lines[2:]:
    node, leafs = l.split(' = ')
    graphe[node] = dict(zip('LR', leafs.strip('()').split(', ')))

pos = 'AAA'
steps = 0
for turn in cycle(path):
    if pos == 'ZZZ':
        break

    pos = graphe[pos][turn]
    steps += 1

print("Part 1:", steps)

steps = []
for p in tuple(p for p in graphe if p[-1]=='A'):
    pos = p
    s = 0
    for turn in cycle(path):
        if pos[-1] == 'Z':
            break

        pos = graphe[pos][turn]
        s += 1

    steps.append(s)

print("Part 2:", lcm(*steps))

