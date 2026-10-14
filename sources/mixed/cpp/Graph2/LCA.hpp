#pragma once
#include "../common.hpp"
// 연결된 무향 트리의 최소 공통 조상. 전처리 O(N log N), 질의 O(log N).
namespace tn {
struct LCA {
    vector<int> depth; vector<vector<int>> up;
    LCA(const vector<vector<int>>& g,int root=0):depth(g.size(),-1) {
        int n=g.size(),levels=1; while ((1LL<<levels)<=n) ++levels;
        up.assign(levels,vector<int>(n,root)); vector<int> order{root}; depth[root]=0;
        for (int i=0;i<int(order.size());i++) {
            int v=order[i];
            for (int u:g[v]) if (depth[u]==-1)
                depth[u]=depth[v]+1,up[0][u]=v,order.push_back(u);
        }
        assert(int(order.size())==n);
        for (int k=1;k<levels;k++) for (int v=0;v<n;v++) up[k][v]=up[k-1][up[k-1][v]];
    }
    int query(int u,int v) const { // 최소 공통 조상 질의 O(log N).
        if (depth[u]<depth[v]) swap(u,v);
        int diff=depth[u]-depth[v];
        for (int k=0;k<int(up.size());k++) if (diff>>k&1) u=up[k][u];
        if (u==v) return u;
        for (int k=int(up.size())-1;k>=0;k--) if (up[k][u]!=up[k][v])
            u=up[k][u],v=up[k][v];
        return up[0][u];
    }
};
}
