#! /usr/bin/env python

from itertools import chain
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

seeds = [ int(a) for a in lines[0].split(': ')[1].split() ]

maps = {}
for l in lines[2:]:
    if not l:
        pass
    elif l.endswith('map:'):
        current_map, _ = l.split()
        maps[current_map] = []
    else:
        dst, src, lg = (int(a) for a in l.split())
        maps[current_map].append((src, lg, dst))

def convert_p1(val: int, src: str, dst: str) -> int:
    for s, l, d in maps[f'{src}-to-{dst}']:
        if s <= val < s+l:
            return d + (val-s)

    return val

paths = ('seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location')

def location_p1(s: int) -> int:
    result = s
    for i in range(len(paths)-1):
        result = convert_p1(result, paths[i], paths[i+1])
    return result

print("Part 1:", min(location_p1(s) for s in seeds))

for m in maps.values():
    m.sort()

def convert_p2(start: int, lg: int, src: str, dst: str) -> int:
    result = []
    for s, l, d in maps[f'{src}-to-{dst}']:
        if s <= start < s+l:
            if start+lg <= s+l:
                result.append((d+(start-s), lg))
                start, lg = -1, 0
            else:
                result.append((d+(start-s), s+l-start))
                start, lg = s+l, start+lg-s-l
                assert lg >= 0
        elif start <= s < start+lg:
            result.append((start, s-start))
            if s+l <= start+lg:
                result.append((d,l))
                start, lg = s+l, start+lg-s-l
                assert lg >= 0
            else:
                result.append((d, start+lg-s))
                start, lg = -1, 0

    if lg:
        result.append((start, lg))

    return result

def location_p2(s: int, l: int) -> int:
    result = [ (s, l) ]
    for i in range(len(paths)-1):
        result = list(chain.from_iterable(convert_p2(a, b, paths[i], paths[i+1]) for (a,b) in result))

    return result

print("Part 2:", min(chain.from_iterable(location_p2(*seeds[i:i+2]) for i in range(0, len(seeds), 2)))[0])
