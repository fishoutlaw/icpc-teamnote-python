"""원본: code/DataStructure/SegmentTree.cpp.
0-based, [l,r). Build O(N), set/sum O(log N), space O(N).
"""


class SegmentTree:
    def __init__(self, values):
        self.n = len(values)
        self.size = 1 << max(0, (self.n - 1).bit_length())
        self.tree = [0] * (2 * self.size)
        self.tree[self.size:self.size + self.n] = values
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def set(self, i, value):
        if not 0 <= i < self.n:
            raise IndexError(i)
        i += self.size
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def sum(self, l, r):
        if not 0 <= l <= r <= self.n:
            raise IndexError((l, r))
        answer = 0
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                answer += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                answer += self.tree[r]
            l //= 2
            r //= 2
        return answer
