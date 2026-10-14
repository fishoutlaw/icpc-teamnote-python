#pragma once
#include "Template.hpp"
// Based on code/Geometry/SegmentIntersection.cpp. O(1), degenerate segments supported.
namespace tn {
struct Intersection {
    int kind; i128 xnum=0,ynum=0,den=1; // 0:none, -1:interval, 1:unique exact rational
};
Intersection segment_intersection(Point a,Point b,Point c,Point d) {
    Point u=sub(b,a),v=sub(d,c),w=sub(c,a); i128 det=cross(u,v);
    if (det) {
        i128 t=cross(w,v),s=cross(w,u);
        if (det<0) det=-det,t=-t,s=-s;
        if (t<0 || t>det || s<0 || s>det) return {0};
        return {1,i128(a.first)*det+t*u.first,i128(a.second)*det+t*u.second,det};
    }
    if (cross(u,w) || cross(v,w)) return {0};
    Point lo=max(min(a,b),min(c,d)),hi=min(max(a,b),max(c,d));
    if (lo>hi) return {0};
    if (lo==hi) return {1,lo.first,lo.second,1};
    return {-1};
}
}
