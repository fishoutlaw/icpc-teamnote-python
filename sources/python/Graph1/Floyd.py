# 모든 쌍 최단 거리 O(V^3). d[v][v]<0이면 음수 사이클이 있다.
# 음수 사이클을 거치는 경로의 거리는 유효하지 않다.
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
