#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

patterns = []
p = []
for l in lines:
    if not l:
        patterns.append(p)
        p = []
    else:
        p.append(list(l))

if p:
    patterns.append(p)


def is_reflexion(pattern, n, delta=0):
    return n + delta + 1 >= len(pattern) \
           or n - delta < 0 \
           or pattern[n-delta] == pattern[n+delta+1]


def hori_reflexion(pattern):
    result = set()

    for y in range(len(pattern)-1):
        if pattern[y] == pattern[y+1]:
            reflexion = y

            for delta in range(1, max(reflexion, len(pattern)-reflexion)):
                if not is_reflexion(pattern, reflexion, delta):
                    break
            else:
                result.add(reflexion+1)

    return result

def transpose(pattern):
    return [
        [ p[i] for p in pattern ]
        for i in range(len(pattern[0]))
    ]


def reflections(pattern):
    return hori_reflexion(pattern), hori_reflexion(transpose(pattern))


#pylint: disable=C0200
def smudges(pattern, horiz, vert):

    def inv(c):
        return '#' if c == '.' else '.'

    for y in range(len(pattern)):
        for x in range(len(pattern[0])):

            pattern[y][x] = inv(pattern[y][x])

            new_h, new_v = reflections(pattern)

            if new_h and (new_h:=new_h-horiz):
                return new_h, {}
            if new_v and (new_v:=new_v-vert):
                return {}, new_v

            pattern[y][x] = inv(pattern[y][x])

    return None, None


result_p1, result_p2 = 0, 0
for p in patterns:
    h, v = reflections(p)
    s_h, s_v = smudges(p, h, v)

    result_p1 += 100*h.pop() if h else 0 + v.pop() if v else 0
    result_p2 += 100*s_h.pop() if s_h else 0 + s_v.pop() if s_v else 0

print("Part 1:", result_p1)
print("Part 2:", result_p2)
