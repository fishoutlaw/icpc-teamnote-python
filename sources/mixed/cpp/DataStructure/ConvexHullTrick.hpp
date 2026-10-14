#pragma once
#include "../common.hpp"
// Based on code/DataStructure/ConvexHullTrick.cpp. Max queries.
// Slopes/intercepts/x within +/-1e9; use negated lines for minima.
namespace tn {
struct Line {
    ll a,b; int id=-1;
    ll at(ll x) const { return a*x+b; }
};
struct MonotoneCHT {
    deque<Line> q; optional<ll> last_a,last_x;
    void add(ll a,ll b,int id=-1) { // nondecreasing slopes, amortized O(1)
        assert(!last_a || a>=*last_a); last_a=a;
        if (!q.empty() && q.back().a==a) {
            if (q.back().b>=b) return; q.pop_back();
        }
        while (q.size()>1) {
            auto x=q[q.size()-2],y=q.back();
            if ((i128(x.b)-y.b)*(a-y.a)<(i128(y.b)-b)*(y.a-x.a)) break;
            q.pop_back();
        }
        q.push_back({a,b,id});
    }
    pair<ll,int> query(ll x) { // nondecreasing x, amortized O(1)
        assert(!q.empty() && (!last_x || x>=*last_x)); last_x=x;
        while (q.size()>1 && q[0].at(x)<=q[1].at(x)) q.pop_front();
        return {q.front().at(x),q.front().id};
    }
};
struct LiChao { // arbitrary order, fixed integer [lo,hi], O(log range)
    struct Node { Line line; int l=-1,r=-1; };
    ll lo,hi; vector<Node> t;
    LiChao(ll lo,ll hi):lo(lo),hi(hi) { assert(lo<=hi); }
    void add(ll a,ll b) {
        Line line{a,b}; if (t.empty()) { t.push_back({line}); return; }
        int v=0; ll l=lo,r=hi;
        while (true) {
            ll m=l+(r-l)/2;
            bool left=line.at(l)>t[v].line.at(l),mid=line.at(m)>t[v].line.at(m);
            if (mid) swap(line,t[v].line);
            if (l==r) return;
            bool go_left=left!=mid; int child=go_left?t[v].l:t[v].r;
            if (child==-1) {
                child=t.size(); if (go_left) t[v].l=child; else t[v].r=child;
                t.push_back({line}); return;
            }
            v=child; if (go_left) r=m; else l=m+1;
        }
    }
    ll query(ll x) const {
        assert(!t.empty() && lo<=x && x<=hi);
        ll result=-INF,l=lo,r=hi; int v=0;
        while (v!=-1) {
            result=max(result,t[v].line.at(x)); if (l==r) break;
            ll m=l+(r-l)/2;
            if (x<=m) v=t[v].l,r=m; else v=t[v].r,l=m+1;
        }
        return result;
    }
};
}
