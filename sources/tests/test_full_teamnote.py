"""Seeded differential tests against small exhaustive/reference implementations."""
import importlib.util
import io
import itertools
import math
from pathlib import Path
import random
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('/', '_'), ROOT / 'python' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FullTeamnoteTest(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(20261014)

    def test_coverage_and_imports(self):
        for source in (ROOT / 'code').rglob('*.cpp'):
            name = source.relative_to(ROOT / 'code').with_suffix('').as_posix()
            load(name)

    def test_sorting_and_search(self):
        stl = load('Sorting/STL')
        compare = load('Sorting/Compare')
        binary = load('Misc/BinarySearch')
        compress = load('Sorting/CoordCompress').coordinate_compress
        for _ in range(100):
            values = [self.rng.randrange(-10, 11) for _ in range(30)]
            ordered = sorted(values)
            k = self.rng.randrange(len(values))
            copy = values[:]
            self.assertEqual(stl.nth_element(copy, k), ordered[k])
            self.assertTrue(all(x <= copy[k] for x in copy[:k]))
            self.assertTrue(all(x >= copy[k] for x in copy[k + 1:]))
            for x in range(-11, 12):
                l, r = stl.equal_range(ordered, x)
                self.assertEqual(r - l, values.count(x))
                self.assertEqual(stl.contains(ordered, x), x in values)
                self.assertEqual(binary.first_true(0, 30, lambda i: ordered[i] >= x), l)
            ranks, unique = compress(values)
            self.assertEqual([unique[i] for i in ranks], values)
        self.assertEqual(compare.sort_points([(1, 2), (1, 1)]), [(1, 1), (1, 2)])

    def test_segment_trees(self):
        plain = load('DataStructure/SegmentTree').SegmentTree
        lazy = load('DataStructure/SegmentTreeLazy').LazySegmentTree
        persistent = load('DataStructure/PersistentSegmentTree').PersistentSegmentTree
        for n in (0, 1, 2, 7, 33):
            values = [0] * n
            a, b = plain(values), lazy(n)
            for _ in range(150):
                l, r = sorted((self.rng.randrange(n + 1), self.rng.randrange(n + 1)))
                delta = self.rng.randrange(-20, 21)
                b.add(l, r, delta)
                for i in range(l, r):
                    values[i] += delta
                    a.set(i, values[i])
                l, r = sorted((self.rng.randrange(n + 1), self.rng.randrange(n + 1)))
                self.assertEqual(a.sum(l, r), sum(values[l:r]))
                self.assertEqual(b.sum(l, r), sum(values[l:r]))
        values = [self.rng.randrange(20) for _ in range(80)]
        tree = persistent(20)
        for i, x in enumerate(values):
            tree.insert(i, x)
        for _ in range(100):
            l = self.rng.randrange(len(values))
            r = self.rng.randrange(l + 1, len(values) + 1)
            k = self.rng.randrange(1, r - l + 1)
            self.assertEqual(tree.kth(l, r, k), sorted(values[l:r])[k - 1])

    def test_line_containers(self):
        mod = load('DataStructure/ConvexHullTrick')
        for _ in range(50):
            lines = [(self.rng.randrange(-20, 21), self.rng.randrange(-100, 101)) for _ in range(40)]
            hull, tree = mod.MonotoneCHT(), mod.LiChao(-50, 50)
            for i, (a, b) in enumerate(sorted(lines)):
                hull.add(a, b, i)
            for a, b in lines:
                tree.add(a, b)
            for x in range(-50, 51):
                expected = max(a * x + b for a, b in lines)
                self.assertEqual(hull.query(x)[0], expected)
                self.assertEqual(tree.query(x), expected)
        hull, lines = mod.MonotoneCHT(), []
        for i in range(60):
            line = (i // 2, self.rng.randrange(-100, 101))
            lines.append(line)
            hull.add(*line)
            x = i - 30
            self.assertEqual(hull.query(x)[0], max(a * x + b for a, b in lines))

    def test_graph_distances_and_scc(self):
        floyd = load('Graph1/Floyd').floyd_warshall
        bellman = load('Graph1/Bellman').bellman_ford
        dijkstra = load('Graph1/Dijkstra').dijkstra
        scc = load('Graph2/SCC').strongly_connected_components
        for _ in range(60):
            n = 7
            edges = [(u, v, self.rng.randrange(10)) for u in range(n) for v in range(n) if self.rng.random() < .2]
            graph, weighted = [[] for _ in range(n)], [[] for _ in range(n)]
            for u, v, w in edges:
                graph[u].append(v)
                weighted[u].append((v, w))
            expected = floyd(n, edges)
            comp, groups = scc(graph)
            self.assertEqual(sorted(sum(groups, [])), list(range(n)))
            for u in range(n):
                self.assertEqual(bellman(n, edges, u), expected[u])
                self.assertEqual(dijkstra(weighted, u)[0], expected[u])
                for v in range(n):
                    self.assertEqual(comp[u] == comp[v], expected[u][v] < math.inf and expected[v][u] < math.inf)
                for v in graph[u]:
                    self.assertLessEqual(comp[u], comp[v])
        self.assertIsNone(bellman(3, [(0, 1, -1), (1, 0, 0)], 0))
        self.assertEqual(bellman(3, [(0, 1, -1), (1, 0, 0)], 2), [math.inf, math.inf, 0])
        self.assertEqual(bellman(3, [(0, 1, -4), (1, 2, 2)], 0), [0, -4, -2])

    def test_bcc_against_deletion(self):
        bcc = load('Graph2/BCC').biconnected_components
        for _ in range(100):
            n = 6
            edges = [tuple(self.rng.sample(range(n), 2)) for _ in range(10)]
            def count(skip_vertex=-1, skip_edge=-1):
                graph = [[] for _ in range(n)]
                for i, (u, v) in enumerate(edges):
                    if skip_vertex not in (u, v) and i != skip_edge:
                        graph[u].append(v)
                        graph[v].append(u)
                seen, total = {skip_vertex}, 0
                for v in range(n):
                    if v not in seen:
                        total += 1
                        seen.add(v)
                        stack = [v]
                        while stack:
                            for u in graph[stack.pop()]:
                                if u not in seen:
                                    seen.add(u)
                                    stack.append(u)
                return total
            cuts, bridges, groups = bcc(n, edges)
            base = count()
            self.assertEqual(cuts, [v for v in range(n) if count(skip_vertex=v) > base])
            self.assertEqual(set(bridges), {i for i in range(len(edges)) if count(skip_edge=i) > base})
            self.assertEqual(set().union(*map(set, groups)), set(range(n)))
            for u, v in edges:
                self.assertEqual(sum(u in group and v in group for group in groups), 1)

    def test_flow_against_all_cuts(self):
        Dinic = load('Graph2/Dinic').Dinic
        for _ in range(80):
            n = 6
            edges = [(u, v, self.rng.randrange(5)) for u in range(n) for v in range(n) if self.rng.random() < .2]
            network = Dinic(n)
            for u, v, c in edges:
                network.add_edge(u, v, c)
            expected = min(sum(c for u, v, c in edges if mask >> u & 1 and not mask >> v & 1)
                           for mask in range(1 << n) if mask & 1 and not mask >> (n - 1) & 1)
            self.assertEqual(network.max_flow(0, n - 1), expected)
            a, b = network.min_cut(0)
            self.assertEqual(sum(c for u, v, c in edges if u in a and v in b), expected)
            self.assertEqual(network.max_flow(0, n - 1), 0)
        network = Dinic(2000)
        for i in range(1999):
            network.add_edge(i, i + 1, 7)
        self.assertEqual(network.max_flow(0, 1999), 7)

    def test_mcmf_exhaustive(self):
        MCF = load('Graph2/MCMF').MinCostFlow
        for _ in range(30):
            edges = [(0, 1, 2, self.rng.randrange(-3, 5)), (0, 2, 2, 2),
                     (1, 2, 1, -2), (1, 3, 2, 3), (2, 3, 2, 1)]
            for limit in (0, 1, 3, None):
                feasible = []
                for amounts in itertools.product(*(range(c + 1) for _, _, c, _ in edges)):
                    net = [0] * 4
                    cost = 0
                    for (u, v, c, w), f in zip(edges, amounts):
                        net[u] -= f
                        net[v] += f
                        cost += f * w
                    if net[1] == net[2] == 0 and (limit is None or net[3] <= limit):
                        feasible.append((net[3], cost))
                expected = min(feasible, key=lambda x: (-x[0], x[1]))
                network = MCF(4)
                for edge in edges:
                    network.add_edge(*edge)
                self.assertEqual(network.run(0, 3, limit), expected)
        network = MCF(2)
        network.add_edge(0, 0, 1, -1)
        network.add_edge(0, 1, 1, 0)
        with self.assertRaises(ValueError):
            network.run(0, 1)

    def test_matching_against_bruteforce(self):
        match = load('Graph2/Hopcroft').hopcroft_karp
        for _ in range(80):
            graph = [[u for u in range(5) if self.rng.random() < .4] for _ in range(5)]
            def brute(v, used):
                if v == len(graph):
                    return 0
                return max([brute(v + 1, used)] + [1 + brute(v + 1, used | {u}) for u in graph[v] if u not in used])
            left, right, (a, b) = match(graph, 5)
            size = sum(x != -1 for x in left)
            self.assertEqual(size, brute(0, set()))
            self.assertEqual(size, len(a) + len(b))
            self.assertTrue(all(v in a or u in b for v in range(5) for u in graph[v]))
            for v, u in enumerate(left):
                if u != -1:
                    self.assertIn(u, graph[v])
                    self.assertEqual(right[u], v)

    def test_lca_hld(self):
        LCA, HLD = load('Graph2/LCA').LCA, load('Graph2/HLD').HLD
        graph = [[] for _ in range(100)]
        parent = [0] + [self.rng.randrange(v) for v in range(1, 100)]
        for v in range(1, 100):
            graph[v].append(parent[v])
            graph[parent[v]].append(v)
        lca, hld = LCA(graph), HLD(graph)
        def ancestors(v):
            result = [v]
            while v:
                v = parent[v]
                result.append(v)
            return result
        for _ in range(150):
            u, v = self.rng.randrange(100), self.rng.randrange(100)
            a, b = ancestors(u), ancestors(v)
            common = next(x for x in a if x in b)
            self.assertEqual(lca.query(u, v), common)
            path = a[:a.index(common)] + b[:b.index(common)] + [common]
            positions = [i for l, r in hld.path_ranges(u, v) for i in range(l, r)]
            self.assertEqual(sorted(positions), sorted(hld.pos[x] for x in path))
            edge_positions = [i for l, r in hld.path_ranges(u, v, True) for i in range(l, r)]
            self.assertEqual(sorted(edge_positions), sorted(hld.pos[x] for x in path if x != common))
        for v in range(100):
            l, r = hld.subtree_range(v)
            self.assertEqual(set(range(l, r)), {hld.pos[u] for u in range(100) if v in ancestors(u)})

    def test_number_theory(self):
        trial = load('Math/Primes')
        sieve = load('Math/Sieve')
        linear = load('Math/LinearSieve').linear_sieve
        mr = load('Math/MillerRabin-PollardRho')
        egcd = load('Math/ExtendedEuclidean').extended_gcd
        division = load('Math/Division')
        primes, spf, phi, mu, tau, sigma = linear(400)
        table = sieve.sieve(400)
        for n in range(1, 401):
            factors = trial.factorize(n)
            self.assertEqual(mr.is_prime(n), trial.is_prime(n))
            self.assertEqual(mr.factorize(n), factors)
            self.assertEqual(sieve.factorize(n, table), factors)
            self.assertEqual(spf[n], table[n])
            divisors = [d for d in range(1, n + 1) if n % d == 0]
            self.assertEqual((tau[n], sigma[n]), (len(divisors), sum(divisors)))
            self.assertEqual(phi[n], sum(math.gcd(i, n) == 1 for i in range(1, n + 1)))
            self.assertEqual(mu[n], 0 if any(e > 1 for _, e in factors) else (-1) ** len(factors))
        self.assertFalse(mr.is_prime(341550071728321))
        self.assertEqual(mr.factorize(1000000007 * 1000000009), [(1000000007, 1), (1000000009, 1)])
        for a in range(-15, 16):
            for b in range(-15, 16):
                g, x, y = egcd(a, b)
                self.assertEqual(a * x + b * y, math.gcd(a, b))
                self.assertEqual(g, math.gcd(a, b))
                if b:
                    self.assertEqual(division.floor_div(a, b), math.floor(a / b))
                    self.assertEqual(division.ceil_div(a, b), math.ceil(a / b))
        pow_mod = load('Math/PowMod').pow_mod
        self.assertEqual(pow_mod(-7, 20, 123), (-7) ** 20 % 123)

    def test_crt_lucas(self):
        crt = load('Math/ChineseRemainderTheorem').crt
        Lucas = load('Math/LucasTheorem').Lucas
        for m in range(1, 10):
            for n in range(1, 10):
                a, b = self.rng.randrange(-20, 21), self.rng.randrange(-20, 21)
                modulus = math.lcm(m, n)
                value = next((x for x in range(modulus) if x % m == a % m and x % n == b % n), None)
                self.assertEqual(crt([(a, m), (b, n)]), None if value is None else (value, modulus))
        for p in (2, 3, 7, 13):
            lucas = Lucas(p)
            for n in range(40):
                for r in range(n + 2):
                    self.assertEqual(lucas.calc(n, r), math.comb(n, r) % p)

    def test_matrix(self):
        gauss = load('Math/Matrix').gauss
        for mod in (None, 101):
            for _ in range(30):
                a = [[self.rng.randrange(-5, 6) for _ in range(3)] for _ in range(3)]
                det = sum((-1) ** sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
                          * math.prod(a[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3)))
                rref, rank, determinant, inverse = gauss(a, mod)
                self.assertEqual(determinant, det if mod is None else det % mod)
                if inverse is not None:
                    for i in range(3):
                        for j in range(3):
                            value = sum(a[i][k] * inverse[k][j] for k in range(3))
                            self.assertEqual(value if mod is None else value % mod, int(i == j))
                else:
                    self.assertLess(rank, 3)
        self.assertEqual(gauss([[1, 2, 3], [2, 4, 6]])[1:], (1, None, None))

    def test_convolutions(self):
        conv = load('Math/Convolution')
        for _ in range(40):
            a = [self.rng.randrange(-100, 101) for _ in range(self.rng.randrange(1, 20))]
            b = [self.rng.randrange(-100, 101) for _ in range(self.rng.randrange(1, 20))]
            expected = [0] * (len(a) + len(b) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    expected[i + j] += x * y
            self.assertEqual(conv.multiply(a, b), expected)
            for mod in (1, 998244353, 1000000007, 10 ** 40):
                self.assertEqual(conv.multiply_mod(a, b, mod), [x % mod for x in expected])
        for kind in ('xor', 'or', 'and'):
            a, b = list(range(8)), list(range(-4, 4))
            expected = [0] * 8
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    index = {'xor': i ^ j, 'or': i | j, 'and': i & j}[kind]
                    expected[index] += x * y
            self.assertEqual(conv.bitwise_convolution(a, b, kind), expected)

    def test_strings(self):
        kmp = load('String/KMP').kmp
        z = load('String/Z').z_function
        manacher = load('String/Manacher').manacher
        suffix = load('String/SuffixArray').suffix_array
        Hashing = load('String/Hashing').Hashing
        for _ in range(100):
            s = ''.join(self.rng.choice('ab#한') for _ in range(self.rng.randrange(30)))
            p = ''.join(self.rng.choice('ab#한') for _ in range(self.rng.randrange(5)))
            self.assertEqual(kmp(s, p), [i for i in range(len(s) + 1) if s.startswith(p, i)])
            expected_z = []
            for i in range(len(s)):
                length = 0
                while i + length < len(s) and s[length] == s[i + length]:
                    length += 1
                expected_z.append(length)
            self.assertEqual(z(s), expected_z)
            sa, lcp = suffix(s)
            self.assertEqual(sa, sorted(range(len(s)), key=lambda i: s[i:]))
            for i in range(1, len(sa)):
                a, b, length = sa[i - 1], sa[i], 0
                while a + length < len(s) and b + length < len(s) and s[a + length] == s[b + length]:
                    length += 1
                self.assertEqual(lcp[i], length)
            palindrome = max((j - i for i in range(len(s) + 1) for j in range(i, len(s) + 1)
                              if s[i:j] == s[i:j][::-1]), default=0)
            self.assertEqual(max(manacher(s)), palindrome)
            h = Hashing(s)
            for i in range(len(s) + 1):
                for j in range(i, len(s) + 1):
                    self.assertEqual(h.get(i, j), Hashing(s[i:j]).get(0, j - i))

    def test_geometry(self):
        hull_fn = load('Geometry/ConvexHull').convex_hull
        inside = load('Geometry/PointInPolygon').point_in_polygon
        convex_inside = load('Geometry/PointInConvexPolygon').point_in_convex_polygon
        calipers = load('Geometry/Calipers').calipers
        area = load('Geometry/PolygonArea').polygon_area2
        template = load('Geometry/Template')
        cross = load('Geometry/SegmentIntersection').segment_intersection
        polar = load('Geometry/PolarSort').polar_sort
        for _ in range(80):
            points = [(self.rng.randrange(-10, 11), self.rng.randrange(-10, 11)) for _ in range(15)]
            hull = hull_fn(points)
            self.assertTrue(all(inside(hull, p) for p in points))
            self.assertTrue(all(template.orient(hull[i - 2], hull[i - 1], hull[i]) > 0 for i in range(len(hull))))
            for _ in range(20):
                p = (self.rng.randrange(-12, 13), self.rng.randrange(-12, 13))
                self.assertEqual(convex_inside(hull, p), inside(hull, p))
            a, b = calipers(hull)
            expected = max(template.distance_squared(x, y) for x in points for y in points)
            self.assertEqual(template.distance_squared(a, b), expected)
        self.assertEqual(area([(0, 0), (4, 0), (4, 3), (0, 3)]), 24)
        self.assertEqual(cross((0, 0), (2, 2), (0, 2), (2, 0)), (1, (1, 1)))
        self.assertEqual(cross((0, 0), (3, 0), (1, 0), (4, 0)), (-1, None))
        self.assertEqual(cross((1, 0), (1, 0), (0, 0), (2, 0)), (1, (1, 0)))
        self.assertEqual(cross((1, 1), (1, 1), (0, 0), (2, 0)), (0, None))
        self.assertEqual(polar([(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]),
                         [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)])
        for hull in ([], [(1, 1)], [(0, 0), (2, 0)]):
            for p in ((0, 0), (1, 1), (1, 0), (3, 0)):
                self.assertEqual(convex_inside(hull, p), inside(hull, p))

    def test_misc(self):
        lis = load('Misc/LIS').lis
        ternary = load('Misc/TernarySearch')
        grammar = load('Misc/Cpp-Grammer')
        reference = load('Misc/Reference')
        for _ in range(80):
            values = [self.rng.randrange(10) for _ in range(10)]
            dp = [1] * len(values)
            for i in range(len(values)):
                for j in range(i):
                    if values[j] < values[i]:
                        dp[i] = max(dp[i], dp[j] + 1)
            result = lis(values)
            self.assertEqual(len(result), max(dp))
            self.assertTrue(all(a < b for a, b in zip(result, result[1:])))
            it = iter(values)
            self.assertTrue(all(any(y == x for y in it) for x in result))
        for center in range(-20, 21):
            self.assertEqual(ternary.ternary_integer(-20, 20, lambda x: (x - center) ** 2), center)
        self.assertAlmostEqual(ternary.ternary_real(-10, 10, lambda x: (x - 2.5) ** 2), 2.5)
        for n in range(1, 100):
            for digit in range(10):
                self.assertEqual(grammar.digit_frequency(n, digit), ''.join(map(str, range(1, n + 1))).count(str(digit)))
            next_value = grammar.next_same_popcount(n)
            self.assertEqual(next_value, next(x for x in range(n + 1, next_value + 1) if x.bit_count() == n.bit_count()))
        for n in range(10):
            for m in range(1, 10):
                for a in range(-3, 8):
                    self.assertEqual(reference.floor_sum(n, m, a, -4), sum((a * i - 4) // m for i in range(n)))
        self.assertEqual([reference.catalan(n) for n in range(6)], [1, 1, 2, 5, 14, 42])
        self.assertEqual([reference.bell(n) for n in range(6)], [1, 1, 2, 5, 15, 52])
        self.assertEqual(reference.derangements(6), 265)
        self.assertAlmostEqual(reference.simpson(lambda x: x ** 3, 0, 2), 4)
        self.assertAlmostEqual(reference.newton(lambda x: x * x - 2, lambda x: 2 * x, 1), math.sqrt(2))
        ordered = grammar.OrderedSet([3, 1, 1])
        ordered.add(2)
        ordered.discard(1)
        self.assertEqual((ordered.order_of_key(3), ordered.find_by_order(0)), (1, 2))

    def test_fast_io(self):
        mod = load('Misc/FastIO')
        data = b' -123\n0 45\t-6\r\n789 +2'
        expected = [-123, 0, 45, -6, 789, 2]
        self.assertEqual(mod.read_ints(io.BytesIO(data)), expected)
        for size in (1, 2, 3, 8, 100):
            self.assertEqual(list(mod.iter_ints(io.BytesIO(data), size)), expected)
        output = io.StringIO()
        mod.write_lines(expected, output)
        self.assertEqual(output.getvalue(), '\n'.join(map(str, expected)))
