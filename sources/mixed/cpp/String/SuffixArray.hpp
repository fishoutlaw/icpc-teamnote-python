#pragma once
#include "../common.hpp"
// Based on code/String/SuffixArray.cpp. Doubling/counting sort O(N log N), O(N) space.
namespace tn {
pair<vector<int>,vector<int>> suffix_array(const string& s) {
    int n=s.size(); if (!n) return {{},{}};
    vector<int> sa(n),rank(n),second(n); iota(sa.begin(),sa.end(),0);
    for (int i=0;i<n;i++) rank[i]=(unsigned char)s[i]+1;
    auto counting=[&](const vector<int>& ids,const vector<int>& key,int classes) {
        vector<int> count(classes+1),out(n);
        for (int i:ids) ++count[key[i]];
        partial_sum(count.begin(),count.end(),count.begin());
        for (int i=n-1;i>=0;i--) out[--count[key[ids[i]]]]=ids[i];
        return out;
    };
    for (int step=1;;step*=2) {
        for (int i=0;i<n;i++) second[i]=i+step<n?rank[i+step]:0;
        int classes=*max_element(rank.begin(),rank.end());
        sa=counting(counting(sa,second,classes),rank,classes);
        vector<int> next(n); classes=1; next[sa[0]]=classes;
        for (int i=1;i<n;i++) {
            int a=sa[i-1],b=sa[i];
            if (pair<int,int>{rank[a],second[a]}!=pair<int,int>{rank[b],second[b]}) ++classes;
            next[b]=classes;
        }
        rank.swap(next); if (classes==n) break;
    }
    vector<int> lcp(n);
    for (int i=0,len=0;i<n;i++) {
        int pos=rank[i]-1; if (pos==0) { len=0; continue; }
        int j=sa[pos-1]; while (i+len<n && j+len<n && s[i+len]==s[j+len]) ++len;
        lcp[pos]=len; if (len) --len;
    }
    return {sa,lcp}; // lcp[i]=LCP(sa[i-1],sa[i]), lcp[0]=0. Byte offsets.
}
}
