# 음이 아닌 가중치의 최단 거리. 최소 힙으로 다음 정점을 고른다.
from collections import deque


from heapq import heappop, heappush


from math import inf


def dijkstra(graph, start):
    # 인접 항목은 (정점, 가중치). (거리, 부모) 반환; 도달 불가는 (inf,-1).
    # 음수 가중치는 허용하지 않는다.
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
    # dijkstra의 부모 배열에서 경로 복원. 도달 불가면 []. O(V).
    path = []
    while target != -1:
        path.append(target)
        if target == start:
            return path[::-1]
        target = parent[target]
    return []
