#! /usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
from functools import cache
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def simplify_springs(l):
    return '.'.join(s for s in l.split('.') if s)

def expand(groups):
    return '.'.join('#'*n for n in groups)


def correct_arrangments(l, groups):
    result = 0
    correct = expand(groups)

    queue = [ (l, '') ]
    while queue:
        rest, beg = queue.pop()

        if not rest:
            if simplify_springs(beg) == correct:
                result += 1
            continue

        c, *rest = rest

        if c != '?':
            queue.append((rest, beg+c))
            continue

        for new in ('#', '.'):
            if correct.startswith(simplify_springs(beg+new)):
                queue.append((rest, beg+new))

    return result

with ThreadPoolExecutor() as executor:
    futures = set()
    for l in lines:
        springs, groups = l.split()
        futures.add(executor.submit(correct_arrangments, list(springs), (int(n) for n in groups.split(','))))

nb_arrangements = sum(f.result() for f in futures)
print("Part 1:", nb_arrangements)


@cache
def rec_arrangments(l, groups, in_block):

    if not l:
        if not groups:
            return 0
        else:
            return 0

    match l[0]:

        case '?':
            if in_block and groups[0] > 0:
                return rec_arrangments('#'+l[1:], groups, in_block)
            elif in_block and groups[0] == 0:
                return rec_arrangments('.'+l[1:], groups, False)
            else:
                return rec_arrangments('#'+l[1:], groups, in_block) + rec_arrangments('.'+l[1:], groups, in_block)

        case '.':
            if not groups or groups == (0, ):
                return 1 if '#' not in l[1:] else 0
            elif in_block and groups[0] > 0:
                return 0

            return rec_arrangments(l[1:], groups if groups[0]>0 else groups[1:], False)

        case '#':
            if not groups:
                return 0
            elif groups[0] > 0:
                return rec_arrangments(l[1:], (groups[0]-1, *groups[1:]), True)
            else:
                return 0

    return -1

nb_arrangements = 0
for l in lines:
    springs, groups = l.split()
    nb_arrangements += rec_arrangments(springs+'.', tuple(int(n) for n in groups.split(',')), False)

print("Part 1 (bis):", nb_arrangements)


# /!\ Only works on the test file!
# with ThreadPoolExecutor() as executor:
#     futures = set()
#     for l in lines:
#         springs, groups = l.split()
#         springs = '?'.join((springs,)*5)
#         groups = ','.join((groups, )*5)
#         futures.add(executor.submit(correct_arrangments, list(springs), (int(n) for n in groups.split(','))))

# nb_arrangements = sum(f.result() for f in futures)
# print("Part 2:", nb_arrangements)

nb_arrangements = 0
for l in lines:
    springs, groups = l.split()
    springs = '?'.join((springs,)*5)
    groups = ','.join((groups, )*5)
    nb_arrangements += rec_arrangments(springs+'.', tuple(int(n) for n in groups.split(',')), False)

print("Part 2 (bis):", nb_arrangements)
