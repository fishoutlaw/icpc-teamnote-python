"""원본: main.tex inline floor-sum and mathematical reference notes.
floor_sum: sum floor((a*i+b)/m), i=0..n-1; n>=0, m>0. O(log m).
Simpson O(steps), Newton O(iterations), Stirling/Bell O(n*k), O(k) space.
"""
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
    """Local root search; may fail to converge. Verify the residual."""
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
