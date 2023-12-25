#! /usr/bin/env python

from collections import defaultdict
from copy import deepcopy
from math import prod
from random import choice
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

graphe_ori = defaultdict(list)
edges_ori = []
for line in lines:
    node, siblings = line.split(': ')
    siblings = siblings.split()
    graphe_ori[node].extend(siblings)
    for n in siblings:
        graphe_ori[n].append(node)
        edges_ori.append(frozenset((node, n)))


# https://en.wikipedia.org/wiki/Karger%27s_algorithm
def remove_node(node, G, E):
    for n in G[node]:
        while True:
            try:
                G[n].remove(node)
            except ValueError:
                break

        while True:
            try:
                E.remove(frozenset((node, n)))
            except ValueError:
                break

    G.pop(node)


def edge_contraction(edge: tuple, G, E):
    n1, n2 = edge

    new_node = f'{n1}.{n2}'
    new_siblings = list(n for n in G[n1] + G[n2] if n not in edge)
    G[new_node] = new_siblings
    for n in new_siblings:
        G[n].append(new_node)
        E.append(frozenset((new_node, n)))
    remove_node(n1, G, E)
    remove_node(n2, G, E)


# choices = ["AC", "ED", "IJ", ("G", "I.J"), ("A.C", "E.D"), ("G.I.J", "H"), ("A.C.E.D", "B"), ("G.I.J.H", "F")]
def min_cut(G_ori, E_ori):

    n = len(G_ori)
    mini = len(E_ori)
    result = None
    for _ in range(int(n**2/2)+1):
        G, E = deepcopy(G_ori), deepcopy(E_ori)
        while len(G) > 2:
            e = choice(E)
            # e = choices.pop(0)
            # print(e, E, G, '-'*8, sep="\n")
            edge_contraction(e, G, E)

        print(mini, len(E), tuple(n.count('.')+1 for n in G))

        if len(E) < mini:
            mini = len(E)
            result = G, E

        if mini <= 3:
            break

    return result

result_G, _ = min_cut(graphe_ori, edges_ori)

print("Part 1:", tuple(n.count('.')+1 for n in result_G))

