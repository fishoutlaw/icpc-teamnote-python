#pragma once
#include "../common.hpp"
// 반복형 타잔으로 단절점·단절선·이중 연결 요소를 구한다. O(V+E).
// 무향 다중 그래프, 자기 루프 금지. 단절점은 여러 묶음에 속한다.
namespace tn {
struct BCCResult { vector<int> cuts,bridges; vector<vector<int>> groups; };
BCCResult biconnected_components(int n,const vector<pair<int,int>>& edges) {
    vector<vector<pair<int,int>>> g(n);
    for (int i=0;i<int(edges.size());i++) {
        auto [u,v]=edges[i]; if (u==v) throw invalid_argument("self loop");
        g[u].push_back({v,i}); g[v].push_back({u,i});
    }
    vector<int> tin(n,-1),low(n),par(n,-1),pe(n,-1),pos(n),children(n),cut(n);
    vector<int> edge_stack,mark(n,-1); int timer=0; BCCResult out;
    for (int root=0;root<n;root++) if (tin[root]==-1) {
        vector<int> st{root}; tin[root]=low[root]=timer++;
        while (!st.empty()) {
            int v=st.back();
            if (pos[v]<int(g[v].size())) {
                auto [u,e]=g[v][pos[v]++]; if (e==pe[v]) continue;
                if (tin[u]==-1) {
                    par[u]=v; pe[u]=e; children[v]++; edge_stack.push_back(e);
                    tin[u]=low[u]=timer++; st.push_back(u);
                } else if (tin[u]<tin[v]) {
                    low[v]=min(low[v],tin[u]); edge_stack.push_back(e);
                }
                continue;
            }
            st.pop_back(); int p=par[v];
            if (p==-1) {
                cut[v]=children[v]>1;
                if (g[v].empty()) out.groups.push_back({v});
            } else {
                low[p]=min(low[p],low[v]);
                if (low[v]>tin[p]) out.bridges.push_back(pe[v]);
                if (low[v]>=tin[p]) {
                    if (par[p]!=-1) cut[p]=1;
                    int id=out.groups.size(); out.groups.push_back({});
                    while (true) {
                        int e=edge_stack.back(); edge_stack.pop_back();
                        for (int x:{edges[e].first,edges[e].second}) if (mark[x]!=id)
                            mark[x]=id,out.groups.back().push_back(x);
                        if (e==pe[v]) break;
                    }
                }
            }
        }
    }
    for (int v=0;v<n;v++) if (cut[v]) out.cuts.push_back(v);
    return out; // 단절선은 입력 간선 번호, 고립점도 별도 묶음.
}
}
