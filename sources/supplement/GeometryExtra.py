import math
from python.Geometry.Template import sub, dot, cross, distance_squared


def area2(a, b, p):
    # 삼각형 넓이의 두 배. 정수 좌표에서는 정확한 정수.
    return abs(cross(sub(b, a), sub(p, a)))


def perpendicular_foot(a, b, p):
    # 직선 AB 위 수선의 발과 비율 t. A!=B, 실수 근삿값 반환.
    v = sub(b, a)
    denom = dot(v, v)
    if denom == 0:
        raise ValueError('A와 B가 같아 직선이 정의되지 않음')
    t = dot(sub(p, a), v) / denom
    h = (a[0] + t * v[0], a[1] + t * v[1])
    return h, t  # 0<=t<=1이면 발이 선분 위에 있다.


def point_line_dist(a, b, p):
    # 점과 무한 직선 사이 거리. A!=B, 실수 오차 주의.
    denom = distance_squared(a, b)
    if denom == 0:
        raise ValueError('A와 B가 같아 직선이 정의되지 않음')
    return area2(a, b, p) / math.sqrt(denom)


def reflected_point(a, b, p):
    # 직선 AB에 대한 점 P의 대칭점. A!=B.
    h, _ = perpendicular_foot(a, b, p)
    return 2 * h[0] - p[0], 2 * h[1] - p[1]


def intersection_x(a, b, c):
    # 직선 AB와 x=c의 교점. 평행·일치·점 입력은 None.
    dx = b[0] - a[0]
    if dx == 0:
        return None
    t = (c - a[0]) / dx
    return c, a[1] + t * (b[1] - a[1])


def intersection_y(a, b, c):
    # 직선 AB와 y=c의 교점. 평행·일치·점 입력은 None.
    dy = b[1] - a[1]
    if dy == 0:
        return None
    t = (c - a[1]) / dy
    return a[0] + t * (b[0] - a[0]), c
