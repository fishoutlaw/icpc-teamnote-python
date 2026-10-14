"""원본: code/Graph1/Dijkstra.cpp. 0-based.
Nonnegative weights. O(V+E log(E+1)), space O(V+E).
"""
from collections import deque


from heapq import heappop, heappush


from math import inf


def dijkstra(graph, start):
    """graph[v]의 항목은 (다음 정점, 가중치). (거리, 부모) 반환.

    도달 불가 거리는 inf, 부모는 -1. 음수 가중치는 ValueError.
    """
    if any(weight < 0 for edges in graph for _, weight in edges):
        raise ValueError('Dijkstra requires nonnegative weights')
    distance = [inf] * len(graph)
    parent = [-1] * len(graph)
    distance[start] = 0
    queue = [(0, start)]
    while queue:
        cost, v = heappop(queue)
        if cost != distance[v]:
            continue
        for u, weight in graph[v]:
            candidate = cost + weight
            if candidate < distance[u]:
                distance[u] = candidate
                parent[u] = v
                heappush(queue, (candidate, u))
    return distance, parent


def restore_path(parent, start, target):
    """dijkstra의 부모 배열에서 경로 복원. 도달 불가면 []. O(V)."""
    path = []
    while target != -1:
        path.append(target)
        if target == start:
            return path[::-1]
        target = parent[target]
    return []
