#! /usr/bin/env python

from enum import Enum
from collections import Counter
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Kind(Enum):
    FIVE = 6
    FOUR = 5
    FULL = 4
    THREE = 3
    TWO = 2
    ONE = 1
    HIGH = 0

class Hand_p1():
    cards: tuple = ()
    bid: int = 0
    type: Kind = None
    card_strength = dict(zip(
        ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'),
        range(13)
    ))

    def __init__(self, line: str):

        cards, bid = line.split()
        self.cards = tuple(cards)
        self.bid = int(bid)

        self.set_type()


    def set_type(self):
        counts = Counter(self.cards)
        a, *b = (c for _,c in counts.most_common(2))

        match (a,b):
            case 5,_:
                self.type = Kind.FIVE
            case 4,_:
                self.type = Kind.FOUR
            case 3,[2]:
                self.type = Kind.FULL
            case 3,_:
                self.type = Kind.THREE
            case 2,[2]:
                self.type = Kind.TWO
            case 2,[1]:
                self.type = Kind.ONE
            case _:
                self.type = Kind.HIGH

    @property
    def _card_key(self):
        return tuple(self.card_strength[c] for c in self.cards)

    def __lt__(self, other: 'Hand_p1'):
        return self.type.value < other.type.value or (
            self.type.value == other.type.value and self._card_key < other._card_key)

    def __repr__(self):
        return ''.join(self.cards)# + f" {self.type}"


hands = sorted(Hand_p1(l) for l in lines)
print("Part 1:", sum((rank+1)*hand.bid for rank, hand in enumerate(hands)))


class Hand_p2(Hand_p1):
    card_strength = dict(zip(
        ('J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'),
        range(13)
    ))

    def set_type(self):
        counts = Counter(self.cards)
        try:
            a, *b = (c for v,c in counts.most_common(2) if v != 'J')
            a += counts['J']
        except ValueError:
            a = counts['J']
            b = []

        match (a,b):
            case 5,_:
                self.type = Kind.FIVE
            case 4,_:
                self.type = Kind.FOUR
            case 3,[2]:
                self.type = Kind.FULL
            case 3,_:
                self.type = Kind.THREE
            case 2,[2]:
                self.type = Kind.TWO
            case 2,_:
                self.type = Kind.ONE
            case _:
                self.type = Kind.HIGH


hands = sorted(Hand_p2(l) for l in lines)
print("Part 2:", sum((rank+1)*hand.bid for rank, hand in enumerate(hands)))

