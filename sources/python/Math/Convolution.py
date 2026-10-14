# FFT·NTT·비트 합성곱 O(N log N). FFT는 큰 계수에서 반올림 오차가 생길 수 있다.
# multiply_mod는 정확한 NTT/CRT, 범위 초과 시 O(len(a)·len(b)) 직접 곱셈.
# 뒤쪽 0을 포함한 len(a)+len(b)-1개 계수를 반환한다.
from cmath import exp, pi


def transform(a, inverse=False, mod=None, root=3):
    n = len(a)
    if not n or n & (n - 1):
        raise ValueError('nonempty power of two required')
    if mod is not None and (mod - 1) % n:
        raise ValueError('transform length must divide mod-1')
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        if mod is None:
            step = exp(((-2 if inverse else 2) * pi * 1j) / length)
        else:
            step = pow(root, (mod - 1) // length, mod)
            if inverse:
                step = pow(step, -1, mod)
        for start in range(0, n, length):
            w = 1
            for j in range(start, start + length // 2):
                u, v = a[j], a[j + length // 2] * w
                a[j], a[j + length // 2] = u + v, u - v
                w *= step
                if mod is not None:
                    a[j] %= mod
                    a[j + length // 2] %= mod
                    w %= mod
        length *= 2
    if inverse:
        scale = 1 / n if mod is None else pow(n, -1, mod)
        for i in range(n):
            a[i] = a[i] * scale if mod is None else a[i] * scale % mod


def multiply(a, b, mod=None, root=3):
    if not a or not b:
        return []
    size = len(a) + len(b) - 1
    n = 1 << (size - 1).bit_length()
    a, b = list(a) + [0] * (n - len(a)), list(b) + [0] * (n - len(b))
    transform(a, mod=mod, root=root)
    transform(b, mod=mod, root=root)
    a = [x * y if mod is None else x * y % mod for x, y in zip(a, b)]
    transform(a, True, mod, root)
    return [round(x.real) for x in a[:size]] if mod is None else a[:size]


def multiply_mod(a, b, mod=998244353, root=3):
    if mod <= 0:
        raise ValueError('positive modulus required')
    if not a or not b:
        return []
    a, b = [x % mod for x in a], [x % mod for x in b]
    size = len(a) + len(b) - 1
    n = 1 << (size - 1).bit_length()
    primes = (167772161, 469762049, 1224736769)
    if mod == 998244353 and n <= 1 << 23:
        return multiply(a, b, mod, root)
    p, q, r = primes
    if n <= 1 << 24 and min(len(a), len(b)) * max(a) * max(b) < p * q * r:
        parts = [multiply(a, b, prime, 3) for prime in primes]
        inv_p, inv_pq = pow(p, -1, q), pow(p * q, -1, r)
        result = []
        for x, y, z in zip(*parts):
            value = x + (y - x) * inv_p % q * p
            value += (z - value) * inv_pq % r * p * q
            result.append(value % mod)
        return result
    result = [0] * size
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] = (result[i + j] + x * y) % mod
    return result


def bitwise_convolution(a, b, kind='xor'):
    # 같은 2의 거듭제곱 길이를 가진 정수 배열의 정확한 비트 합성곱.
    n = len(a)
    if n != len(b) or not n or n & (n - 1) or kind not in ('xor', 'or', 'and'):
        raise ValueError('invalid length or transform kind')

    def fwht(values, inverse=False):
        step = 1
        while step < n:
            for base in range(0, n, step * 2):
                for j in range(base, base + step):
                    u, v = values[j], values[j + step]
                    if kind == 'xor':
                        values[j], values[j + step] = u + v, u - v
                    elif kind == 'or':
                        values[j + step] = v - u if inverse else v + u
                    else:
                        values[j] = u - v if inverse else u + v
            step *= 2
        if inverse and kind == 'xor':
            values[:] = [x // n for x in values]

    a, b = list(a), list(b)
    fwht(a)
    fwht(b)
    result = [x * y for x, y in zip(a, b)]
    fwht(result, True)
    return result
