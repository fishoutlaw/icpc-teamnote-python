import random
import unittest
from math import inf
from python.graph import bfs, dfs, topological_sort, dijkstra, restore_path
from python.mst import DSU, kruskal
from python.search_sort import coordinate_compress, first_true, last_true


class AlgorithmsTest(unittest.TestCase):
    def test_search(self):
        for lo in range(-5, 6):
            for hi in range(lo, 7):
                for t in range(lo - 1, hi + 2):
                    self.assertEqual(first_true(lo, hi, lambda x: x >= t),
                                     next((x for x in range(lo, hi) if x >= t), hi))
                    self.assertEqual(last_true(lo, hi, lambda x: x <= t),
                                     max((x for x in range(lo, hi) if x <= t), default=lo - 1))
        self.assertEqual(coordinate_compress([50, 31, 24, 10, 46, 10]),
                         ([4, 2, 1, 0, 3, 0], [10, 24, 31, 46, 50]))
        self.assertEqual(coordinate_compress([]), ([], []))

    def test_graph(self):
        graph = [[1, 2], [2, 3], [0], [], []]
        self.assertEqual(bfs(graph, 0), [0, 1, 1, 2, -1])
        self.assertEqual(dfs(graph, 0), [0, 1, 2, 3])
        self.assertIsNone(topological_sort(graph))
        dag = [[1, 1, 2], [3], [3], [], []]
        order = topological_sort(dag)
        pos = {v: i for i, v in enumerate(order)}
        self.assertTrue(all(pos[v] < pos[u] for v in range(5) for u in dag[v]))
        self.assertEqual(topological_sort([]), [])
        self.assertEqual(len(dfs([[i + 1] for i in range(9999)] + [[]], 0)), 10000)

    def test_dijkstra_against_floyd(self):
        rng = random.Random(42)
        for _ in range(40):
            n = rng.randrange(1, 10)
            graph = [[] for _ in range(n)]
            expected = [[inf] * n for _ in range(n)]
            for v in range(n):
                expected[v][v] = 0
                for u in range(n):
                    if rng.random() < 0.25:
                        w = rng.randrange(10)
                        graph[v].append((u, w))
                        expected[v][u] = min(expected[v][u], w)
            for k in range(n):
                for v in range(n):
                    for u in range(n):
                        expected[v][u] = min(expected[v][u], expected[v][k] + expected[k][u])
            for start in range(n):
                distance, parent = dijkstra(graph, start)
                self.assertEqual(distance, expected[start])
                for target in range(n):
                    path = restore_path(parent, start, target)
                    if distance[target] == inf:
                        self.assertEqual(path, [])
                    else:
                        self.assertEqual((path[0], path[-1]), (start, target))
                        cost = sum(min(w for u, w in graph[a] if u == b)
                                   for a, b in zip(path, path[1:]))
                        self.assertEqual(cost, distance[target])
        with self.assertRaises(ValueError):
            dijkstra([[(0, -1)]], 0)

    def test_mst(self):
        dsu = DSU(4)
        self.assertTrue(dsu.union(0, 1))
        self.assertFalse(dsu.union(1, 0))
        self.assertEqual(dsu.components, 3)
        self.assertEqual(dsu.size[dsu.find(1)], 2)
        edges = [(-2, 0, 1), (3, 1, 2), (8, 0, 2), (-9, 2, 2), (3, 1, 2)]
        self.assertEqual(kruskal(4, edges), (1, [(-2, 0, 1), (3, 1, 2)]))
        self.assertEqual(kruskal(0, []), (0, []))
