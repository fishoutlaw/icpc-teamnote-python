#pragma once
#include "../common.hpp"
// Based on code/Math/LinearSieve.cpp (ahgus89). O(N) time/space.
namespace tn {
struct LinearSieve {
    vector<int> primes,spf,phi,mu,tau; vector<ll> sigma;
    explicit LinearSieve(int n):spf(n+1),phi(n+1),mu(n+1),tau(n+1),sigma(n+1) {
        vector<int> exponent(n+1),power(n+1);
        if (n) spf[1]=phi[1]=mu[1]=tau[1]=sigma[1]=1;
        for (int i=2;i<=n;i++) {
            if (!spf[i]) {
                primes.push_back(i); spf[i]=power[i]=i; exponent[i]=1;
                phi[i]=i-1; mu[i]=-1; tau[i]=2; sigma[i]=i+1;
            }
            for (int p:primes) {
                if (ll(i)*p>n) break; int x=i*p; spf[x]=p;
                if (i%p==0) {
                    exponent[x]=exponent[i]+1; power[x]=power[i]*p;
                    phi[x]=phi[i]*p; mu[x]=0;
                    tau[x]=tau[i]/(exponent[i]+1)*(exponent[x]+1);
                    sigma[x]=sigma[i]+ll(power[x])*sigma[i/power[i]]; break;
                }
                exponent[x]=1; power[x]=p; phi[x]=phi[i]*(p-1); mu[x]=-mu[i];
                tau[x]=tau[i]*2; sigma[x]=sigma[i]*(p+1);
            }
        }
    }
};
}
