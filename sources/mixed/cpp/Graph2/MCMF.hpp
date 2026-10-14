#pragma once
#include "../common.hpp"
// Based on code/Graph2/MCMF.cpp. Bellman-Ford augmentations O(A VE).
// Reachable negative residual cycles rejected. Total cost must fit (-INF,INF).
namespace tn {
struct MinCostFlow {
    struct Edge { int u,v; ll cap,cost; };
    int n; vector<Edge> edges;
    explicit MinCostFlow(int n):n(n) {}
    void add_edge(int u,int v,ll cap,ll cost) {
        assert(cap>=0); edges.push_back({u,v,cap,cost}); edges.push_back({v,u,0,-cost});
    }
    pair<ll,ll> run(int s,int t,ll limit=INF) { // additional (flow,cost)
        assert(s!=t); ll flow=0,cost=0;
        while (flow<limit) {
            vector<ll> d(n,INF); vector<int> p(n,-1); d[s]=0;
            for (int step=0;step<n;step++) {
                bool changed=false;
                for (int i=0;i<int(edges.size());i++) {
                    auto e=edges[i];
                    if (e.cap>0 && d[e.u]!=INF && d[e.v]>d[e.u]+e.cost)
                        d[e.v]=d[e.u]+e.cost,p[e.v]=i,changed=true;
                }
                if (!changed) break;
                if (step==n-1) throw invalid_argument("negative cost cycle");
            }
            if (d[t]==INF) break;
            ll amount=limit-flow;
            for (int v=t;v!=s;v=edges[p[v]].u) amount=min(amount,edges[p[v]].cap);
            for (int v=t;v!=s;v=edges[p[v]].u) {
                edges[p[v]].cap-=amount; edges[p[v]^1].cap+=amount;
            }
            flow+=amount; cost+=amount*d[t];
        }
        return {flow,cost};
    }
};
}
