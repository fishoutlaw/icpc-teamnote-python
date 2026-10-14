# 음수도 처리하는 정수 나눗셈·최대공약수·최소공배수. 나누는 수는 0이 아니어야 한다.
from math import gcd, lcm


def floor_div(a, b):
    return a // b


def ceil_div(a, b):
    return -(-a // b)
