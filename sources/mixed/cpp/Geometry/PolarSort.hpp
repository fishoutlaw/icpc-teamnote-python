#pragma once
#include "Template.hpp"
// Based on code/Geometry/PolarSort.cpp. O(N log N); origin, then +x CCW.
namespace tn {
vector<Point> polar_sort(vector<Point> points) {
    auto half=[](Point p) { return !(p.second>0 || (p.second==0 && p.first>=0)); };
    sort(points.begin(),points.end(),[&](Point a,Point b) {
        if (a==Point{0,0} || b==Point{0,0}) return a==Point{0,0} && b!=Point{0,0};
        if (half(a)!=half(b)) return half(a)<half(b);
        i128 c=cross(a,b); return c?c>0:dot(a,a)<dot(b,b);
    });
    return points; // equal angles: nearest first
}
}
