#pragma once
#include "../common.hpp"
// uint64_t 전체 범위의 소수 판별·소인수분해.
// 밀러 라빈은 확정 판별, 폴라드 로는 기대 O(sqrt(최소 소인수)).
namespace tn {
u64 mul_mod(u64 a,u64 b,u64 m) { return u128(a)*b%m; }
u64 pow_mod64(u64 a,u64 b,u64 m) {
    u64 result=1%m;
    for (a%=m;b;b>>=1,a=mul_mod(a,a,m)) if (b&1) result=mul_mod(result,a,m);
    return result;
}
bool is_prime64(u64 n) {
    if (n<2) return false;
    for (u64 p:{2,3,5,7,11,13,17,19,23,29,31,37}) if (n%p==0) return n==p;
    u64 d=n-1; int s=0; while (!(d&1)) d>>=1,++s;
    for (u64 a:{2ULL,325ULL,9375ULL,28178ULL,450775ULL,9780504ULL,1795265022ULL}) {
        if (a%n==0) continue; u64 x=pow_mod64(a,d,n);
        if (x==1 || x==n-1) continue;
        bool pass=false;
        for (int j=1;j<s;j++) if ((x=mul_mod(x,x,n))==n-1) { pass=true; break; }
        if (!pass) return false;
    }
    return true;
}
u64 pollard_rho(u64 n) { // n>1인 합성수에 사용한다.
    if (!(n&1)) return 2;
    static mt19937_64 rng(20261014);
    while (true) {
        u64 x=2+rng()%(n-2),y=x,c=1+rng()%(n-1),d=1;
        auto f=[&](u64 a)->u64 { return (u128(mul_mod(a,a,n))+c)%n; };
        while (d==1) { x=f(x); y=f(f(y)); d=gcd(x>y?x-y:y-x,n); }
        if (d!=n) return d;
    }
}
vector<pair<u64,int>> factorize64(u64 n) {
    if (!n) throw invalid_argument("positive integer required");
    vector<u64> st{n}; map<u64,int> factors;
    while (!st.empty()) {
        u64 x=st.back(); st.pop_back(); if (x==1) continue;
        if (is_prime64(x)) ++factors[x];
        else { u64 d=pollard_rho(x); st.push_back(d); st.push_back(x/d); }
    }
    return {factors.begin(),factors.end()};
}
}
