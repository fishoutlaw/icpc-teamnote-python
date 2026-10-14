"""원본: code/DataStructure/ConvexHullTrick.cpp.
MonotoneCHT: max, increasing slopes and query x, amortized O(1), O(N) space.
LiChao: arbitrary slopes/order, integer x in fixed [lo,hi], O(log range).
For min queries negate slopes/intercepts and the returned value.
"""
from collections import deque


class MonotoneCHT:
    def __init__(self):
        self.lines = deque()
        self.last_slope = self.last_x = None

    def add(self, a, b, index=None):
        if self.last_slope is not None and a < self.last_slope:
            raise ValueError('slopes must be nondecreasing')
        self.last_slope = a
        q = self.lines
        if q and q[-1][0] == a:
            if q[-1][1] >= b:
                return
            q.pop()
        while len(q) >= 2:
            x, y = q[-2], q[-1]
            if (x[1] - y[1]) * (a - y[0]) < (y[1] - b) * (y[0] - x[0]):
                break
            q.pop()
        q.append((a, b, index))

    def query(self, x):
        if self.last_x is not None and x < self.last_x:
            raise ValueError('query x must be nondecreasing')
        self.last_x = x
        q = self.lines
        if not q:
            raise ValueError('empty hull')
        while len(q) >= 2 and q[0][0] * x + q[0][1] <= q[1][0] * x + q[1][1]:
            q.popleft()
        a, b, index = q[0]
        return a * x + b, index


class LiChao:
    def __init__(self, lo, hi):
        if lo > hi:
            raise ValueError('empty domain')
        self.lo, self.hi = lo, hi
        self.lines = {}

    def add(self, a, b):
        line = (a, b)
        v, l, r = 1, self.lo, self.hi
        while True:
            if v not in self.lines:
                self.lines[v] = line
                return
            old = self.lines[v]
            m = (l + r) // 2
            left = line[0] * l + line[1] > old[0] * l + old[1]
            middle = line[0] * m + line[1] > old[0] * m + old[1]
            if middle:
                self.lines[v], line = line, old
            if l == r:
                return
            if left != middle:
                v, r = v * 2, m
            else:
                v, l = v * 2 + 1, m + 1

    def query(self, x):
        if not self.lo <= x <= self.hi:
            raise ValueError('x outside domain')
        if not self.lines:
            raise ValueError('empty hull')
        answer = -float('inf')
        v, l, r = 1, self.lo, self.hi
        while v in self.lines:
            a, b = self.lines[v]
            answer = max(answer, a * x + b)
            if l == r:
                break
            m = (l + r) // 2
            if x <= m:
                v, r = v * 2, m
            else:
                v, l = v * 2 + 1, m + 1
        return answer
