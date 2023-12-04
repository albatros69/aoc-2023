#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

digits = [[a for a in line if a.isdigit()] for line in lines]
print("Part 1:", sum(int(a[0]+a[-1]) for a in digits if a))

trans_table = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
}
w_digits = (
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine')

def convert(l: str):
    _, left = min((l.find(w), w) for w in w_digits if w in l)
    _, right = max((l.rfind(w), w) for w in w_digits)
    if not left.isdigit():
        left = trans_table[left]
    if not right.isdigit():
        right = trans_table[right]

    return int(left+right)

print("Part 2:", sum(convert(l) for l in lines))
