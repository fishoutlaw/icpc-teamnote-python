# 양의 모듈러스인 합동식을 병합한다. (나머지, 최소공배수), 불가능하면 None.
# 빈 입력은 (0,1). O(K log M).
from math import gcd


def crt(congruences):
    a, m = 0, 1
    for b, n in congruences:
        if n <= 0:
            raise ValueError('positive modulus required')
        g = gcd(m, n)
        if (b - a) % g:
            return None
        reduced = n // g
        t = ((b - a) // g * pow(m // g, -1, reduced)) % reduced
        a += m * t
        m *= reduced
        a %= m
    return a, m
