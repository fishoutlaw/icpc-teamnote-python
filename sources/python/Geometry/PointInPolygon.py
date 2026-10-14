# 단순 다각형 내부 판별 O(N). 감김 수를 사용하며 경계를 포함한다.


def point_in_polygon(points, p):
    winding = 0
    for i, a in enumerate(points):
        b = points[(i + 1) % len(points)]
        cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cross == 0 and min(a, b) <= p <= max(a, b):
            return True
        if a[1] <= p[1] < b[1] and cross > 0:
            winding += 1
        if b[1] <= p[1] < a[1] and cross < 0:
            winding -= 1
    return winding != 0
