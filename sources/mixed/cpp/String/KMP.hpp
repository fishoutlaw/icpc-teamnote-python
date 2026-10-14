#pragma once
#include "../common.hpp"
// Based on code/String/KMP.cpp. O(N+M), auxiliary O(M). Byte offsets.
namespace tn {
vector<int> prefix_function(const string& p) {
    vector<int> fail(p.size());
    for (int i=1,j=0;i<int(p.size());i++) {
        while (j && p[i]!=p[j]) j=fail[j-1];
        if (p[i]==p[j]) ++j; fail[i]=j;
    }
    return fail;
}
vector<int> kmp(const string& s,const string& p) {
    vector<int> result;
    if (p.empty()) { result.resize(s.size()+1); iota(result.begin(),result.end(),0); return result; }
    auto fail=prefix_function(p);
    for (int i=0,j=0;i<int(s.size());i++) {
        while (j && s[i]!=p[j]) j=fail[j-1];
        if (s[i]==p[j]) ++j;
        if (j==int(p.size())) result.push_back(i-j+1),j=fail[j-1];
    }
    return result; // empty pattern matches all N+1 boundaries
}
}
