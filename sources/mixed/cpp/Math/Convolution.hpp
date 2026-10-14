#pragma once
#include "../common.hpp"
// Based on code/Math/Convolution.cpp. O(N log N), space O(N).
// NTT/CRT exact; FFT approximate. All len(a)+len(b)-1 coefficients retained.
namespace tn {
ll mod_power(ll a,ll b,ll mod) {
    ll out=1; for (;b;b>>=1,a=i128(a)*a%mod) if (b&1) out=i128(out)*a%mod;
    return out;
}
void ntt(vector<ll>& a,bool inverse,ll mod=998244353,ll root=3) {
    int n=a.size(); assert(n && !(n&(n-1)) && (mod-1)%n==0);
    for (int i=1,j=0;i<n;i++) {
        int bit=n/2; for (;j&bit;bit>>=1) j^=bit; j^=bit;
        if (i<j) swap(a[i],a[j]);
    }
    for (int len=2;len<=n;len*=2) {
        ll step=mod_power(root,(mod-1)/len,mod);
        if (inverse) step=mod_power(step,mod-2,mod);
        for (int start=0;start<n;start+=len) {
            ll w=1;
            for (int j=start;j<start+len/2;j++) {
                ll u=a[j],v=i128(a[j+len/2])*w%mod;
                a[j]=(u+v)%mod; a[j+len/2]=(u-v+mod)%mod; w=i128(w)*step%mod;
            }
        }
    }
    if (inverse) { ll scale=mod_power(n,mod-2,mod); for (ll& x:a) x=i128(x)*scale%mod; }
}
vector<ll> ntt_multiply(vector<ll> a,vector<ll> b,ll mod=998244353,ll root=3) {
    if (a.empty() || b.empty()) return {};
    int size=a.size()+b.size()-1,n=1; while (n<size) n*=2;
    for (ll& x:a) x=(x%mod+mod)%mod;
    for (ll& x:b) x=(x%mod+mod)%mod;
    a.resize(n); b.resize(n); ntt(a,false,mod,root); ntt(b,false,mod,root);
    for (int i=0;i<n;i++) a[i]=i128(a[i])*b[i]%mod;
    ntt(a,true,mod,root); a.resize(size); return a;
}
vector<ll> multiply_mod(vector<ll> a,vector<ll> b,ll mod=998244353) {
    // Any 1<=mod<=2^31-1; N<=2^24. CRT bound checked explicitly.
    assert(1<=mod && mod<=INT_MAX); if (a.empty() || b.empty()) return {};
    int size=a.size()+b.size()-1,n=1; while (n<size) n*=2;
    if (n>(1<<24)) throw length_error("NTT length exceeds 2^24");
    if (mod==998244353 && n<=(1<<23)) return ntt_multiply(a,b);
    for (ll& x:a) x=(x%mod+mod)%mod;
    for (ll& x:b) x=(x%mod+mod)%mod;
    ll p=167772161,q=469762049,r=1224736769;
    i128 bound=i128(min(a.size(),b.size()))*(*max_element(a.begin(),a.end()))
        *(*max_element(b.begin(),b.end()));
    if (bound>=i128(p)*q*r) throw overflow_error("CRT bound exceeded");
    auto x=ntt_multiply(a,b,p),y=ntt_multiply(a,b,q),z=ntt_multiply(a,b,r);
    ll ip=mod_power(p,q-2,q),ipq=mod_power(ll(i128(p)*q%r),r-2,r);
    for (int i=0;i<size;i++) {
        i128 value=x[i]+i128((y[i]-x[i]+q)%q)*ip%q*p;
        ll t=ll((z[i]-value%r+r)%r); value+=i128(t)*ipq%r*p*q;
        x[i]=value%mod;
    }
    return x;
}
void fft(vector<complex<long double>>& a,bool inverse=false) {
    int n=a.size(); assert(n && !(n&(n-1)));
    for (int i=1,j=0;i<n;i++) {
        int bit=n/2; for (;j&bit;bit>>=1) j^=bit; j^=bit;
        if (i<j) swap(a[i],a[j]);
    }
    for (int len=2;len<=n;len*=2) {
        auto step=polar(1.0L,(inverse?-2:2)*acosl(-1)/len);
        for (int s=0;s<n;s+=len) {
            complex<long double> w=1;
            for (int j=s;j<s+len/2;j++) {
                auto u=a[j],v=a[j+len/2]*w;
                a[j]=u+v; a[j+len/2]=u-v; w*=step;
            }
        }
    }
    if (inverse) for (auto& x:a) x/=n;
}
vector<ll> multiply_fft(const vector<ll>& a,const vector<ll>& b) {
    if (a.empty() || b.empty()) return {};
    int size=a.size()+b.size()-1,n=1; while (n<size) n*=2;
    vector<complex<long double>> x(a.begin(),a.end()),y(b.begin(),b.end());
    x.resize(n); y.resize(n); fft(x); fft(y);
    for (int i=0;i<n;i++) x[i]*=y[i]; fft(x,true);
    vector<ll> result(size); for (int i=0;i<size;i++) result[i]=llroundl(x[i].real());
    return result; // rounding may fail for large coefficients; results must fit ll
}
vector<ll> bitwise_convolution(vector<ll> a,vector<ll> b,char kind) {
    int n=a.size(); assert(n && !(n&(n-1)) && int(b.size())==n);
    assert(kind=='^' || kind=='|' || kind=='&');
    auto transform=[&](vector<ll>& v,bool inverse) {
        for (int step=1;step<n;step*=2) for (int s=0;s<n;s+=2*step)
            for (int j=s;j<s+step;j++) {
                ll x=v[j],y=v[j+step];
                if (kind=='^') v[j]=x+y,v[j+step]=x-y;
                else if (kind=='|') v[j+step]=inverse?y-x:y+x;
                else v[j]=inverse?x-y:x+y;
            }
        if (inverse && kind=='^') for (ll& x:v) x/=n;
    };
    transform(a,false); transform(b,false);
    for (int i=0;i<n;i++) a[i]*=b[i]; transform(a,true); return a;
}
}
