#! /usr/bin/env python

import sys
from collections import defaultdict
from operator import mul

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

schema = defaultdict(lambda: '.')
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        schema[x,y] = c

size_x, size_y = max(schema.keys())

parts = []
gears = defaultdict(list)
for y in range(size_y+1):
    current_number = ''
    is_part = False
    is_gear = ()

    for x in range(size_x+1):
        if not schema[x,y].isdigit():
            if current_number and is_part:
                parts.append(int(current_number))
                if is_gear:
                    gears[is_gear].append(int(current_number))

            current_number = ''
            is_part = False
            is_gear = ()

            continue

        current_number += schema[x,y]

        neigh_coords = ((x,y+1), (x,y-1), (x+1,y), (x+1,y+1), (x+1,y-1), (x-1,y), (x-1,y+1), (x-1,y-1))
        neighs = ''.join(schema[c] for c in neigh_coords)
        is_part = is_part or any(c != '.' and not c.isdigit() for c in neighs)
        try:
            is_gear = neigh_coords[neighs.index('*')]
        except ValueError:
            pass

    if current_number and is_part:
        parts.append(int(current_number))
        if is_gear:
            gears[is_gear].append(int(current_number))

print("Part 1:", sum(parts))
print("Part 2:", sum(mul(*l) for l in gears.values() if len(l)==2))
