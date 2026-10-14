#pragma once
#include "../common.hpp"
// 음이 아닌 가중치의 최단 거리. 최소 힙으로 다음 정점을 고른다.
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
    return {d,p}; // 도달 불가는 거리 INF, 부모 -1.
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
