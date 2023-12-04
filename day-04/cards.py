#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

matches = {}
for l in lines:
    card, rest = l.split(': ')
    win_nums, nums = (
        set(int(a) for a in s.split() if a) for s in rest.split(' | ') )

    n = int(card.split()[1])
    matches[n] = {
        'score': len(win_nums&nums),
        'nb': 1
    }

print("Part 1:",
      sum(2**(m['score']-1) if m['score'] else 0 for m in matches.values()))

for c,m in matches.items():
    for n in range(c+1, c+m['score']+1):
        matches[n]['nb'] += m['nb']

print("Part 2:", sum(m['nb'] for m in matches.values()))
