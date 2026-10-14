#pragma once
#include "../common.hpp"
// 간선을 반복 완화하는 최단 거리 O(VE). 음수 사이클이면 nullopt.
namespace tn {
optional<vector<ll>> bellman_ford(int n,const vector<tuple<int,int,ll>>& e,int s) {
    vector<ll> d(n,INF); d[s]=0;
    for (int step=0;step<n;step++) {
        bool changed=false;
        for (auto [u,v,w]:e) if (d[u]!=INF && d[v]>d[u]+w)
            d[v]=d[u]+w, changed=true;
        if (!changed) return d;
    }
    return nullopt; // 도달 가능한 음수 사이클.
}
}
