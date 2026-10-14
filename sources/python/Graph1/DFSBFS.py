"""원본: code/Graph1/DFSBFS.cpp. 0-based.
BFS/iterative DFS O(V+E), space O(V).
"""
from collections import deque


from heapq import heappop, heappush


from math import inf


def bfs(graph, start):
    """시작점에서의 간선 수 거리. 도달 불가는 -1."""
    distance = [-1] * len(graph)
    distance[start] = 0
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for u in graph[v]:
            if distance[u] == -1:
                distance[u] = distance[v] + 1
                queue.append(u)
    return distance


def dfs(graph, start):
    """재귀 DFS와 같은 인접 리스트 순서로 방문. 재귀 깊이 제한 없음."""
    seen = [False] * len(graph)
    seen[start] = True
    order = [start]
    stack = [iter(graph[start])]
    while stack:
        u = next(stack[-1], None)
        if u is None:
            stack.pop()
        elif not seen[u]:
            seen[u] = True
            order.append(u)
            stack.append(iter(graph[u]))
    return order
