#pragma once
#include "../common.hpp"
// 점 대입과 구간 [l,r) 합 O(log N). 초기화 O(N).
namespace tn {
struct SegmentTree {
    int n,size=1; vector<ll> tree;
    explicit SegmentTree(const vector<ll>& a):n(a.size()) {
        while (size<n) size*=2;
        tree.assign(2*size,0); copy(a.begin(),a.end(),tree.begin()+size);
        for (int i=size-1;i;i--) tree[i]=tree[i*2]+tree[i*2+1];
    }
    void set(int i,ll value) {
        assert(0<=i && i<n); tree[i+=size]=value;
        while (i/=2) tree[i]=tree[i*2]+tree[i*2+1];
    }
    ll sum(int l,int r) const {
        assert(0<=l && l<=r && r<=n); ll result=0;
        for (l+=size,r+=size;l<r;l/=2,r/=2) {
            if (l&1) result+=tree[l++];
            if (r&1) result+=tree[--r];
        }
        return result;
    }
};
}
