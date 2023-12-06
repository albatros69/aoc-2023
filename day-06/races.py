#! /usr/bin/env python

from math import sqrt, floor, ceil
import sys
from functools import reduce

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

_, times = lines[0].split(': ')
_, distances = lines[1].split(': ')

times = [ int(a) for a in times.split() ]
distances = [ int(a) for a in distances.split() ]

def races(times, distances):
    result = []
    for time, dist in zip(times, distances):
        race = []
        for hold_time in range(time):
            d = hold_time*(time-hold_time)
            if d > dist:
                race.append(d)
            elif hold_time > time//2:
                # We're past the maximum so no need to continue
                break

        if race:
            result.append(race)

    return result

print("Part 1:", reduce(lambda x,y: x*y, (len(r) for r in races(times, distances))))

def solve(t, d):
    s_delta = sqrt(t**2 - 4*d)
    if s_delta == int(s_delta):
        return int(s_delta)-1
    return floor((t+s_delta)/2) - ceil((t-s_delta)/2) + 1

print("Part 1 (bis):", reduce(lambda x,y: x*y, (solve(t, d) for (t,d) in zip(times, distances))))

times = [int(''.join(str(a) for a in times))]
distances = [int(''.join(str(a) for a in distances))]

print("Part 2:", len(races(times, distances)[0]))
print("Part 2 (bis):", solve(times[0], distances[0]))
