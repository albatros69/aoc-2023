#! /usr/bin/env python

import sys
from typing import List

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

games = {}
for l in lines:
    g, sets = l.split(': ')
    games[int(g.split()[1])] = []
    for s in sets.split('; '):
        draw = {}
        for x in s.split(', '):
            v, c = x.split()
            draw[c] = int(v)
        games[int(g.split()[1])].append(draw)

bag = { 'red': 12, 'green': 13, 'blue': 14 }
def is_valid(game: List[dict]) -> bool:
    return all(all(draw[color] <= bag[color] for color in draw) for draw in game)

print("Part 1:", sum(i for i,g in games.items() if is_valid(g)))

def power(game: List[dict]) -> int:
    result = { 'red': 0, 'green': 0, 'blue': 0 }
    for draw in game:
        for color in draw:
            result[color] = max(result[color], draw[color])

    return result['red']*result['green']*result['blue']

print("Part 2:", sum(power(g) for g in games.values()))
