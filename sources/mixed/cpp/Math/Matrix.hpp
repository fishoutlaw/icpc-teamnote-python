#pragma once
#include "../common.hpp"
// Based on code/Math/Matrix.cpp. RREF/rank/determinant/inverse, O(R^2 C).
// RealOps is approximate (absolute EPS); Python default uses exact Fraction.
// ModOps + prime modulus gives exact finite-field results in both languages.
namespace tn {
struct RealOps {
    using T=long double; T eps=1e-12L;
    T norm(T x) const { return x; }
    bool zero(T x) const { return abs(x)<=eps; }
    T sub(T a,T b) const { return a-b; }
    T mul(T a,T b) const { return a*b; }
    T inv(T x) const { return 1/x; }
    bool better(T a,T b) const { return abs(a)>abs(b); }
};
struct ModOps { // prime 2 <= mod <= 2^31-1
    using T=ll; ll mod;
    T norm(T x) const { x%=mod; return x<0?x+mod:x; }
    bool zero(T x) const { return x==0; }
    T sub(T a,T b) const { return norm(a-b); }
    T mul(T a,T b) const { return i128(a)*b%mod; }
    T inv(T x) const {
        T result=1; for (ll e=mod-2;e;e>>=1,x=mul(x,x)) if (e&1) result=mul(result,x);
        return result;
    }
    bool better(T a,T b) const { return b==0 && a!=0; }
};
template<class T> struct GaussResult {
    vector<vector<T>> rref; int rank; optional<T> determinant;
    optional<vector<vector<T>>> inverse;
};
template<class Ops> GaussResult<typename Ops::T> gauss(
    vector<vector<typename Ops::T>> a,Ops op) {
    using T=typename Ops::T; int n=a.size(),m=n?a[0].size():0,rank=0;
    vector<vector<T>> inv(n,vector<T>(n)); T det=1;
    for (int i=0;i<n;i++) {
        assert(int(a[i].size())==m); inv[i][i]=1;
        for (T& x:a[i]) x=op.norm(x);
    }
    for (int col=0;col<m && rank<n;col++) {
        int p=rank;
        for (int i=rank+1;i<n;i++) if (op.better(a[i][col],a[p][col])) p=i;
        if (op.zero(a[p][col])) continue;
        if (p!=rank) { swap(a[p],a[rank]); swap(inv[p],inv[rank]); det=op.sub(0,det); }
        T pivot=a[rank][col],scale=op.inv(pivot); det=op.mul(det,pivot);
        for (T& x:a[rank]) x=op.mul(x,scale);
        for (T& x:inv[rank]) x=op.mul(x,scale);
        for (int i=0;i<n;i++) if (i!=rank) {
            T factor=a[i][col];
            for (int j=0;j<m;j++) a[i][j]=op.sub(a[i][j],op.mul(factor,a[rank][j]));
            for (int j=0;j<n;j++) inv[i][j]=op.sub(inv[i][j],op.mul(factor,inv[rank][j]));
        }
        ++rank;
    }
    GaussResult<T> out{a,rank,nullopt,nullopt};
    if (n==m) { out.determinant=rank==n?det:T(0); if (rank==n) out.inverse=inv; }
    return out;
}
}
