# N까지 소수·최소 소인수·오일러 함수·뫼비우스 함수·약수 개수·합을 구한다. O(N).


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
