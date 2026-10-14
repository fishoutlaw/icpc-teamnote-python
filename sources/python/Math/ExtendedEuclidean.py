"""원본: code/Math/ExtendedEuclidean.cpp. O(log max(|a|,|b|)), O(1) integers.
Returns (g,x,y): ax+by=g=gcd(a,b)>=0, supports negative and zero inputs.
"""


def extended_gcd(a, b):
    old_r, r, old_x, x, old_y, y = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    sign = -1 if old_r < 0 else 1
    return sign * old_r, sign * old_x, sign * old_y
