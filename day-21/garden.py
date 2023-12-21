#! /usr/bin/env python

from collections import defaultdict
from functools import cache
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

garden = defaultdict(lambda: '!')
for y,line in enumerate(lines[::-1]):
    for x,c in enumerate(line):
        garden[x+y*1j] = c
        if c == 'S':
            start = x+y*1j
            garden[start] = '.'

def walk(start, max_steps):
    queue = set((start,))
    for _ in range(max_steps):
        new_q = set()

        for pos in queue:
            new_q.update(new_p for new_p in (pos+1,pos-1,pos+1j,pos-1j) if garden[new_p]=='.')

        queue = new_q

    return len(queue)

print("Part 1:", walk(start, 64))

size = len(lines)
steps = 26501365
sr, sc = start.imag, start.real

# https://www.youtube.com/watch?v=9UOMZSL0JTg

grid_width = steps // size - 1

odd = (grid_width // 2 * 2 + 1) ** 2
even = ((grid_width + 1) // 2 * 2) ** 2

odd_points = walk(start, size * 2 + 1)
even_points = walk(start, size * 2)

corner_t = walk((size - 1)*1j + sc, size - 1)
corner_r = walk(sr*1j, size - 1)
corner_b = walk(sc, size - 1)
corner_l = walk(sr*1j + size - 1, size - 1)

small_tr = walk((size - 1)*1j, size // 2 - 1)
small_tl = walk((size - 1)*(1+1j), size // 2 - 1)
small_br = walk(0, size // 2 - 1)
small_bl = walk(size - 1, size // 2 - 1)

large_tr = walk((size - 1)*1j, size * 3 // 2 - 1)
large_tl = walk((size - 1)*(1+1j), size * 3 // 2 - 1)
large_br = walk(0, size * 3 // 2 - 1)
large_bl = walk(size - 1, size * 3 // 2 - 1)

print("Part 2:",
    odd * odd_points +
    even * even_points +
    corner_t + corner_r + corner_b + corner_l +
    (grid_width + 1) * (small_tr + small_tl + small_br + small_bl) +
    grid_width * (large_tr + large_tl + large_br + large_bl)
)
