"""원본: code/Geometry/PolarSort.cpp. O(N log N), O(N) space.
Origin first, then +x axis counterclockwise. Equal angle: nearest first.
"""
from functools import cmp_to_key


def polar_sort(points):
    def half(p):
        return 0 if p[1] > 0 or p[1] == 0 and p[0] >= 0 else 1

    def compare(a, b):
        if a == (0, 0) or b == (0, 0):
            return (b == (0, 0)) - (a == (0, 0))
        if half(a) != half(b):
            return half(a) - half(b)
        cross = a[0] * b[1] - a[1] * b[0]
        if cross:
            return -1 if cross > 0 else 1
        da, db = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2
        return (da > db) - (da < db)

    return sorted(points, key=cmp_to_key(compare))
