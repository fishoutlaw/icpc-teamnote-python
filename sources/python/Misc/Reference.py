# 바닥 함수 합·카탈란 수·수치 적분·근 찾기·집합 분할 수.
from math import comb


def floor_sum(n, m, a, b):
    if n < 0 or m <= 0:
        raise ValueError('n >= 0 and m > 0 required')
    answer = 0
    while True:
        q, a = divmod(a, m)
        answer += q * n * (n - 1) // 2
        q, b = divmod(b, m)
        answer += q * n
        top = a * n + b
        if top < m:
            return answer
        n, b = divmod(top, m)
        m, a = a, m


def catalan(n):
    return comb(2 * n, n) // (n + 1)


def simpson(f, a, b, steps=1000):
    if steps <= 0 or steps % 2:
        raise ValueError('positive even steps required')
    h = (b - a) / steps
    return h / 3 * (f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h)
                                      for i in range(1, steps)))


def newton(f, derivative, x, tolerance=1e-12, iterations=100):
    # 뉴턴법으로 근을 찾는다. 수렴 실패 가능: 결과의 잔차를 확인한다.
    for _ in range(iterations):
        value = f(x)
        if abs(value) <= tolerance:
            return x
        slope = derivative(x)
        if slope == 0:
            raise ValueError('zero derivative')
        x -= value / slope
    if abs(f(x)) <= tolerance:
        return x
    raise ValueError('iteration limit reached')


def stirling2_row(n, k):
    row = [1] + [0] * k
    for _ in range(n):
        for j in range(k, 0, -1):
            row[j] = j * row[j] + row[j - 1]
        row[0] = 0
    return row


def bell(n):
    return sum(stirling2_row(n, n))


def derangements(n):
    a, b = 1, 0
    if n == 0:
        return a
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b
