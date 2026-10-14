#pragma once
#include "../common.hpp"
// Based on code/String/Hashing.cpp. O(N) build/space; O(1) substring [l,r).
// Byte strings. Collisions possible: verify matches or use two moduli.
namespace tn {
struct Hashing {
    ll mod; vector<ll> h{0},p{1};
    Hashing(const string& s,ll base=917,ll mod=998244353):mod(mod) {
        for (unsigned char c:s) h.push_back((h.back()*base+c)%mod),p.push_back(p.back()*base%mod);
    }
    ll get(int l,int r) const {
        assert(0<=l && l<=r && r<int(h.size()));
        return (h[r]-h[l]*p[r-l]%mod+mod)%mod;
    }
};
}
