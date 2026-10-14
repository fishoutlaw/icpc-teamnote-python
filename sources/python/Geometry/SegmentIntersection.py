"""원본: code/Geometry/SegmentIntersection.cpp. Exact integer geometry O(1).
Returns (0,None), (1,point), or (-1,None) for overlapping interval.
Unique intersection coordinates are Fractions. Point segments supported.
"""
from fractions import Fraction


def segment_intersection(a, b, c, d):
    def cross(u, v):
        return u[0] * v[1] - u[1] * v[0]

    def sub(u, v):
        return u[0] - v[0], u[1] - v[1]

    u, v, w = sub(b, a), sub(d, c), sub(c, a)
    det = cross(u, v)
    if det:
        t, s = Fraction(cross(w, v), det), Fraction(cross(w, u), det)
        if 0 <= t <= 1 and 0 <= s <= 1:
            return 1, (a[0] + t * u[0], a[1] + t * u[1])
        return 0, None
    if cross(u, w) or cross(v, w):
        return 0, None
    lo, hi = max(min(a, b), min(c, d)), min(max(a, b), max(c, d))
    if lo > hi:
        return 0, None
    return (1, lo) if lo == hi else (-1, None)
