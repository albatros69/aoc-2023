#! /usr/bin/env python

from ast import literal_eval
from dataclasses import dataclass, asdict
import re
import sys
from typing import List


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s

@dataclass
class QuadPart:
    x: tuple=(1, 4001)
    m: tuple=(1, 4001)
    a: tuple=(1, 4001)
    s: tuple=(1, 4001)

    @property
    def size(self):
        return (self.x[1]-self.x[0])*(self.m[1]-self.m[0])*(self.a[1]-self.a[0])*(self.s[1]-self.s[0])

EMPTY = QuadPart((0,0), (0,0), (0,0), (0,0))


class SingleRule():
    test: str
    dest: str

    def __init__(self, rule) -> None:
        if ':' in rule:
            test, self.dest = rule.split(':')
            self.test = (test[0], test[1], int(test[2:]))
        else:
            self.test = None
            self.dest = rule

    def apply_p1(self, part: Part) -> str:
        if self.test is None:
            return self.dest
        elif self.test[1] == '<' and getattr(part, self.test[0]) < self.test[2]:
            return self.dest
        elif self.test[1] == '>' and getattr(part, self.test[0]) > self.test[2]:
            return self.dest
        else:
            return None


    def apply_p2(self, part: QuadPart) -> tuple[str,QuadPart,QuadPart]:
        if self.test is None:
            return self.dest, part, EMPTY

        result = QuadPart(**asdict(part))
        cresult = QuadPart(**asdict(part))

        inter_ori = getattr(part, self.test[0])

        if self.test[1] == '<':
            interval = inter_ori[0], min(inter_ori[1], self.test[2])
            cinterval = min(inter_ori[1], self.test[2]), inter_ori[1]
        elif self.test[1] == '>':
            interval = max(inter_ori[0], self.test[2]+1), inter_ori[1]
            cinterval = inter_ori[0], max(inter_ori[0], self.test[2]+1)

        setattr(result, self.test[0], interval)
        setattr(cresult, self.test[0], cinterval)
        if interval[1] <= interval[0]:
            result = EMPTY
        if cinterval[1] <= cinterval[0]:
            cresult = EMPTY

        return self.dest, result, cresult


    def __str__(self) -> str:
        if self.test is None:
            return self.dest
        else:
            return f'{self.test}:{self.dest}'


re_rule = re.compile(r'(?P<name>[a-z]+){(?P<workflow>.+)}')
class Workflow():
    name: str
    rules: List[SingleRule]

    def __init__(self, line) -> None:
        m = re_rule.match(line)
        self.name = m.group('name')
        self.rules = [ SingleRule(r) for r in m.group('workflow').split(',') ]

    def __str__(self) -> str:
        return f'{self.name}{{{",".join(str(r) for r in self.rules)}}}'

    def __repr__(self) -> str:
        return str(self)

    def apply_p1(self, part: Part) -> str:
        for r in self.rules:
            dest = r.apply_p1(part)
            if dest in ('A', 'R'):
                return dest
            elif dest is None:
                continue
            else:
                return rules[dest].apply_p1(part)

    def apply_p2(self, qpart: QuadPart) -> List[QuadPart]:
        result = []
        qp = qpart
        for r in self.rules:
            dest, qp, cqp = r.apply_p2(qp)

            if dest == 'A':
                result.append(qp)
            elif dest in (None, 'R'):
                pass
            else:
                result.extend(rules[dest].apply_p2(qp))

            qp = cqp

        return result


rules = dict()
parts = []
for l in lines:
    if not l:
        continue
    elif l.startswith('{'):
        p = literal_eval(l.replace('{','{"').replace('=', '":').replace(',',',"'))
        parts.append(Part(**p))
    else:
        w = Workflow(l)
        rules[w.name] = w


IN = rules['in']

print("Part 1:", sum(p.rating for p in parts if IN.apply_p1(p)=='A'))

print("Part 2:", sum(qp.size for qp in IN.apply_p2(QuadPart())))
