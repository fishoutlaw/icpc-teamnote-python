"""원본: code/Math/PowMod.cpp. O(log exponent) modular multiplications.
Python pow avoids fixed-width overflow. exponent >= 0, modulus >= 1.
"""


def pow_mod(base, exponent, modulus):
    if exponent < 0 or modulus < 1:
        raise ValueError('exponent >= 0 and modulus >= 1 required')
    return pow(base, exponent, modulus)
