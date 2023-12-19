#! /usr/bin/env python

from collections import defaultdict
import sys

lines = []
for line in sys.stdin:
    if not line.strip():
        break
    lines.append(line.rstrip('\n'))

directions = dict(zip('UDRL', (1j,-1j,1,-1)))

ground = defaultdict(lambda: {}, {0: {}})
pos = 0
min_x, min_y, max_x, max_y = float('+inf'), float('+inf'), float('-inf'), float('-inf')
for l in lines:
    direction, length, color = l.split()
    color = color.strip('()')
    ground[pos][direction] = color
    for _ in range(int(length)):
        pos += directions[direction]
        ground[pos][direction] = color
    min_x, max_x = min(min_x, int(pos.real)), max(max_x, int(pos.real))
    min_y, max_y = min(min_y, int(pos.imag)), max(max_y, int(pos.imag))
ground[pos][direction] = color

# for y in range(max_y, min_y-1, -1):
#     print(''.join(
#         '#' if ground[x+y*1j] else '.'
#         for x in range(min_x, max_x+1)
#     ))

def shape(pos: complex) -> str:
    match ''.join(ground[pos].keys()):
        case 'U'|'D':
            return '|'
        case 'L'|'R':
            return '-'
        case 'RU'|'DL':
            return 'J'
        case 'RD'|'UL':
            return '\\'
        case 'DR'|'LU':
            return 'L'
        case 'LD'|'UR':
            return '/'
        case _:
            raise ValueError


def is_edge(pos: complex) -> bool:
    return any(e in ground[pos] for e in 'UDRL')

def is_inside(pos: complex) -> bool:
    z = pos + 1 + 1j
    cpt = 0
    while min_x-1 <= z.real <= max_x+1 and min_y -1 <= z.imag <= max_y+1:
        cpt += is_edge(z) and shape(z) not in 'J/'
        z += 1+1j
    return cpt%2

for y in range(max_y, min_y-1, -1):
    for x in range(min_x, max_x+1):
        pos = x + y*1j
        if is_edge(pos):
            pass
        elif is_inside(pos):
            ground[pos] = {'B': '#000000'}

# print()
# for y in range(max_y, min_y-1, -1):
#     print(''.join(
#         '#' if ground[x+y*1j] else '.'
#         for x in range(min_x, max_x+1)
#     ))

print("Part 1:", sum(bool(ground[z]) for z in ground))

polygon = []
pos = 0
total_length = 0
for l in lines:
    _, _, color = l.split()
    color = color.strip('()')
    length, direction = int(color[1:6], 16), 'RDLU'[int(color[6])]
    # To apply this method to Part 1...
    # direction, length, color = l.split()
    # length = int(length)

    pos += directions[direction]*length
    polygon.append(pos)

    total_length += length


def area_polygon(poly: list) -> int:
    # https://en.wikipedia.org/wiki/Shoelace_formula
    match poly:
        case []: return 0
        case [p1, p2]:
            return p1.real*p2.imag - p2.real*p1.imag
        case [p1, p2, *l]:
            return p1.real*p2.imag - p2.real*p1.imag + area_polygon([p2, *l])


area = area_polygon(polygon+[polygon[0]])
area = area/2 if area > 0 else -area/2
# https://en.wikipedia.org/wiki/Pick's_theorem
result = total_length + int(area - total_length/2 + 1)

print("Part 2:", result)
