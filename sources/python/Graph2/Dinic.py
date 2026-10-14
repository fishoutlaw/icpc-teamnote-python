"""원본: code/Graph2/Dinic.cpp. Integer capacities, vertices 0..n-1.
Iterative Dinic O(V^2 E), O(V+E) space. Calls consume residual capacities.
max_flow returns additional flow; min_cut returns current residual partition.
"""
from collections import deque


class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]
        self.to, self.capacity = [], []

    def add_edge(self, u, v, capacity, reverse_capacity=0):
        if min(capacity, reverse_capacity) < 0:
            raise ValueError('negative capacity')
        eid = len(self.to)
        self.graph[u].append(eid)
        self.graph[v].append(eid ^ 1)
        self.to.extend((v, u))
        self.capacity.extend((capacity, reverse_capacity))
        return eid

    def _levels(self, source):
        level = [-1] * len(self.graph)
        level[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for e in self.graph[v]:
                u = self.to[e]
                if self.capacity[e] > 0 and level[u] == -1:
                    level[u] = level[v] + 1
                    queue.append(u)
        return level

    def max_flow(self, source, sink, limit=None):
        if source == sink:
            raise ValueError('source equals sink')
        if limit is None:
            limit = sum(self.capacity[e] for e in self.graph[source])
        flow = 0
        while flow < limit:
            level = self._levels(source)
            if level[sink] == -1:
                break
            pos = [0] * len(self.graph)
            while flow < limit:
                vertices, path = [source], []
                while vertices and vertices[-1] != sink:
                    v = vertices[-1]
                    while pos[v] < len(self.graph[v]):
                        e = self.graph[v][pos[v]]
                        if self.capacity[e] > 0 and level[self.to[e]] == level[v] + 1:
                            break
                        pos[v] += 1
                    if pos[v] == len(self.graph[v]):
                        level[v] = -1
                        vertices.pop()
                        if path:
                            path.pop()
                    else:
                        e = self.graph[v][pos[v]]
                        path.append(e)
                        vertices.append(self.to[e])
                if not vertices:
                    break
                amount = min(limit - flow, min(self.capacity[e] for e in path))
                for e in path:
                    self.capacity[e] -= amount
                    self.capacity[e ^ 1] += amount
                flow += amount
        return flow

    def min_cut(self, source):
        """Call after unrestricted max_flow. Returns (source side, other side)."""
        level = self._levels(source)
        return ([v for v, d in enumerate(level) if d != -1],
                [v for v, d in enumerate(level) if d == -1])
