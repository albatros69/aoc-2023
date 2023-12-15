#! /usr/bin/env python

from collections import defaultdict
from functools import reduce
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
sequences = lines[0].split(',')


def HASH(seq: str) -> int:
    return reduce(lambda n,s: (17*(n+s))%256, (ord(c) for c in seq), 0)

print("Part 1:", sum(HASH(s) for s in sequences))


class Lens():
    label: str
    focal: int

    def __init__(self, seq: str) -> None:
        self.label, focal = seq.split('=')
        self.focal = int(focal)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Lens):
            return self.label == other.label
        elif isinstance(other, str):
            return self.label == other

        raise TypeError

    @property
    def box(self) -> int:
        return HASH(self.label)

    def __str__(self):
        return f"[{self.label} {self.focal}]"


boxes = defaultdict(list)

def print_boxes():
    for i,b in boxes.items():
        if b:
            print(f"Box {i}:", ' '.join(str(l) for l in b))


for s in sequences:
    # print('--- After', s)
    if '=' in s:
        lens = Lens(s)
        try:
            pos = boxes[lens.box].index(lens)
            boxes[lens.box][pos] = lens
        except ValueError:
            boxes[lens.box].append(lens)
    elif s.endswith('-'):
        label = s.strip('-')
        box = HASH(label)
        try:
            boxes[box].remove(label)
        except ValueError:
            pass
    # print_boxes()

print("Part 2:", sum((n+1)*sum(l.focal*(i+1) for i,l in enumerate(b)) for n,b in boxes.items()))
