"""원본: code/Geometry/PolygonArea.cpp. Simple polygon in boundary order.
Returns twice area (exact integer), O(N) time, O(1) auxiliary space.
"""


def polygon_area2(points):
    return abs(sum(points[i][0] * points[(i + 1) % len(points)][1]
                   - points[i][1] * points[(i + 1) % len(points)][0]
                   for i in range(len(points))))
