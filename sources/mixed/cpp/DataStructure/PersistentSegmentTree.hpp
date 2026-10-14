#pragma once
#include "../common.hpp"
// 빈도 트리의 버전 보존. 삽입·k번째 질의 O(log N), 공간 O(Q log N).
namespace tn {
struct PersistentSegmentTree {
    struct Node { int l=0,r=0,count=0; };
    int n; vector<Node> nodes{{}}; vector<int> roots{0};
    explicit PersistentSegmentTree(int n):n(n) { assert(n>0); }
    int update(int old,int l,int r,int x) {
        int v=nodes.size(); nodes.push_back(nodes[old]); ++nodes[v].count;
        if (r-l>1) {
            int m=(l+r)/2;
            if (x<m) { int child=update(nodes[old].l,l,m,x); nodes[v].l=child; }
            else { int child=update(nodes[old].r,m,r,x); nodes[v].r=child; }
        }
        return v;
    }
    int insert(int version,int x) {
        assert(0<=x && x<n); int root=update(roots.at(version),0,n,x);
        roots.push_back(root); return int(roots.size())-1;
    }
    int kth(int before,int after,int k) const {
        int a=roots.at(before),b=roots.at(after),l=0,r=n;
        assert(1<=k && k<=nodes[b].count-nodes[a].count);
        // 버전 간 빈도 차는 음수가 아니어야 하며 k는 1부터 시작한다.
        while (r-l>1) {
            int m=(l+r)/2, count=nodes[nodes[b].l].count-nodes[nodes[a].l].count;
            if (k<=count) a=nodes[a].l,b=nodes[b].l,r=m;
            else k-=count,a=nodes[a].r,b=nodes[b].r,l=m;
        }
        return l;
    }
};
}
