#! /usr/bin/env python

from collections import defaultdict
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

ground = defaultdict(lambda: '.')
start_pos = None
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        ground[x-y*1j] = c
        if c == 'S':
            start_pos = x-y*1j

possible_neighs = {
    '|': {1j: {'7', 'F', '|'}, -1j: {'L', 'J', '|'}},
    '-': {1: {'J', '7', '-'},  -1: {'F', 'L', '-'}},
    'L': {1: {'J', '7', '-'}, 1j: {'7', 'F', '|'}},
    'J': {-1: {'F', 'L', '-'}, 1j: {'7', 'F', '|'}},
    '7': {-1: {'F', 'L', '-'}, -1j: {'L', 'J', '|'}},
    'F': {1: {'J', '7', '-'}, -1j: {'L', 'J', '|'}},
}

def start_letter(s: complex):
    possible_letters = set(possible_neighs.keys())
    for z in (1, -1, 1j, -1j):
        try:
            possible_letters.intersection_update(possible_neighs[ground[s+z]][-z])
        except KeyError:
            pass

    assert len(possible_letters) == 1
    return possible_letters.pop()


ground[start_pos] = start_letter(start_pos)

def walk_loop(start):

    pos, letter = start, ground[start]
    result = [start]
    direction = 0
    while True:
        for d in possible_neighs[letter]:
            if d == -direction:
                continue

            if pos+d == start:
                pos += d
                break

            if ground[pos+d] in possible_neighs[letter][d]:
                direction = d
                pos += d
                letter = ground[pos]
                result.append(pos)
                break

        if pos == start:
            break

    return result

loop = walk_loop(start_pos)
print("Part 1:", len(loop)//2)


def ray(pos):
    crosses = 0
    p = pos
    while p in ground:
        crosses += p in loop and ground[p] not in ('L', '7')
        p += 1-1j

    return bool(crosses%2)

inside = set(p for p in ground if p not in loop and ray(p))
print("Part 2:", len(inside))
