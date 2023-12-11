#! /usr/bin/env python

import sys
from itertools import product, combinations

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

universe = [ list(l) for l in lines ]

nb_rows = len(lines)
nb_cols = len(lines[0])

def is_empty_row(r):
    return r == ['.', ]*nb_cols
def is_empty_col(c):
    return c == ['.', ]*nb_rows


def expand():
    empty_rows = []
    empty_cols = []

    for n in (range(nb_rows-1, -1, -1)):
        if is_empty_row(universe[n]):
            empty_rows.append(n)
    for n in range(nb_cols-1, -1, -1):
        if is_empty_col([universe[i][n] for i in range(nb_rows)]):
            empty_cols.append(n)

    return empty_rows, empty_cols

def dist(a, b):
    return sum(abs(b[i]-a[i]) for i in (0,1))

empty_rows, empty_cols = expand()

galaxies = tuple((y,x) for (y,x) in product(range(nb_rows), range(nb_cols)) if universe[y][x] == '#')

def expansion(a,b, factor=2):
    result = sum(a[0] < n < b[0] or b[0] < n < a[0] for n in empty_rows) \
        + sum(a[1] < n < b[1] or b[1] < n < a[1] for n in empty_cols)

    return result * (factor-1)

print("Part 1:", sum(dist(a, b)+expansion(a,b) for (a,b) in combinations(galaxies, 2)))

# print("Part 2:", sum(dist(a, b)+expansion(a, b, 10) for (a,b) in combinations(galaxies, 2)))
# print("Part 2:", sum(dist(a, b)+expansion(a, b, 100) for (a,b) in combinations(galaxies, 2)))

print("Part 2:", sum(dist(a, b)+expansion(a, b, 1000000) for (a,b) in combinations(galaxies, 2)))
