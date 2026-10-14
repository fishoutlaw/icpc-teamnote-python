# 연결된 무향 트리의 경로를 O(log N)개 구간으로 분해한다. 초기화 O(N).
# 구간은 [l,r), 순서 미보장: 교환 가능한 연산에만 사용한다.
# 간선 값은 자식 위치에 저장하고 edges=True로 질의한다.


class HLD:
    def __init__(self, graph, root=0):
        n = len(graph)
        self.parent = [-1] * n
        self.depth = [0] * n
        self.parent[root] = root
        order = [root]
        for v in order:
            for u in graph[v]:
                if self.parent[u] == -1:
                    self.parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    order.append(u)
        if len(order) != n or sum(map(len, graph)) != 2 * (n - 1):
            raise ValueError('connected undirected tree required')
        self.size = [1] * n
        heavy = [-1] * n
        for v in reversed(order[1:]):
            p = self.parent[v]
            self.size[p] += self.size[v]
            if heavy[p] == -1 or self.size[v] > self.size[heavy[p]]:
                heavy[p] = v
        self.head, self.pos = [0] * n, [0] * n
        stack, timer = [(root, root)], 0
        while stack:
            v, head = stack.pop()
            while v != -1:
                self.head[v], self.pos[v] = head, timer
                timer += 1
                for u in graph[v]:
                    if self.parent[u] == v and u != v and u != heavy[v]:
                        stack.append((u, u))
                v = heavy[v]

    def path_ranges(self, u, v, edges=False):
        ranges = []
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            ranges.append((self.pos[self.head[u]], self.pos[u] + 1))
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        l, r = self.pos[u] + int(edges), self.pos[v] + 1
        if l < r:
            ranges.append((l, r))
        return ranges

    def subtree_range(self, v):
        return self.pos[v], self.pos[v] + self.size[v]
