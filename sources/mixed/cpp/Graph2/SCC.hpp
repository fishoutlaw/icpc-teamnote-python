#pragma once
#include "../common.hpp"
// Based on code/Graph2/SCC.cpp. Iterative Kosaraju, O(V+E) time/space.
namespace tn {
pair<vector<int>,vector<vector<int>>> strongly_connected_components(
    const vector<vector<int>>& g) {
    int n=g.size(); vector<vector<int>> rev(n),groups;
    for (int v=0;v<n;v++) for (int u:g[v]) rev[u].push_back(v);
    vector<int> seen(n),order,comp(n,-1),pos(n);
    for (int s=0;s<n;s++) if (!seen[s]) {
        vector<int> st{s}; seen[s]=1;
        while (!st.empty()) {
            int v=st.back();
            if (pos[v]==int(g[v].size())) { order.push_back(v); st.pop_back(); }
            else { int u=g[v][pos[v]++]; if (!seen[u]) seen[u]=1,st.push_back(u); }
        }
    }
    reverse(order.begin(),order.end());
    for (int s:order) if (comp[s]==-1) {
        int id=groups.size(); groups.push_back({}); comp[s]=id; vector<int> st{s};
        while (!st.empty()) {
            int v=st.back(); st.pop_back(); groups.back().push_back(v);
            for (int u:rev[v]) if (comp[u]==-1) comp[u]=id,st.push_back(u);
        }
    }
    return {comp,groups}; // IDs in topological order
}
}
