"""원본: code/Graph1/Floyd.cpp. 0-based directed edges (u,v,w).
O(V^3) time / O(V^2) space. Negative cycle: some d[v][v] < 0.
Distances affected by negative cycles are not valid shortest distances.
"""
from math import inf


def floyd_warshall(n, edges):
    d = [[inf] * n for _ in range(n)]
    for v in range(n):
        d[v][v] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            if d[i][k] == inf:
                continue
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d
