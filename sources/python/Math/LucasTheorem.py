# 소수 p에 대한 이항 계수. 전처리 O(p), 질의 O(log_p(n+1)).


class Lucas:
    def __init__(self, p):
        if p < 2:
            raise ValueError('prime p >= 2 required')
        self.p = p
        self.fac = [1] * p
        self.inv = [1] * p
        for i in range(1, p):
            self.fac[i] = self.fac[i - 1] * i % p
        self.inv[-1] = pow(self.fac[-1], p - 2, p)
        for i in range(p - 2, -1, -1):
            self.inv[i] = self.inv[i + 1] * (i + 1) % p

    def calc(self, n, r):
        if r < 0 or n < r:
            return 0
        result, p = 1, self.p
        while n or r:
            a, b = n % p, r % p
            if b > a:
                return 0
            result = result * self.fac[a] * self.inv[b] * self.inv[a - b] % p
            n //= p
            r //= p
        return result
