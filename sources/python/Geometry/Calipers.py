"""원본: code/Geometry/Calipers.cpp. CCW strict convex hull (no repeated end).
O(N) time, O(1) space. Return farthest point pair; empty -> None.
"""


def calipers(hull):
    n = len(hull)
    if not n:
        return None
    if n <= 2:
        return hull[0], hull[-1]

    def area(i, k, j):
        a, b, c = hull[i], hull[k], hull[j]
        return abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))

    best, pair, j = -1, None, 1
    for i in range(n):
        k = (i + 1) % n
        while area(i, k, (j + 1) % n) > area(i, k, j):
            j = (j + 1) % n
        for a, b in ((hull[i], hull[j]), (hull[k], hull[j])):
            distance = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            if distance > best:
                best, pair = distance, (a, b)
    return pair
