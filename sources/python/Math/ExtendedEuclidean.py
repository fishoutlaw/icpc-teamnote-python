# ax+by=gcd(a,b)를 만족하는 (g,x,y)를 구한다. 음수·0도 처리한다.


def extended_gcd(a, b):
    old_r, r, old_x, x, old_y, y = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    sign = -1 if old_r < 0 else 1
    return sign * old_r, sign * old_x, sign * old_y
