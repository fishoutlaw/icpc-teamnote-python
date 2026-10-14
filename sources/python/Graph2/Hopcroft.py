# 왼쪽에서 오른쪽 정점 번호로 향하는 인접 리스트의 최대 이분 매칭.
# 양쪽 매칭 배열과 최소 정점 커버를 반환한다. O((V+E) sqrt(V)).
from collections import deque


def hopcroft_karp(graph, m):
    n = len(graph)
    left, right = [-1] * n, [-1] * m
    while True:
        distance = [-1] * n
        queue = deque()
        for v in range(n):
            if left[v] == -1:
                distance[v] = 0
                queue.append(v)
        shortest = n + 1
        while queue:
            v = queue.popleft()
            if distance[v] >= shortest:
                continue
            for u in graph[v]:
                w = right[u]
                if w == -1:
                    shortest = distance[v] + 1
                elif distance[w] == -1:
                    distance[w] = distance[v] + 1
                    queue.append(w)
        if shortest == n + 1:
            break
        pos = [0] * n
        for start in range(n):
            if left[start] != -1:
                continue
            stack, links = [start], []
            while stack:
                v = stack[-1]
                if pos[v] == len(graph[v]):
                    distance[v] = -1
                    stack.pop()
                    if links:
                        links.pop()
                    continue
                u = graph[v][pos[v]]
                pos[v] += 1
                w = right[u]
                if w == -1 and distance[v] + 1 == shortest:
                    for a, b in zip(stack, links + [u]):
                        left[a], right[b] = b, a
                    break
                if w != -1 and distance[w] == distance[v] + 1:
                    stack.append(w)
                    links.append(u)
    seen_l = {v for v in range(n) if left[v] == -1}
    seen_r = set()
    queue = deque(seen_l)
    while queue:
        v = queue.popleft()
        for u in graph[v]:
            if u == left[v] or u in seen_r:
                continue
            seen_r.add(u)
            w = right[u]
            if w != -1 and w not in seen_l:
                seen_l.add(w)
                queue.append(w)
    cover = ([v for v in range(n) if v not in seen_l], sorted(seen_r))
    return left, right, cover
