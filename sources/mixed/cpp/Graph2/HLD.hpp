#pragma once
#include "../common.hpp"
// Based on code/Graph2/HLD.cpp. Iterative O(N) build; path O(log N) intervals.
// Combine with SegmentTree: point set O(log N), path sum O(log^2 N).
namespace tn {
struct HLD {
    vector<int> parent,depth,size,head,pos;
    HLD(const vector<vector<int>>& g,int root=0) {
        int n=g.size(); parent.assign(n,-1); depth.assign(n,0); size.assign(n,1);
        head.resize(n); pos.resize(n); vector<int> order{root},heavy(n,-1); parent[root]=root;
        for (int i=0;i<int(order.size());i++) {
            int v=order[i];
            for (int u:g[v]) if (parent[u]==-1)
                parent[u]=v,depth[u]=depth[v]+1,order.push_back(u);
        }
        assert(int(order.size())==n);
        for (int i=n-1;i>0;i--) {
            int v=order[i],p=parent[v]; size[p]+=size[v];
            if (heavy[p]==-1 || size[v]>size[heavy[p]]) heavy[p]=v;
        }
        vector<pair<int,int>> st{{root,root}}; int timer=0;
        while (!st.empty()) {
            auto [v,h]=st.back(); st.pop_back();
            for (;v!=-1;v=heavy[v]) {
                head[v]=h; pos[v]=timer++;
                for (int u:g[v]) if (parent[u]==v && u!=v && u!=heavy[v]) st.push_back({u,u});
            }
        }
    }
    vector<pair<int,int>> path_ranges(int u,int v,bool edges=false) const {
        vector<pair<int,int>> ranges; // unordered; commutative operations only
        while (head[u]!=head[v]) {
            if (depth[head[u]]<depth[head[v]]) swap(u,v);
            ranges.push_back({pos[head[u]],pos[u]+1}); u=parent[head[u]];
        }
        if (depth[u]>depth[v]) swap(u,v);
        int l=pos[u]+edges,r=pos[v]+1; if (l<r) ranges.push_back({l,r});
        return ranges; // edge values stored at the deeper endpoint
    }
    pair<int,int> subtree_range(int v) const { return {pos[v],pos[v]+size[v]}; }
};
}
