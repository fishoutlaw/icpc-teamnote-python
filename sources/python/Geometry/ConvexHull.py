"""원본: code/Geometry/ConvexHull.cpp. Monotone chain replaces Graham scan.
O(N log N), O(N) space. CCW hull; no repeated end or collinear interior points.
"""


def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def chain(items):
        hull = []
        for p in items:
            while len(hull) > 1 and orient(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull

    return chain(points)[:-1] + chain(reversed(points))[:-1]
