# 제곱근까지 나누어 소인수분해한다. O(sqrt(N)).
from math import isqrt


def is_prime(n):
    return n >= 2 and all(n % p for p in range(2, isqrt(n) + 1))


def factorize(n):
    if n < 1:
        raise ValueError('positive integer required')
    result, p = [], 2
    while p * p <= n:
        count = 0
        while n % p == 0:
            n //= p
            count += 1
        if count:
            result.append((p, count))
        p += 1
    if n > 1:
        result.append((n, 1))
    return result
