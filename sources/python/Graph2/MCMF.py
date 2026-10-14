"""원본: code/Graph2/MCMF.cpp. 0-based, integral capacities/costs.
Bellman-Ford augmenting paths: O(A VE), A = augmentation count; O(V+E) space.
Negative costs allowed; reachable residual negative cycles raise ValueError.
run(s,t,k=None) returns additional (flow,cost), mutates residual network.
"""
from math import inf


class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.edges = []

    def add_edge(self, u, v, capacity, cost):
        if capacity < 0:
            raise ValueError('negative capacity')
        self.edges.extend(([u, v, capacity, cost], [v, u, 0, -cost]))

    def run(self, source, sink, limit=None):
        if source == sink:
            raise ValueError('source equals sink')
        if limit is None:
            limit = sum(c for u, v, c, w in self.edges if u == source)
        flow = cost = 0
        while flow < limit:
            d, parent = [inf] * self.n, [-1] * self.n
            d[source] = 0
            for step in range(self.n):
                changed = False
                for eid, (u, v, capacity, weight) in enumerate(self.edges):
                    if capacity and d[u] != inf and d[v] > d[u] + weight:
                        d[v], parent[v] = d[u] + weight, eid
                        changed = True
                if not changed:
                    break
                if step == self.n - 1:
                    raise ValueError('reachable negative cost cycle')
            if d[sink] == inf:
                break
            amount, v = limit - flow, sink
            while v != source:
                e = parent[v]
                amount = min(amount, self.edges[e][2])
                v = self.edges[e][0]
            v = sink
            while v != source:
                e = parent[v]
                self.edges[e][2] -= amount
                self.edges[e ^ 1][2] += amount
                v = self.edges[e][0]
            flow += amount
            cost += amount * d[sink]
        return flow, cost
