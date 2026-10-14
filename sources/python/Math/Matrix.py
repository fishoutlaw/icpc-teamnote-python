# 가우스 조던 소거로 (기약 행렬, 계수, 행렬식, 역행렬)을 구한다. O(행^2·열).
# 기본은 정확한 Fraction 연산, mod에는 소수를 지정한다. 입력은 보존한다.
# 정의되지 않는 행렬식·역행렬은 None. 정확한 소수 입력은 Fraction으로 전달한다.
from fractions import Fraction


def gauss(matrix, mod=None):
    n = len(matrix)
    m = len(matrix[0]) if n else 0
    if any(len(row) != m for row in matrix):
        raise ValueError('ragged matrix')
    convert = Fraction if mod is None else lambda x: x % mod
    a = [[convert(x) for x in row] for row in matrix]
    inv = [[convert(i == j) for j in range(n)] for i in range(n)]
    norm = (lambda x: x) if mod is None else lambda x: x % mod
    rank, det = 0, convert(1)
    for col in range(m):
        pivot = next((i for i in range(rank, n) if a[i][col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[pivot], a[rank] = a[rank], a[pivot]
            inv[pivot], inv[rank] = inv[rank], inv[pivot]
            det = -det
        value = a[rank][col]
        det = norm(det * value)
        scale = 1 / value if mod is None else pow(value, -1, mod)
        a[rank] = [norm(x * scale) for x in a[rank]]
        inv[rank] = [norm(x * scale) for x in inv[rank]]
        for i in range(n):
            if i == rank:
                continue
            scale = a[i][col]
            a[i] = [norm(x - scale * y) for x, y in zip(a[i], a[rank])]
            inv[i] = [norm(x - scale * y) for x, y in zip(inv[i], inv[rank])]
        rank += 1
        if rank == n:
            break
    determinant = norm(det) if rank == n else 0
    return a, rank, determinant if n == m else None, inv if n == m == rank else None
