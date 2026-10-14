#pragma once
#include "../common.hpp"
// Based on code/Graph2/Dinic.cpp. Iterative Dinic O(V^2 E), space O(V+E).
namespace tn {
struct Dinic {
    vector<vector<int>> g; vector<int> to; vector<ll> cap;
    explicit Dinic(int n):g(n) {}
    int add_edge(int u,int v,ll c,ll reverse=0) {
        assert(c>=0 && reverse>=0); int e=to.size();
        g[u].push_back(e); g[v].push_back(e^1);
        to.push_back(v); to.push_back(u); cap.push_back(c); cap.push_back(reverse);
        return e;
    }
    vector<int> levels(int s) const {
        vector<int> d(g.size(),-1); queue<int> q; d[s]=0; q.push(s);
        while (!q.empty()) {
            int v=q.front(); q.pop();
            for (int e:g[v]) if (cap[e]>0 && d[to[e]]==-1)
                d[to[e]]=d[v]+1,q.push(to[e]);
        }
        return d;
    }
    ll max_flow(int s,int t,ll limit=INF) { // additional flow, consumes residual
        assert(s!=t); ll flow=0;
        while (flow<limit) {
            auto level=levels(s); if (level[t]==-1) break;
            vector<int> pos(g.size());
            while (flow<limit) {
                vector<int> vertices{s},path;
                while (!vertices.empty() && vertices.back()!=t) {
                    int v=vertices.back();
                    while (pos[v]<int(g[v].size())) {
                        int e=g[v][pos[v]];
                        if (cap[e]>0 && level[to[e]]==level[v]+1) break;
                        ++pos[v];
                    }
                    if (pos[v]==int(g[v].size())) {
                        level[v]=-1; vertices.pop_back();
                        if (!path.empty()) path.pop_back();
                    } else { int e=g[v][pos[v]]; path.push_back(e); vertices.push_back(to[e]); }
                }
                if (vertices.empty()) break;
                ll amount=limit-flow; for (int e:path) amount=min(amount,cap[e]);
                for (int e:path) cap[e]-=amount,cap[e^1]+=amount;
                flow+=amount;
            }
        }
        return flow;
    }
    pair<vector<int>,vector<int>> min_cut(int s) const { // after full max_flow
        auto d=levels(s); vector<int> a,b;
        for (int v=0;v<int(g.size());v++) (d[v]==-1?b:a).push_back(v);
        return {a,b};
    }
};
}
