# 빈도 트리의 이전 버전을 보존한다. 삽입·k번째 값 O(log N).
# k는 1부터 시작하며 두 버전의 빈도 차는 음수가 아니어야 한다.


class PersistentSegmentTree:
    def __init__(self, n):
        if n <= 0:
            raise ValueError('n must be positive')
        self.n = n
        self.left, self.right, self.count = [0], [0], [0]
        self.roots = [0]

    def insert(self, version, x):
        if not 0 <= x < self.n:
            raise IndexError(x)

        def update(old, l, r):
            v = len(self.count)
            self.left.append(self.left[old])
            self.right.append(self.right[old])
            self.count.append(self.count[old] + 1)
            if r - l > 1:
                m = (l + r) // 2
                if x < m:
                    self.left[v] = update(self.left[old], l, m)
                else:
                    self.right[v] = update(self.right[old], m, r)
            return v

        self.roots.append(update(self.roots[version], 0, self.n))
        return len(self.roots) - 1

    def kth(self, before, after, k):
        a, b = self.roots[before], self.roots[after]
        if not 1 <= k <= self.count[b] - self.count[a]:
            raise ValueError('k outside version difference')
        l, r = 0, self.n
        while r - l > 1:
            m = (l + r) // 2
            count = self.count[self.left[b]] - self.count[self.left[a]]
            if k <= count:
                a, b, r = self.left[a], self.left[b], m
            else:
                k -= count
                a, b, l = self.right[a], self.right[b], m
        return l
