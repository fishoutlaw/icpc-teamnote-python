"""원본: code/String/Hashing.cpp. Build O(N), get O(1), space O(N).
0-based [l,r). Hash equality can collide; verify strings or use two moduli.
"""


class Hashing:
    def __init__(self, text, base=917, mod=998244353):
        self.mod = mod
        self.h, self.p = [0], [1]
        for char in text:
            value = ord(char) if isinstance(char, str) else char
            self.h.append((self.h[-1] * base + value) % mod)
            self.p.append(self.p[-1] * base % mod)

    def get(self, l, r):
        if not 0 <= l <= r < len(self.h):
            raise IndexError((l, r))
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.mod
