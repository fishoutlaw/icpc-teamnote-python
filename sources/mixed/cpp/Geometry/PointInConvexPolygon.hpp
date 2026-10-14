#pragma once
#include "Template.hpp"
// 반시계 볼록 다각형 내부 판별 O(log N). 끝점 중복·일직선 내부점 제거.
namespace tn {
bool point_in_convex_polygon(const vector<Point>& h,Point p) {
    int n=h.size(); if (n<3) return n && on_segment(h.front(),h.back(),p);
    Point a=h[0]; i128 first=orient(a,h[1],p),last=orient(a,h.back(),p);
    if (first<0 || last>0) return false;
    if (first==0) return on_segment(a,h[1],p);
    if (last==0) return on_segment(a,h.back(),p);
    int l=1,r=n-1;
    while (r-l>1) { int m=(l+r)/2; if (orient(a,h[m],p)>=0) l=m; else r=m; }
    return orient(h[l],h[r],p)>=0;
}
}
