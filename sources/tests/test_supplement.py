import itertools
import math
import random
import unittest
from functools import lru_cache
from pathlib import Path

from supplement.MultiplicationTable import kth_multiplication_table
from supplement.EditDistance import edit_distance
from supplement.GeometryExtra import (
    area2, perpendicular_foot, point_line_dist, reflected_point,
    intersection_x, intersection_y,
)


class SupplementTests(unittest.TestCase):
    def test_multiplication_table_all_ranks(self):
        for n in range(1, 21):
            values = sorted(i * j for i in range(1, n + 1) for j in range(1, n + 1))
            for k, expected in enumerate(values, 1):
                self.assertEqual(kth_multiplication_table(n, k), expected)

    def test_edit_distance_exhaustive(self):
        words = [''.join(p) for n in range(4) for p in itertools.product('ab', repeat=n)]
        @lru_cache(None)
        def reference(a, b):
            if not a or not b:
                return len(a) + len(b)
            return min(1 + reference(a[1:], b), 1 + reference(a, b[1:]),
                       (a[0] != b[0]) + reference(a[1:], b[1:]))
        for a in words:
            for b in words:
                self.assertEqual(edit_distance(a, b), reference(a, b))
        self.assertEqual(edit_distance('kitten', 'sitting'), 3)

    def test_geometry_projection_and_intersections(self):
        rng = random.Random(42)
        for _ in range(300):
            a, b, p = [tuple(rng.randint(-20, 20) for _ in range(2)) for _ in range(3)]
            if a == b:
                continue
            h, t = perpendicular_foot(a, b, p)
            dx, dy = b[0] - a[0], b[1] - a[1]
            self.assertAlmostEqual((p[0] - h[0]) * dx + (p[1] - h[1]) * dy, 0)
            self.assertAlmostEqual((h[0] - a[0]) * dy - (h[1] - a[1]) * dx, 0)
            self.assertAlmostEqual(point_line_dist(a, b, p), math.dist(p, h))
            self.assertAlmostEqual(area2(a, b, p), math.dist(p, h) * math.dist(a, b))
            reflected_twice = reflected_point(a, b, reflected_point(a, b, p))
            for actual, expected in zip(reflected_twice, p):
                self.assertAlmostEqual(actual, expected)
            for axis, intersect in enumerate((intersection_x, intersection_y)):
                q = intersect(a, b, 7)
                if b[axis] == a[axis]:
                    self.assertIsNone(q)
                else:
                    self.assertEqual(q[axis], 7)
                    self.assertAlmostEqual((q[0] - a[0]) * dy - (q[1] - a[1]) * dx, 0)
        for fn in (perpendicular_foot, point_line_dist, reflected_point):
            with self.assertRaises(ValueError):
                fn((1, 1), (1, 1), (0, 0))

    def test_quick_reference_syntax(self):
        path = Path(__file__).resolve().parents[1] / 'supplement/QuickReference.py'
        source = path.read_text(encoding='utf-8')
        compile(source, str(path), 'exec')
        self.assertFalse(any(line.lstrip().startswith('#') for line in source.splitlines()))


if __name__ == '__main__':
    unittest.main()
