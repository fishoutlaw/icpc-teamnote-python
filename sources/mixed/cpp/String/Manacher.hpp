#pragma once
#include "../common.hpp"
// 바이트 문자열의 팰린드롬 반지름 O(N).
// 2N+1개 반지름은 원문 팰린드롬 길이. 구분자는 입력과 충돌하지 않는다.
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
