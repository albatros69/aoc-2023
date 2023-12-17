#! /usr/bin/env python

from collections import defaultdict
from heapq import heappop, heappush
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

city = dict()
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        city[x,y] = int(c)
finish = len(lines[0])-1, len(lines)-1


def add_dir(pt: tuple, d) -> tuple:
    match d:
        case 'N': return (pt[0], pt[1]-1)
        case 'S': return (pt[0], pt[1]+1)
        case 'E': return (pt[0]+1, pt[1])
        case 'W': return (pt[0]-1, pt[1])

reverse_dir = { 'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E', '': '' }


queue = [ (0, (0,0), '', 0, '') ]
already_seen = defaultdict(lambda: float('inf'), {((0,0),'', 0): 0})
while queue:
    heatloss, pos, direction, cpt, path = heappop(queue)

    if pos == finish:
        # print(path)
        break

    for new_dir in 'NSEW':
        if new_dir == reverse_dir[direction]:
            continue
        elif new_dir == direction and cpt >= 3:
            continue
        else:
            new_cpt = cpt+1 if new_dir == direction else 1
            new_pos = add_dir(pos, new_dir)
            if new_pos in city:
                new_heatloss = heatloss + city[new_pos]
                if new_heatloss < already_seen[new_pos, new_dir, new_cpt]:
                    already_seen[new_pos, new_dir, new_cpt] = new_heatloss
                    heappush(queue, (new_heatloss, new_pos, new_dir, new_cpt, path+new_dir))

print("Part 1:", heatloss)


queue = [ (0, (0,0), '', 0, '') ]
already_seen = defaultdict(lambda: float('inf'), {((0,0),'', 0): 0})
while queue:
    heatloss, pos, direction, cpt, path = heappop(queue)

    if pos == finish and cpt >= 4:
        # print(path)
        break

    for new_dir in 'NSEW':
        if new_dir == reverse_dir[direction]:
            continue
        elif new_dir == direction and cpt >= 10:
            continue
        elif new_dir != direction and 1 <= cpt <= 3:
            continue
        else:
            new_cpt = cpt+1 if new_dir == direction else 1
            new_pos = add_dir(pos, new_dir)
            if new_pos in city:
                new_heatloss = heatloss + city[new_pos]
                if new_heatloss < already_seen[new_pos, new_dir, new_cpt]:
                    already_seen[new_pos, new_dir, new_cpt] = new_heatloss
                    heappush(queue, (new_heatloss, new_pos, new_dir, new_cpt, path+new_dir))

print("Part 2:", heatloss)
