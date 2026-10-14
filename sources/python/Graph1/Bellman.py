# 간선 (u,v,w)를 반복 완화한다. O(VE). 도달 가능한 음수 사이클은 None.
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
