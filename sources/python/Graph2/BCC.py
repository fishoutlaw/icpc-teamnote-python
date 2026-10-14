# 무향 간선 (u,v)의 단절점·단절선 번호·이중 연결 정점 묶음. O(V+E).
# 다중 간선 허용, 자기 루프 금지. 고립점도 묶음이며 단절점은 중복 소속 가능.


def biconnected_components(n, edges):
    graph = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        if u == v:
            raise ValueError('self loops are not supported')
        graph[u].append((v, eid))
        graph[v].append((u, eid))
    tin, low, parent = [-1] * n, [0] * n, [-1] * n
    children = [0] * n
    cuts, bridges, groups, edge_stack = set(), [], [], []
    timer = 0
    for root in range(n):
        if tin[root] != -1:
            continue
        tin[root] = low[root] = timer
        timer += 1
        stack = [(root, -1, iter(graph[root]))]
        while stack:
            v, pe, it = stack[-1]
            item = next(it, None)
            if item is not None:
                u, eid = item
                if eid == pe:
                    continue
                if tin[u] == -1:
                    parent[u] = v
                    children[v] += 1
                    edge_stack.append((v, u, eid))
                    tin[u] = low[u] = timer
                    timer += 1
                    stack.append((u, eid, iter(graph[u])))
                elif tin[u] < tin[v]:
                    low[v] = min(low[v], tin[u])
                    edge_stack.append((v, u, eid))
                continue
            stack.pop()
            p = parent[v]
            if p == -1:
                if children[v] > 1:
                    cuts.add(v)
                if not graph[v]:
                    groups.append([v])
            else:
                low[p] = min(low[p], low[v])
                if low[v] > tin[p]:
                    bridges.append(pe)
                if low[v] >= tin[p]:
                    if parent[p] != -1:
                        cuts.add(p)
                    group = set()
                    while True:
                        a, b, eid = edge_stack.pop()
                        group.update((a, b))
                        if eid == pe:
                            break
                    groups.append(list(group))
    return sorted(cuts), bridges, groups
