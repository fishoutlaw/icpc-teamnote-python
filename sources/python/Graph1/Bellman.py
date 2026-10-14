"""원본: code/Graph1/Bellman.cpp. 0-based edges (u,v,w).
O(VE) time, O(V) space. Return None for a reachable negative cycle.
"""
from math import inf


def bellman_ford(n, edges, start):
    edges = list(edges)
    d = [inf] * n
    d[start] = 0
    for step in range(n):
        changed = False
        for u, v, w in edges:
            if d[u] != inf and d[v] > d[u] + w:
                d[v] = d[u] + w
                changed = True
        if not changed:
            return d
    return None
