#pragma once
#include "../common.hpp"
// Based on code/DataStructure/SegmentTreeLazy.cpp. Range add/sum O(log N).
namespace tn {
struct LazySegmentTree {
    int n; vector<ll> tree,lazy;
    explicit LazySegmentTree(int n):n(n),tree(4*max(1,n)),lazy(tree.size()) {}
    void apply(int v,int l,int r,ll x) { tree[v]+=(r-l)*x; lazy[v]+=x; }
    void push(int v,int l,int r) {
        int m=(l+r)/2;
        apply(v*2,l,m,lazy[v]); apply(v*2+1,m,r,lazy[v]); lazy[v]=0;
    }
    ll query(int v,int l,int r,int a,int b,optional<ll> x) {
        if (b<=l || r<=a) return 0;
        if (a<=l && r<=b) { if (x) apply(v,l,r,*x); return tree[v]; }
        push(v,l,r); int m=(l+r)/2;
        ll answer=query(v*2,l,m,a,b,x)+query(v*2+1,m,r,a,b,x);
        tree[v]=tree[v*2]+tree[v*2+1]; return answer;
    }
    void add(int l,int r,ll x) {
        assert(0<=l && l<=r && r<=n); if (l<r) query(1,0,n,l,r,x);
    }
    ll sum(int l,int r) {
        assert(0<=l && l<=r && r<=n); return l<r?query(1,0,n,l,r,nullopt):0;
    }
};
}
