#pragma once
#include "../common.hpp"
// 모든 쌍 최단 거리 O(V^3), 공간 O(V^2).
namespace tn {
vector<vector<ll>> floyd_warshall(int n,const vector<tuple<int,int,ll>>& edges) {
    vector<vector<ll>> d(n,vector<ll>(n,INF));
    for (int i=0;i<n;i++) d[i][i]=0;
    for (auto [u,v,w]:edges) d[u][v]=min(d[u][v],w);
    for (int k=0;k<n;k++) for (int i=0;i<n;i++) if (d[i][k]!=INF)
        for (int j=0;j<n;j++) if (d[k][j]!=INF)
            d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
    return d; // d[v][v]<0이면 음수 사이클. 이를 거치는 거리는 유효하지 않다.
}
}
