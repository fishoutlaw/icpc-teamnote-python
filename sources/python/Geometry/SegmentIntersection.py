# 선분 교차 O(1). (0,None): 없음, (1,점): 한 점, (-1,None): 구간 겹침.
# 교점은 Fraction으로 정확히 계산하며 길이 0인 선분도 처리한다.
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
