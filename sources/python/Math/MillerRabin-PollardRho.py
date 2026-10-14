# 0 이상 2^64 미만의 소수 판별·소인수분해.
# 밀러 라빈은 확정 판별, 폴라드 로는 최소 소인수 p에 대해 기대 O(sqrt(p)).
from collections import Counter
from math import gcd
from random import randrange


def is_prime(n):
    if n >= 1 << 64:
        raise ValueError('deterministic range is below 2^64')
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x = y = randrange(2, n)
        c, d = randrange(1, n), 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


def factorize(n):
    if not 1 <= n < 1 << 64:
        raise ValueError('1 <= n < 2^64 required')
    factors, stack = [], [n]
    while stack:
        x = stack.pop()
        if x == 1:
            continue
        if is_prime(x):
            factors.append(x)
        else:
            d = _rho(x)
            stack.extend((d, x // d))
    return sorted(Counter(factors).items())
