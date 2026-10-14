#pragma once
#include "../common.hpp"
// 층별 증가 경로를 찾는 최대 이분 매칭 O((V+E)sqrt(V)).
namespace tn {
struct MatchingResult { vector<int> left,right,cover_left,cover_right; };
MatchingResult hopcroft_karp(const vector<vector<int>>& g,int m) {
    int n=g.size(); vector<int> le(n,-1),ri(m,-1);
    while (true) {
        vector<int> d(n,-1),pos(n); queue<int> q; int shortest=n+1;
        for (int v=0;v<n;v++) if (le[v]==-1) d[v]=0,q.push(v);
        while (!q.empty()) {
            int v=q.front(); q.pop(); if (d[v]>=shortest) continue;
            for (int u:g[v]) {
                int w=ri[u];
                if (w==-1) shortest=d[v]+1;
                else if (d[w]==-1) d[w]=d[v]+1,q.push(w);
            }
        }
        if (shortest==n+1) break;
        for (int s=0;s<n;s++) if (le[s]==-1) {
            vector<int> st{s},links;
            while (!st.empty()) {
                int v=st.back();
                if (pos[v]==int(g[v].size())) {
                    d[v]=-1; st.pop_back(); if (!links.empty()) links.pop_back(); continue;
                }
                int u=g[v][pos[v]++],w=ri[u];
                if (w==-1 && d[v]+1==shortest) {
                    links.push_back(u);
                    for (int i=0;i<int(st.size());i++) le[st[i]]=links[i],ri[links[i]]=st[i];
                    break;
                }
                if (w!=-1 && d[w]==d[v]+1) st.push_back(w),links.push_back(u);
            }
        }
    }
    vector<int> sl(n),sr(m),a,b; queue<int> q;
    for (int v=0;v<n;v++) if (le[v]==-1) sl[v]=1,q.push(v);
    while (!q.empty()) {
        int v=q.front(); q.pop();
        for (int u:g[v]) if (u!=le[v] && !sr[u]) {
            sr[u]=1; int w=ri[u]; if (w!=-1 && !sl[w]) sl[w]=1,q.push(w);
        }
    }
    for (int v=0;v<n;v++) if (!sl[v]) a.push_back(v);
    for (int u=0;u<m;u++) if (sr[u]) b.push_back(u);
    return {le,ri,a,b}; // 최소 정점 커버는 cover_left와 cover_right의 합집합.
}
}
