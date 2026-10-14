#pragma once
#include "../common.hpp"
// Based on code/Math/ChineseRemainderTheorem.cpp. General CRT, O(K log M).
// Positive moduli; final LCM must fit signed 64-bit. nullopt = inconsistent.
namespace tn {
tuple<i128,i128,i128> extended_gcd128(i128 a,i128 b) {
    i128 x=1,y=0,u=0,v=1;
    while (b) { i128 q=a/b; tie(a,b)=make_tuple(b,a-q*b);
        tie(x,u)=make_tuple(u,x-q*u); tie(y,v)=make_tuple(v,y-q*v); }
    return {a,x,y};
}
optional<pair<ll,ll>> crt(const vector<pair<ll,ll>>& equations) {
    i128 a=0,m=1;
    for (auto [bb,nn]:equations) {
        if (nn<=0) throw invalid_argument("positive modulus required");
        i128 b=bb,n=nn; auto [g,x,y]=extended_gcd128(m,n);
        if ((b-a)%g) return nullopt;
        i128 reduced=n/g,t=((b-a)/g*x)%reduced;
        if (t<0) t+=reduced;
        a+=m*t; m*=reduced;
        if (m>LLONG_MAX) throw overflow_error("CRT modulus overflow");
        a%=m; if (a<0) a+=m;
    }
    return pair<ll,ll>{ll(a),ll(m)};
}
}
