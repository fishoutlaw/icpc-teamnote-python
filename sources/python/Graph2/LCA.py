# 연결된 무향 트리의 최소 공통 조상. 전처리 O(N log N), 질의 O(log N).


class LCA:
    def __init__(self, graph, root=0):
        n = len(graph)
        self.depth = [-1] * n
        self.depth[root] = 0
        parent = [root] * n
        order = [root]
        for v in order:
            for u in graph[v]:
                if self.depth[u] == -1:
                    parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    order.append(u)
        if len(order) != n or sum(map(len, graph)) != 2 * (n - 1):
            raise ValueError('connected undirected tree required')
        self.up = [parent]
        for _ in range(1, n.bit_length()):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(n)])

    def query(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        for k in range(len(self.up)):
            if diff >> k & 1:
                u = self.up[k][u]
        if u == v:
            return u
        for level in reversed(self.up):
            if level[u] != level[v]:
                u, v = level[u], level[v]
        return self.up[0][u]
