#! /usr/bin/env python

from concurrent.futures import ProcessPoolExecutor
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

grid = dict()
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        grid[x+y*1j] = c

def new_directions(d, c):
    match d,c:
        case (1, '|') | (-1, '|'):
            return (1j, -1j)
        case (1j, '-') | (-1j, '-'):
            return (1, -1)
        case (1, '/') | (-1, '/') | (1j, '\\') | (-1j, '\\'):
            return (-1j*d, )
        case (1j, '/') | (-1j, '/') | (1, '\\') | (-1, '\\'):
            return (1j*d, )
        case _:
            return (d, )

def light(s, ds):
    queue = [ (s, ds) ]
    already_seen = set()
    while queue:
        pos, direction = queue.pop()
        if pos not in grid or (pos, direction) in already_seen:
            continue

        already_seen.add((pos, direction))

        for d in new_directions(direction, grid[pos]):
            queue.append((pos+d, d))

    return len(set(p for p, _ in already_seen))

print("Part 1:", light(0, 1))

maxi = 0
m, n = len(lines), len(lines[0])
with ProcessPoolExecutor() as executor:
    futures = set()
    for y in range(m):
        futures.add(executor.submit(light, y*1j, 1))
        futures.add(executor.submit(light, n-1+y*1j, -1))
    for x in range(n):
        futures.add(executor.submit(light, x, 1j))
        futures.add(executor.submit(light, x+(m-1)*1j, -1j))

maxi = max(f.result() for f in futures)
print("Part 2:", maxi)

