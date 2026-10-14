#pragma once
#include "../common.hpp"
// 가중치순으로 간선을 선택하는 최소 신장 포리스트. O(V+E log E).
namespace tn {
struct DSU {
    vector<int> parent,size; int components;
    explicit DSU(int n):parent(n),size(n,1),components(n) {
        iota(parent.begin(),parent.end(),0);
    }
    int find(int v) {
        while (parent[v]!=v) v=parent[v]=parent[parent[v]];
        return v;
    }
    bool unite(int u,int v) {
        u=find(u); v=find(v); if (u==v) return false;
        if (size[u]<size[v]) swap(u,v);
        parent[v]=u; size[u]+=size[v]; --components; return true;
    }
};
pair<ll,vector<tuple<ll,int,int>>> kruskal(int n,vector<tuple<ll,int,int>> edges) {
    sort(edges.begin(),edges.end()); DSU d(n); ll cost=0;
    vector<tuple<ll,int,int>> chosen;
    for (auto [w,u,v]:edges) if (d.unite(u,v)) cost+=w,chosen.push_back({w,u,v});
    return {cost,chosen}; // 비연결이면 포리스트. 간선은 (가중치,u,v).
}
}
