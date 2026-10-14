"""원본: code/Graph2/SCC.cpp. Iterative Kosaraju, 0-based adjacency.
O(V+E) time/space. Component IDs are in topological order.
"""


def strongly_connected_components(graph):
    n = len(graph)
    reverse = [[] for _ in graph]
    for v in range(n):
        for u in graph[v]:
            reverse[u].append(v)
    seen = [False] * n
    order = []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, iter(graph[start]))]
        while stack:
            v, children = stack[-1]
            u = next(children, None)
            if u is None:
                order.append(v)
                stack.pop()
            elif not seen[u]:
                seen[u] = True
                stack.append((u, iter(graph[u])))
    component = [-1] * n
    groups = []
    for start in reversed(order):
        if component[start] != -1:
            continue
        component[start] = len(groups)
        group, stack = [], [start]
        while stack:
            v = stack.pop()
            group.append(v)
            for u in reverse[v]:
                if component[u] == -1:
                    component[u] = component[start]
                    stack.append(u)
        groups.append(group)
    return component, groups
