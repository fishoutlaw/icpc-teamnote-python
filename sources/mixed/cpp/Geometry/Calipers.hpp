#pragma once
#include "Template.hpp"
// 끝점 중복·일직선 내부점 없는 반시계 볼록 껍질의 가장 먼 두 점. O(N).
namespace tn {
optional<pair<Point,Point>> calipers(const vector<Point>& h) {
    int n=h.size(); if (!n) return nullopt;
    if (n<=2) return pair<Point,Point>{h.front(),h.back()};
    auto area=[&](int i,int k,int j) { i128 x=orient(h[i],h[k],h[j]); return x<0?-x:x; };
    i128 best=-1; pair<Point,Point> result; int j=1;
    for (int i=0;i<n;i++) {
        int k=(i+1)%n;
        while (area(i,k,(j+1)%n)>area(i,k,j)) j=(j+1)%n;
        for (int v:{i,k}) { i128 d=distance_squared(h[v],h[j]);
            if (d>best) best=d,result={h[v],h[j]}; }
    }
    return result;
}
}
