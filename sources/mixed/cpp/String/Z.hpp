#pragma once
#include "../common.hpp"
// 각 바이트 위치에서 접두사와 일치하는 길이. O(N), z[0]=N.
namespace tn {
vector<int> z_function(const string& s) {
    int n=s.size(); vector<int> z(n); if (n) z[0]=n;
    for (int i=1,l=0,r=0;i<n;i++) {
        if (i<r) z[i]=min(r-i,z[i-l]);
        while (i+z[i]<n && s[z[i]]==s[i+z[i]]) ++z[i];
        if (i+z[i]>r) l=i,r=i+z[i];
    }
    return z;
}
}
