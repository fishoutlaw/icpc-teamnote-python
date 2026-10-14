#pragma once
#include "../common.hpp"
// Based on code/Graph1/Bellman.cpp. O(VE), auxiliary O(V).
namespace tn {
optional<vector<ll>> bellman_ford(int n,const vector<tuple<int,int,ll>>& e,int s) {
    vector<ll> d(n,INF); d[s]=0;
    for (int step=0;step<n;step++) {
        bool changed=false;
        for (auto [u,v,w]:e) if (d[u]!=INF && d[v]>d[u]+w)
            d[v]=d[u]+w, changed=true;
        if (!changed) return d;
    }
    return nullopt; // reachable negative cycle (Python: None)
}
}
