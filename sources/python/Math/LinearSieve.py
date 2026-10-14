"""원본: code/Math/LinearSieve.cpp. O(N) arithmetic operations / space.
Returns primes, spf, phi, mu, tau (divisor count), sigma (divisor sum).
All tables include index N. Python integer bit costs are additional.
"""


def linear_sieve(n):
    spf, phi, mu, tau, sigma = ([0] * (n + 1) for _ in range(5))
    exponent, power = [0] * (n + 1), [0] * (n + 1)
    primes = []
    if n:
        spf[1] = phi[1] = mu[1] = tau[1] = sigma[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            primes.append(i)
            spf[i], exponent[i], power[i] = i, 1, i
            phi[i], mu[i], tau[i], sigma[i] = i - 1, -1, 2, i + 1
        for p in primes:
            x = i * p
            if x > n:
                break
            spf[x] = p
            if i % p == 0:
                exponent[x] = exponent[i] + 1
                power[x] = power[i] * p
                phi[x] = phi[i] * p
                mu[x] = 0
                tau[x] = tau[i] // (exponent[i] + 1) * (exponent[x] + 1)
                sigma[x] = sigma[i] + power[x] * sigma[i // power[i]]
                break
            exponent[x], power[x] = 1, p
            phi[x], mu[x] = phi[i] * (p - 1), -mu[i]
            tau[x], sigma[x] = tau[i] * 2, sigma[i] * (p + 1)
    return primes, spf, phi, mu, tau, sigma
