#! /usr/bin/env python

from itertools import product
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

ori_platform = {}
size = len(lines)
for (y,l) in enumerate(lines):
    for x,r in enumerate(l):
        ori_platform[x+y*1j] = r


def str_platform(p: dict) -> str:
    return '\n'.join(
        ''.join(p[x+y*1j] for x in range(size))
        for y in range(size)
    )


def move_north(p: dict, z: complex):
    if p[z] != 'O':
        return None

    new_z = z
    while new_z.imag > 0 and p[new_z-1j] == '.':
        new_z -= 1j

    if new_z != z:
        p[new_z] = 'O'
        p[z] = '.'


def tilt(p: dict):
    for y in range(1, size):
        for x in range(size):
            move_north(p, x+y*1j)


def load(p: dict) -> int:
    return sum(size-y for (x,y) in product(range(size), repeat=2)
               if p[x+y*1j] == 'O')


part_1 = ori_platform.copy()
tilt(part_1)
print("Part 1:", load(part_1))


def rotation(p: dict):
    return { z*1j + size-1: v for (z,v) in p.items() }


part_2 = ori_platform.copy()
already_seen = { }
step = 0
maxi = 1000000000

while step < maxi:
    for _ in 'NWSE':
        tilt(part_2)
        part_2 = rotation(part_2)

    hash = str_platform(part_2)
    if hash in already_seen:
        cycle = already_seen[hash]
        nb_cycles = (maxi-step)//(step-cycle)
        step += nb_cycles*(step-cycle)
        already_seen = {}

    already_seen[hash] = step
    step += 1

print("Part 2:", load(part_2))
