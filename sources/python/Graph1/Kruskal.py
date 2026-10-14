# 간선을 가중치순으로 골라 최소 신장 포리스트를 만든다. O(V+E log(E+1)).
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, v):
        while self.parent[v] != v:
            self.parent[v] = self.parent[self.parent[v]]
            v = self.parent[v]
        return v

    def union(self, u, v):
        u, v = self.find(u), self.find(v)
        if u == v:
            return False
        if self.size[u] < self.size[v]:
            u, v = v, u
        self.parent[v] = u
        self.size[u] += self.size[v]
        self.components -= 1
        return True


def kruskal(n, edges):
    # 간선은 (가중치,u,v). (비용, 선택 간선) 반환; 연결 그래프면 간선 수 n-1.
    dsu = DSU(n)
    total = 0
    selected = []
    for weight, u, v in sorted(edges):
        if dsu.union(u, v):
            total += weight
            selected.append((weight, u, v))
    return total, selected
