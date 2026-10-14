"""원본: code/Geometry/PointInConvexPolygon.cpp. O(log N), O(1) space.
Strict CCW convex hull without repeated endpoint (use convex_hull output).
Boundary included; 0/1/2-vertex degenerate hulls supported.
"""


def point_in_convex_polygon(hull, p):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def on_segment(a, b):
        return orient(a, b, p) == 0 and min(a, b) <= p <= max(a, b)

    n = len(hull)
    if n < 3:
        return bool(n) and on_segment(hull[0], hull[-1])
    a = hull[0]
    first, last = orient(a, hull[1], p), orient(a, hull[-1], p)
    if first < 0 or last > 0:
        return False
    if first == 0:
        return on_segment(a, hull[1])
    if last == 0:
        return on_segment(a, hull[-1])
    l, r = 1, n - 1
    while r - l > 1:
        m = (l + r) // 2
        if orient(a, hull[m], p) >= 0:
            l = m
        else:
            r = m
    return orient(hull[l], hull[r], p) >= 0
