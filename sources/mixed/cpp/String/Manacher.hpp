#pragma once
#include "../common.hpp"
// Based on code/String/Manacher.cpp. O(N) time/space; byte string.
// 2*N+1 radii; radius = original palindrome length. Sentinel cannot collide.
namespace tn {
vector<int> manacher(const string& s) {
    vector<int> v{-1}; for (unsigned char c:s) v.push_back(c),v.push_back(-1);
    int n=v.size(); vector<int> radius(n);
    for (int i=0,center=0,right=0;i<n;i++) {
        if (i<right) radius[i]=min(right-i,radius[2*center-i]);
        while (i-radius[i]>0 && i+radius[i]+1<n && v[i-radius[i]-1]==v[i+radius[i]+1]) ++radius[i];
        if (i+radius[i]>right) center=i,right=i+radius[i];
    }
    return radius;
}
}
