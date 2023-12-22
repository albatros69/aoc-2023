#! /usr/bin/env python

from __future__ import annotations

import sys
from ast import literal_eval
from functools import cached_property
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Brick:
    first_end: dict
    last_end: dict
    name: str

    def __init__(self, line, name=None):
        b1, b2 = sorted(map(literal_eval, line.split('~')))
        self.first_end = dict(zip("xyz", b1))
        self.last_end = dict(zip("xyz", b2))
        self.altitude = self.last_end['z']
        self.supports = list()
        self.supported_by = list()
        self.name = name
        self.kaboom = False

    @property
    def is_horizontal(self) -> bool:
        return self.first_end['z'] == self.last_end['z']

    @cached_property
    def cubes(self) -> set:
        return set(c for c in product(*(range(self.first_end[i], self.last_end[i]+1) for i in "xy")))

    def intersect(self, other: Brick) -> bool:
        return len(self.cubes & other.cubes) >= 1

    def move_down(self, steps=1):
        self.first_end['z'] -= steps
        self.last_end['z'] -= steps
        self.altitude -= steps

    def __str__(self) -> str:
        return (f"{self.name}: " if self.name is not None else '') + \
               f"{self.first_end}~{self.last_end}"
    def __repr__(self) -> str:
        return str(self)

    @property
    def safe_to_disintegrate(self) -> bool:
        return not any(len(b.supported_by)==1 for b in self.supports)

    def chain_reaction(self) -> int:
        self.kaboom = True
        return sum(1 + b.chain_reaction() for b in self.supports
                   if all(c.kaboom for c in b.supported_by))


stack = []
for i,line in enumerate(lines):
    stack.append(Brick(line)) #, name=chr(ord('A')+i)))
stack.sort(key=lambda b: b.first_end['z'], reverse=True)

settled_stack = []
max_z = 0
while stack:
    new_brick = stack.pop()
    if new_brick.altitude > max_z:
        new_brick.move_down(new_brick.altitude-max_z-1)
        max_z += 1

    for b in settled_stack:
        if new_brick.intersect(b):
            if new_brick.is_horizontal:
                new_brick.move_down(new_brick.altitude-b.altitude-1)
            else:
                new_brick.move_down(new_brick.first_end['z']-b.altitude-1)
            break
    else:
        if new_brick.is_horizontal:
            new_brick.move_down(new_brick.altitude-1)
        else:
            new_brick.move_down(new_brick.first_end['z']-1)

    for b in settled_stack:
        if new_brick.first_end['z'] - b.altitude > 1:
            continue
        elif new_brick.intersect(b):
            b.supports.append(new_brick)
            new_brick.supported_by.append(b)

    max_z = new_brick.altitude
    settled_stack.append(new_brick)
    settled_stack.sort(key=lambda b: b.altitude, reverse=True)


print("Part 1:", sum(b.safe_to_disintegrate for b in settled_stack))

total = 0
for b in settled_stack[::-1]:
    total += b.chain_reaction()
    for c in settled_stack:
        c.kaboom = False
print("Part 2:", total)
