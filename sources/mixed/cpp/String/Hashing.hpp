#pragma once
#include "../common.hpp"
// 구간 [l,r) 해시. 전처리 O(N), 질의 O(1).
// 바이트 문자열. 충돌 가능: 실제 값 확인 또는 두 모듈러스 사용.
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
