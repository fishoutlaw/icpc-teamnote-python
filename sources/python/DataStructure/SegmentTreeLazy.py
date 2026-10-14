"""원본: code/DataStructure/SegmentTreeLazy.cpp.
0-based [l,r): range add / sum. O(log N) per query; O(N) space.
Recursion depth O(log N), not O(N).
"""


class LazySegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * max(n, 1))
        self.lazy = [0] * len(self.tree)

    def _apply(self, v, l, r, value):
        self.tree[v] += (r - l) * value
        self.lazy[v] += value

    def _push(self, v, l, r):
        m = (l + r) // 2
        self._apply(v * 2, l, m, self.lazy[v])
        self._apply(v * 2 + 1, m, r, self.lazy[v])
        self.lazy[v] = 0

    def _query(self, v, l, r, a, b, value):
        if b <= l or r <= a:
            return 0
        if a <= l and r <= b:
            if value is not None:
                self._apply(v, l, r, value)
            return self.tree[v]
        self._push(v, l, r)
        m = (l + r) // 2
        answer = self._query(v * 2, l, m, a, b, value)
        answer += self._query(v * 2 + 1, m, r, a, b, value)
        self.tree[v] = self.tree[v * 2] + self.tree[v * 2 + 1]
        return answer

    def add(self, l, r, value):
        if not 0 <= l <= r <= self.n:
            raise IndexError((l, r))
        if l < r:
            self._query(1, 0, self.n, l, r, value)

    def sum(self, l, r):
        if not 0 <= l <= r <= self.n:
            raise IndexError((l, r))
        return self._query(1, 0, self.n, l, r, None) if l < r else 0
