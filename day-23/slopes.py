#! /usr/bin/env python

from collections import defaultdict
from functools import cache
import sys


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

island = defaultdict(lambda: '#')
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        island[x+y*1j] = c

start = 1
finish = len(lines[0])-2 + (len(lines)-1)*1j


slopes = { '>': 1, '<': -1, 'v': 1j, '^': -1j}
def neigh_p1(pos):
    if island[pos] in '<>v^':
        return (pos+slopes[island[pos]], )
    elif island[pos] == '.':
        return (pos+1, pos-1, pos+1j, pos-1j)
    else:
        return ()


queue = [ (0, start, (start, ))]
max_steps = 0
while queue:
    steps, pos, path = queue.pop()

    if pos == finish:
        max_steps = max(max_steps, steps)
        continue

    for new_pos in neigh_p1(pos):
        if island[new_pos] != '#' and new_pos not in path:
            queue.append((steps+1, new_pos, (*path, new_pos)))

print("Part 1:", max_steps)


def neigh_p2(pos):
    if island[pos] != '#':
        return tuple(p for p in (pos+1, pos-1, pos+1j, pos-1j) if island[p] != '#')
    else:
        return ()

def walk(prev, n):
    s = 1
    while len(tmp:=neigh_p2(n)) == 2:
        s += 1
        (m, ) = (p for p in tmp if p != prev)
        prev, n = n, m

    return n, s

@cache
def compr_neigh_p2(pos):
    result = neigh_p2(pos)

    if len(result) != 2:
        return tuple((p, 1) for p in result)
    else:
        n1, n2 = result
        return (walk(pos, n1), walk(pos, n2))


queue = [ (0, start, (start,)) ]
already_seen = dict()
max_steps = 0
while queue:
    steps, pos, path = queue.pop()

    try:
        if already_seen[pos] > steps:
            continue
    except KeyError:
        pass

    if pos == finish:
        if steps > max_steps:
            # print(len(queue), max_steps, steps)
            max_steps = steps
            for s,p in enumerate(path):
                already_seen[p] = s
        continue

    for (new_pos, new_steps) in compr_neigh_p2(pos):
        if new_pos not in path:
            queue.append((steps+new_steps, new_pos, (*path, new_pos)))

print("Part 2:", max_steps)
