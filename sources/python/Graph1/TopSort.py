"""원본: code/Graph1/TopSort.cpp. 0-based.
Topological sort O(V+E), space O(V). Cycle -> None.
"""
from collections import deque


from heapq import heappop, heappush


from math import inf


def topological_sort(graph):
    """DAG의 위상 순서. 사이클이 있으면 None. 빈 그래프는 []."""
    indegree = [0] * len(graph)
    for neighbors in graph:
        for u in neighbors:
            indegree[u] += 1
    queue = deque(v for v, degree in enumerate(indegree) if degree == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in graph[v]:
            indegree[u] -= 1
            if indegree[u] == 0:
                queue.append(u)
    return order if len(order) == len(graph) else None
