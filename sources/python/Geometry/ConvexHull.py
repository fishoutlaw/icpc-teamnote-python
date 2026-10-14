# 단조 체인 볼록 껍질 O(N log N). 반시계 방향, 끝점 중복·일직선 내부점 제거.


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
