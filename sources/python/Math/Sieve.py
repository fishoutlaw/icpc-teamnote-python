"""원본: code/Math/Sieve.cpp. O(N log log N) time, O(N) space.
spf[x] = smallest prime factor, spf[1]=1. Factorization O(log x).
"""


def sieve(n):
    spf = list(range(n + 1))
    for p in range(2, int(n ** 0.5) + 1):
        if spf[p] == p:
            for x in range(p * p, n + 1, p):
                if spf[x] == x:
                    spf[x] = p
    return spf


def factorize(n, spf):
    if not 1 <= n < len(spf):
        raise ValueError('n outside sieve')
    result = []
    while n > 1:
        p, count = spf[n], 0
        while n % p == 0:
            n //= p
            count += 1
        result.append((p, count))
    return result
