#! /usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
from math import prod
from random import choice
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

graphe_ori = set()
edges_ori = []
for line in lines:
    node, siblings = line.split(': ')
    siblings = siblings.split()
    graphe_ori.add(node)
    for n in siblings:
        graphe_ori.add(n)
        edges_ori.append(frozenset((node, n)))


# https://en.wikipedia.org/wiki/Karger%27s_algorithm

def edge_contraction(edge: set, G, E):
    new_node = '.'.join(edge)
    return (G-edge)|{new_node}, [ (e-edge)|{new_node} if e&edge else e for e in E if e != edge ]


def cut_graph(G, E):
    while len(G) > 2:
        e = choice(tuple(E))
        # e = set(choices.pop(0))
        # print(e, E, G, '-'*8, sep="\n")
        G, E = edge_contraction(e, G, E)

    return G, E


# choices = ["AC", "ED", "IJ", ("G", "I.J"), ("A.C", "D.E"), ("G.I.J", "H"), ("A.C.D.E", "B"), ("G.I.J.H", "F")]
def min_cut(G_ori, E_ori):

    n = len(G_ori)
    mini = len(E_ori)
    result = None

    with ThreadPoolExecutor() as executor:
        futures = set()
        for _ in range(int(n**2/2)+1):
            futures.add(executor.submit(cut_graph, G_ori, E_ori))

            for f in as_completed(futures):
                G, E = f.result()
                print(mini, len(E), tuple(n.count('.')+1 for n in G))

                if len(E) < mini:
                    mini = len(E)
                    result = G, E

            if mini <= 3:
                for f in futures:
                    f.cancel()
                break

    return result

result_G, _ = min_cut(graphe_ori, edges_ori)

print("Part 1:", prod(n.count('.')+1 for n in result_G))

