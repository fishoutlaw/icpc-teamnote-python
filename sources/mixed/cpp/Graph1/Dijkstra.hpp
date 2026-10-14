#pragma once
#include "../common.hpp"
// Based on code/Graph1/Dijkstra.cpp. O(V+E log(E+1)), space O(V+E).
namespace tn {
pair<vector<ll>,vector<int>> dijkstra(
    const vector<vector<pair<int,ll>>>& g, int s) {
    for (auto& row:g) for (auto [v,w]:row)
        if (w<0) throw invalid_argument("negative weight");
    vector<ll> d(g.size(),INF); vector<int> p(g.size(),-1);
    priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<pair<ll,int>>> q;
    d[s]=0; q.push({0,s});
    while (!q.empty()) {
        auto [cost,v]=q.top(); q.pop(); if (cost!=d[v]) continue;
        for (auto [u,w]:g[v]) if (cost+w<d[u]) {
            d[u]=cost+w; p[u]=v; q.push({d[u],u});
        }
    }
    return {d,p}; // INF = unreachable; parent=-1
}
vector<int> restore_path(const vector<int>& p,int s,int t) {
    vector<int> path;
    for (;t!=-1;t=p[t]) {
        path.push_back(t);
        if (t==s) { reverse(path.begin(),path.end()); return path; }
    }
    return {};
}
}
