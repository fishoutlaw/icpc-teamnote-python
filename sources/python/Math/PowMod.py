# 모듈러 거듭제곱 O(log 지수). 지수는 0 이상, 모듈러스는 1 이상.


def pow_mod(base, exponent, modulus):
    if exponent < 0 or modulus < 1:
        raise ValueError('exponent >= 0 and modulus >= 1 required')
    return pow(base, exponent, modulus)
