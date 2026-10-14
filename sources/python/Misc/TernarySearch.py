# 단봉 함수의 최솟값. 닫힌 구간 [lo,hi], 정수는 가장 작은 최소 위치 반환.
# 최소 구간 밖에서 엄격히 감소·증가해야 한다. 정수 O(log 범위).


def ternary_integer(lo, hi, f):
    if lo > hi:
        raise ValueError('empty interval')
    while hi - lo > 3:
        a = lo + (hi - lo) // 3
        b = hi - (hi - lo) // 3
        if f(a) > f(b):
            lo = a + 1
        else:
            hi = b - 1
    return min(range(lo, hi + 1), key=f)


def ternary_real(lo, hi, f, iterations=100):
    for _ in range(iterations):
        a, b = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if f(a) > f(b):
            lo = a
        else:
            hi = b
    return (lo + hi) / 2
