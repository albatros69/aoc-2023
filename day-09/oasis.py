#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append([int(n) for n in line.rstrip('\n').split()])

def extrapolate(report):
    if all(x==0 for x in report):
        return 0

    assert len(report) > 0
    new = [ report[i]-report[i-1] for i in range(1, len(report)) ]
    return report[-1] + extrapolate(new)

print("Part 1:", sum(extrapolate(l) for l in lines))

def extrapolate_back(report):
    if all(x==0 for x in report):
        return 0

    assert len(report) > 0
    new = [ report[i]-report[i-1] for i in range(1, len(report)) ]
    return report[0] - extrapolate_back(new)

print("Part 2:", sum(extrapolate_back(l) for l in lines))
